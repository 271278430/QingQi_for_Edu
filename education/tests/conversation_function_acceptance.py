"""Independent bounded math checks, beyond the screenshot's one parameter set."""
import math
import json
from qingqi.function_solver import identify,analyze_function
from qingqi.visual_teaching import render_visuals
from qingqi.contracts import ContractError

checks=[]
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True})
for k,c in ((2,1),(4,2),(1,.5),(3,12)):
    for interval in ((-1,1),(-2,2),(2,3)):
        r=(2*c/k)**(1/3);p=1.5*k*r
        task=identify(f'f(x)={k}x³-ax²+{c}在(0,∞)内有且仅有一个零点，在[{interval[0]},{interval[1]}]求最值。')
        assert task
        report=analyze_function(**task['arguments'])
        f=lambda x:k*x**3-p*x*x+c
        dense=[f(interval[0]+(interval[1]-interval[0])*i/20000) for i in range(20001)]
        check(f'variant_{k}_{c}_{interval}_zero_and_extrema',math.isclose(report['parameter_value'],p) and abs(f(r))<1e-8 and abs(f(-r/2))<1e-8 and abs(report['minimum']-min(dense))<1e-5 and abs(report['maximum']-max(dense))<1e-5)
        visuals=[render_visuals(visuals=[v])['visuals'][0] for v in report['approved_solution_visuals']]
        check(f'variant_{k}_{c}_{interval}_plot_derivative_consistency',all(abs(point['y']-f(point['x']))<1e-7 for point in visuals[0]['plot']['samples']) and all(abs(point['y']-(3*k*point['x']**2-2*p*point['x']))<1e-7 for point in visuals[1]['plot']['samples']))
for expression in ('2x³-ax²+1+x','2x³-ax²+1-x','2x³-ax²+1/x','2x⁴-ax²+1','-2x³-ax²+1','2x³-ax²-1'):
    check('unsupported_'+expression,identify('f(x)='+expression+'在(0,∞)有且仅有一个零点，在[-1,1]求最值。') is None)
spec=report['approved_solution_visuals'][0];spec={**spec,'params':{**spec['params'],'markers':[{'x':0,'y':99,'label':'错误点'}]}}
try:render_visuals(visuals=[spec])
except ContractError:check('incorrect_marker_is_rejected',True)
else:raise AssertionError('off-curve marker accepted')
print(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False))
