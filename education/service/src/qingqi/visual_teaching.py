"""Bounded, deterministic teaching figures. The owner binds input before execution."""
import math
import re
from fractions import Fraction

from .contracts import ContractError, Denied, fingerprint, obj, validate
from .domain_tools import ToolSpec, number
from .animation_teaching import SCHEMAS as ANIMATION_SCHEMAS, normalize as normalize_animation, render as render_animation
from .advanced_visuals import COORD_FIELDS,FUNCTION,AREA,coordinates,function_plot,area_model

VERSION = 'visual_teaching_v9'
LABEL = {'type':'string','minLength':1,'maxLength':160}
NUM = {'type':'number','minimum':-10000,'maximum':10000}
POINT = obj({'label':LABEL,'x':NUM,'y':NUM}, ['label','x'])
MOVE = obj({'start':NUM,'delta':NUM,'label':LABEL})
EDGE = obj({'source':{'type':'integer','minimum':0,'maximum':7},'target':{'type':'integer','minimum':0,'maximum':7},'label':LABEL})
SPEC = obj({'kind':{'type':'string','enum':['number_line','coordinates','table','bar_chart','scene']},
            'title':LABEL,'basis':{'type':'string','enum':['problem','example']},'caption':{'type':'string','maxLength':240},
            'points':{'type':'array','items':POINT,'minItems':1,'maxItems':8},
            'moves':{'type':'array','items':MOVE,'maxItems':4},
            'columns':{'type':'array','items':LABEL,'minItems':1,'maxItems':6},
            'rows':{'type':'array','items':{'type':'array','items':{'type':'string','maxLength':160},'maxItems':6},'minItems':1,'maxItems':12},
            'bars':{'type':'array','items':obj({'label':LABEL,'value':NUM}),'minItems':1,'maxItems':8},
            'nodes':{'type':'array','items':LABEL,'minItems':2,'maxItems':8},
            'edges':{'type':'array','items':EDGE,'minItems':1,'maxItems':10}}, ['kind','title','basis'])
# 直接采用 ZCode json-schema.ts 支持的 oneOf；模型和执行器看到同一份分类型必填约束。
COMMON={k:v for k,v in SPEC['properties'].items() if k in {'title','basis','caption'}}
FIELDS={'number_line':('points','moves'),'coordinates':('points',),'table':('columns','rows'),'bar_chart':('bars',),'scene':('nodes','edges')}
POINTS={kind:{'type':'array','items':obj({'label':LABEL,'x':NUM,**({'y':NUM} if kind=='coordinates' else {})}),'minItems':1,'maxItems':8} for kind in ('number_line','coordinates')}
SPEC={'oneOf':[obj({**COMMON,'kind':{'type':'string','enum':[kind]},**{key:POINTS[kind] if key=='points' else SPEC['properties'][key] for key in fields}}, ['kind','title','basis',*[key for key in fields if key!='moves']]) for kind,fields in FIELDS.items()]}
SPEC['oneOf'][1]['properties'].update(COORD_FIELDS)
FIELDS['coordinates']=('points','segments','polygons','circles')
SPEC['oneOf'] += [FUNCTION,AREA]
FIELDS['function_plot']=('function','a','b','c','d','domain','markers','focus_interval','display','axis_labels')
FIELDS['area_model']=('numerator','denominator','shape')
SPEC['oneOf']+=ANIMATION_SCHEMAS
SPEC['oneOf'] += [{**schema,'properties':{**schema['properties'],'kind':{'type':'string','enum':['reasoning_diagram']}}} for schema in ANIMATION_SCHEMAS if schema['properties']['template']['enum'][0] in {'function_reasoning','nonnegative_reasoning','identity_probe'}]
FIELDS['animation_scene']=('template','params','duration')
FIELDS['reasoning_diagram']=('template','params','duration')
INPUT = obj({'visuals':{'type':'array','items':SPEC,'minItems':1,'maxItems':1}})
OUTPUT = obj({'visuals':{'type':'array','items':{'type':'object'},'maxItems':1},'version':LABEL})
TOOL = ToolSpec('render_teaching_visual', 'Create ONE bounded teaching visual: a picture OR an animation. coordinates supports real segments, polygons and circles; connect points using source/target indices. function_plot samples linear/quadratic/cubic coefficients; area_model partitions a fraction. Animations use fixed templates, never frames/code. Use example for analogous examples; problem for bound given or symbolic-tool-approved data. No HTML, JS, URLs or hidden final answers.', INPUT, OUTPUT)


def normalize_selection(arguments,*,prefer_animation=False):
    """Complete only a missing discriminator when one schema fits all actual data."""
    if not isinstance(arguments,dict) or not isinstance(arguments.get('visuals'),list):return arguments
    visuals=[]
    for raw in arguments['visuals']:
        raw=normalize_animation(raw)
        if prefer_animation and isinstance(raw,dict) and raw.get('kind')=='function_plot' and raw.get('function') in {'linear','quadratic','cubic'}:
            validate(raw,FUNCTION)
            raw={**{k:v for k,v in raw.items() if k in {'title','basis','caption'}},'kind':'animation_scene','template':'function_trace',
                 'params':{k:v for k,v in raw.items() if k in {'function','a','b','c','d','domain','markers','focus_interval','display'}}}
        if prefer_animation and isinstance(raw,dict) and raw.get('kind')=='coordinates' and raw.get('segments') and set(raw)<={'kind','title','basis','caption','points','segments','polygons','circles'}:
            # 明确要求动画时，把完整合法的静态连线数据适配为同一组点线的绘制动画。
            raw={**{k:v for k,v in raw.items() if k in {'title','basis','caption'}},'kind':'animation_scene','template':'coordinate_drawing','params':{k:v for k,v in raw.items() if k in {'points','segments','polygons','circles'}}}
        candidates=[]
        if isinstance(raw,dict) and 'kind' not in raw:
            for kind in FIELDS:
                candidate={**raw,'kind':kind}
                try:validate(candidate,SPEC)
                except ContractError:continue
                candidates.append(candidate)
        visuals.append(candidates[0] if len(candidates)==1 else raw)
    return {**arguments,'visuals':visuals}


def _strings(value):
    if isinstance(value,str):
        yield value
    elif isinstance(value,dict):
        for item in value.values():yield from _strings(item)
    elif isinstance(value,list):
        for item in value:yield from _strings(item)


def _numbers(value):
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        yield value
    elif isinstance(value,dict):
        for key,item in value.items():
            if key not in {'source','target','center','vertices','duration','at','range','extent','domain','y_range','visible_segments','reveal','length'}:yield from _numbers(item)
    elif isinstance(value,list):
        for item in value:yield from _numbers(item)


def _literals(text):
    # Unicode \w 包括汉字，旧边界会漏掉“终点14”这种中文后紧接的可见答案。
    return {Fraction(v) for v in re.findall(r'(?<![A-Za-z0-9_.])[+-]?\d+(?:\.\d+)?', text)}


def _check_labels(spec):
    for text in _strings(spec):
        if re.search(r'<\s*/?\s*[A-Za-z][^>]*>|<[!?]|https?://|javascript:|data:|```|\[\[|\]\]',text,re.I):
            raise ContractError('visual labels must be plain text')
        for left,right in re.findall(r'([A-Za-z0-9_.+*/×÷()（）°∠\s\-]+)=([A-Za-z0-9_.+*/×÷()（）°∠\s\-]+)',text):
            # 旧正则把 x+x+40=180 截成 40=180，误拒绝合法代数关系；只核验完整纯数值式。
            if re.search(r'[A-Za-z_°∠]',left+right):continue
            left,right=(s.strip().replace('（','(').replace('）',')') for s in (left,right))
            if not left or not right:continue
            if left.count('(')-left.count(')')==1 and right.count(')')-right.count('(')==1 and left.startswith('(') and right.endswith(')'):
                left,right=left[1:],right[:-1]
            try:
                if number(left)!=number(right):raise ContractError('false arithmetic equality in visual')
            except (SyntaxError,ZeroDivisionError,OverflowError,ValueError) as error:
                raise ContractError('invalid arithmetic equality in visual') from error


def render_visuals(*, visuals):
    validate({'visuals':visuals}, INPUT)
    if len(visuals)!=1:raise ContractError('one teaching turn must render exactly one visual')
    result=[]
    fields={kind:set(items) for kind,items in FIELDS.items()}
    required={kind:items-{'moves','duration','segments','polygons','circles','c','d','markers','focus_interval','display','axis_labels'} for kind,items in fields.items()}
    for spec in visuals:
        kind=spec['kind']
        present=set(spec)-{'kind','title','basis','caption'}
        if not required[kind]<=present or not present<=fields[kind]:raise ContractError('visual fields differ from selected type')
        if any(not math.isfinite(n) for n in _numbers(spec)):raise ContractError('visual numbers must be finite')
        _check_labels(spec)
        output={**spec,'id':'visual:'+fingerprint(spec)[:24], 'provenance':'原题已知数值 · 图示不等于整题核验' if spec['basis']=='problem' else '相似例子 / 情景示意', 'version':VERSION}
        output['presentation_role']='animation' if kind=='animation_scene' else 'picture'
        if spec['basis']=='problem' and kind in {'function_plot','area_model'}:output['provenance']='依据当前表达式 · 工具计算'
        if kind=='animation_scene':output.update(render_animation(spec))
        if kind=='reasoning_diagram':
            from .teaching_visual_pair import static_lesson
            output.update(static_lesson(render_animation(spec)))
        if kind=='function_plot':output.update(function_plot(spec))
        if kind=='area_model':output.update(area_model(spec))
        if kind=='number_line':
            if any('y' in p for p in spec['points']):raise ContractError('number line cannot contain y coordinates')
            output['moves']=[{**m,'end':float(Fraction(str(m['start']))+Fraction(str(m['delta'])))} for m in spec.get('moves',[])]
            values=[p['x'] for p in spec['points']]+[n for m in output['moves'] for n in (m['start'],m['end'])]
            lo,hi=min(values),max(values)
            span=max(hi-lo,2)
            output['range']=[lo-span*.15,hi+span*.15] if hi>lo else [lo-1,hi+1]
        if kind=='coordinates':
            if any('y' not in p for p in spec['points']):raise ContractError('coordinates require x and y')
            output.update(coordinates(spec))
        if kind=='table' and any(len(row)!=len(spec['columns']) for row in spec['rows']):raise ContractError('table rows must match columns')
        if kind=='scene':
            if any(e['source']>=len(spec['nodes']) or e['target']>=len(spec['nodes']) or e['source']==e['target'] for e in spec['edges']):raise ContractError('scene edge must reference different existing nodes')
            def quoted(label):return '"'+label.replace('"','＂').replace('\n',' ').replace('[','（').replace(']','）').replace('|','／').replace('<','＜').replace('>','＞')+'"'
            lines=['flowchart LR']+[f'n{i}[{quoted(label)}]' for i,label in enumerate(spec['nodes'])]
            lines += [f'n{e["source"]} -->|{quoted(e["label"])}| n{e["target"]}' for e in spec['edges']]
            output['mermaid']='\n'.join(lines)
        result.append(output)
    return {'visuals':result,'version':VERSION}


def validate_binding(args,state):
    validate(args,INPUT)
    output=render_visuals(**args)
    request=state.get('effective_request',{})
    entry=state.get('practice_entry',{})
    source=' '.join(str(v) for v in (request.get('question',''),request.get('expression',''),entry.get('expression',''),state.get('image_question',{}).get('text',''),state.get('problem_question',{}).get('text','')))
    given=_literals(source)
    protected=[]
    for observation in state.get('observations',[]):
        if observation['tool'] in {'review_arithmetic','worker_review27b'}:protected.append(observation['result'].get('answer',''))
    if entry.get('key',{}).get('kind')=='numeric':
        from .practice_tutoring import identity_answer
        exact=identity_answer(entry)
        protected+=[exact['display']] if exact else entry['key']['values']
    if entry.get('key',{}).get('kind')=='choice' and entry.get('options'):
        key=entry['key']['values'][0]
        if len(key)==1 and 'A'<=key<=chr(64+len(entry['options'])):protected.append(entry['options'][ord(key)-65])
    for raw,spec in zip(args['visuals'],output['visuals']):
        if raw['kind']=='reasoning_diagram':
            from .teaching_visual_pair import canonical_animation,companion
            original=canonical_animation(raw,state)
            if not original or raw!=companion(original,state):raise ContractError('static reasoning diagram must match the owned compiler projection')
            validate_binding({'visuals':[original]},state)
            continue
        if (state.get('visual_task') or {}).get('operation')=='nonnegative_story':
            # 静态与动态共用原题编译器；必须匹配本轮披露许可，而非模型任选曲线。
            from .nonnegative_reasoning import specification,static_specifications
            expected=static_specifications(entry or {'expression':source},state['route']['teaching']['allow_final_answer']) if raw['kind']=='function_plot' else [specification(entry or {'expression':source},state['route']['teaching']['allow_final_answer'])]
            if raw not in expected:raise ContractError('nonnegative curve disclosure must match the current owned equation')
            continue
        if raw.get('template')=='identity_probe':
            from .identity_animation import specification
            expected=specification(entry or {'expression':source},state['route']['teaching']['allow_final_answer'],scenario='scorekeepers' if (state.get('presentation') or {}).get('kind')=='story' else None)
            if raw!=expected:raise ContractError('identity animation parameters and disclosure must match the current owned equation')
            continue
        function_report=next((o['result'] for o in state.get('observations',[]) if o['tool']=='analyze_function'),None)
        if not function_report and raw.get('template')=='function_reasoning':
            from .function_solver import identify
            owned=identify((state.get('image_question') or state.get('problem_question') or {}).get('text','') or source)
            expected={**owned['arguments'],'lesson_mode':'solution' if state['route']['teaching']['allow_final_answer'] else 'hint'} if owned else None
            if raw['params']!=expected:raise ContractError('function reasoning must match the current owned equation and disclosure mode')
            continue
        if function_report:
            from .function_solver import static_visuals
            if raw in function_report.get('approved_problem_hint_visuals',[]):continue
            if state['route']['teaching']['allow_final_answer'] and raw in function_report.get('approved_problem_solution_visuals',[]):continue
            if raw in function_report['approved_hint_visuals'] or raw in static_visuals(function_report['approved_hint_visuals']):continue
            if state['route']['teaching']['allow_final_answer'] and (raw in function_report['approved_solution_visuals'] or raw in static_visuals(function_report['approved_solution_visuals'])):continue
            # 求解参数和原题图只能使用当前核验工具批准的数据，不能改参或夹带答案。
            raise ContractError('function teaching visual must use the current authorized symbolic result')
        if raw.get('template')=='nonnegative_reasoning':
            from .nonnegative_reasoning import specification
            expected=specification(entry or {'expression':source},state['route']['teaching']['allow_final_answer'])
            if raw!=expected:raise ContractError('nonnegative reasoning must use the complete owned equation, target and disclosure mode')
            continue
        if raw.get('display') or raw.get('params',{}).get('display'):
            literal_figures=(state.get('visual_task') or {}).get('arguments',{}).get('visuals',[])
            from .teaching_visual_pair import companion
            # 同题静态/动画转码保留精确标签；父图仍须来自本轮字面表达式编译器。
            derived=any(v['kind']=='animation_scene' and companion(v,state)==raw for v in literal_figures)
            if raw not in literal_figures and not derived and not (raw['kind']=='animation_scene' and companion(raw,state) in literal_figures):raise ContractError('exact visual labels must come from owned symbolic or literal-expression output')
        if raw.get('function') in {'square_root','absolute'}:
            raise ContractError('outer function plots require the current owned nonnegative expression compiler')
        geometry=next((o['result'] for o in state.get('observations',[]) if o['tool']=='solve_geometry'),None)
        approved=raw
        if raw.get('template') in {'triangle_rotation','geometry_motion'} and 'lesson_mode' in raw.get('params',{}):
            allowed=state['route']['teaching']['allow_final_answer']
            scope=state.get('tutoring_scope')
            if scope:
                part=1 if raw['template']=='triangle_rotation' else 2 if raw['params'].get('lesson_goal')=='ratio' else 3
                unit=next((u for u in scope['units'] if u['part']==part),None)
                if unit is None:raise ContractError('geometry animation must belong to a requested part')
                if unit['teaching']['plan']['visual']['forbid_animation']:raise ContractError('this question part explicitly declined animation')
                allowed=unit['allow_final_answer']
            if raw['params']['lesson_mode']=='solution' and not allowed:
                raise ContractError('complete teaching steps require owner-authorized final answer disclosure')
            if raw['params'].get('teaching_mode'):
                expected_mode=unit['teaching']['mode'] if scope else state['route']['teaching']['mode']
                if raw['params']['teaching_mode']!=expected_mode:raise ContractError('animation teaching mode must match the current owner decision')
            approved={**raw,'params':{k:v for k,v in raw['params'].items() if k not in {'lesson_mode','lesson_goal','teaching_mode'}}}
        if raw.get('params',{}).get('lesson_goal')=='ratio' and (not geometry or 'ratio' not in geometry['parts']):
            raise ContractError('ratio storyboard must belong to the current symbolic question')
        from .teaching_visual_pair import companion
        if geometry and (approved in geometry['approved_visuals'] or raw.get('template')=='coordinate_drawing' and companion(raw,state) in geometry['approved_visuals']):
            if state.get('tutoring_scope') and raw['kind']=='coordinates':
                parts={u['part'] for u in state['tutoring_scope']['units']}
                if raw['title'].startswith('第（1）问') and 1 not in parts or not raw['title'].startswith('第（1）问') and parts=={1} and 'midpoint' in geometry['parts']:raise ContractError('geometry diagram belongs to another question part')
            # 图中坐标由受控几何构造推导，不按逐字数字白名单误拒绝，也不能让模型改动它们。
            continue
        if raw.get('template') in {'triangle_rotation','geometry_motion'}:raise ContractError('geometry animation must use parameters approved by the owned symbolic geometry result')
        if raw['basis']=='problem':
            # 表格数字也是可见数据；减法的移动方向可取负，但长度仍须来自题面。
            data={k:v for k,v in raw.items() if k not in {'moves','title','caption'}}
            literals={Fraction(str(n)) for n in _numbers(data)}|_literals(' '.join(_strings(data)))
            if raw['kind']=='function_plot' or raw.get('template')=='function_trace':
                from .visual_expressions import specified_functions,polynomial
                function=raw['params'] if raw.get('template')=='function_trace' else raw
                # 展开式系数未必逐字出现在原式中；比较代数系数，不能随意换另一个函数。
                actual=tuple(Fraction(str(v)) for v in ((function['a'],function['b'],function.get('c',0),function.get('d',0)) if function['function']=='cubic' else (0,function['a'],function['b'],function.get('c',0)) if function['function']=='quadratic' else (0,0,function['a'],function['b'])))
                candidates=[]
                for expression in specified_functions(source):
                    coefficients=polynomial(expression)
                    candidates.append(tuple(coefficients.get(i,Fraction(0)) for i in (3,2,1,0)))
                if not any(all(math.isclose(float(a),float(b),rel_tol=1e-10,abs_tol=1e-12) for a,b in zip(actual,candidate)) for candidate in candidates):raise ContractError('function must match the current specified expression')
            elif not literals<=given|{Fraction(0)} or any(Fraction(str(m['start'])) not in given or abs(Fraction(str(m['delta']))) not in {abs(n) for n in given} for m in raw.get('moves',[])):
                raise ContractError('visual problem values must come from current given data; use basis example for an illustrative example')
            if raw['kind']=='coordinates' or raw.get('template')=='coordinate_drawing':
                from .visual_tasks import coordinate_pairs
                actual=raw['points'] if raw['kind']=='coordinates' else raw['params']['points']
                pairs={(p['x'],p['y']) for p in coordinate_pairs(source)}
                if any((p['x'],p['y']) not in pairs for p in actual):raise ContractError('coordinate pairs must match the current given points, not scattered numbers')
        if not state['route']['teaching']['allow_final_answer']:
            text=' '.join(_strings(raw))
            if re.search(r'最终答案|正确选项|答案[是为:=：]',text):raise ContractError('visual must not state final answer')
            visible={Fraction(str(n)) for n in _numbers({k:v for k,v in spec.items() if k not in {'range','extent'}})}|_literals(text)
            if spec['kind']=='coordinates' or spec.get('template')=='coordinate_drawing':
                from .visual_tasks import coordinate_pairs
                known={(p['x'],p['y']) for p in coordinate_pairs(source)}
                hidden={(p['x'],p['y']) for value in protected for p in coordinate_pairs(value)}-known
                points=spec['points'] if spec['kind']=='coordinates' else spec['geometry']['points']
                if hidden & {(p['x'],p['y']) for p in points}:raise ContractError('visual reveals the protected missing coordinate; choose another example')
            for answer in protected:
                try:value=number(answer)
                except (ValueError,SyntaxError,ZeroDivisionError,OverflowError):continue
                # 给定数本来就可见；新图不能通过条形高度/数轴终点夹带受保护答案。
                if value not in given and value in visible:raise ContractError('visual example overlaps protected final value; choose another example')
            if raw['basis']=='problem' and raw.get('moves'):
                raise ContractError('use a different example for full arithmetic movement while hinting')
            if raw['basis']=='problem' and raw.get('template') in {'number_line_motion','travel_motion'}:
                raise ContractError('use a different motion example while hinting')
    return output


def suggest_visual(request,state):
    from .visual_tasks import refuses_drawing
    if refuses_drawing(request.question) or state.get('annotation_source'):return None
    source=request.expression
    match=re.fullmatch(r'\s*([+-]?\d+(?:\.\d+)?)\s*([+-])\s*(\d+(?:\.\d+)?)\s*',source)
    if not match:
        template=state.get('teaching_plan',{}).get('visual',{}).get('recommended_template')
        source=(state.get('problem_question') or {}).get('text') or request.question
        common={'kind':'animation_scene','basis':'example','duration':12,'caption':'使用明确标注的例子理解当前概念，原题最后的结果仍由你完成。'}
        proposed=None
        if template=='absolute_distance':proposed={'visuals':[{**common,'template':'absolute_distance','title':'绝对值：移动位置，观察到原点的距离','params':{'values':[-3,2]}}]}
        elif template=='square_root':proposed={'visuals':[{**common,'template':'square_root','title':'平方根：正方形面积与边长怎样对应','params':{'areas':[4,16]}}]}
        elif not state.get('practice_entry') and not state.get('image_question') and re.search('顶点|抛物线|二次函数',source) and state.get('teaching_plan',{}).get('goal')=='concept':
            proposed={'visuals':[{**common,'template':'function_trace','title':'以y=x²理解顶点和对称轴','caption':'这是用于理解概念的y=x²例子；标记原点，沿曲线观察对称位置与最低点。','params':{'function':'quadratic','a':1,'b':0,'c':0,'domain':[-3,3],'markers':[{'x':0,'y':0,'label':'顶点与对称轴的交点'}]}}]}
        elif '分数' in source and re.search('含义|是什么|什么是|理解|分子|分母',source):proposed={'visuals':[{**common,'template':'fraction_fill','title':'理解分数：先等分，再观察所占部分','params':{'numerator':2,'denominator':5}}]}
        if proposed:
            try:validate_binding(proposed,state)
            except ContractError:return None
            return proposed
        return None
    a,b=float(match[1]),float(match[3])*(1 if match[2]=='+' else -1)
    # 明确提示请求用不同例子演示，不能把原题完整计算结果画在数轴上。
    candidates=[(a,b)] if state['route']['teaching']['allow_final_answer'] else [(-2,3),(-3,5),(-4,7),(-5,9)] if b>=0 else [(4,-3),(2,-5),(-2,-3),(-3,-4)]
    for a,b in candidates:
        proposed={'visuals':[{'kind':'number_line','title':'沿数轴理解加减','basis':'example' if not state['route']['teaching']['allow_final_answer'] else 'problem','points':[{'label':'起点','x':a}], 'moves':[{'start':a,'delta':b,'label':'向右加' if b>=0 else '向左减'}]}]}
        try:validate_binding(proposed,state)
        except ContractError:continue
        return proposed
    return None
