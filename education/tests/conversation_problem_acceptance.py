"""Regression for the exact reported same-session follow-up, through product HTTP."""
import base64
import copy
import http.cookiejar
import json
import urllib.request
from conversation_problem_fixture import Fixture, SOURCE
from multimodal_fixture import sample_image
from qingqi.storage import Store
from qingqi.contracts import Identity, ContractError, canonical
from qingqi.visual_teaching import validate_binding

f=Fixture(); f.start(); owner=Store(f.root); checks=[]
o=urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(f.base+path,timeout=90) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    with o.open(urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']}),timeout=90) as r:return json.load(r)
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def continuity(response):return json.loads(owner.db.execute('select state from runs where id=?',(response['run_id'],)).fetchone()[0])['route']['continuity']
try:
    image=post('/api/tutor/images',{'request_id':'picture','name':'cubic.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})['id']
    session=post('/api/sessions',{})['id']; identity=Identity('edu-math-student',session)
    def teach(q,rid,images=None):
        try:return post('/api/teach',{'session':session,'request':{'request_id':rid,'question':q,**({'images':images} if images else {})}})['response']
        except Exception:
            row=owner.db.execute('select state from runs order by id desc limit 1').fetchone()
            if row:
                state=json.loads(row[0]);print(json.dumps({k:state.get(k) for k in ('error','last_error','route','function_task')},ensure_ascii=False),flush=True)
            raise
    full=teach('直接给完整的答案','full',[image])
    animation=teach('给出关键可视化教学动画','animation')
    check('reported_short_animation_retains_original_image_problem_and_published_solution',continuity(animation)=='continuation' and len(animation.get('visuals',[]))==1 and animation['visuals'][0]['template']=='function_reasoning' and animation['visuals'][0]['reasoning_lesson']['mode']=='solution' and '−3' in animation['text'])
    requested=teach('给出答案和可视化辅导','answer-and-visual')
    check('natural_give_answer_and_visual_uses_original_solution',all(v['basis']=='problem' for v in requested.get('visuals',[])) and '−3' in requested['text'])
    redrawn=teach('重新给一个图解，其中如果小数位太多就用分数或者其他形式表示，不要算干净','reported-redraw')
    check('reported_redraw_and_numeric_preference_remain_same_problem',continuity(redrawn)=='continuation' and len(redrawn.get('visuals',[]))==1 and redrawn['visuals'][0]['template']=='function_reasoning' and redrawn['teaching_action']!='clarify')
    reformatted=teach('这些小数应改为分数或根号显示，请重新给一个图解','format-is-not-correction')
    fmt_state=json.loads(owner.db.execute('select state from runs where id=?',(reformatted['run_id'],)).fetchone()[0])
    check('format_change_does_not_overwrite_owned_image_question',fmt_state['image_question']['text']==SOURCE and len(reformatted['visuals'])==1 and reformatted['visuals'][0]['reasoning_lesson']['given']['k']==2)
    again=teach('就是上面那道题','above')
    check('above_problem_reference_retains_same_problem',continuity(again)=='continuation' and owner.current_problem(identity)['image_question']['text']==SOURCE)
    check('one_ocr_for_entire_image_conversation',len([c for c in f.calls if c.get('required_output_schema')])==1)
    swapped=teach('换一种方法解释','method')
    check('change_method_is_not_change_problem',continuity(swapped)=='continuation')
    natural=teach('能换一种更直观的说法吗？','natural-followup')
    payload=f.calls[-1]['input']
    check('natural_followup_receives_original_problem_and_published_solution',natural['controller']=='glm_general_text_controller' and payload.get('problem',{}).get('text')==SOURCE and any('−3' in t['reply'] for t in payload.get('history',[])))
    check('natural_explanation_preserves_owned_image_resource',owner.current_problem(identity).get('image_question',{}).get('images')==[image] and not natural.get('visuals'))
    simpler=teach('能更简单一点吗？','natural-simpler')
    payload=f.calls[-1]['input']
    check('successive_natural_followup_receives_previous_explanation',simpler['controller']=='glm_general_text_controller' and payload.get('problem',{}).get('text')==SOURCE and any(t['question']=='能换一种更直观的说法吗？' for t in payload.get('history',[])))
    back_to_visual=teach('重新给一个图解','after-natural-visual')
    check('original_problem_visual_still_available_after_natural_tutoring',len(back_to_visual['visuals'])==1 and back_to_visual['visuals'][0]['template']=='function_reasoning' and all(v['basis']=='problem' for v in back_to_visual['visuals']) and len([c for c in f.calls if c.get('required_output_schema')])==1)
    # 模拟旧版本两次clarify覆盖当前题，静态原题仍从已接受历史恢复。
    with owner.db:
        owner.db.execute('update dialogue_state set data=?,updated=0 where student=? and session=?',(canonical({'verified_work':None,'active_task':None,'pending':None}),identity.student,identity.session))
    recovered=teach('给出关键可视化教学动画','recovered')
    check('legacy_empty_binding_recovers_same_session_accepted_question',len(recovered['visuals'])==1 and recovered['visuals'][0]['reasoning_lesson']['given']['k']==2)
    with owner.db:owner.db.execute('update dialogue_state set updated=0 where student=? and session=?',(identity.student,identity.session))
    expired=owner.dialogue(identity)
    check('ttl_preserves_static_question_and_expires_teaching_preferences',expired['expired'] and expired['verified_work'].get('image_question') and expired['pending'] is None and not expired.get('no_final_requested'))
    after=teach('上面这题画个图','expired')
    check('expired_question_still_teaches_original_cubic',bool(after.get('visuals')))
    state=json.loads(owner.db.execute('select state from runs where id=?',(animation['run_id'],)).fetchone()[0])
    check('function_analysis_runs_through_native_zcode_tool_chain',[v['tool'] for v in state['observations']]==['analyze_function','render_teaching_visual'])
    v=next(v for v in animation['visuals'] if v['kind']=='animation_scene')
    solution_animation=teach('把完整解题步骤用动画演示，并直接给答案','explicit-solution-animation')
    solved_visual=next(v for v in solution_animation['visuals'] if v['kind']=='animation_scene' and v['template']=='function_reasoning')
    reasoning=solved_visual['reasoning_lesson']
    check('cubic_markers_focus_and_steps_are_mathematically_bound',reasoning['given']=={'k':2,'constant':1,'parameter':'a','interval':[-1,1]} and any(p['x']==1 and abs(p['y'])<1e-9 for p in reasoning['candidates']) and len(reasoning['steps'])>=7)
    check('cubic_samples_and_frames_have_exact_values',all(abs(point['y']-(2*point['x']**3-3*point['x']**2+1))<1e-8 for point in reasoning['curve']['samples']) and v['frames'][-1]['at']==v['duration'])
    check('cross_student_and_session_never_recover_question',owner.current_problem(Identity(identity.student,'other-session')) is None and owner.current_problem(Identity('other-student',session)) is None)
    raw=copy.deepcopy(state['observations'][1]['result']['visuals'][0]);spec=copy.deepcopy(state['observations'][0]['result']['approved_solution_visuals'][0]);spec['params']['a']=3
    try:validate_binding({'visuals':[spec]},state)
    except ContractError:check('function_parameters_cannot_be_changed_by_model',True)
    else:raise AssertionError('modified parameters accepted')
    hint=teach('给出关键可视化教学动画，不要答案','hint')
    check('current_no_answer_overrides_previous_disclosure',hint['visuals'][0]['reasoning_lesson']['mode']=='hint' and 'solved' not in hint['visuals'][0]['reasoning_lesson'] and '−3' not in hint['text'])
    replay=teach('给出关键可视化教学动画','animation')
    check('replay_is_identical_without_new_ocr_or_tools',replay['cache_hit'] and replay['visuals']==animation['visuals'])
    check('tutoring_animation_does_not_create_grades',get('/api/learning')['summary']['attempts']==0)
    new=teach('请画函数 y=2x+1 的动画，不用讲解','new-function')
    check('explicit_new_function_replaces_current_image',next(v for v in new['visuals'] if v['kind']=='animation_scene')['plot']['function']=='linear' and next(v for v in new['visuals'] if v['kind']=='animation_scene')['plot']['a']==2)
    rational=teach('请用动画画一次函数 y=x/3，不用讲解','rational-function')
    check('literal_rational_function_retains_exact_fraction_label','frac' in next(v for v in rational['visuals'] if v['kind']=='animation_scene')['plot']['display']['formula'] and next(v for v in rational['visuals'] if v['kind']=='animation_scene')['plot']['a']==1/3)
    check('new_text_function_does_not_resurrect_old_image',owner.current_problem(identity).get('image_question') is None)
    teach('取消当前任务','cancel')
    check('cancel_blocks_old_question_recovery',owner.current_problem(identity) is None)
    session=post('/api/sessions',{})['id']
    text=teach(SOURCE+'直接给完整答案','text')
    text_follow=teach('给出关键可视化教学动画','text-follow')
    check('plain_text_problem_also_survives_generic_followup',len(text_follow['visuals'])==1 and text_follow['visuals'][0]['reasoning_lesson']['given']['k']==2 and text_follow['visuals'][0]['reasoning_lesson']['mode']=='solution')
    session=post('/api/sessions',{})['id']
    teach('二次函数的顶点是什么？','concept')
    teach('换一种方法讲解上面的知识点','concept-follow')
    payload=f.calls[-1]['input']
    check('general_tutor_receives_owned_topic_and_relevant_history',payload.get('problem',{}).get('text')=='二次函数的顶点是什么？' and len(payload.get('history',[]))>=1)
    teach('能更简单一点吗？','concept-simpler')
    payload=f.calls[-1]['input']
    check('natural_concept_followup_keeps_original_topic',payload.get('problem',{}).get('text')=='二次函数的顶点是什么？' and bool(payload.get('history')))
    teach('平方根是什么？','new-concept')
    payload=f.calls[-1]['input']
    check('explicit_new_concept_does_not_inherit_old_topic',payload.get('problem',{}).get('text')=='平方根是什么？' and not payload.get('history'))
    calls=len(f.calls)
    teach('你好','unrelated-chat')
    check('chat_does_not_trigger_old_problem_tutoring',len(f.calls)==calls)
    separate=teach('1/3','independent-arithmetic')
    separate_state=json.loads(owner.db.execute('select state from runs where id=?',(separate['run_id'],)).fetchone()[0])
    check('independent_arithmetic_does_not_inherit_old_concept',not separate_state.get('general_turns') and not separate_state.get('problem_question'))
    session=post('/api/sessions',{})['id']
    teach('解方程 2x+3=7，直接给答案','linear')
    linear=teach('就是上面那道题','linear-above')
    linear_state=json.loads(owner.db.execute('select state from runs where id=?',(linear['run_id'],)).fetchone()[0])
    check('free_linear_question_also_binds_above_reference',linear_state.get('practice_entry',{}).get('id')=='student-linear' and continuity(linear)=='continuation' and linear['teaching_action']!='clarify')
    kept=teach('不要换题，就是上面那道题','keep-problem')
    check('negated_change_request_keeps_current_question',continuity(kept)=='continuation' and kept['teaching_action']!='clarify')
    teach('换一道新题','explicit-new')
    check('explicit_change_without_new_content_clears_old_binding',owner.current_problem(Identity('edu-math-student',session)) is None)
    print(json.dumps({'passed':len(checks),'root':str(f.root)},ensure_ascii=False))
finally:owner.close();f.close()
