"""Repeatable visual teaching acceptance, including the actual ZCode executor."""
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'service/src'))
from qingqi.agent import Agent, PROJECT, InjectedInterruption
from qingqi.contracts import Identity, Request, ContractError, Denied
from qingqi.visual_teaching import render_visuals, validate_binding


def run():
    root = PROJECT / 'runs/visual-teaching-acceptance' / uuid.uuid4().hex
    agent = Agent(root, PROJECT / 'data/curriculum.sqlite')
    tests = []

    def check(name, condition):
        assert condition, name
        tests.append({'name': name, 'passed': True})
        print(json.dumps(tests[-1]), flush=True)

    def reject(name, fn):
        try:
            fn()
        except (ContractError, Denied):
            check(name, True)
            return
        raise AssertionError(name)

    number_line = {'kind': 'number_line', 'title': '先看一个相似例子', 'basis': 'example', 'points': [{'label': '起点', 'x': -2}], 'moves': [{'start': -2, 'delta': 3, 'label': '向右移动'}]}
    try:
        value = render_visuals(visuals=[number_line])
        check('number_line_endpoint_computed_by_tool', value['visuals'][0]['moves'][0]['end'] == 1)
        check('deterministic_visual_id', value == render_visuals(visuals=[number_line]))
        for kind, data in [
            ('coordinates', {'points': [{'label': 'A', 'x': 2, 'y': -3}]}),
            ('table', {'columns': ['条件', '含义'], 'rows': [['速度', '每小时走的路程']]}),
            ('bar_chart', {'bars': [{'label': '甲', 'value': 3}, {'label': '乙', 'value': 5}]}),
            ('scene', {'nodes': ['家', '学校'], 'edges': [{'source': 0, 'target': 1, 'label': '行走'}]}),
        ]:
            spec = {'kind': kind, 'title': '辅助理解', 'basis': 'example', **data}
            check(kind + '_bounded_spec', render_visuals(visuals=[spec])['visuals'][0]['kind'] == kind)
        reject('ragged_table_rejected', lambda: render_visuals(visuals=[{'kind':'table','title':'表','basis':'example','columns':['A','B'],'rows':[['1']]}]))
        reject('false_arithmetic_label_rejected', lambda: render_visuals(visuals=[{**number_line, 'title':'2+2=5'}]))
        check('algebraic_equation_not_misread_as_numeric_suffix',render_visuals(visuals=[{'kind':'table','title':'类比方程','basis':'example','columns':['关系'],'rows':[['x+x+40=180'],['（2+2=4）']]}])['visuals'][0]['rows'][0][0]=='x+x+40=180')
        check('plain_mathematical_inequality_is_not_html',render_visuals(visuals=[{'kind':'table','title':'不等关系','basis':'example','columns':['关系'],'rows':[['0<x<5'],['x>0']]}])['visuals'][0]['rows'][0][0]=='0<x<5')
        reject('unknown_script_field_rejected', lambda: render_visuals(visuals=[{**number_line,'html':'<script>alert(1)</script>'}]))
        reject('non_finite_number_rejected', lambda: render_visuals(visuals=[{**number_line,'points':[{'label':'A','x':float('nan')}]}]))
        reject('more_than_two_visuals_rejected', lambda: render_visuals(visuals=[number_line]*3))
        reject('cross_type_fields_rejected', lambda: render_visuals(visuals=[{**number_line,'rows':[['1']]}]))
        reject('coordinates_missing_y_rejected', lambda: render_visuals(visuals=[{'kind':'coordinates','title':'点','basis':'example','points':[{'label':'A','x':2}]}]))
        reject('scene_missing_endpoint_rejected', lambda: render_visuals(visuals=[{'kind':'scene','title':'关系','basis':'example','nodes':['A','B'],'edges':[{'source':0,'target':2,'label':'关系'}]}]))
        reject('html_and_url_label_rejected', lambda: render_visuals(visuals=[{**number_line,'title':'<img src=https://example.com>'}]))
        reject('numeric_bound_rejected', lambda: render_visuals(visuals=[{**number_line,'points':[{'label':'A','x':10001}]}]))
        state = {'effective_request':{'question':'请解释 2+3*4','expression':'2+3*4'}, 'route':{'teaching':{'allow_final_answer':False}}, 'observations':[{'tool':'review_arithmetic','result':{'answer':'14'}}]}
        reject('original_final_answer_not_hidden_in_chart', lambda: validate_binding({'visuals':[{'kind':'bar_chart','title':'结果','basis':'example','bars':[{'label':'答案','value':14}]}]}, state))
        reject('invented_problem_values_rejected', lambda: validate_binding({'visuals':[{**number_line,'basis':'problem'}]}, state))
        reject('invented_problem_table_literal_rejected', lambda: validate_binding({'visuals':[{'kind':'table','title':'条件','basis':'problem','columns':['数量'],'rows':[['99']]}]},state))
        for kind,data in [('table',{'columns':['数值'],'rows':[['14']]}),('coordinates',{'points':[{'label':'A','x':14,'y':0}]}),('scene',{'nodes':['起点','终点14'],'edges':[{'source':0,'target':1,'label':'关系'}]})]:
            reject('protected_answer_in_'+kind,lambda kind=kind,data=data: validate_binding({'visuals':[{'kind':kind,'title':'辅助','basis':'example',**data}]},state))
        ident = Identity('visual-student', 'visual-session')
        request = Request('visual-1','请用数轴直观讲解 2+3，不要直接给答案。',expression='2+3')
        result = agent.run(ident, request)
        state = json.loads(agent.store.db.execute('SELECT state FROM runs WHERE id=?',(result['run_id'],)).fetchone()[0])
        check('actual_zcode_executor_visual_attached', result['visuals'][0]['kind'] == 'number_line' and any(o['tool']=='render_teaching_visual' and o['runtime']['source']=='@zcode/core/ToolExecutor' for o in state['observations']))
        repeated = agent.run(ident, request)
        check('same_request_replays_same_visuals', repeated['cache_hit'] and repeated['visuals']==result['visuals'])
        other = agent.run(Identity('other-visual-student','other-session'),Request('visual-1','你好'))
        check('other_student_does_not_inherit_visual', not other.get('visuals'))
        alternative = agent.run(ident,Request('answer-overlap','请用数轴讲解 3-2，不要直接答案。',expression='3-2'))
        check('analogous_example_avoids_protected_answer_overlap',alternative['visuals'][0]['moves'][0]['end']!=1)
        subtraction=agent.run(Identity('subtraction-student','s'),Request('subtraction','请用数轴讲解 2-3，请直接给答案。',expression='2-3'))
        check('original_subtraction_direction_is_valid_given_magnitude',subtraction['visuals'][0]['moves'][0]['end']==-1)
        resumed_request=Request('resume-visual','请用数轴讲解 4+5，不要直接答案。',expression='4+5')
        try:agent.run(ident,resumed_request,interrupt_after_tool='render_teaching_visual')
        except InjectedInterruption:pass
        row=agent.store.db.execute('SELECT id,state FROM runs WHERE request_id=?',(resumed_request.request_id,)).fetchone()
        state=json.loads(row['state'])
        check('interrupted_after_durable_visual_before_observation',state['pending_action']['tool']=='render_teaching_visual' and state['phase']=='interrupted')
        value=agent.run(ident,resumed_request)
        check('durable_visual_result_resumes_without_execution_repeat',value['visuals'][0]['kind']=='number_line' and agent.store.db.execute("SELECT COUNT(*) FROM calls WHERE run_id=? AND call_id LIKE '%:render_teaching_visual'",(row['id'],)).fetchone()[0]==1)
        floating=agent.registry.call('render_teaching_visual',{'visuals':[{**number_line,'points':[{'label':'小数起点','x':2.0}],'moves':[{'start':2.0,'delta':0.0001,'label':'小步移动'}]}]},{'render_teaching_visual'})
        check('json_integer_float_equivalence_and_decimal_precision',floating['result']['visuals'][0]['moves'][0]['end']==2.0001)
    finally:
        agent.close()
    report={'passed':len(tests),'checks':tests,'actualZCodeRuntime':True,'realModel':False}
    (PROJECT.parent/'.local/reports/visual-teaching-acceptance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')


if __name__ == '__main__':
    run()
