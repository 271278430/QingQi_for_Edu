"""Real HTTP regression for a generic animation follow-up on the current problem."""
import http.cookiejar,json,urllib.request,urllib.error
from pathlib import Path
from owned_visual_fixture import Fixture

f=Fixture();checks=[]
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(f.base+path,timeout=20) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    request=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'X-Qingqi-CSRF':boot['csrf'],'Content-Type':'application/json'})
    try:r=opener.open(request,timeout=40)
    except urllib.error.HTTPError as error:r=error
    with r:
        result=json.load(r);assert r.status in (200,201),(r.status,result);return result
def check(name,value):
    assert value,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
try:
    before=get('/api/learning')['summary'];request={'request_id':'generic-animation','question':'给我一个动画帮助理解'}
    result=post('/api/teach',{'session':f.session,'request':request})['response']
    animation=result['visuals'][0]
    check('reported_generic_followup_produces_a_real_opposite_animation',animation['kind']=='animation_scene' and animation['template']=='opposite_numbers' and len(animation['frames'])>=4)
    check('known_visual_task_does_not_call_reasoning_only_model',not f.calls)
    check('animation_uses_given_example_and_preserves_unknown_parameter',animation['params']['value']==2 and '22' not in json.dumps(result['visuals']) and 'm=22' not in result['text'].replace(' ',''))
    check('accepted_turn_keeps_current_question_binding',get('/api/session?id='+f.session)['practice']['item']['id']==f.entry['id'])
    check('replay_does_not_duplicate_tool_or_model_work',post('/api/teach',{'session':f.session,'request':request})['response']['run_id']==result['run_id'] and not f.calls)
    check('animation_assistance_does_not_write_independent_grade',get('/api/learning')['summary']['attempts']==before['attempts'])
    repeated=post('/api/teach',{'session':f.session,'request':{'request_id':'animation-again','question':'再给我一个动画帮助理解'}})['response']
    check('subsequent_animation_request_reuses_same_owned_scene',repeated['visuals'][0]['template']=='opposite_numbers' and not f.calls)
    f.reply_valid=True
    result=post('/api/teach',{'session':f.session,'request':{'request_id':'concept-static','question':'从本质讲解相反数的概念，给我一张静态图帮助理解，不要最终答案。'}})['response']
    tools=next(c['tools'] for c in f.calls if c.get('tools'))
    branches=tools[0]['function']['parameters']['properties']['visuals']['items']['oneOf']
    check('actual_model_request_uses_small_current_visual_contract',len(json.dumps(tools))<12000 and len(branches)<=6 and all(b['properties']['kind']['enum'][0]!='animation_scene' for b in branches))
    check('narrowed_tool_still_runs_through_real_registry_and_owner',result['visuals'][0]['kind']=='number_line' and result['text'] and result['tool_calls']==1)
    from qingqi.contracts import Identity,Request
    from qingqi.visual_tasks import plan
    from qingqi.animation_teaching import render
    check('visual_reference_does_not_cross_student_or_session',f.owner.prior_visual(Identity('edu-other',f.session),f.entry,all_kinds=True) is None and f.owner.prior_visual(Identity(f.student,'another-session'),f.entry,all_kinds=True) is None)
    check('explicit_text_only_does_not_plan_an_animation',plan(Request('text-only','只用文字，不要动画'),f.entry,animation) is None)
    check('mirror_positions_are_exact_and_finite_through_every_keyframe',all(frame['values']['value']==-frame['values']['opposite'] for frame in animation['frames']))
    generic=render({'template':'function_trace','params':{'function':'quadratic','a':1,'b':0,'c':0,'domain':[-3,3],'markers':[{'label':'顶点','x':0,'y':0}]}})
    check('generic_function_animation_does_not_borrow_another_problem_solution',all('唯一正零点' not in step['explanation'] and '区间最值' not in step['explanation'] for step in generic['inspection_steps']))
finally:f.close()
Path('education/.local/reports/owned-visual-acceptance.local.json').write_text(json.dumps({'checks':checks,'passed':len(checks)},indent=2),encoding='utf-8')
