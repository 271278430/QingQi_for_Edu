"""Exact radical/fraction labels and legacy read-only projection regression."""
import copy
import json
import re
import sqlite3
from pathlib import Path
from qingqi.function_solver import analyze_function
from qingqi.projection import project_response
from qingqi.visual_teaching import render_visuals
from qingqi.math_display import compact_response

checks=[]
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True})
from qingqi.function_reasoning import render
lesson=render({'k':1,'constant':4,'parameter':'a','interval':[-1,2],'lesson_mode':'solution'},20)['reasoning_lesson']
check('trial_parameter_uses_exact_known_ratio',not re.search(r'\d{12,}',json.dumps([c['curve']['formula'] for c in lesson['cases']])) and '5' in lesson['cases'][2]['curve']['formula'])
irrational=render({'k':4,'constant':8,'parameter':'a','interval':[-1,1],'lesson_mode':'solution'},20)['reasoning_lesson']
check('trial_ticks_keep_exact_radicals',any('sqrt[3]' in t['label'] for t in irrational['cases'][0]['curve']['x_ticks']) and not re.search(r'\d{12,}',json.dumps([c['curve']['formula'] for c in irrational['cases']])))
report=analyze_function(k=4,constant=8,parameter='a',interval=[-1,1])
visuals=[render_visuals(visuals=[v])['visuals'][0] for v in report['approved_solution_visuals']]
check('irrational_function_and_derivative_use_exact_cube_roots',all('sqrt[3]' in v['plot']['display']['formula'] for v in visuals) and 'sqrt[3]' in report['exact_values']['positive_root'])
check('exact_labels_never_contain_long_decimal_tails',not re.search(r'\d+\.\d{3,}',json.dumps([v['plot']['display'] for v in visuals])))
fraction=analyze_function(k=2,constant=1,parameter='a',interval=[1/3,1])
# 题目显式十进制输入与精确分数应区分；工具输出的根式不会从float反猜。
check('numeric_sampling_keeps_original_function',all(abs(p['y']-(4*p['x']**3-6*4**(1/3)*p['x']**2+8))<1e-7 for p in visuals[0]['plot']['samples']))
legacy={'controller':'grounded_symbolic_function_v1','route':{'teaching':{'allow_final_answer':False}},'visuals':copy.deepcopy(visuals),'text':'历史回复'}
for v in legacy['visuals']:v['params'].pop('display');v['plot'].pop('display')
before=copy.deepcopy(legacy);shown=project_response(legacy)
check('legacy_visuals_gain_exact_labels_without_mutating_history',legacy==before and all(v['plot'].get('display') for v in shown['visuals']) and [v['id'] for v in shown['visuals']]==[v['id'] for v in legacy['visuals']])
actual=sqlite3.connect('file:education/service/runs/product/agent.sqlite?mode=ro',uri=True)
row=actual.execute('select response from runs where id=62').fetchone();actual.close()
if row:
    shown=project_response(json.loads(row[0]))
    check('reported_existing_run62_has_exact_function_labels',all(v['plot'].get('display') for v in shown['visuals']) and not re.search(r'\d+\.\d{3,}',json.dumps([v['plot']['display'] for v in shown['visuals']])))
check('unknown_model_decimal_is_marked_approximate_not_fake_fraction',compact_response('答案 x=0.3333333333333333。')=='答案 x≈0.33。')
check('model_code_and_urls_are_not_rewritten',compact_response('`x=0.33333` https://test.example/0.33333')=='`x=0.33333` https://test.example/0.33333')
Path('education/.local/reports/system-precise-math.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'passed':len(checks)},ensure_ascii=False))
