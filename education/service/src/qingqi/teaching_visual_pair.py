"""Select one teaching visual, reusing existing owned math/animation projections."""
import re,copy

def static_lesson(rendered):
    """Only the static reader's data; retain exact ticks/markers while bounding samples."""
    def compact(value):
        if isinstance(value,dict):
            result={}
            for key,item in value.items():
                if key=='samples' and isinstance(item,list):
                    sampled=item[::max(1,(len(item)-1+59)//60)]
                    if item and sampled[-1]!=item[-1]:sampled.append(item[-1])
                    result[key]=sampled
                else:result[key]=compact(item)
            return result
        if isinstance(value,list):return [compact(v) for v in value]
        return value
    lesson=rendered.get('reasoning_lesson')
    if lesson:
        # 整套动画采样与步骤重复曾超过工具64KB限额；静态图仅保留实际展示的字段。
        fields={'version','kind','mode','problem','goal','given','curve','derivative_curve','term_curves'}
        data={k:v for k,v in lesson.items() if k in fields}
        data['cases']=lesson.get('cases',[]) if lesson['mode']=='hint' else []
        data['steps']=[s for s in lesson['steps'] if s['scene']=='conditions']
        return {'reasoning_lesson':compact(data)}
    algebra=rendered.get('algebra_lesson')
    return {'algebra_lesson':{k:algebra[k] for k in ('mode','equation','rearranged','conditions','story') if k in algebra}} if algebra else {}

def canonical_animation(raw,state):
    """Restore the original compiler title; all source/permission checks still run."""
    p=raw['params'];template=raw['template']
    source=state.get('practice_entry') or {'expression':(state.get('image_question') or state.get('problem_question') or {}).get('text') or state.get('effective_request',{}).get('question','')}
    if template=='function_reasoning':
        from .function_reasoning import specification
        return specification({k:p[k] for k in ('k','constant','parameter','interval')},p['lesson_mode']=='solution')
    if template=='nonnegative_reasoning':
        from .nonnegative_reasoning import specification
        return specification(source,p['lesson_mode']=='solution')
    if template=='identity_probe':
        from .identity_animation import specification
        return specification(source,p['lesson_mode']=='solution',scenario=p.get('scenario'))
    return None

def delivery(question):
    from .visual_tasks import refuses_animation,refuses_drawing,wants_animation
    if re.search(r'只(?:用|要)?文字|仅(?:用)?文字|(?:改|换)(?:为|成)文字(?:故事|讲解)',question) or refuses_drawing(question) and not wants_animation(question):return 'text'
    if refuses_animation(question) or re.search(r'(?:只|仅)(?:要|给|看|用|需)[^。！？\n]{0,8}(?:图片|图像|静态图|一张图)',question):return 'picture'
    # 同时提及两种形式不是生成双份的许可，仍按当前教学目标择一。
    if re.search(r'(?:图|图片|图像)\s*(?:和|与|或|及|跟).{0,6}动画|动画\s*(?:和|与|或|及|跟).{0,6}(?:图|图片|图像)',question):return 'auto'
    if wants_animation(question):return 'animation'
    if re.search(r'画.*(?:图|曲线)|函数图|静态图',question):return 'picture'
    return 'auto'

def choose_delivery(question):
    explicit=delivery(question)
    if explicit!='auto':return explicit,'按学生当前明确的呈现要求。'
    if re.search(r'旋转|平移|运动|变化|逐条|依次|解题步骤|解题过程|推导|一步一步|一步步',question):
        return 'animation','当前需要观察变化、构造顺序或连续推导，优先动画。'
    return 'picture','当前先看清条件、位置、关系或概念，一张讲解图更直接。'

def companion(animation,state):
    template=animation.get('template');p=animation.get('params',{});common={k:animation[k] for k in ('basis','caption') if k in animation}
    if template=='opposite_numbers':
        return {**common,'kind':'number_line','title':'相反数：零两侧的对称位置','points':[{'label':'正向位置','x':p['value']},{'label':'相反位置','x':-p['value']}]}
    if template in {'function_reasoning','nonnegative_reasoning','identity_probe'}:
        return {**copy.deepcopy(animation),'kind':'reasoning_diagram','title':{'function_reasoning':'原题曲线：关键情形与条件','nonnegative_reasoning':'原式图解：两项的图像与非负条件','identity_probe':'原式图解：变化项与固定项'}[template]}
    geometry=next((o['result'] for o in state.get('observations',[]) if o['tool']=='solve_geometry'),None)
    if template in {'triangle_rotation','geometry_motion'} and geometry:
        midpoint=template=='triangle_rotation'
        return next(copy.deepcopy(v) for v in geometry['approved_visuals'] if v['kind']=='coordinates' and ('第（1）问' in v['title'])==midpoint and '所有点' not in v['title'] and '全部点' not in v['title'])
    if template=='function_trace':return {**common,'kind':'function_plot','title':animation['title'],**copy.deepcopy(p)}
    if template=='coordinate_drawing':return {**common,'kind':'coordinates','title':animation['title'],**copy.deepcopy(p)}
    if template=='number_line_motion':
        return {**common,'kind':'number_line','title':'数轴：起点、方向与位移','points':[{'label':'起点','x':p['start']}],
                'moves':[{'start':p['start'],'delta':p['delta'],'label':'向右' if p['delta']>=0 else '向左'}]}
    if template=='fraction_fill':return {**common,'kind':'area_model','title':'分数：整体、等份与部分','numerator':p['numerator'],'denominator':p['denominator'],'shape':'rectangle'}
    if template=='absolute_distance':return {**common,'kind':'number_line','title':'绝对值：位置与到原点的距离','points':[{'label':'原点','x':0}]+[{'label':f'距离 {abs(v)}','x':v} for v in p['values'][:6]]}
    if template=='square_root':return {**common,'kind':'table','title':'正方形的面积与边长','columns':['面积','边长的精确表示'],
                                       'rows':[[str(a),r'$\sqrt{'+str(a)+'}$'] for a in p['areas']]}
    if template=='nonnegative_sum':return {**common,'kind':'table','title':'两项非负时，总和怎样变化','columns':['第一项','第二项','总和'],
                                          'rows':[[str(a),str(b),str(a+b)] for a,b in p['pairs']]}
    if template=='travel_motion':
        end=min(p['until'],5)
        return {**common,'kind':'table','title':'位置随时间变化：对照两条运动规律','columns':['时间','甲的位置','乙的位置'],
                'rows':[[str(t),str(p['start_a']+p['speed_a']*t),str(p['start_b']+p['speed_b']*t)] for t in (0,end/2,end)]}
    if template=='pythagorean':return {**common,'kind':'table','title':'勾股关系：直角边与面积','columns':['边','对应正方形面积'],
                                     'rows':[['a',str(p['a']**2)],['b',str(p['b']**2)],['c²=a²+b²',str(p['a']**2+p['b']**2)]]}
    return None

def prepare(arguments,state):
    from .contracts import validate
    from .visual_teaching import INPUT
    # 符号Controller可给最多两个内部候选；真正工具Schema和模型Schema都只接受一个。
    if isinstance(arguments,dict) and isinstance(arguments.get('visuals'),list) and 1<=len(arguments['visuals'])<=2:
        for visual in arguments['visuals']:validate({**arguments,'visuals':[visual]},INPUT)
    else:validate(arguments,INPUT)
    figures=copy.deepcopy(arguments['visuals']);policy=state.get('teaching_plan',{}).get('visual',{})
    scope=state.get('tutoring_scope') or {};q=state.get('original_question') or state.get('effective_request',{}).get('question','')
    form=policy.get('delivery')
    if form not in {'text','picture','animation'}:form=choose_delivery(q)[0]
    if form=='text':
        from .contracts import ContractError
        raise ContractError('student requested text only; do not execute a visual tool')
    active=scope.get('active_part')
    source_parts=state.get('scoped_visual_parts',[])
    mapped=[v for part,v in zip(source_parts,figures) if part==active] if len(source_parts)==len(figures) else []
    if active:state['scoped_visual_parts']=[active]
    # 多小问候选只取当前教学问；不能为了保留两种形式而扩大发布范围。
    preferred='triangle_rotation' if active==1 else 'geometry_motion' if active in {2,3} else None
    goal='ratio' if active==2 else 'function'
    matching=[v for v in figures if v.get('template')==preferred and (preferred!='geometry_motion' or v.get('params',{}).get('lesson_goal')==goal)]
    if mapped:first=mapped[0]
    elif matching:first=matching[0]
    elif re.search(r'导函数|导数图',q):first=next((v for v in figures if '导函数' in v['title']),figures[0])
    else:first=figures[0]
    if form=='picture':
        # 两幅原题曲线可放在同一个静态推理图内，不生成两个独立卡片。
        report=next((o['result'] for o in state.get('observations',[]) if o['tool']=='analyze_function'),None)
        if report:
            key='approved_problem_solution_visuals' if state['route']['teaching']['allow_final_answer'] else 'approved_problem_hint_visuals'
            first=companion(report[key][0],state)
        elif (state.get('visual_task') or {}).get('operation')=='nonnegative_story':
            from .nonnegative_reasoning import specification
            source=state.get('practice_entry') or {'expression':(state.get('image_question') or state.get('problem_question') or {}).get('text') or q}
            first=companion(specification(source,state['route']['teaching']['allow_final_answer']),state)
        elif first['kind']=='animation_scene':first=companion(first,state)
        if first is None:
            from .contracts import ContractError
            raise ContractError('requested static picture has no supported matching representation')
        return {'visuals':[first]}
    if first['kind']=='animation_scene':return {'visuals':[first]}
    common={k:first[k] for k in ('title','basis','caption') if k in first}
    if first['kind']=='reasoning_diagram':motion=canonical_animation(first,state)
    elif first['kind']=='number_line' and first.get('moves'):
        move=first['moves'][0];motion={**common,'kind':'animation_scene','template':'number_line_motion','duration':12,'params':{k:move[k] for k in ('start','delta')}}
    elif first['kind']=='function_plot' and first.get('function') in {'linear','quadratic','cubic'}:
        motion={**common,'kind':'animation_scene','template':'function_trace','duration':12,'params':{k:v for k,v in first.items() if k in {'function','a','b','c','d','domain','markers','focus_interval','display'}}}
    elif first['kind']=='coordinates' and first.get('segments'):
        motion={**common,'kind':'animation_scene','template':'coordinate_drawing','duration':12,'params':{k:v for k,v in first.items() if k in {'points','segments','polygons','circles'}}}
    elif first['kind']=='area_model':motion={**common,'kind':'animation_scene','template':'fraction_fill','duration':12,'params':{k:first[k] for k in ('numerator','denominator')}}
    else:
        if policy.get('explicit_animation'):
            from .contracts import ContractError
            raise ContractError('requested animation needs a supported changing mathematical scene')
        policy.update(delivery='picture',prefer_animation=False,forbid_animation=True,selection_reason='当前构造只有可信静态解释，选择相关讲解图。')
        return {'visuals':[first]}
    return {'visuals':[motion]}
