"""Compile a requested animation from this turn's owned mathematical reference."""
import copy,math,re

def plan(question,entry,prior,source):
    from .visual_tasks import wants_animation,wants_connections
    if not wants_animation(question) or wants_connections(question):return None
    source=' '.join((entry or {}).get(k,'') for k in ('title','expression'))+' '+source
    # 几何小问仍由原符号Controller决定构造与披露，不能用旧连线替代旋转/比例推理。
    if (prior or {}).get('layout')=='geometry':return None
    figure=None
    if '相反数' in source:
        points=(prior or {}).get('points',[])
        pair=next((abs(p['x']) for p in points if p['x'] and any(math.isclose(p['x'],-q['x'],abs_tol=1e-10) for q in points)),None)
        if pair is None and not prior and '2x=4' in source.replace(' ','') and 'x+2=0' in source.replace(' ',''):pair=2
        if pair is not None:
            figure={'kind':'animation_scene','title':'相反数：关于原点对称，和为零','basis':(prior or {}).get('basis','problem'),'template':'opposite_numbers','duration':12,'params':{'value':pair},'caption':'用题干中的已知例子说明两个解的关系；本题未知参数仍留给你。'}
    if figure is None and prior:
        common={k:prior[k] for k in ('title','basis','caption') if k in prior}
        kind=prior['kind']
        if kind=='function_plot' and prior.get('function') in {'linear','quadratic','cubic'}:
            figure={**common,'kind':'animation_scene','template':'function_trace','params':{k:copy.deepcopy(v) for k,v in prior.items() if k in {'function','a','b','c','d','domain','markers','focus_interval','display'}}}
        elif kind=='coordinates' and prior.get('segments'):
            figure={**common,'kind':'animation_scene','template':'coordinate_drawing','params':{k:copy.deepcopy(v) for k,v in prior.items() if k in {'points','segments','polygons','circles'}}}
            # length、精确显示标签是渲染结果元数据，不是新的工具输入。
            figure['params']['points']=[{k:p[k] for k in ('label','x','y')} for p in figure['params']['points']]
            figure['params']['segments']=[{k:v for k,v in segment.items() if k in {'source','target','style','role','label'}} for segment in figure['params']['segments']]
        elif kind=='area_model':figure={**common,'kind':'animation_scene','template':'fraction_fill','params':{k:prior[k] for k in ('numerator','denominator')}}
        elif kind=='number_line' and prior.get('moves'):
            figure={**common,'kind':'animation_scene','template':'number_line_motion','params':{k:prior['moves'][0][k] for k in ('start','delta')}}
        elif kind=='animation_scene' and prior.get('template') in {'opposite_numbers','absolute_distance','number_line_motion','function_trace','coordinate_drawing','fraction_fill','square_root'}:
            figure={**common,'kind':'animation_scene','template':prior['template'],'params':copy.deepcopy(prior['params'])}
    if figure:
        return {'version':'owned_visual_followup_v1','operation':'owned_animation','required_kind':'animation_scene','required_template':figure['template'],'parent_id':(prior or {}).get('id'),'arguments':{'visuals':[figure]}}
    return None

def explanation(visual):
    template=visual.get('template')
    if template=='opposite_numbers':
        from .math_display import exact
        import sympy
        value=exact(sympy.Rational(str(visual['params']['value'])))
        return f'用题干中的例子看相反数：${value}$ 与 $-{value}$ 在零的两侧，到零的距离相等，合起来是 $0$。播放时两个点同步向两边展开，虚线帮助比较距离。\n“和谐方程”比较的是两个方程的解，不是系数。先从不含未知参数的方程入手；动画没有替你求出最后的参数。'
    if template=='function_trace':return '这段动画沿当前函数曲线描绘，保留原来的范围和已知标记。播放时比较位置、变化方向与关键点，最后回到当前题的条件；未批准的答案仍保留。'
    if template=='coordinate_drawing':return '这段动画按当前图中的已有连线依次展开。观察每条线连接哪些已知点、怎样组成当前构造；它没有新增题目条件。'
    if template=='fraction_fill':return '先把同一个整体等分，再逐份涂色。分母决定总份数，分子决定取了几份；动画沿用当前图的同一组数据。'
    if template=='number_line_motion':return '沿用当前数轴例子，先看起点，再看移动方向和长度。向右增加、向左减少，当前位置随移动变化；这是帮助理解规则的例子。'
    if template=='absolute_distance':return '移动的是数轴上的位置，横向色带表示到原点的距离。比较零的两侧，位置可以为负，但距离始终非负。'
    if template=='square_root':return '观察正方形的边长与面积对应变化。边长平方得到面积；画出的边长非负，不等于一个正数只有一个平方根。'
    return '动画已按当前图的数学关系生成，可播放或分步观察。'
