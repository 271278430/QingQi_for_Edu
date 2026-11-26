"""Semantic reasoning checks through isolated product HTTP, not just visible animation."""
import base64
import http.cookiejar
import json
import urllib.error
import urllib.request
from pathlib import Path
from conversation_problem_fixture import Fixture,SOURCE
from multimodal_fixture import sample_image
from qingqi.storage import Store

def run():
    f=Fixture();f.start();owner=Store(f.root);checks=[]
    o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with o.open(f.base+path,timeout=100) as r:return json.load(r)
    boot=get('/api/bootstrap')
    def post(path,body):
        req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        try:
            with o.open(req,timeout=100) as r:return json.load(r)
        except urllib.error.HTTPError as e:
            print(e.read().decode(),flush=True)
            row=owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone()
            if row:
                state=json.loads(row[0]);print(json.dumps({k:state.get(k) for k in ('last_error','presentation','visual_task','problem_question')},ensure_ascii=False),flush=True)
            raise
    def teach(s,q,rid,images=None):return post('/api/teach',{'session':s,'request':{'request_id':rid,'question':q,**({'images':images} if images else {})}})['response']
    def motion(response):return next(v for v in response['visuals'] if v['kind']=='animation_scene')
    def check(name,value):
        assert value,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
    try:
        image=post('/api/tutor/images',{'request_id':'photo','name':'original.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})['id']
        session=post('/api/sessions',{})['id']
        hint=teach(session,'请针对原题用动画演示推理，先不要答案','hint',[image]);v=motion(hint);h=v['reasoning_lesson']
        check('hint_has_coherent_picture_and_original_problem_animation',len(hint['visuals'])==1 and sum(x['kind']=='animation_scene' for x in hint['visuals'])==1 and v['template']=='function_reasoning' and v['basis']=='problem' and h['kind']=='function' and h['mode']=='hint')
        check('hint_keeps_original_coefficients_and_interval',h['given']['k']==2 and h['given']['constant']==1 and h['given']['interval']==[-1,1])
        check('zero_cases_have_meaningful_mathematical_comparison',[p['root_count'] for p in h['cases']]==[0,1,2] and h['cases'][0]['minimum']['y']>0 and h['cases'][1]['minimum']['y']==0 and h['cases'][2]['minimum']['y']<0)
        check('each_step_has_condition_action_rule_and_formula',all(step['given'] and step['action'] and step['rule'] and step['formula'] for step in h['steps']))
        check('formula_commands_survive_without_control_character_corruption',r'\to+\infty' in h['steps'][1]['formula'] and all(not any(c in step['formula'] for c in '\t\r\b\f\v') for step in h['steps']))
        check('hint_stops_at_conditions_without_final_parameter_or_result','solved' not in h and 'curve' not in h and 'negative_root' not in h and h['steps'][-1]['scene']=='conditions' and not any(s['scene'] in {'solve','factor','extrema','result'} for s in h['steps']))
        full=teach(session,'用原题的动画完整演示解题步骤，直接给答案','full');lesson=motion(full)['reasoning_lesson']
        check('full_lesson_has_parameter_roots_derivative_and_extrema_stages',{'solve','factor','derivative','extrema','result'}<=set(s['scene'] for s in lesson['steps']))
        check('actual_problem_solution_is_mathematically_exact',lesson['solved']['parameter']=='3' and lesson['solved']['root']=='1' and lesson['solved']['minimum']=='−4' and lesson['solved']['maximum']=='1' and lesson['solved']['sum']=='−3')
        check('only_endpoints_and_in_interval_stationary_points_are_compared',[(c['x'],c['y']) for c in lesson['candidates']]==[(-1,-4),(0,1),(1,0)])
        from qingqi.visual_teaching import validate_binding
        from qingqi.teaching_visual_pair import companion
        from qingqi.contracts import ContractError
        state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(full['run_id'],)).fetchone()[0])
        report=next(o['result'] for o in state['observations'] if o['tool']=='analyze_function')
        picture=companion(report['approved_problem_solution_visuals'][0],state)
        validate_binding({'visuals':[picture]},state)
        check('standalone_function_diagram_passes_the_owned_source_check',True)
        wrong=json.loads(json.dumps(picture));wrong['params']['k']=3
        denied=False
        try:validate_binding({'visuals':[wrong]},state)
        except ContractError:denied=True
        check('standalone_function_diagram_cannot_change_the_original_equation',denied)
        count=len(f.calls);again=teach(session,'用原题的动画完整演示解题步骤，直接给答案','full')
        check('reasoning_replay_is_identical_without_new_ocr_or_tools',again['cache_hit'] and again['visuals']==full['visuals'] and len(f.calls)==count)
        other=post('/api/sessions',{})['id']
        variant=teach(other,'若函数 f(x)=x³-ax²+2 在(0,∞)内有且仅有一个零点，求在[-2,-1]的最大最小值之和。请用动画完整解答，给出答案。','variant')
        vl=motion(variant)['reasoning_lesson']
        from qingqi.contracts import canonical
        check('irrational_picture_and_animation_fit_the_existing_tool_budget',len(canonical({'visuals':variant['visuals'],'version':variant['visual_version']}).encode())<64000 and len(variant['visuals'])==1)
        check('stationary_points_outside_requested_interval_are_not_candidates',[c['x'] for c in vl['candidates']]==[-2,-1] and vl['given']['k']==1 and vl['given']['constant']==2)
        check('irrational_solution_labels_use_radicals_not_long_decimals','sqrt' in vl['solved']['parameter'] and not any(__import__('re').search(r'\d+\.\d{3,}',s['formula']) for s in vl['steps']))
        nsession=post('/api/sessions',{})['id']
        question='若实数a,b满足 $\\sqrt{a-3}+|b+2|=0$，求 $a+b$。'
        nn=teach(nsession,question+'请用针对原题的动画讲解，先不要答案。','nn-hint');nl=motion(nn)['reasoning_lesson']
        check('nonnegative_animation_binds_real_expressions',nn['visuals'][0]['template']=='nonnegative_reasoning' and nn['visuals'][0]['basis']=='problem' and nl['terms']==[r'\sqrt{a-3}','|b+2|'])
        check('nonnegative_proof_demonstrates_each_positive_contradiction',{'positive_left','positive_right','zero'}<=set(s['scene'] for s in nl['steps']) and 'solved' not in nl)
        solved=motion(teach(nsession,'请动画演示完整解题步骤，直接给答案','nn-full'))['reasoning_lesson']
        check('nonnegative_solution_keeps_negative_b_and_actual_goal',solved['solved']['variables']=={'a':'3','b':'-2'} and solved['solved']['result']=='1' and solved['target']=='a+b')
        fs=post('/api/sessions',{})['id']
        fractional=motion(teach(fs,'已知 $\\sqrt{2a-1}+|3b+2|=0$，求 $a+b$。用动画完整解答，给出答案。','fractional'))['reasoning_lesson']
        check('fractional_parameters_and_sum_stay_exact',fractional['solved']['variables']=={'a':r'\frac{1}{2}','b':r'-\frac{2}{3}'} and fractional['solved']['result']==r'-\frac{1}{6}')
        check('reasoning_does_not_create_student_grades',get('/api/learning')['summary']['attempts']==0)
        auto_session=post('/api/sessions',{})['id']
        auto=teach(auto_session,SOURCE+'请完整讲解，直接给答案。','auto-function')
        check('function_graph_pair_is_selected_without_a_drawing_command',len(auto['visuals'])==1 and auto['visuals'][0]['template']=='function_reasoning')
        ac=auto['visuals'][0]['reasoning_lesson']['curve']
        check('solved_graph_has_original_formula_exact_ticks_and_candidates',ac['formula']==r'2 x^{3} - 3 x^{2} + 1' and any(t['value']==-1 and t['label']=='−1' for t in ac['x_ticks']) and len(ac['markers'])==3)
        static=teach(auto_session,'不用动画，只画原题的函数图，先不要答案。','static-function')
        sd=static['visuals'][0]
        check('static_hint_keeps_original_coefficients_interval_and_unresolved_cases',len(static['visuals'])==1 and sd['kind']=='reasoning_diagram' and sd['basis']=='problem' and sd['params']['k']==2 and sd['params']['constant']==1 and sd['params']['interval']==[-1,1] and [c['root_count'] for c in sd['reasoning_lesson']['cases']]==[0,1,2] and 'solved' not in sd['reasoning_lesson'])
        no_plot=teach(auto_session,'不要画图，不用动画，只用文字给我一点提示，先不要答案。','no-plot')
        check('explicit_no_graph_preserves_text_tutoring',not no_plot.get('visuals'))
        auto_nn_session=post('/api/sessions',{})['id']
        auto_nn=teach(auto_nn_session,question+'帮我理解这道题，先不要答案。','auto-nn')
        check('nonnegative_curves_are_automatic_and_use_inner_expression_axes',auto_nn['visuals'][0]['reasoning_lesson']['term_curves'][0]['curve']['axis_labels']['x']=='a−3' and auto_nn['visuals'][0]['reasoning_lesson']['term_curves'][1]['curve']['axis_labels']['x']=='b+2')
        static_nn=teach(auto_nn_session,'不要动画，画对应的函数图，直接给答案。','static-nn')
        check('one_static_nonnegative_diagram_contains_both_correct_variable_axes',len(static_nn['visuals'])==1 and static_nn['visuals'][0]['kind']=='reasoning_diagram' and [t['curve']['axis_labels']['x'] for t in static_nn['visuals'][0]['reasoning_lesson']['term_curves']]==['a','b'])
        negative_session=post('/api/sessions',{})['id']
        negative=teach(negative_session,r'已知 $\sqrt{1-2a}+|3b+2|=0$，求 $a+b$。不用动画，画图并给出答案。','negative')
        term=negative['visuals'][0]['reasoning_lesson']['term_curves'][0]
        check('negative_sqrt_coefficient_respects_its_actual_domain',term['curve']['domain'][1]==.5 and term['zero']['x']==.5 and all(p['y']>=0 for p in term['curve']['samples']))
        from qingqi.tutor_images import optional_choices_recognition
        raw={'text':SOURCE,'unclear':True,'note':'图片仅含题干，末尾为冒号，具体选项或要求残缺；无法补造。'}
        check('complete_numeric_target_does_not_require_missing_choices',optional_choices_recognition(raw)['unclear'] is False and optional_choices_recognition(raw)['text']==SOURCE)
        ambiguous={**raw,'note':'缺少选项，函数系数看不清，可能是2或3。'}
        check('uncertain_symbols_still_require_clarification',optional_choices_recognition(ambiguous)==ambiguous)
        no_goal={**raw,'text':'函数 f(x)=2x³-ax²+1 在(0,∞)内有且仅有一个零点，选择正确选项。'}
        check('missing_actual_target_is_not_recovered',optional_choices_recognition(no_goal)==no_goal)
        f.ocr_result=raw
        photo_session=post('/api/sessions',{})['id']
        recovered=teach(photo_session,'请讲解这道题，先不要答案。','ocr-missing-options',[image])
        recovered_state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(recovered['run_id'],)).fetchone()[0])
        check('missing_choices_recovery_works_through_the_normal_photo_entry',recovered['visuals'][0]['template']=='function_reasoning' and recovered_state['vision_adjustment']['original_note']==raw['note'])
        f.ocr_result=ambiguous
        blurry_session=post('/api/sessions',{})['id']
        blurry=teach(blurry_session,'请画出函数图。','ocr-blurry-symbols',[image])
        check('ambiguous_photo_is_not_forced_into_a_function_graph',not blurry.get('visuals') and blurry['teaching_action']=='clarify')
    finally:owner.close();f.close()
    Path('education/.local/reports/problem-reasoning-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':run()
