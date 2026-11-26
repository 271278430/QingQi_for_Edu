"""New visual-task contracts, owned HTTP and composable pedagogy regressions."""
import http.cookiejar
import json
import threading
import urllib.request
import uuid
from visual_tasks_fixture import Fixture
from qingqi.contracts import ContractError,Request,Route
from qingqi.storage import Store
from qingqi.teaching_policy import choose
from qingqi.visual_teaching import render_visuals,validate_binding


def run():
    fixture=Fixture();fixture.start();owner=Store(fixture.root);checks=[]
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(fixture.base+path,timeout=60) as response:return json.load(response)
    boot=get('/api/bootstrap')
    def post(path,body):
        request=urllib.request.Request(fixture.base+path,data=json.dumps(body).encode(),headers={'Origin':fixture.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        with opener.open(request,timeout=60) as response:return json.load(response)
    def teach(session,q,rid=None):return post('/api/teach',{'session':session,'request':{'request_id':rid or uuid.uuid4().hex,'question':q}})
    def check(name,ok):
        assert ok,name
        checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
    def rejects(name,fn):
        try:fn()
        except ContractError:check(name,True)
        else:raise AssertionError(name)
    try:
        entry=next(e for e in owner.catalogue.bank.values() if '正方形' in e['expression'] and '-2' in e['expression'] and '三个顶点' in e['expression'])
        a=post('/api/practice/start',{'item_id':entry['id'],'request_id':'square'})
        linked=teach(a['session'],'你可以把这个坐标系的图片中的点都给我划线连起来吗','connect-screenshot')
        visual=linked['response']['visuals'][0]
        check('reported_three_points_really_have_three_segments',visual['kind']=='coordinates' and len(visual['points'])==3 and len(visual['segments'])==3)
        check('pure_connection_receipt_uses_real_tool_without_model_inference',not linked['response']['model_inference'] and '3 条' in linked['response']['text'])
        check('connect_does_not_add_missing_square_answer',len(visual['points'])==3 and all((p['x'],p['y'])!=(-2,-2) for p in visual['points']))
        calls=len(fixture.calls)
        replay=teach(a['session'],'你可以把这个坐标系的图片中的点都给我划线连起来吗','connect-screenshot')
        check('connected_visual_replay_is_identical_without_model_call',replay['response']['cache_hit'] and replay['response']['visuals']==linked['response']['visuals'] and len(fixture.calls)==calls)
        guided=teach(a['session'],'能一步步苏格拉底式的讲解吗')
        state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(guided['response']['run_id'],)).fetchone()[0]);plan=state['teaching_plan']
        check('stepwise_socratic_is_composable_not_rejected',plan['content_style']=='stepwise' and plan['interaction_style']=='guided_question' and not plan['allow_final_answer'] and guided['response']['teaching_action']=='ask')
        check('combined_strategy_has_explanation_budget_and_correct_label',plan['budget']['target_max']>=220 and guided['response']['route']['teaching']['label']=='逐步引导')
        from qingqi.teaching_plan import validate_text
        validate_text('纵坐标相同意味着两个点同高。你判断 AB 是哪个方向？能说明理由吗？',plan)
        check('related_subquestions_do_not_fail_a_valid_guided_turn',plan['budget']['questions']==1 and plan['budget']['review_questions']==2 and plan['budget']['hard_questions'] is None)
        check('excessive_questions_trigger_one_focus_rewrite_without_protocol_failure',guided['response']['repairs']==0 and state.get('quality_rewrite',{}).get('attempted') and len([c for c in fixture.calls if c.get('quality_rewrite')])==1)
        for phrase,reason in [('测试聚焦失败','failed_optional_rewrite_keeps_verified_original'),('测试聚焦泄露','unsafe_optional_rewrite_cannot_replace_verified_original')]:
            value=teach(a['session'],'逐步苏格拉底，'+phrase)['response']
            quality_state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(value['run_id'],)).fetchone()[0])
            check(reason,value['repairs']==0 and not quality_state['quality_rewrite']['accepted'] and quality_state['quality_rewrite'].get('failure_type') and '(-2,-2)' not in value['text'] and quality_state.get('soft_quality_flags'))
        animated=teach(a['session'],'请把图上的点逐条连起来，用动画展示。')
        check('connect_animation_draws_the_same_actual_edges',animated['response']['visuals'][0]['template']=='coordinate_drawing' and animated['response']['visuals'][0]['frames'][-1]['values']['visible_segments']==3)
        check('known_coordinates_are_not_duplicated_in_labels',all('(' not in p['label'] for p in visual['points']))
        step=teach(a['session'],'为什么 AB 是水平线？')
        state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(step['response']['run_id'],)).fetchone()[0])
        check('drawing_zero_questions_does_not_become_student_preference',not state['route']['teaching']['no_questions_requested'] and state['teaching_plan']['budget']['questions']==1)
        check('drawing_turns_do_not_advance_unverified_generic_steps',state['practice_assessment']['stage']==0)
        other=post('/api/sessions',{})['id']
        check('new_session_does_not_borrow_old_plot',teach(other,'把图上的点连起来。')['response']['teaching_action']=='clarify')
        false_claim=teach(other,'请给坐标提示，测试虚假完成。')
        check('claimed_drawing_without_execution_is_repaired',false_claim['response']['repairs']==1 and not false_claim['response'].get('visuals'))
        teach(a['session'],'取消')
        check('cancel_does_not_restore_plot_by_reference',teach(a['session'],'把图上的点连起来。')['response']['teaching_action']=='clarify')
        examples=fixture.examples()
        from qingqi.visual_tasks import plan
        existing=render_visuals(visuals=[examples['geometry']])['visuals'][0]
        edit=plan(Request('edit','把图上的 A 到 B 连起来。'),prior=existing)['arguments']['visuals'][0]
        check('point_edit_preserves_unmodified_polygons_and_circles',edit['polygons']==existing['polygons'] and edit['circles']==existing['circles'] and len(edit['segments'])==1)
        from qingqi.visual_tasks import normalize_references
        visual_state={'observations':[{'tool':'render_teaching_visual','result':{'visuals':[existing]}}]}
        cleaned=normalize_references('![图]('+existing['id']+')\n\n[图示：已经展示]\n解释坐标关系。',visual_state)
        check('owned_visual_reference_uses_structured_figure_without_broken_image',cleaned=='解释坐标关系。')
        rejects('invented_visual_reference_cannot_claim_a_real_asset',lambda:normalize_references('![图](visual:invented)',visual_state))
        for name,spec in examples.items():
            result=render_visuals(visuals=[spec])['visuals'][0]
            check('compiler_'+name,result==render_visuals(visuals=[spec])['visuals'][0])
        line=render_visuals(visuals=[examples['linear']])['visuals'][0]
        check('linear_samples_follow_original_formula',all(abs(p['y']-(2*p['x']+1))<1e-9 for p in line['samples']))
        specified=plan(Request('explicit-function','请画函数 y=2x+1 的图。'))['arguments']['visuals'][0]
        check('specified_function_parameters_are_bound_to_original_expression',specified['a']==2 and specified['b']==1)
        compact=plan(Request('compact-function','请画函数y=(x+1)^2的图。'))['arguments']['visuals'][0]
        function_state={'effective_request':{'question':'请画函数y=(x+1)^2的图。'},'route':{'teaching':{'allow_final_answer':False}},'observations':[],
                        'visual_task':{'arguments':{'visuals':[compact]}}}
        bound=validate_binding({'visuals':[compact]},function_state)['visuals'][0]
        check('chinese_adjacent_function_is_equivalent_and_has_current_provenance',compact['basis']=='problem' and (compact['a'],compact['b'],compact['c'])==(1,2,1) and '当前表达式' in bound['provenance'])
        rejects('different_polynomial_cannot_claim_current_expression',lambda:validate_binding({'visuals':[{**compact,'b':3}]},function_state))
        from qingqi.visual_expressions import polynomial
        rejects('polynomial_parser_does_not_execute_calls',lambda:polynomial('open(1)'))
        check('unsupported_function_clarifies_instead_of_drawing_another',bool(plan(Request('unsupported','请画函数y=1/x的图。')).get('clarify')))
        check('too_many_requested_functions_are_not_silently_truncated',bool(plan(Request('too-many','请画函数y=x、y=2x、y=3x的图。')).get('clarify')))
        specified_area=plan(Request('explicit-area','请画 3/4 的分数面积图。'))['arguments']['visuals'][0]
        check('specified_fraction_is_not_replaced_with_another_example',specified_area['numerator']==3 and specified_area['denominator']==4 and specified_area['basis']=='problem')
        animated_function=plan(Request('animated-function','请画函数y=(x+1)^2的动画。'))['arguments']['visuals'][0]
        function_result=render_visuals(visuals=[animated_function])['visuals'][0]
        check('specified_function_animation_is_not_a_static_plot',animated_function['template']=='function_trace' and all(abs(p['y']-(p['x']+1)**2)<1e-9 for p in function_result['plot']['samples']))
        animated_fraction=plan(Request('animated-fraction','请画3/4的分数动画。'))['arguments']['visuals'][0]
        check('specified_fraction_animation_keeps_original_fraction',animated_fraction['params']=={'numerator':3,'denominator':4} and render_visuals(visuals=[animated_fraction])['visuals'][0]['frames'][-1]['values']['filled']==3)
        from qingqi.visual_teaching import normalize_selection
        nested=normalize_selection({'visuals':[{'kind':'animation_scene','animation_scene':True,'basis':'example','title':'连点','params':{'template':'coordinate_drawing','points':visual['points'],'segments':[{k:v for k,v in s.items() if k!='length'} for s in visual['segments']]}}]})
        check('reported_nested_template_shape_is_normalized_once',nested['visuals'][0]['template']=='coordinate_drawing' and 'template' not in nested['visuals'][0]['params'] and 'animation_scene' not in nested['visuals'][0])
        neutral=plan(Request('neutral-connect','请连接(0,0)、(1,2)、(3,1)的所有点。'))['arguments']['visuals'][0]
        check('ordinary_slanted_connection_is_not_called_diagonal',all(s['role']=='connection' and s['style']=='solid' for s in neutral['segments']))
        check('square_connection_draws_edges_before_diagonal',[s['role'] for s in visual['segments']]==['edge','edge','diagonal'])
        rotated=plan(Request('rotated-square','请连接正方形已知点(0,0)、(1,1)、(2,0)。'))['arguments']['visuals'][0]
        check('rotated_square_edges_are_classified_by_distance',len([s for s in rotated['segments'] if s['role']=='edge'])==2)
        curve=render_visuals(visuals=[examples['quadratic']])['visuals'][0]
        check('quadratic_samples_follow_original_formula',all(abs(p['y']-p['x']**2)<1e-9 for p in curve['samples']))
        area=render_visuals(visuals=[examples['fraction_area']])['visuals'][0]
        check('fraction_area_has_exact_partition',area['ratio']==.75 and area['denominator']==4 and area['numerator']==3)
        frac=render_visuals(visuals=[examples['fraction_animation']])['visuals'][0]
        check('fraction_animation_ends_at_target',frac['frames'][-1]['values']['filled']==3)
        pyth=render_visuals(visuals=[examples['pythagorean']])['visuals'][0]
        check('pythagorean_areas_are_independently_correct',pyth['frames'][-1]['values']['c']==5 and pyth['frames'][-1]['values']['c_area']==25)
        bad={**examples['geometry'],'segments':[{'source':0,'target':9,'style':'solid','role':'edge'}]}
        rejects('nonexistent_segment_endpoint_rejected',lambda:render_visuals(visuals=[bad]))
        rejects('invalid_fraction_rejected',lambda:render_visuals(visuals=[{**examples['fraction_area'],'numerator':5}]))
        rejects('quadratic_zero_leading_coefficient_rejected',lambda:render_visuals(visuals=[{**examples['quadratic'],'a':0}]))
        rejects('point_label_cannot_contradict_plotted_position',lambda:render_visuals(visuals=[{'kind':'coordinates','title':'错标签','basis':'example','points':[{'label':'A(-2,1)','x':1,'y':-2}]}]))
        from qingqi.visual_tasks import validate_selection
        rejects('subset_of_requested_points_rejected_before_execution',lambda:validate_selection({'visuals':[{'kind':'coordinates','points':[{'label':'A','x':-2,'y':1}]}]}, {'visual_task':{'required_points':[{'x':-2,'y':1},{'x':1,'y':1}]}}))
        rejects('wrong_coordinate_pair_cannot_use_scattered_given_numbers',lambda:validate_binding({'visuals':[{'kind':'coordinates','basis':'problem','title':'错误点','points':[{'label':'A','x':-2,'y':-2}]}]}, {'effective_request':{'question':entry['expression']},'practice_entry':entry,'route':{'teaching':{'allow_final_answer':False}},'observations':[]}))
        rejects('missing_answer_coordinate_cannot_hide_in_example',lambda:validate_binding({'visuals':[{'kind':'coordinates','basis':'example','title':'例子','points':[{'label':'P','x':-2,'y':-2}]}]}, {'effective_request':{'question':entry['expression']},'practice_entry':entry,'route':{'teaching':{'allow_final_answer':False}},'observations':[]}))
        direct=choose(Request('direct','逐步讲解，不要反问，也不要答案。'),Route(('tutor',),()),[])
        check('direct_stepwise_and_answer_disclosure_are_independent',direct['plan']['content_style']=='stepwise' and direct['plan']['interaction_style']=='direct' and direct['budget']['questions']==0 and not direct['allow_final_answer'])
        rejects('explicit_no_questions_remains_a_hard_request',lambda:validate_text('纵坐标相同意味着两个点同高，你明白了吗？',direct['plan']))
        simple=choose(Request('stepwise','请分步讲解这道题。'),Route(('tutor',),()),[])
        complete=choose(Request('complete','请从头完整讲解解法。'),Route(('tutor',),()),[])
        check('stepwise_format_does_not_implicitly_reveal_final_answer',not simple['allow_final_answer'] and complete['allow_final_answer'])
        check('visual_and_animation_do_not_create_grades',get('/api/learning')['summary']['attempts']==0)
        import base64
        from multimodal_fixture import sample_image
        image=post('/api/tutor/images',{'request_id':'unclear-image','name':'unclear.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})
        value=post('/api/teach',{'session':other,'request':{'request_id':'unclear-draw','question':'图片模糊，请把图上所有点连起来。','images':[image['id']]}})
        check('partial_unclear_image_cannot_be_forced_into_a_completed_drawing',value['response']['teaching_action']=='clarify' and not value['response'].get('visuals'))
    finally:owner.close();fixture.close()
    from qingqi.agent import PROJECT
    (PROJECT.parent/'.local/reports/visual-tasks-v3-acceptance.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'real_model':False,'actual_zcode_runtime':True},ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__':run()
