"""Behavioral bad cases on real HTTP, SQLite and ZCode, with synthetic model output."""
import http.cookiejar
import json
import re
import urllib.request
import urllib.error
import uuid
from tutoring_evolution_fixture import Fixture,animation
from qingqi.agent import PROJECT
from qingqi.contracts import ContractError,Denied,Request,Route
from qingqi.storage import Store
from qingqi.visual_teaching import render_visuals
from qingqi.teaching_policy import choose
from qingqi.product import server
import threading


def run():
    fixture=Fixture();fixture.start();owner=Store(fixture.root);checks=[]
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(fixture.base+path,timeout=60) as response:return json.load(response)
    boot=get('/api/bootstrap')
    def post(path,body):
        request=urllib.request.Request(fixture.base+path,data=json.dumps(body).encode(),headers={'Origin':fixture.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        with opener.open(request,timeout=60) as response:return json.load(response)
    def check(name,passed):
        assert passed,name
        checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
    def teach(session,q,rid=None):return post('/api/teach',{'session':session,'request':{'request_id':rid or uuid.uuid4().hex,'question':q}})
    try:
        entry=next(e for e in owner.catalogue.bank.values() if 'a-3' in e['expression'].replace(' ','') and 'b+2' in e['expression'].replace(' ','') and '绝对值' in e['title'])
        assignment=post('/api/practice/start',{'item_id':entry['id'],'request_id':'reported-question'})
        q='我不太能理解这个根号计算和绝对值运算，能告诉我怎么更好的理解这个吗'
        value=teach(assignment['session'],q,'reported-concept')
        state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(value['response']['run_id'],)).fetchone()[0])
        check('exact_reported_phrase_binds_owned_question_and_answers_concepts',state['practice_entry']['id']==entry['id'] and state['route']['teaching']['mode']=='explain' and '根号' in value['response']['text'] and '绝对值' in value['response']['text'] and '你希望查询' not in value['response']['text'])
        check('teaching_plan_uses_actual_learning_and_no_final_answer',state['teaching_plan']['goal']=='concept' and state['context']['content']['learner']['matched_problem'] and not state['route']['teaching']['allow_final_answer'])
        check('replay_does_not_regenerate',teach(assignment['session'],q,'reported-concept')['response']['cache_hit'])
        zero=teach(assignment['session'],'不要再反问我，直接解释绝对值是什么意思。')
        check('natural_zero_question_override','？' not in zero['response']['text'] and zero['response']['teaching_action']=='explain')
        follow=teach(assignment['session'],'这一步的依据是什么？')
        check('same_problem_retains_zero_question_preference','？' not in follow['response']['text'])
        teach(assignment['session'],'先给提示，不要给答案。')
        with owner.db:owner.db.execute('UPDATE dialogue_state SET updated=updated-4000 WHERE session=?',(assignment['session'],))
        after=teach(assignment['session'],'解释一下这个根号。')
        state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(after['response']['run_id'],)).fetchone()[0])
        check('expired_summary_keeps_owned_question_answer_preference',state['practice_entry']['id']==entry['id'] and state['route']['teaching']['no_final_requested'] and not state['route']['teaching']['allow_final_answer'])
        combined=teach(assignment['session'],'谢谢，能帮我理解绝对值吗？')
        check('greeting_does_not_erase_compound_teaching_intent','绝对值' in combined['response']['text'] and combined['response']['teaching_action']=='explain')
        direct=teach(assignment['session'],'现在直接给正确答案。')
        check('explicit_answer_preference_overrides_previous_hint',direct['response']['teaching_action']=='give_answer' and entry['key']['values'][0] in direct['response']['text'])
        scalar=teach(assignment['session'],'直接给 √9 的结果。')
        state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(scalar['response']['run_id'],)).fetchone()[0])
        check('new_scalar_computation_is_not_old_choice',not state.get('practice_entry') and '3' in scalar['response']['text'] and not re.search(r'选.*D',scalar['response']['text']))
        check('new_task_hides_old_problem_card',get('/api/session?id='+assignment['session'])['practice'] is None)
        teach(assignment['session'],'返回原练习，先提示我这道题。')
        check('explicit_return_restores_original_problem',get('/api/session?id='+assignment['session'])['practice']['item']['id']==entry['id'])
        numeric=teach(assignment['session'],'2+3*4')
        state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(numeric['response']['run_id'],)).fetchone()[0])
        check('new_numeric_expression_is_not_owned_algebra',not state.get('practice_entry') and state['effective_request']['expression']=='2+3*4')
        teach(assignment['session'],'返回原练习，先提示我这道题。')
        long_kept=teach(assignment['session'],'测试持续过长，请简短解释这一步。')
        check('stylistic_length_does_not_exhaust_protocol_repairs',long_kept['response']['repairs']==0 and long_kept['response']['text'])
        try:teach(assignment['session'],'测试持续空回复，请简短解释这一步。')
        except urllib.error.HTTPError as error:
            check('exhausted_model_repairs_are_not_account_403',error.code==502 and json.load(error)['error']=='model_protocol')
        else:raise AssertionError('continuously invalid model response accepted')
        isolated=post('/api/sessions',{})['id'];general=teach(isolated,'什么是绝对值？')
        check('unbound_clear_concept_is_taught_without_question_form','绝对值' in general['response']['text'] and '请提供' not in general['response']['text'])
        continuation=teach(isolated,'那负数呢？')
        check('unbound_concept_followup_receives_same_session_history',continuation['response']['teaching_action']=='explain' and fixture.calls[-1]['input']['history'][0]['question'].replace('?','？')=='什么是绝对值？')
        another=post('/api/sessions',{})['id']
        unbound=teach(another,'那负数呢？')
        check('new_session_does_not_borrow_another_concept_dialogue',unbound['response']['teaching_action']=='clarify')
        teach(isolated,'取消')
        check('cancelled_concept_dialogue_is_not_inherited',teach(isolated,'再举一个例子。')['response']['teaching_action']=='clarify')
        long=teach(assignment['session'],'测试过长回复，请简短解释这一步。')
        check('complete_overlong_response_repaired_with_new_invocation',long['response']['repairs']==0 and len(long['response']['text'])<300)
        initial=get('/api/learning')['summary']['attempts']
        for word,template in [('距离','absolute_distance'),('开方','square_root'),('非负','nonnegative_sum'),('加减','number_line_motion'),('路程','travel_motion')]:
            value=teach(isolated,f'请用{word}动画演示帮助理解。')
            check('native_animation_'+template,value['response']['visuals'][0]['template']==template and value['response']['visuals'][0]['frames'])
        check('visual_help_does_not_create_grades',get('/api/learning')['summary']['attempts']==initial)
        for template in ('absolute_distance','square_root','nonnegative_sum','number_line_motion','travel_motion'):
            result=render_visuals(visuals=[animation(template)])
            check('deterministic_frames_'+template,result==render_visuals(visuals=[animation(template)]))
        try:render_visuals(visuals=[{**animation('square_root'),'params':{'areas':[-1]}}])
        except (ContractError,Denied):check('negative_root_area_rejected',True)
        else:raise AssertionError('negative root accepted')
        weak={'current_topic':{'state':'needs_practice','recent_independent_attempts':5,'accuracy':20},'related_topics':[]}
        strong={'current_topic':{'state':'secure','recent_independent_attempts':5,'accuracy':100},'related_topics':[]}
        req=Request('budget','请解释这一步。');route=Route(('tutor',),())
        a=choose(req,route,[],continuing_problem=True,learner=weak,problem={'level':3})
        b=choose(req,route,[],continuing_problem=True,learner=strong,problem={'level':1})
        check('difficulty_and_learning_change_budget',a['budget']['target_max']>b['budget']['target_max'])
        no_answer_hint=choose(Request('negation','不要给答案，请给我追问。'),route,[])
        check('answer_negation_does_not_negate_requested_questions',not no_answer_hint['no_questions'] and no_answer_hint['budget']['questions']==1 and not no_answer_hint['allow_final_answer'])
        fresh=next(e for e in owner.catalogue.bank.values() if e['id'] not in owner.catalogue.initial.get('historical_items',[]) and e['grade']=='7' and e.get('eligible',True))
        one=post('/api/practice/start',{'item_id':fresh['id'],'request_id':'greeting-before-work'})
        teach(one['session'],'你好')
        feedback=post('/api/practice/answer',{'assignment_id':one['id'],'request_id':'independent-answer','answer':fresh['key']['values'][0]})
        check('greeting_does_not_mark_independent_work_assisted',feedback['independent'] and feedback['unassisted'])
        from qingqi.teaching_plan import validate_text
        try:validate_text('绝对值表示到零的距离，对吗？',{**a['plan'],'goal':'concept'})
        except ContractError:check('concept_cannot_be_only_a_leading_question',True)
        else:raise AssertionError('concept only asked, not explained')
        second=server(0,root=fixture.root);threading.Thread(target=second.serve_forever,daemon=True).start()
        try:
            with opener.open(f'http://127.0.0.1:{second.server_port}/api/bootstrap',timeout=20) as response:json.load(response)
            check('two_web_entry_cookies_do_not_replace_each_other',bool(post('/api/sessions',{})['id']))
        finally:second.shutdown();second.server_close()
        from qingqi.web_store import WebStore
        numeric_owner=WebStore(PROJECT/'runs/tutoring-evolution-numeric'/uuid.uuid4().hex)
        try:
            sample=numeric_owner.start_practice('numeric-student',{'item_id':'order-1','request_id':'numeric-assignment'})
            with numeric_owner.db:
                numeric_owner.db.execute('INSERT INTO runs(student,session,request_id,payload_hash,request,state,response) VALUES(?,?,?,?,?,?,?)',('numeric-student',sample['session'],'numeric-help','fixture',json.dumps({'question':'先提示 2×3+4'}),json.dumps({'effective_request':{'expression':'2+3×4'}}),json.dumps({'teaching_action':'ask'})))
            fb=numeric_owner.owner._practice_feedback('numeric-student',sample,'14')
            check('equivalent_multiplication_symbol_does_not_erase_help',not fb['independent'] and not fb['unassisted'])
        finally:numeric_owner.close()
    finally:owner.close();fixture.close()
    (PROJECT.parent/'.local/reports/tutoring-evolution-acceptance.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'realModel':False,'actualZCodeRuntime':True},ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__':run()
