"""HTTP/native-tool acceptance of useful paired visuals and persisted teaching modes."""
import base64,http.cookiejar,json,urllib.request,urllib.error
from pathlib import Path
from geometry_product_fixture import Fixture
from multimodal_fixture import sample_image
from qingqi.storage import Store
from qingqi.contracts import Identity

f=Fixture();f.start();owner=Store(f.root);checks=[]
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(f.base+path,timeout=90) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'X-Qingqi-CSRF':boot['csrf'],'Content-Type':'application/json'})
    try:r=o.open(req,timeout=90)
    except urllib.error.HTTPError as error:r=error
    with r:
        value=json.load(r);assert r.status<400,value
        return value
def check(name,ok):assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def single_motion(response,template):
    visuals=response.get('visuals',[])
    return len(visuals)==1 and visuals[0]['kind']=='animation_scene' and visuals[0].get('template')==template and len(visuals[0].get('frames',[]))>1
try:
    image=post('/api/tutor/images',{'request_id':'photo','name':'geometry.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})['id']
    session=post('/api/sessions',{})['id'];identity=Identity('edu-'+boot['profile'],session)
    def teach(q,id,images=None):return post('/api/teach',{'session':session,'request':{'request_id':id,'question':q,**({'images':images} if images else {})}})['response']
    first=teach('第（1）问：为什么要连接CD？请讲清楚当前这一步。','first',[image])
    check('default_geometry_relationship_uses_only_one_static_picture',len(first['visuals'])==1 and first['visuals'][0]['kind']=='coordinates' and '动画' not in first['text'])
    mode=owner.dialogue(identity).get('teaching_mode',{})
    check('conceptual_why_uses_explanation_and_saves_mode',mode.get('mode')=='explain' and mode.get('part')==1 and mode.get('source_run_id')==first['run_id'])
    animated=teach('第（1）问请用动画讲清楚旋转这一步。','animation')
    a=animated['visuals'][0]
    check('explicit_animation_uses_one_actual_animation',single_motion(animated,'triangle_rotation'))
    check('animation_teaches_original_auxiliary_line_then_rotation',any('CD' in step.get('formula','') for step in a['lesson']['steps']) and len(a['lesson']['steps'])>=3 and len(a['geometry']['points'])>=6)
    continued=teach('继续讲当前这一步','continue')
    if owner.dialogue(identity).get('teaching_mode',{}).get('mode')!='explain' or continued['text']==first['text']:
        print(json.dumps({'diagnosis':{'mode':owner.dialogue(identity).get('teaching_mode'),'first':first['text'],'continued':continued['text']}},ensure_ascii=False),flush=True)
    check('same_problem_continuation_restores_teaching_mode',owner.dialogue(identity)['teaching_mode']['mode']=='explain' and continued['text']!=first['text'])
    socratic=teach('第（1）问先用苏格拉底式追问引导我，不要给答案。','socratic')
    check('explicit_socratic_request_changes_only_teaching_mode',owner.dialogue(identity)['teaching_mode']['mode']=='socratic' and socratic['teaching_action']=='ask' and len(socratic['visuals'])==1 and socratic['visuals'][0]['kind']=='coordinates')
    confused=teach('我还是不懂，旋转这一步具体为什么成立？','confused')
    check('continued_struggle_switches_to_step_explanation',owner.dialogue(identity)['teaching_mode']['mode']=='explain' and confused['route']['teaching']['mode']=='explain')
    second=teach('第（2）问给我一点提示，先不要最终答案。','second')
    check('new_question_uses_hint_mode_without_inheriting_old_mode',owner.dialogue(identity)['teaching_mode']['mode']=='heuristic' and owner.dialogue(identity)['teaching_mode']['part']==2)
    check('second_question_picture_matches_current_question',len(second['visuals'])==1 and second['visuals'][0]['kind']=='coordinates' and second['visuals'][0]['teaching_part']==2)
    full=teach('第（1）问直接给完整解答，配合图和动画。','full')
    check('request_mentioning_both_forms_still_publishes_only_one',len(full['visuals'])==1 and full['teaching_action']=='give_answer')
    explained=teach('第（1）问解释刚才旋转对应为什么成立。','published-follow')
    check('published_solution_can_be_explained_in_context',owner.dialogue(identity)['teaching_mode']['mode']=='explain' and next(v for v in explained['visuals'] if v['kind']=='animation_scene')['lesson']['mode']=='solution')
    other=teach('第（3）问解释一下该从哪里开始。','unpublished-part')
    check('published_answer_permission_does_not_leak_to_another_question',len(other['visuals'])==1 and not other['route']['teaching']['allow_final_answer'] and 'y=8' not in other['text'].replace(' ',''))
    mixed=teach('第（1）问给答案和静态图，第（2）问给提示和静态图，不要第二问答案。','mixed-pictures')
    import math
    pa,pb,pc,pd,*_=mixed['visuals'][0]['points']
    not_midpoint=not math.isclose(pd['x'],(pa['x']+pb['x'])/2,abs_tol=1e-9) or not math.isclose(pd['y'],(pa['y']+pb['y'])/2,abs_tol=1e-9)
    check('two_explicit_picture_requests_choose_the_current_question_only',len(mixed['visuals'])==1 and mixed['visuals'][0]['kind']=='coordinates' and mixed['visuals'][0]['teaching_part']==2 and not_midpoint and mixed['tutoring_scope']['units'][0]['allow_final_answer'] and not mixed['tutoring_scope']['units'][1]['allow_final_answer'])
    static=teach('第（1）问直接给完整解答，只给静态图，不要动画。','static')
    check('static_only_response_never_claims_an_animation',static.get('visuals') and all(v['kind']!='animation_scene' for v in static['visuals']) and '动画用来' not in static['text'])
    text=teach('第（1）问直接给完整答案，这次只用文字，不要图和动画。','text')
    check('text_only_request_has_no_fake_visual_claim',not text.get('visuals') and '动画用来' not in text['text'])
    before=len(f.calls);replay=teach('第（1）问直接给完整解答，配合图和动画。','full')
    check('single_visual_replays_without_new_inference',replay['cache_hit'] and replay['visuals']==full['visuals'] and len(f.calls)==before)
    check('mode_and_visuals_do_not_write_mastery',get('/api/learning')['summary']['attempts']==0)
    restored=get('/api/session?id='+session)
    check('refresh_returns_persisted_mode_and_matching_artifact',restored['messages'][0]['response']['route']['teaching']['mode']=='explain' and len(restored['messages'][0]['response']['visuals'])==1 and restored['messages'][0]['response']['visuals'][0]['kind']=='coordinates')
    from qingqi.agent import Agent
    from qingqi.contracts import Request,ContractError
    request=Request.parse({'request_id':'static-unavailable-animation','question':'解释当前概念'})
    state={'route':{'intents':['tutor'],'task_dag':{'nodes':[]},'teaching':{'allow_final_answer':False}},'native_schedule':{'order':[]},'observations':[],'effective_request':request.dump(),'teaching_plan':{'visual':{'prefer_animation':True,'explicit_animation':False}}}
    action={'tool':'render_teaching_visual','arguments':{'visuals':[{'kind':'table','basis':'example','title':'条件与动作','columns':['条件','动作'],'rows':[['比较系数','分别整理变化项和固定项']]}]}}
    Agent.__new__(Agent)._bind(request,state,action)
    check('default_visual_preference_does_not_reject_a_legal_static_explanation',True)
    from qingqi.teaching_visual_pair import prepare
    state['teaching_plan']['visual']['delivery']='animation'
    selected=prepare(action['arguments'],state)
    check('unsupported_automatic_motion_records_the_actual_picture_selection',len(selected['visuals'])==1 and selected['visuals'][0]['kind']=='table' and state['teaching_plan']['visual']['delivery']=='picture' and not state['teaching_plan']['visual']['prefer_animation'])
    state['teaching_plan']['visual']['explicit_animation']=True
    denied=False
    try:Agent.__new__(Agent)._bind(request,state,action)
    except ContractError:denied=True
    check('explicit_animation_still_requires_actual_motion',denied)
    Path('education/.local/reports/contextual-teaching.local.json').write_text(json.dumps({'checks':checks,'passed':len(checks),'isolated':True},indent=2),encoding='utf-8')
finally:owner.close();f.close()
