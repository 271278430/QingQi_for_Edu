"""Isolated HTTP/model-protocol regressions for actual question and speaker grounding."""
import http.cookiejar
import json
import os
import threading
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment, server
from qingqi.storage import Store


def fixture():
    root=fixture_root();calls=[]
    class Model(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_POST(self):
            body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            payload=json.loads(body['messages'][1]['content'])['input'];calls.append(payload)
            if payload.get('story_opening_only') and getattr(self.server,'fail_story_opening',False):
                self.send_error(503,'isolated optional opening unavailable');return
            evidence=payload.get('dialogue_evidence',{})
            hints=evidence.get('teacher_hints',[])
            if '只求提示' in payload.get('question',''):
                text='代入后，最终结果是 $(-3)^{2026}$。'
            elif '不要个位' in payload.get('question',''):
                text='先看3的个位循环，答案的个位是9。'
            elif 'protocol_error' not in payload:
                text='很好，你已经抓住了“乘数必须为0”这个关键！我们继续看方程。'
            elif 'mx-8=5x+n' in payload.get('problem',{}).get('text','').replace(' ',''):
                text=('先把 $mx-8=5x+n$ 整理为 $(m-5)x=n+8$。右边不随 $x$ 改变，左边怎样才能对所有 $x$ 都成立？' if len(hints)<1 else
                      '继续看 $(m-5)x=n+8$。可以分别取 $x=0$ 和 $x=1$，比较两个等式，先确定 $m-5$ 必须满足的条件。')
            else:text='回到当前题的 $x=6$ 和 $2x+y=16$：先用已知的 $x$ 替换第二个方程中的 $x$，再整理剩下的未知数。'
            raw=json.dumps({'choices':[{'message':{'content':text}}]}).encode()
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    model=ThreadingHTTPServer(('127.0.0.1',0),Model);threading.Thread(target=model.serve_forever,daemon=True).start()
    os.environ['EDU_HINT_FIXTURE_KEY']='local-fixture'
    config=root/'hint-model.fixture.json'
    config.write_text(json.dumps({'turn_seconds':60,'lease_seconds':80,'models':{'vision':{'enabled':True,'base_url':f'http://127.0.0.1:{model.server_port}/v1','model':'glm-5.3-flash','key_env':'EDU_HINT_FIXTURE_KEY','allowed_hosts':['127.0.0.1'],'timeout':20}}}),encoding='utf-8')
    instance=server(0,root=root,deployment=Deployment(config=config));threading.Thread(target=instance.serve_forever,daemon=True).start()
    return root,instance,model,calls


def run():
    root,instance,model,calls=fixture();base=f'http://127.0.0.1:{instance.server_port}'
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(base+path,timeout=80) as r:return json.load(r)
    boot=get('/api/bootstrap')
    def post(path,body):
        req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        try:
            with opener.open(req,timeout=80) as r:return json.load(r)
        except urllib.error.HTTPError as error:
            print('HTTP diagnostic:',error.code,error.read().decode(),flush=True)
            raise
    checks=[]
    def check(name,value):
        checks.append({'name':name,'passed':bool(value)});print(json.dumps(checks[-1]),flush=True)
        assert value,name
    owner=Store(root)
    try:
        entry=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and '个位' not in e['expression'])
        a=post('/api/practice/start',{'item_id':entry['id'],'request_id':'bound-start'})
        body={'assignment_id':a['id'],'style':'heuristic','request_id':'hint-one'}
        first=post('/api/practice/hint',body)
        check('practice_hint_analyzes_full_equation_not_topic_label','m-5' in first['text'] and 'n+8' in first['text'])
        accepted=json.loads(owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone()[0])
        check('natural_false_student_progress_is_repaired',len(calls)==1 and '抓住' not in first['text'] and accepted.get('reply_source')=='verified_practice_hint')
        check('hint_button_has_no_question_or_request_for_reply',not __import__('re').search(r'[?？]|告诉我|你能|请给出',first['text']) and accepted['teaching_plan']['interaction_style']=='hint_only' and accepted['teaching_plan']['budget']['hard_questions']==0)
        check('hint_card_does_not_generate_an_invisible_visual',accepted['teaching_plan']['visual']['delivery']=='text' and not accepted.get('observations'))
        check('teacher_and_student_sources_are_separate',calls[-1]['dialogue_evidence']['teacher_hints']==[] and calls[-1]['dialogue_evidence']['current_assessment']['status']=='unverified')
        count=len(calls);again=post('/api/practice/hint',body)
        check('same_hint_command_replays_without_model_call',again==first and len(calls)==count)
        conflict=False
        try:post('/api/practice/hint',{**body,'style':'socratic'})
        except urllib.error.HTTPError as e:conflict=e.code==403
        check('conflicting_hint_command_is_rejected',conflict)
        second=post('/api/practice/hint',{**body,'request_id':'hint-two'})
        check('continued_hint_increases_help_without_claiming_student_work',second['text']!=first['text'] and 'x=0' in second['text'] and calls[-1]['dialogue_evidence']['teacher_hints']==[first['text']])
        teach=post('/api/teach',{'session':a['session'],'request':{'request_id':'continue','question':'继续给我提示'}})
        check('conversation_after_hint_retains_question_and_never_invents_mastery','抓住' not in teach['response']['text'] and 'm-5' in teach['response']['text'])
        state=json.loads(owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone()[0])
        check('hint_count_is_not_verified_stage',state['practice_assessment']['stage']==0 and state['practice_assessment']['status']=='unverified')
        check('hint_and_reply_commit_once_without_grades',owner.db.execute("SELECT count(*) FROM practice_events WHERE kind='hint'").fetchone()[0]==2 and get('/api/learning')['summary']['attempts']==0)
        other=next(e for e in owner.catalogue.bank.values() if '遮住' in e['expression'] and 'x=6' in e['expression'].replace(' ','') and '2x+y=16' in e['expression'].replace(' ',''))
        b=post('/api/practice/start',{'item_id':other['id'],'request_id':'other-start'})
        switched=post('/api/practice/hint',{'assignment_id':b['id'],'style':'heuristic','request_id':'other-hint'})
        check('another_problem_does_not_inherit_old_hints','2x+y=16' in switched['text'] and calls[-1]['dialogue_evidence']['teacher_hints']==[])
        from qingqi.practice_tutoring import guidance
        variant={**entry,'expression':'已知 $mx+6=2x+n$ 对任意x恒成立，求 $(m+n)^4$。'}
        check('offline_hint_uses_actual_parameters','m-2' in guidance(variant,'heuristic',0) and '6' in guidance(variant,'heuristic',0))
        check('offline_repeated_help_never_asserts_completed_work',all(not any(s in owner.catalogue.hint(entry,'heuristic',i,0) for s in ['已求出','中间结果代回','这一步正确']) for i in range(4)))
        from qingqi.teaching_plan import validate_text, practice_hint_plan
        from qingqi.contracts import ContractError
        plan=practice_hint_plan(accepted['teaching_plan'])
        for text in ['你先算出结果，再告诉我。','把答案告诉我。','你能先求出来吗？','看这张数轴图，把结果发给我。']:
            rejected=False
            try:validate_text(text,plan)
            except ContractError:rejected=True
            check('hint_rejects_solicitation_'+str(len(checks)),rejected)
        opposite=next(e for e in owner.catalogue.bank.values() if '和谐方程' in e['expression'] and '4x' in e['expression'])
        for hint_level in range(3):
            text=guidance(opposite,'heuristic',0,help_level=hint_level,interactive=False)
            check('opposite_equation_hint_is_declarative_'+str(hint_level),'4x' in text and not __import__('re').search(r'[?？]|告诉我|你能|请给出',text))
        from qingqi.tutoring_grounding import validate_attribution
        from qingqi.contracts import ContractError
        bad=False
        try:validate_attribution('你已经求出了正确答案。',{'question':'继续提示','history':[{'question':'不会','reply':'m=5'}]}, {})
        except ContractError:bad=True
        check('assistant_conclusion_is_not_student_answer',bad)
        wrong=post('/api/teach',{'session':a['session'],'request':{'request_id':'wrong-step','question':'m=0'}})
        check('wrong_step_is_not_praised',wrong['response']['teaching_action']=='ask' and '调整' in wrong['response']['text'])
        correct=post('/api/teach',{'session':a['session'],'request':{'request_id':'correct-step','question':'m=5'}})
        check('only_verified_step_advances',correct['response']['teaching_action']=='confirm' and '求 $n$' in correct['response']['text'])
        check('full_power_does_not_use_units_answer',not owner.catalogue.grade(entry,'9') and owner.catalogue.grade(entry,'3^2026') and owner.catalogue.grade(entry,'(-3)^2026'))
        units=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and '个位' in e['expression'])
        check('units_question_still_checks_units',owner.catalogue.grade(units,'9') and not owner.catalogue.grade(units,'3^2026'))
        choice={**units,'key':{'kind':'choice','values':['A']},'options':['9','3']}
        check('choice_answer_keeps_its_letter_contract',owner.catalogue.grade(choice,'A') and not owner.catalogue.grade(choice,'B'))
        from qingqi.learning import numeric_answer
        check('exact_power_preserves_sign_precedence',numeric_answer('-3^2')==-9 and numeric_answer('(-3)^2')==9 and numeric_answer('(1/2)^2')==__import__('fractions').Fraction(1,4))
        from qingqi.visual_tasks import validate_result
        validate_result('已知点A在线段BC上，先根据中点定义整理条件。',{})
        rejected=False
        try:validate_result('我已经画好线段AB。',{})
        except ContractError:rejected=True
        check('given_segments_are_distinct_from_drawing_completion',rejected)
        leak=post('/api/teach',{'session':a['session'],'request':{'request_id':'protected-power','question':'只求提示，不要答案'}})
        check('unsafe_numeric_final_power_is_replaced_by_current_scaffold','2026' not in leak['response']['text'] and 'm-5' not in leak['response']['text'] and '求 $n$' in leak['response']['text'])
        units_hint=post('/api/teach',{'session':a['session'],'request':{'request_id':'wrong-units','question':'继续提示，不要个位'}})
        check('full_power_hint_does_not_switch_to_units_problem','循环' not in units_hint['response']['text'])
        from qingqi.contracts import canonical
        legacy=canonical({'text':'你已经求出了乘数。你能把下一步告诉我吗？','style':'heuristic','hint_count':2})
        with owner.db:owner.db.execute("UPDATE practice_events SET data=? WHERE request_id='hint-two'",(legacy,))
        before=owner.db.execute("SELECT data FROM practice_events WHERE request_id='hint-two'").fetchone()[0]
        student=owner.db.execute("SELECT student FROM practice_events WHERE request_id='hint-two'").fetchone()[0]
        projected=owner.prepare_model_hint(student,{**body,'request_id':'hint-two'})['result']
        check('legacy_hint_replay_projects_current_declarative_rule',not __import__('re').search(r'[?？]|告诉我|你能|已经',projected['text']) and 'm-5' in projected['text'])
        check('legacy_hint_refresh_and_replay_are_consistent',owner.practice_assignment(student,a['id'])['guidance']==projected['text'])
        check('legacy_hint_projection_does_not_rewrite_evidence',owner.db.execute("SELECT data FROM practice_events WHERE request_id='hint-two'").fetchone()[0]==before)
        check('verified_parameter_stage_targets_the_remaining_parameter','求 $n$' in guidance(entry,'heuristic',1,interactive=False) and '求 $m$' in guidance(entry,'heuristic',2,interactive=False))
    finally:
        owner.close();instance.shutdown();instance.server_close();model.shutdown();model.server_close()
    report={'passed':len(checks),'checks':checks,'real_model':False,'isolated':True}
    Path('education/.local/reports/grounded-hint-acceptance.local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':run()
