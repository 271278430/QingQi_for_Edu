import base64
import http.cookiejar
import json
import urllib.request
from pathlib import Path
from geometry_product_fixture import Fixture
from multimodal_fixture import sample_image
from qingqi.storage import Store
from qingqi.contracts import ContractError
from qingqi.contracts import Identity
from qingqi.projection import project_response
import copy
from qingqi.visual_teaching import validate_binding

def motion(response):return next(v for v in response['visuals'] if v['kind']=='animation_scene')

f=Fixture();f.start();owner=Store(f.root);checks=[]
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(f.base+path,timeout=90) as response:return json.load(response)
boot=get('/api/bootstrap')
def post(path,body):
    with o.open(urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']}),timeout=90) as response:return json.load(response)
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
try:
    image=post('/api/tutor/images',{'request_id':'picture','name':'geometry.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})['id']
    session=post('/api/sessions',{})['id']
    def teach(q,rid,images=None):
        try:return post('/api/teach',{'session':session,'request':{'request_id':rid,'question':q,**({'images':images} if images else {})}})['response']
        except Exception:
            last=json.loads(owner.db.execute('select state from runs order by id desc limit 1').fetchone()[0])
            print(json.dumps({k:last.get(k) for k in ('error','last_error','visual_task','geometry_task','route')},ensure_ascii=False),flush=True)
            raise
    hint=teach('解这道题','hint',[image])
    check('image_uses_symbolic_geometry_and_default_related_diagram',hint['controller']=='grounded_symbolic_geometry_v1' and hint['teaching_action']=='ask' and len(f.calls)==1 and hint['tool_calls']==2 and hint['visuals'][0]['kind']=='coordinates' and len(hint['visuals'][0]['points'])==6)
    progressed=teach('这两个角都是45度，接下来怎么做？','next-hint')
    check('geometry_guidance_advances_instead_of_repeating',progressed['text']!=hint['text'] and '的像' in progressed['text'] and progressed['teaching_action'] in {'ask','explain'})
    full=teach('我想要你直接给我完整答案，并且附上合适的动画教学','complete')
    check('reported_full_answer_animation_request_is_completed',full['teaching_action']=='give_answer' and full['repairs']==0 and len(full['visuals'])==1 and len(f.calls)==1)
    check('all_three_parts_have_verified_results',all(word in full['text'] for word in ('（1）','（2）','（3）','45','8 - 2 x','\\le4')) and '\\fmac' not in full['text'])
    check('full_answer_has_five_trusted_teaching_steps',all(v['lesson']['mode']=='solution' and len(v['lesson']['steps'])==5 for v in full['visuals'] if v['kind']=='animation_scene'))
    scoped=teach('请把第（1）问的完整解题步骤做成动画。','proof-only')
    check('complete_steps_phrase_selects_only_requested_proof',len(scoped['visuals'])==1 and motion(scoped)['template']=='triangle_rotation' and motion(scoped)['lesson']['mode']=='solution')
    ratio=teach('请把第（2）问的完整解题步骤做成动画。','ratio-only')
    check('ratio_question_has_its_own_symbolic_steps',len(ratio['visuals'])==1 and motion(ratio)['lesson']['goal']=='ratio' and not motion(ratio).get('plot') and '\\sim' in motion(ratio)['lesson']['steps'][3]['formula'] and len(motion(ratio)['geometry']['helpers'])==2)
    why=teach('这两个锐角为什么相等？','why-similarity')
    check('animation_followup_explains_current_geometry','并不固定为' in why['text'] and '\\perp' in why['text'] and why['teaching_action']=='explain' and why['tutoring_scope']['active_part']==2)
    degenerate=teach('重合的时候还可以用相似吗？','degenerate')
    check('degenerate_followup_does_not_claim_similarity','不能' in degenerate['text'] and '直接比较' in degenerate['text'])
    motion_lesson=next(v['lesson'] for v in full['visuals'] if v.get('template')=='geometry_motion')
    check('motion_teaches_equation_and_domain',motion_lesson['domain']=={'upper':4.0,'upper_closed':True} and any('y' in s.get('formula','') for s in motion_lesson['steps']))
    state=json.loads(owner.db.execute('select state from runs where id=?',(full['run_id'],)).fetchone()[0])
    check('native_zcode_solver_and_visual_are_both_observed',[o['tool'] for o in state['observations']]==['solve_geometry','render_teaching_visual'])
    check('complex_image_question_drives_answer_budget',state['teaching_plan']['difficulty']['level']==3 and state['teaching_plan']['budget']['target_max']>=900)
    legacy=copy.deepcopy(full)
    legacy['visuals']=[v for v in legacy['visuals'] if v['kind']=='animation_scene']
    for v in legacy['visuals']:
        v.pop('lesson');v['params'].pop('lesson_mode');v['params'].pop('lesson_goal',None);v['geometry'].pop('bounds');v['geometry'].pop('ray_end')
    projected=project_response(legacy)
    check('legacy_visual_projection_restores_teaching_steps_without_mutating_record',all(v.get('lesson') for v in projected['visuals']) and all(not v.get('lesson') for v in legacy['visuals']) and [v['id'] for v in projected['visuals']]==[v['id'] for v in legacy['visuals']])
    replay=teach('我想要你直接给我完整答案，并且附上合适的动画教学','complete')
    check('complete_answer_replay_is_identical_without_new_calls',replay['cache_hit'] and replay['visuals']==full['visuals'] and len(f.calls)==1)
    correction=teach('第（1）问的∠ECD为什么是90度？','wrong-angle')
    check('incorrect_previous_angle_is_corrected_from_geometry_report','45' in correction['text'] and 'ECD=90' not in correction['text'])
    selected=teach('直接给第（2）问的完整答案。','only-part-two')
    check('explicit_answer_scope_does_not_reveal_other_parts','（2）' in selected['text'] and '（1）' not in selected['text'] and '（3）' not in selected['text'])
    concise=teach('只要最终答案，不要推导。','concise')
    check('explicit_concise_answer_is_actually_concise',len(concise['text'])<150 and '旋转' not in concise['text'])
    static=teach('请画出原题的几何示意图。','static')
    check('geometry_static_drawing_has_six_points_and_actual_segments',static['visuals'][0]['kind']=='coordinates' and len(static['visuals'][0]['points'])==6 and len(static['visuals'][0]['segments'])>=6)
    connected=teach('请把图中的点全部连起来。','connect')
    check('prior_verified_geometry_points_are_all_connected',len(connected['visuals'][0]['segments'])==15 and '15' in connected['text'])
    animation=teach('请画几何动画，不要直接给答案。','animation-only')
    check('animation_has_no_static_requirement_or_zero_point_receipt',len(animation['visuals'])>=1 and sum(v['kind']=='animation_scene' for v in animation['visuals'])==1 and '0 个点' not in animation['text'] and '播放' in animation['text'])
    check('hint_animation_does_not_disclose_full_proof',all(v['lesson']['mode']=='hint' and len(v['lesson']['steps'])>=3 and not any('DE=DF' in s.get('formula','') for s in v['lesson']['steps']) for v in animation['visuals'] if v['kind']=='animation_scene'))
    function=teach('请用动画画一次函数 y=2x+1，不用讲解。','other-function')
    check('explicit_other_function_is_not_hijacked_by_geometry',function['controller']!='grounded_symbolic_geometry_v1' and motion(function)['template']=='function_trace' and motion(function)['params']['a']==2)
    fraction=teach('请用动画演示分数 3/4，不用讲解。','other-fraction')
    check('explicit_other_fraction_is_not_hijacked_by_geometry',fraction['controller']!='grounded_symbolic_geometry_v1' and motion(fraction)['params']['numerator']==3 and motion(fraction)['params']['denominator']==4)
    described=teach('只描述这张图片的内容，不要解题。','describe')
    check('image_description_is_not_hijacked_by_geometry',described['controller']=='glm_vision_text_controller' and '不展开证明' in described['text'])
    raw=next(v for v in state['observations'][0]['result']['approved_visuals'] if v.get('template')=='geometry_motion')
    try:validate_binding({'visuals':[{**raw,'params':{**raw['params'],'ratio':2}}]},state)
    except ContractError:check('model_cannot_replace_verified_geometry_parameters',True)
    else:raise AssertionError('unbound geometry accepted')
    restricted=json.loads(owner.db.execute('select state from runs where id=?',(hint['run_id'],)).fetchone()[0])
    try:validate_binding({'visuals':[{**raw,'params':{**raw['params'],'lesson_mode':'solution'}}]},restricted)
    except ContractError:check('full_storyboard_cannot_bypass_hint_permission',True)
    else:raise AssertionError('unauthorized full lesson accepted')
    check('geometry_tutoring_and_animation_do_not_create_grades',get('/api/learning')['summary']['attempts']==0)
    session=post('/api/sessions',{})['id']
    first_connection=teach('请把图中的点全部连起来。','first-connect',[image])
    check('missing_coordinate_clarification_is_resolved_by_owned_construction',first_connection['controller']=='grounded_symbolic_geometry_v1' and len(first_connection['visuals'])==1 and len(first_connection['visuals'][0]['segments'])==15)
    connected_animation=teach('请用动画逐条连接图中的全部点。','first-connect-animation')
    check('explicit_connection_animation_contains_all_requested_segments',len(connected_animation['visuals'])==1 and motion(connected_animation)['template']=='coordinate_drawing' and len(motion(connected_animation)['geometry']['segments'])==15 and motion(connected_animation)['frames'][-1]['values']['visible_segments']==15)
    check('referenced_image_never_crosses_session_student_or_ttl',owner.referenced_image(Identity('edu-math-student','other-session')) is None and owner.referenced_image(Identity('other-student',session)) is None and owner.referenced_image(Identity('edu-math-student',session),ttl=-1) is None)
    teach('取消当前任务','cancel')
    check('explicit_cancel_prevents_restoring_old_image',owner.referenced_image(Identity('edu-math-student',session)) is None)
finally:owner.close();f.close()
Path('education/.local/reports/geometry-product-acceptance.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'actual_zcode_runtime':True,'real_model':False},ensure_ascii=False,indent=2),encoding='utf-8')
