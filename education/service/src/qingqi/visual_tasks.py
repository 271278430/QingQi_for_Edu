"""Pure explicit visual-task planner. The Store supplies owned prior figures."""
import re
import math
from fractions import Fraction
from itertools import combinations
from .contracts import ContractError

VERSION='visual_task_v1'


def _animation_text(question):
    from .request_controls import strip_denied
    return strip_denied(question,r'动画|动态|动图|演示')


def wants_animation(question):return bool(re.search(r'动画|动态|动图|演示',_animation_text(question)[0]))


def refuses_animation(question):return (_animation_text(question)[1] or bool(re.search(r'静态(?:函数)?图',question))) and not wants_animation(question)

def wants_connections(question):
    match=re.search(r'连(?:起来|接|线)|划线',question)
    if not match:return False
    # “为什么要连接CD”是在问当前依据，不是要求把全部点重连；连点命令另走绘制动画。
    prefix=re.split(r'[。！？；\n]',question[:match.start()])[-1]
    return not re.search(r'为什么|为何',prefix)

def wants_explanation(question):
    # “不用讲解”不能被正向关键词当成讲解请求，否则只画图也会多调用模型。
    from .request_controls import strip_denied
    from .request_controls import answer_directives
    commands=answer_directives(question)
    if commands and commands[-1]['allowed']:return True
    positive=strip_denied(question,r'解释|讲解|追问')[0]
    return bool(re.search(r'解释|讲解|讲清楚|讲明白|继续讲|为什么|理解|教学|辅导|教我|追问|苏格拉底|解题(?:过程|步骤)|推导|完整',positive))


def wants_drawing(question):
    from .request_controls import strip_denied
    positive=_animation_text(question)[0]
    target=r'可视化|图示|图解|绘图|画[^，,。；;！？\n]{0,12}图|静态(?:函数)?图|函数图'
    positive=strip_denied(positive,target)[0]
    return wants_animation(question) or bool(re.search(target,positive))


def refuses_drawing(question):
    from .request_controls import strip_denied
    positive,denied=strip_denied(question,r'画[^，,。；;！？\n]{0,12}图|绘图|图示|图解|可视化|函数图|图像|图片|图')
    return denied and not wants_drawing(positive)


def coordinate_pairs(source):
    text=source.replace('−','-').replace('（','(').replace('）',')').replace('，',',')
    text=re.sub(r'\\(?:left|right)', '',text)
    text=re.sub(r'\\frac\{([+-]?\d+)\}\{(\d+)\}',r'\1/\2',text)
    n=r'[+-]?\d+(?:\.\d+)?(?:/\d+)?'
    points=[];seen=set()
    for match in re.finditer(r'\(\s*('+n+r')\s*,\s*('+n+r')\s*\)',text):
        try:pair=tuple(float(Fraction(v)) for v in match.groups())
        except ZeroDivisionError as error:raise ContractError('coordinate denominator cannot be zero') from error
        if pair not in seen:
            points.append({'label':chr(65+len(points)),'x':pair[0],'y':pair[1]});seen.add(pair)
    return points[:8]


def plan(request,entry=None,prior=None,*,image_text='',presentation=None):
    q=request.question
    from .teaching_visual_pair import delivery
    if delivery(q)=='text':return None
    animation=wants_animation(q)
    story=(presentation or {}).get('kind')=='story'
    if story and (presentation or {}).get('requested') and (presentation or {}).get('animation')!='off' and not refuses_animation(q):animation=True
    connect=wants_connections(q)
    if not connect and not refuses_drawing(q):
        from .nonnegative_reasoning import specification as nn_spec,static_specifications
        source=entry or {'expression':image_text or q}
        spec=nn_spec(source)
        if spec:
            # 由完整原题主动选择实际曲线；自动绘图不得改写学生的提示/答案许可。
            static=refuses_animation(q)
            return {'version':VERSION,'operation':'nonnegative_story','automatic':not wants_drawing(q),
                    'required_kind':'function_plot' if static else 'animation_scene',
                    **({} if static else {'required_template':'nonnegative_reasoning'}),
                    'arguments':{'visuals':static_specifications(source) if static else [spec]}}
    if not refuses_drawing(q) and not connect:
        from .identity_animation import specification
        spec=specification(entry or {'expression':image_text or q},scenario='scorekeepers' if story else None)
        if spec:
            from .teaching_visual_pair import companion
            static=refuses_animation(q)
            return {'version':VERSION,'operation':'identity_probe','automatic':not wants_drawing(q),'required_kind':'reasoning_diagram' if static else 'animation_scene','required_template':'identity_probe','arguments':{'visuals':[companion(spec,{}) if static else spec]}}
    if animation and not connect:
        from .nonnegative_reasoning import specification as nonnegative_specification
        spec=nonnegative_specification(entry or {'expression':image_text or q})
        if spec:return {'version':VERSION,'operation':'nonnegative_story','required_kind':'animation_scene','required_template':'nonnegative_reasoning','arguments':{'visuals':[spec]}}
    if not connect:
        # 泛化“给我动画”必须绑定当前已批准图，而不是重发全部模板让模型重新猜原题。
        from .visual_followup import plan as followup_plan
        followup=followup_plan(q,entry,prior,image_text)
        if followup:return followup
        if not animation and not re.search(r'(?:请|帮我|能|可以|给我|希望|想).{0,24}(?:画|绘|图示|可视化)|^(?:画|绘)|(?:用|来个|来一).{0,12}图示|可视化',q):return None
        kind='function_plot' if re.search(r'函数|曲线|抛物线',q) else 'area_model' if re.search(r'分数|分区|饼图',q) else 'coordinates' if re.search(r'坐标|辅助线|三角形|几何',q) else None
        template='fraction_fill' if re.search(r'分数|分区|饼图',q) and animation else 'pythagorean' if '勾股' in q and animation else None
        if kind=='function_plot' and animation:template='function_trace'
        if template:kind='animation_scene'
        if not kind:return None
        if kind=='function_plot' or template=='function_trace':
            from .visual_expressions import specified_functions,polynomial
            if re.search(r'sin|cos|tan|log|ln|反比例|指数|对数',q,re.I):return {'version':VERSION,'operation':'render','clarify':'当前函数图支持最高三次多项式；这类函数需要新增绘图模板，可以先讨论它的性质。'}
            expressions=specified_functions(q)
            if expressions:
                if len(expressions)>2:return {'version':VERSION,'operation':'render','clarify':'一次可以展示两张函数图，请先选择其中两条函数。'}
                visuals=[]
                try:
                    for expression in expressions:
                        coefficients=polynomial(expression);a=coefficients.get(2,0);b=coefficients.get(1,0);c=coefficients.get(0,0)
                        spec={'kind':'function_plot','basis':'problem','title':'函数 y='+expression,'function':'quadratic' if a else 'linear','a':float(a if a else b),'b':float(b if a else c),'domain':[-3,3]}
                        if a:spec['c']=float(c)
                        if coefficients.get(3):spec.update(function='cubic',a=float(coefficients[3]),b=float(a),c=float(b),d=float(c))
                        import sympy as s
                        from .math_display import exact
                        X=s.Symbol('x');formula=sum(s.Rational(value.numerator,value.denominator)*X**degree for degree,value in coefficients.items())
                        spec['display']={'formula':exact(formula),'domain':['−3','3'],'markers':[]}
                        from .advanced_visuals import function_plot
                        function_plot(spec)
                        if template=='function_trace':spec={'kind':'animation_scene','title':spec['title']+' · 动态描绘','basis':'problem','template':template,'params':{k:v for k,v in spec.items() if k in {'function','a','b','c','d','domain','display'}}}
                        visuals.append(spec)
                except ContractError as error:return {'version':VERSION,'operation':'render','clarify':str(error)}
                return {'version':VERSION,'operation':'render','required_kind':kind,'arguments':{'visuals':visuals}}
        if kind=='area_model' or template=='fraction_fill':
            fraction=re.search(r'(?<![\d.])(\d{1,2})\s*[/／]\s*(\d{1,2})(?![\d.])',q)
            if fraction:
                n,d=map(int,fraction.groups())
                if not 1<=d<=24 or n>d:return {'version':VERSION,'operation':'render','clarify':'当前面积图支持一个整体内的分数，请给出分母不超过24、分子不大于分母的分数。'}
                spec={'kind':'area_model','title':'用面积理解分数','basis':'problem','numerator':n,'denominator':d,'shape':'circle' if '饼' in q or '圆' in q else 'rectangle'}
                if template=='fraction_fill':spec={'kind':'animation_scene','title':'逐份理解分数','basis':'problem','template':template,'params':{'numerator':n,'denominator':d}}
                return {'version':VERSION,'operation':'render','required_kind':kind,'arguments':{'visuals':[spec]}}
        points=coordinate_pairs((entry or {}).get('expression','')+' '+image_text+' '+q) if kind=='coordinates' else []
        return {'version':VERSION,'operation':'render','required_kind':kind,**({'required_template':template} if template else {}),**({'required_points':points} if points else {})}
    source=(entry or {}).get('expression','')+' '+image_text+' '+request.question
    current=coordinate_pairs(source)
    prior=prior or {}
    if re.search(r'图(?:上|中|里)|这个.*(?:图|坐标系)|这(?:幅|张).*图',q) and not coordinate_pairs(q):
        current=prior.get('points') or prior.get('params',{}).get('points') or current
    if not current and prior.get('kind')=='coordinates':current=prior['points']
    # 精确标签是已接受图的显示元数据，不能再次作为工具参数突破strict schema。
    display_points=[p for p in current if p.get('x_tex') or p.get('y_tex')]
    current=[{key:value for key,value in p.items() if key in {'label','x','y'}} for p in current]
    if not current and prior.get('template')=='coordinate_drawing':current=prior['params']['points']
    if len(current)<2:return {'version':VERSION,'operation':'connect_points','clarify':'请给出要连接的点坐标，或上传坐标图；我会实际画出连线。'}
    names={p['label'].split('(')[0].strip():i for i,p in enumerate(current)}
    for label,index in list(names.items()):
        if re.search(r'[A-Z]$',label):names[label[-1]]=index
    specified=[]
    mentions=re.findall(r'([A-Z])\s*(?:到|和|与|[-—→])\s*([A-Z])',q.upper())+re.findall(r'(?<![A-Z])([A-Z])([A-Z])(?![A-Z])',q.upper())
    for left,right in mentions:
        if left in names and right in names:specified.append((names[left],names[right]))
    pairs=list(dict.fromkeys(tuple(sorted(pair)) for pair in specified)) or list(combinations(range(len(current)),2))
    if len(pairs)>16:return {'version':VERSION,'operation':'connect_points','clarify':'点较多，请说明要连接哪些点对，例如 A 到 B、B 到 C。'}
    # 斜向不代表对角线。只有题面声明正方形且点距满足边/对角线关系才推断角色。
    distances=[(current[a]['x']-current[b]['x'])**2+(current[a]['y']-current[b]['y'])**2 for a,b in combinations(range(len(current)),2)]
    side=min(distances)
    square=bool('正方形' in source and len(current) in {3,4} and side>0 and
                sum(math.isclose(d,side,rel_tol=1e-8) for d in distances)==(2 if len(current)==3 else 4) and
                sum(math.isclose(d,2*side,rel_tol=1e-8) for d in distances)==(1 if len(current)==3 else 2))
    segments=[]
    for a,b in pairs:
        pa,pb=current[a],current[b]
        diagonal=square and math.isclose((pa['x']-pb['x'])**2+(pa['y']-pb['y'])**2,2*side,rel_tol=1e-8)
        segments.append({'source':a,'target':b,'style':'dashed' if diagonal else 'solid','role':'diagonal' if diagonal else 'edge' if square else 'connection'})
    if not specified:segments.sort(key=lambda s:s['role']=='diagonal')
    animation=wants_animation(q) or bool(re.search(r'逐条|依次.*画',q)) and not refuses_animation(q)
    spec={'kind':'animation_scene' if animation else 'coordinates','title':'逐条连接已知点' if animation else '已知点的真实连线','basis':'problem' if entry or image_text else prior.get('basis','example'),
          'caption':'只连接已知点；实线表示正方形的边，虚线表示对角线。' if square else '按请求连接已有点，不额外推断几何性质。'}
    previous=prior.get('points') or prior.get('geometry',{}).get('points') or []
    mapping={i:next((j for j,p in enumerate(current) if (p['x'],p['y'])==(old['x'],old['y'])),None) for i,old in enumerate(previous)}
    geometry=prior.get('geometry',prior)
    shapes={'polygons':[{'vertices':[mapping[i] for i in polygon['vertices']]} for polygon in geometry.get('polygons',[]) if all(mapping.get(i) is not None for i in polygon['vertices'])],
            'circles':[{**circle,'center':mapping[circle['center']]} for circle in geometry.get('circles',[]) if mapping.get(circle['center']) is not None]}
    if previous and all((p['x'],p['y']) in {(old['x'],old['y']) for old in previous} for p in current):spec['basis']=prior['basis']
    if animation:spec.update(template='coordinate_drawing',params={'points':current,'segments':segments,**shapes},duration=12)
    else:spec.update(points=current,segments=segments,**shapes)
    return {'version':VERSION,'operation':'connect_points','required_segments':len(segments),'points':current,'display_points':display_points,'source_layout':prior.get('layout'),'parent_id':prior.get('id'),'arguments':{'visuals':[spec]}}


def matches_task(visual,task,state):
    expected=task.get('required_kind')
    template=task.get('required_template')
    if visual['kind']==expected and (not template or visual.get('template')==template):return True
    # 数学结构与呈现形式分开：同一原题的静态投影不能因原候选是动画而被误拒绝。
    if visual['kind']=='reasoning_diagram':
        return visual.get('template')==template or task.get('operation')=='nonnegative_story' and visual.get('template')=='nonnegative_reasoning'
    mapping={'function_plot':'function_trace','coordinates':'coordinate_drawing','area_model':'fraction_fill','number_line':'number_line_motion'}
    if visual['kind']=='animation_scene' and mapping.get(expected)==visual.get('template'):return True
    originals=(task.get('arguments') or {}).get('visuals',[])
    return expected=='animation_scene' and any(mapping.get(visual['kind'])==v.get('template') for v in originals)

def validate_result(text,state):
    task=state.get('visual_task') or {}
    observed=next((o['result']['visuals'] for o in state.get('observations',[]) if o['tool']=='render_teaching_visual'),[])
    # 实际产物决定呈现名称；不能把静态图说成已生成或可播放的动画。
    if not any(v['kind']=='animation_scene' for v in observed) and re.search(r'动画(?:用来|用于|展示|已(?:经)?生成)|(?:已(?:经)?生成|已准备|已经创建)[^。！？\n]{0,12}动画|点击播放[^。！？\n]{0,12}动画',text):
        raise ContractError('animation claim requires an actual animation_scene result')
    if task.get('required_kind') and not any(matches_task(v,task,state) for v in observed):
        raise ContractError('explicit visual request requires the requested figure from the actual tool, not text only')
    if task.get('arguments'):
        count=max((len(v.get('segments',[])) if v['kind']=='coordinates' else len(v.get('params',{}).get('segments',[])) for v in observed),default=0)
        if count<task.get('required_segments',0):raise ContractError('requested point connections are missing from the actual tool result')
    if re.search(r'已经?(?:画|绘|连接)|已(?:经)?画好|图里.*(?:画好|连好)',text) and not observed:
        raise ContractError('cannot claim drawing completion without a visual tool result')
    # “已知点在线段上”是题干，不是绘图完成声明；必须存在明确的绘制/连接动作。
    if re.search(r'(?:已(?:经)?(?:把[^。！？\n]{0,24})?(?:连线|连接|连好|画出|画好|绘制)|画好)[^。！？\n]{0,12}(?:线段|连线|连接)|已(?:经)?(?:连线|连接)',text):
        actual=any(v.get('segments') or v.get('params',{}).get('segments') for v in observed)
        if not actual:raise ContractError('cannot claim completed segments when the figure only contains points')


def validate_selection(args,state):
    task=state.get('visual_task') or {}
    if task.get('required_kind') and not any(matches_task(v,task,state) for v in args['visuals']):
        raise ContractError('select the visual_task required_kind and required_template before tool execution')
    if task.get('required_points'):
        expected={(p['x'],p['y']) for p in task['required_points']}
        if not any((v.get('kind')=='coordinates' or v.get('template')=='coordinate_drawing') and expected<={(p['x'],p['y']) for p in (v['points'] if v.get('kind')=='coordinates' else v['params']['points'])} for v in args['visuals']):
            raise ContractError('draw ALL requested given points in one coordinate figure, not only a subset')


def normalize_references(text,state):
    """A structured visual ID is not an image URL; never render a fake asset."""
    # 模型曾把已生成动画的内部ID当作图片URL；只移除真实引用，虚构引用必须拒绝。
    known={v['id'] for o in state.get('observations',[]) if o['tool']=='render_teaching_visual' for v in o['result']['visuals']}
    def replace(match):
        if match[1] not in known:raise ContractError('visual image reference must identify an actual tool result')
        return ''
    text=re.sub(r'!\[[^\]\n]*\]\((visual:[^\s)]+)\)',replace,text)
    if known:text=re.sub(r'\[图示[：:][^\]\n]*\]', '',text)
    return text.strip()


def receipt(state):
    visuals=next((o['result']['visuals'] for o in state.get('observations',[]) if o['tool']=='render_teaching_visual'),[])
    story=(state.get('presentation') or {}).get('kind')=='story'
    if visuals and (state.get('visual_task') or {}).get('operation')=='nonnegative_story' and (not state.get('practice_assessment') or state['practice_assessment']['status']=='unverified'):
        from .nonnegative_teaching import story_text
        lesson=visuals[0].get('reasoning_lesson') or {'mode':'solution' if state['route']['teaching']['allow_final_answer'] else 'hint'}
        source=state.get('practice_entry') or {'expression':(state.get('image_question') or state.get('problem_question') or {}).get('text','')}
        from .nonnegative_reasoning import explanation
        text=story_text(source,lesson['mode']=='solution') if story else explanation(source,lesson['mode']=='solution')
        if text:
            text+='\n这个图示内两幅曲线的横轴分别对应各自的一次式，不能把它们当作同一个变量。' if lesson['mode']=='hint' else '\n图中分别标出两个表达式的零点；播放可核对归零、等式变形与代入过程。' if visuals[0]['kind']=='animation_scene' else '\n静态图分别标出两个表达式的零点。'
            return {'kind':'respond','reply':{'text':text,'teaching_action':'explain','evidence_refs':[],'step_refs':[]}}
    if story and (not state.get('practice_assessment') or state['practice_assessment']['status']=='unverified'):
        from .nonnegative_teaching import story_text as nonnegative_story_text
        source=state.get('practice_entry') or {'expression':(state.get('image_question') or state.get('problem_question') or {}).get('text','')}
        narrative=nonnegative_story_text(source,state['route']['teaching']['allow_final_answer'])
        if narrative and (visuals and (state.get('visual_task') or {}).get('operation')=='nonnegative_story' or not visuals and not (state.get('visual_task') or {}).get('arguments')):
            if visuals:narrative+='\n动画：相似积分从有结余变为两项都为零，可观察总量随两项变化。'
            return {'kind':'respond','reply':{'text':narrative,'teaching_action':'explain','evidence_refs':[],'step_refs':[]}}
    if not visuals:
        if story and not (state.get('visual_task') or {}).get('arguments') and state.get('practice_assessment',{}).get('status')=='unverified':
            from .identity_animation import story_text
            text=story_text(state['practice_entry'],state['route']['teaching']['allow_final_answer'])
            if text:return {'kind':'respond','reply':{'text':text,'teaching_action':'explain','evidence_refs':[],'step_refs':[]}}
        return None
    v=next((v for v in visuals if v['kind']=='animation_scene'),visuals[0])
    if (state.get('visual_task') or {}).get('operation') in {'owned_animation','owned_picture'}:
        if state['route']['teaching']['allow_final_answer']:return None
        if state['visual_task']['operation']=='owned_picture':
            text='数轴已重新排版，编号对应下方完整点名和位置。请沿着当前图观察，原题数据保持不变。' if v['kind']=='number_line' else '图示已使用当前题同一组数据重绘，原题条件保持不变。'
            return {'kind':'respond','reply':{'text':text,'teaching_action':'explain','evidence_refs':[],'step_refs':[]}}
        from .visual_followup import explanation
        return {'kind':'respond','reply':{'text':explanation(v),'teaching_action':'explain','evidence_refs':[],'step_refs':[]}}
    if (state.get('visual_task') or {}).get('operation')=='identity_probe' and v.get('algebra_lesson'):
        # 自动配图不能用固定回执代替学生当前问题或作答核对；正文仍由原导师处理。
        lesson=v['algebra_lesson']
        if state['visual_task'].get('automatic') and not lesson.get('story'):return None
        if lesson.get('story'):
            from .identity_animation import story_text
            text=story_text(state.get('practice_entry') or {'expression':lesson['equation']+'对任意x恒成立'},lesson['mode']=='solution')
            return {'kind':'respond','reply':{'text':text,'teaching_action':'explain','evidence_refs':[],'step_refs':[]}}
        text='恒成立意味着每个 $x$ 都要满足原方程。'+('这段动画先移项，再依次代入 $x=0$、$x=1$、$x=2$，对照变化的系数项与不变的常数。' if any(v['kind']=='animation_scene' for v in visuals) else '静态图把原式整理成变化项与固定项，对照两边需要满足的参数条件。')
        text+='最后按原题的所求保留精确结果。' if lesson['mode']=='solution' else '最后只给出两个参数条件，留给你自己求参数和最终结果。'
        return {'kind':'respond','reply':{'text':text,'teaching_action':'explain','evidence_refs':[],'step_refs':[]}}
    if state.get('route',{}).get('teaching',{}).get('label')!='图示辅助':return None
    if v['kind']=='coordinates':
        if v.get('segments'):
            names=['—'.join((v['points'][s['source']]['label'],v['points'][s['target']]['label'])) for s in v['segments']]
            text=f'已画出 {len(names)} 条连线：'+'、'.join(names)+'。可放大查看。'
        else:text=f'已画出 {len(v["points"])} 个点，坐标标在图下方，可放大查看。'
    elif v.get('template')=='coordinate_drawing':text=f'连线动画已准备，共 {len(v["geometry"]["segments"])} 条线段。点击播放或下一步，观察它们依次出现。'
    elif v['kind']=='area_model':text=f'已将整体分成 {v["denominator"]} 份，涂色 {v["numerator"]} 份。'
    else:text='图示已生成，可放大观察。'+('动画可以播放、暂停或逐步查看。' if any(v['kind']=='animation_scene' for v in visuals) else '')
    return {'kind':'respond','reply':{'text':text,'teaching_action':'explain','evidence_refs':[],'step_refs':[]}}
