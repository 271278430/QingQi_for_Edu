"""A bounded subset of the original Registry schema, never a new tool authority."""
import copy,re

def select(contracts,state):
    source=' '.join(str(v) for v in ((state.get('practice_entry') or {}).get('expression',''),(state.get('image_question') or state.get('problem_question') or {}).get('text',''),state.get('effective_request',{}).get('question','')))
    policy=state['teaching_plan']['visual'];animation=policy.get('explicit_animation') or policy.get('prefer_animation')
    preferred=(state.get('visual_task') or {}).get('required_template') or policy.get('recommended_template')
    if preferred:templates={preferred}
    elif '相反数' in source:templates={'opposite_numbers'}
    elif '绝对值' in source:templates={'absolute_distance'}
    elif '平方根' in source:templates={'square_root'}
    elif '分数' in source:templates={'fraction_fill'}
    elif re.search(r'函数|y\s*=|f\s*\(',source):templates={'function_trace'}
    elif re.search(r'几何|三角形|坐标|连线|辅助线',source):templates={'coordinate_drawing','pythagorean'} if '勾股' in source else {'coordinate_drawing'}
    else:templates={'number_line_motion','function_trace','coordinate_drawing','fraction_fill'}
    kinds={'number_line','table','scene','bar_chart'}
    kinds|={'function_plot'} if 'function_trace' in templates else set()
    kinds|={'coordinates'} if 'coordinate_drawing' in templates else set()
    kinds|={'area_model'} if 'fraction_fill' in templates else set()
    selected=copy.deepcopy(contracts)
    for tool in selected:
        if tool['name']!='render_teaching_visual':continue
        items=tool['inputSchema']['properties']['visuals']['items']
        # 仅缩小原Schema分支；执行仍由Registry完整Schema和原题/许可核验决定。
        branches=[b for b in items['oneOf'] if (not policy.get('forbid_animation') and b['properties']['kind']['enum'][0]=='animation_scene' and b['properties']['template']['enum'][0] in templates) or (not animation and b['properties']['kind']['enum'][0] in kinds)]
        if branches:items['oneOf']=branches
    return selected
