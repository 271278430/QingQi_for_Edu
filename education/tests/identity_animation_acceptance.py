"""Owned identity animation, typed model argument adaptation and learner evidence regressions."""
import http.cookiejar
import json
import threading
import urllib.error
import urllib.request
from pathlib import Path
from grounded_hint_acceptance import fixture
from qingqi.contracts import ContractError,Request
from qingqi.storage import Store
from qingqi.visual_teaching import normalize_selection,INPUT,validate_binding
from qingqi.contracts import validate


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
            print('HTTP diagnostic:',error.code,error.read().decode(),flush=True);raise
    def teach(q,rid):return post('/api/teach',{'session':a['session'],'request':{'request_id':rid,'question':q}})['response']
    def motion(response):return next(v for v in response['visuals'] if v['kind']=='animation_scene')
    checks=[]
    def check(name,value):
        assert value,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
    owner=Store(root)
    try:
        entry=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and '个位' not in e['expression'])
        a=post('/api/practice/start',{'item_id':entry['id'],'request_id':'start'})
        teach('给我一点提示，不要答案','first');before=len(calls)
        result=teach('能给动画的教学方式吗','reported-animation')
        v=motion(result)
        check('generic_animation_request_executes_owned_identity_template',v['template']=='identity_probe' and result['tool_calls']==1)
        check('known_identity_does_not_depend_on_invented_model_frames',len(calls)==before and not result['model_inference'])
        lesson=v['algebra_lesson']
        check('storyboard_binds_original_equation_and_rearrangement',lesson['equation']=='mx-8=5x+n' and lesson['rearranged']=='(m-5)x=n+8')
        check('animation_explains_three_probe_values_and_two_conditions',[s['probe'] for s in lesson['steps'] if 'probe' in s]==[0,1,2] and lesson['conditions']==['m-5=0','n+8=0'])
        check('hint_storyboard_preserves_parameter_and_final_answer_task',lesson['mode']=='hint' and not any('m=5' in s.get('formula','') or '(-3)' in s.get('formula','') for s in lesson['steps']))
        replay=teach('能给动画的教学方式吗','reported-animation')
        check('accepted_animation_replays_without_new_tool_or_model_call',replay['cache_hit'] and replay['visuals']==result['visuals'] and len(calls)==before)
        detail=get('/api/session?id='+a['session'])
        check('saved_conversation_replays_same_animation',any(m.get('response',{}).get('visuals')==result['visuals'] for m in detail['messages'] if m.get('response')))
        continued=teach('继续动态演示，并解释这一步','continue-animation')
        check('animation_with_explanation_and_followup_keeps_same_owned_problem',motion(continued)['algebra_lesson']['equation']==lesson['equation'] and '恒成立' in continued['text'])
        struggled=teach('还是不懂，继续给我提示','reported-struggle')
        check('explicit_hint_after_struggle_keeps_current_condition_and_one_diagram','m-5' in struggled['text'] and '5 应该' not in struggled['text'] and '抓住' not in struggled['text'] and struggled['route']['teaching']['mode']=='heuristic' and len(struggled['visuals'])==1 and struggled['visuals'][0]['kind']=='reasoning_diagram' and struggled['visuals'][0]['algebra_lesson']['equation']==lesson['equation'])
        complete=teach('把这道题的完整解题过程用动画展示，直接给答案','complete-animation')
        final=motion(complete)['algebra_lesson']
        check('authorized_solution_uses_exact_power_not_wrong_units_label',final['mode']=='solution' and '(-3)^{2026}' in final['steps'][-1]['formula'])
        check('hints_and_animation_never_create_student_grades',get('/api/learning')['summary']['attempts']==0)
        from qingqi.identity_animation import specification
        variant={'expression':'已知 $ax+6=2x-b$ 对任意x恒成立，求 $(a+b)^4$。'}
        spec=specification(variant,False)
        check('template_uses_actual_other_parameters_and_right_sign',spec['params']['equation']=='ax+6=2x-b')
        state=json.loads(owner.db.execute("SELECT state FROM runs WHERE json_extract(request,'$.request_id')='reported-animation'").fetchone()[0])
        wrong=json.loads(json.dumps(state['visual_task']['arguments']));wrong['visuals'][0]['params']['equation']='mx-7=5x+n'
        denied=False
        try:validate_binding(wrong,state)
        except ContractError:denied=True
        check('animation_cannot_change_owned_equation',denied)
        from qingqi.visual_tasks import wants_animation,plan
        negative=plan(Request.parse({'request_id':'negative','question':'不用动画，先解释这道题'}),entry)
        check('negated_animation_keeps_only_the_owned_static_diagram',not wants_animation('不用动画，先讲一下') and all(v['kind']!='animation_scene' for v in negative['arguments']['visuals']))
        static=teach('不要动画，只看这道题的静态图，先不要答案','static-only')
        check('standalone_static_identity_is_bound_without_fake_animation',len(static['visuals'])==1 and static['visuals'][0]['kind']=='reasoning_diagram' and static['visuals'][0]['algebra_lesson']['equation']==lesson['equation'] and '这段动画' not in static['text'])
        static={'kind':'function_plot','basis':'example','title':'一次函数示例','function':'linear','a':2,'b':1,'domain':[-2,2]}
        normalized=normalize_selection({'visuals':[static]},prefer_animation=True);validate(normalized,INPUT)
        check('valid_static_function_is_adapted_to_animation_without_changing_data',normalized['visuals'][0]['template']=='function_trace' and normalized['visuals'][0]['params']=={k:static[k] for k in ['function','a','b','domain']})
        flat={**static,'kind':'animation_scene','template':'function_trace'}
        normalized=normalize_selection({'visuals':[flat]},prefer_animation=True);validate(normalized,INPUT)
        check('valid_flat_animation_parameters_are_nested_once','a' not in normalized['visuals'][0] and normalized['visuals'][0]['params']['a']==2)
        conflict=False
        try:normalize_selection({'visuals':[{**flat,'params':{'a':3}}]},prefer_animation=True)
        except ContractError:conflict=True
        check('conflicting_flat_and_nested_parameters_are_rejected',conflict)
        unknown=False
        try:validate(normalize_selection({'visuals':[{**flat,'unknown_field':'x'}]},prefer_animation=True),INPUT)
        except ContractError:unknown=True
        check('normalization_does_not_discard_unknown_fields',unknown)
        from qingqi.providers import _validate_tutoring_text
        wrong_target=False
        try:_validate_tutoring_text('由 $m-5=0$，5 应该等于什么才能让差为0？',state['teaching_plan'],state,{'question':'解释这一步'})
        except ContractError as error:wrong_target=str(error).startswith('identity_variable_question')
        check('model_question_cannot_turn_known_constant_into_unknown',wrong_target)
        fresh_entry=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and '个位' in e['expression'])
        fresh=post('/api/practice/start',{'item_id':fresh_entry['id'],'request_id':'fresh-selected'})
        first_visual=post('/api/teach',{'session':fresh['session'],'request':{'request_id':'first-is-animation','question':'能给动画的教学方式吗'}})['response']
        check('first_request_after_selecting_question_can_be_animation',first_visual['visuals'][0]['template']=='identity_probe' and first_visual['repairs']==0)
        explicit=plan(Request.parse({'request_id':'explicit-connect','question':'请把(0,0)和(1,1)连起来，用动画演示。'}),entry)
        check('explicit_point_connection_is_not_replaced_by_identity_animation',explicit['operation']=='connect_points' and explicit['arguments']['visuals'][0]['template']=='coordinate_drawing')
    finally:owner.close();instance.shutdown();instance.server_close();model.shutdown();model.server_close()
    Path('education/.local/reports/identity-animation-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True,'real_model':False},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':run()
