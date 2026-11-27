"""Trusted math-animation templates. Models provide parameters, never frames or code."""
import math
from fractions import Fraction
from .contracts import obj,validate,ContractError
from .advanced_visuals import POINT,SEGMENT,COORD_FIELDS,coordinates,FUNCTION,function_plot
from .geometry_animation import PARAMS as GEOMETRY_PARAMS, render as render_geometry
from .identity_animation import PARAMS as IDENTITY_PARAMS,render as render_identity
from .function_reasoning import PARAMS as FUNCTION_REASONING_PARAMS,render as render_function_reasoning
from .nonnegative_reasoning import PARAMS as NONNEGATIVE_REASONING_PARAMS,render as render_nonnegative_reasoning

NUM={'type':'number','minimum':-10000,'maximum':10000}
ARRAY={'type':'array','items':NUM,'minItems':1,'maxItems':6}
PARAMS={
    'opposite_numbers':obj({'value':{'type':'number','minimum':0,'maximum':10000}}),
    'absolute_distance':obj({'values':ARRAY}),
    'square_root':obj({'areas':{'type':'array','items':{'type':'number','minimum':0,'maximum':100},'minItems':1,'maxItems':6}}),
    'nonnegative_sum':obj({'pairs':{'type':'array','items':{'type':'array','items':{'type':'number','minimum':0,'maximum':100},'minItems':2,'maxItems':2},'minItems':1,'maxItems':6}}),
    'number_line_motion':obj({'start':NUM,'delta':NUM}),
    'travel_motion':obj({'start_a':NUM,'speed_a':NUM,'start_b':NUM,'speed_b':NUM,'until':{'type':'number','minimum':1,'maximum':60}}),
    'coordinate_drawing':obj({'points':{'type':'array','items':POINT,'minItems':2,'maxItems':8},'segments':{'type':'array','items':SEGMENT,'minItems':1,'maxItems':16},'polygons':COORD_FIELDS['polygons'],'circles':COORD_FIELDS['circles']},['points','segments']),
    'fraction_fill':obj({'numerator':{'type':'integer','minimum':0,'maximum':24},'denominator':{'type':'integer','minimum':1,'maximum':24}}),
    'pythagorean':obj({'a':{'type':'number','minimum':.1,'maximum':10},'b':{'type':'number','minimum':.1,'maximum':10}}),
    **GEOMETRY_PARAMS,
    'identity_probe':IDENTITY_PARAMS,
    'function_reasoning':FUNCTION_REASONING_PARAMS,
    'nonnegative_reasoning':NONNEGATIVE_REASONING_PARAMS,
    'function_trace':obj({k:FUNCTION['properties'][k] for k in ('function','a','b','c','d','domain','markers','focus_interval','display')},['function','a','b','domain']),
}
# 根式/绝对值静态图有独立原题编译器；通用function_trace仍只接受原多项式协议。
PARAMS['function_trace']['properties']['function']={'type':'string','enum':['linear','quadratic','cubic']}
LABEL={'type':'string','minLength':1,'maxLength':160}
SCHEMAS=[obj({'kind':{'type':'string','enum':['animation_scene']},'title':LABEL,'basis':{'type':'string','enum':['problem','example']},'caption':{'type':'string','maxLength':240},'template':{'type':'string','enum':[template]},'params':params,'duration':{'type':'number','minimum':8,'maximum':20}},['kind','title','basis','template','params']) for template,params in PARAMS.items()]


def normalize(spec):
    if isinstance(spec,dict) and spec.get('kind')=='animation_scene':
        function_keys=set(PARAMS['function_trace']['properties'])
        flat={k:v for k,v in spec.items() if k in function_keys}
        if flat and spec.get('template','function_trace')=='function_trace':
            nested=spec.get('params',{})
            if not isinstance(nested,dict):return spec
            if any(k in nested and nested[k]!=v for k,v in flat.items()):
                raise ContractError('conflicting flat and nested animation parameters')
            combined={**nested,**flat}
            validate(combined,PARAMS['function_trace'])
            spec={**{k:v for k,v in spec.items() if k not in function_keys},'template':'function_trace','params':combined}
        spec={k:v for k,v in spec.items() if not (k=='animation_scene' and v is True)}
        nested=(spec.get('params') or {}).get('template') if isinstance(spec.get('params'),dict) else None
        if isinstance(nested,str) and nested in PARAMS and spec.get('template',nested)==nested:
            spec={**spec,'template':nested,'params':{k:v for k,v in spec['params'].items() if k!='template'}}
    if not isinstance(spec,dict) or 'template' in spec or not isinstance(spec.get('params'),dict):return spec
    matches=[]
    for template,schema in PARAMS.items():
        try:validate(spec['params'],schema)
        except ContractError:continue
        matches.append(template)
    return {**spec,'template':matches[0]} if len(matches)==1 else spec


def render(spec):
    kind=spec['template'];p=spec['params'];validate(p,PARAMS[kind]);duration=spec.get('duration',12)
    if kind=='identity_probe':return render_identity(p,duration)
    if kind=='function_reasoning':return render_function_reasoning(p,duration)
    if kind=='nonnegative_reasoning':return render_nonnegative_reasoning(p,duration)
    if kind in GEOMETRY_PARAMS:return render_geometry(kind,p,duration)
    if kind=='opposite_numbers':
        value=p['value'];extent=max(value,1)*1.3
        steps=[{'at':0,'title':'从原点开始','explanation':'原点表示零，两个点从同一个中心同步展开。'},
               {'at':.4,'title':'相反方向','explanation':'两点离开原点的方向相反，移动的距离始终相等。'},
               {'at':.75,'title':'比较距离','explanation':'虚线两边等长；两个解互为相反数，这正是题干的定义。'},
               {'at':1,'title':'和为零','explanation':'正负两部分抵消，和为零。把这一关系用于当前两个方程，未知参数仍由你求。'}]
        return {'duration':duration,'frames':[{'at':duration*t,'values':{'value':value*min(1,t/.75),'opposite':-value*min(1,t/.75),'reveal':t}} for t in (0,.4,.75,1)],'range':[-extent,extent],'extent':extent,'inspection_steps':steps}
    if kind=='function_trace':
        plot=function_plot(p);lo,hi=p['domain']
        # 通用函数描绘不能套用另一道“唯一正零点/区间最值”题的专用解说。
        steps=[{'at':0,'title':'先看显示范围','explanation':'沿当前函数曲线观察位置和变化方向。'+('阴影标出当前题指定的区间。' if p.get('focus_interval') else '')}]+[{'at':(m['x']-lo)/(hi-lo),'title':m['label'],'explanation':f'当前关键点 x={m["x"]:.6g}，y={m["y"]:.6g}。注意该点在题目中扮演的角色。'} for m in sorted(p.get('markers',[]),key=lambda m:m['x'])]+[{'at':1,'title':'回到题目要求','explanation':'曲线已描绘完整；对照当前题的条件、标记与变化规律。'}]
        if p.get('display'):
            for step,marker in zip(steps[1:-1],p['display']['markers']):step['explanation']=f'关键点 $x={marker["x"]}$，$y={marker["y"]}$。'+step['title']+'。'
        return {'duration':duration,'frames':[{'at':duration*i/80,'values':{'x':sample['x'],'y':sample['y']}} for i,sample in enumerate(plot['samples'])],'range':[lo,hi],'extent':max(abs(v) for v in plot['y_range']),'plot':{**p,**plot},**({'inspection_steps':steps} if p.get('markers') else {})}
    states=[]
    if kind=='absolute_distance':states=[{'value':v,'distance':abs(v)} for v in p['values']]
    elif kind=='square_root':states=[{'area':v,'side':math.sqrt(v)} for v in p['areas']]
    elif kind=='nonnegative_sum':states=[{'a':a,'b':b,'total':float(Fraction(str(a))+Fraction(str(b)))} for a,b in p['pairs']]
    elif kind=='number_line_motion':
        end=float(Fraction(str(p['start']))+Fraction(str(p['delta'])))
        states=[{'value':p['start'],'start':p['start'],'delta':0},{'value':end,'start':p['start'],'delta':p['delta']}]
    elif kind=='travel_motion':
        states=[{'time':t,'a':float(Fraction(str(p['start_a']))+Fraction(str(p['speed_a']))*Fraction(str(t))),'b':float(Fraction(str(p['start_b']))+Fraction(str(p['speed_b']))*Fraction(str(t)))} for t in (0,p['until']/2,p['until'])]
    elif kind=='coordinate_drawing':
        coordinates(p)
        states=[{'visible_segments':i} for i in range(len(p['segments'])+1)]
    elif kind=='fraction_fill':
        if p['numerator']>p['denominator']:raise ContractError('fraction fill numerator exceeds denominator')
        states=[{'filled':i,'denominator':p['denominator']} for i in range(p['numerator']+1)]
    elif kind=='pythagorean':
        a,b=p['a'],p['b'];c=math.hypot(a,b)
        states=[{'a':a,'b':b,'c':c,'a_area':a*a,'b_area':b*b,'c_area':a*a+b*b,'reveal':i} for i in range(4)]
    if any(not math.isfinite(v) for state in states for v in state.values()):raise ContractError('animation values must be finite')
    if len(states)==1:states=[states[0],states[0]]
    frames=[{'at':duration*i/(len(states)-1),'values':s} for i,s in enumerate(states)]
    values=[0]+[v for s in states for key,v in s.items() if key in {'value','start','a','b'}]
    lo,hi=min(values),max(values);padding=max(1,(hi-lo)*.12)
    extra={'geometry':coordinates(p)} if kind=='coordinate_drawing' else {}
    return {'duration':duration,'frames':frames,'range':[lo-padding,hi+padding],'extent':max(1,max(v for s in states for v in s.values())),**extra}
