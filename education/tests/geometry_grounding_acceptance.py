"""Independent algebra and actual native-tool/HTTP evidence for grounded geometry."""
import json
from fractions import Fraction
from pathlib import Path
from qingqi.geometry_tasks import identify
from qingqi.geometry_solver import solve_geometry
from qingqi.geometry_animation import scene_at

from geometry_fixture_data import SOURCE
checks=[]
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)

task=identify(SOURCE);assert task
report=solve_geometry(**task['arguments'])
check('symbolic_identities_and_rotation_are_verified',report['status']=='verified' and all(report['proof_checks'].values()))
check('reported_problem_function_and_domain_are_exact',report['function']['slope']=='-2' and report['function']['intercept']=='8' and report['function']['upper']=='4' and report['function']['upper_closed'])
check('reported_wrong_right_angle_is_corrected',report['midpoint']['angles']['ECD']==45 and report['midpoint']['angles']['ADC']==90)
for ratio in ('1/4','1/2','1','2','5'):
    varied=SOURCE.replace('=6','=9').replace('=1:2','=1:4' if ratio=='1/4' else '=1:2' if ratio=='1/2' else '=1:1' if ratio=='1' else '=2:1' if ratio=='2' else '=5:1')
    result=solve_geometry(**identify(varied)['arguments'])
    check('generic_ratio_'+ratio,result['status']=='verified' and Fraction(result['function']['slope'])==-1/Fraction(ratio))
    motion=next(v for v in result['approved_visuals'] if v.get('template')=='geometry_motion')
    for i in range(41):
        scene=scene_at(motion['template'],motion['params'],i/40)
        points={p['label']:p for p in scene['points']};d,e,f=(points[v] for v in ('D','E','F'))
        dot=(e['x']-d['x'])*(f['x']-d['x'])+(e['y']-d['y'])*(f['y']-d['y'])
        assert abs(dot)<1e-7
        assert abs(scene['de']/scene['df']-float(Fraction(ratio)))<1e-8
    check('all_intermediate_motion_frames_respect_geometry_'+ratio,True)
renamed=SOURCE.translate(str.maketrans('ABCDEF','PQRSTU'))
check('renamed_geometry_is_not_tied_to_screenshot_labels',identify(renamed)['arguments']['labels']['a']=='P')
check('non_isosceles_problem_is_not_solved_as_this_family',identify(SOURCE.replace('AC=BC，','AC≠BC，')) is None)
check('missing_perpendicular_condition_is_not_invented',identify(SOURCE.replace('DF⊥DE，','')) is None)
check('zero_division_ratio_is_clarified',bool(identify(SOURCE.replace('=1:2','=1:0')).get('clarify')))
rotation=report['approved_visuals'][0]
from qingqi.geometry_animation import render
varied=solve_geometry(**identify(SOURCE.replace('=6','=9').replace('=1:2','=2:1'))['arguments'])
motion=next(v for v in varied['approved_visuals'] if v.get('template')=='geometry_motion')
lesson=render(motion['template'],{**motion['params'],'lesson_mode':'solution'},18)['lesson']
check('lesson_function_and_open_domain_change_with_ratio_and_scale',lesson['domain']=={'upper':9.0,'upper_closed':False} and lesson['coefficients']=={'a':-.5,'b':6.0})
near=solve_geometry(**identify(SOURCE.replace('=1:2','=999999:1000000'))['arguments'])
motion=next(v for v in near['approved_visuals'] if v.get('template')=='geometry_motion')
lesson=render(motion['template'],{**motion['params'],'lesson_mode':'solution'},18)['lesson']
check('nearly_one_ratio_preserves_exact_domain_closure',lesson['domain']['upper_closed'] and lesson['domain']['upper']<6 and '999999' in lesson['steps'][3]['formula'])
small=solve_geometry(**identify(SOURCE.replace('=1:2','=1:100000'))['arguments'])
motion=next(v for v in small['approved_visuals'] if v.get('template')=='geometry_motion')
scene=render(motion['template'],{**motion['params'],'lesson_mode':'solution'},18)
check('small_positive_ratio_keeps_valid_geometry_function_plot',scene['plot']['a']==-100000 and abs(scene['plot']['samples'][-1]['y'])<1e-8)
renamed=solve_geometry(**identify(SOURCE.translate(str.maketrans('ABCDEF','PQRSTU')).replace('PT=x','PT=u').replace('QU=y','QU=v'))['arguments'])
motion=next(v for v in renamed['approved_visuals'] if v.get('template')=='geometry_motion')
lesson=render(motion['template'],{**motion['params'],'lesson_mode':'solution'},18)['lesson']
check('lesson_uses_owned_variable_and_point_labels',lesson['symbols']=={'x':'u','y':'v'} and 'v=8-2u' in lesson['steps'][3]['formula'] and 'U' in lesson['steps'][0]['explanation'])
end=scene_at(rotation['template'],rotation['params'],1)
points={p['label']:p for p in end['points']}
check('rotation_really_maps_a_to_c_and_e_to_f',all(abs(points[a][k]-points[b][k])<1e-8 for a,b in (("A′","C"),("E′","F"),("C′","B")) for k in ('x','y')))
Path('education/.local/reports/geometry-grounding-acceptance.json').write_text(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
