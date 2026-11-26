"""Pure, bounded teaching-figure geometry and numeric compilers."""
import math
from .contracts import ContractError,obj

LABEL={'type':'string','minLength':1,'maxLength':160}
NUM={'type':'number','minimum':-10000,'maximum':10000}
INDEX={'type':'integer','minimum':0,'maximum':7}
POINT=obj({'label':LABEL,'x':NUM,'y':NUM})
SEGMENT=obj({'source':INDEX,'target':INDEX,'style':{'type':'string','enum':['solid','dashed']},'role':{'type':'string','enum':['edge','diagonal','auxiliary','connection']},'label':LABEL},['source','target'])
POLYGON=obj({'vertices':{'type':'array','items':INDEX,'minItems':3,'maxItems':8}})
CIRCLE=obj({'center':INDEX,'radius':{'type':'number','exclusiveMinimum':0,'minimum':0.01,'maximum':100}})
COORD_FIELDS={'segments':{'type':'array','items':SEGMENT,'maxItems':16},'polygons':{'type':'array','items':POLYGON,'maxItems':4},'circles':{'type':'array','items':CIRCLE,'maxItems':4}}
COMMON={'title':LABEL,'basis':{'type':'string','enum':['problem','example']},'caption':{'type':'string','maxLength':240}}
INTERVAL={'type':'array','items':{'type':'number','minimum':-20,'maximum':20},'minItems':2,'maxItems':2}
DISPLAY=obj({'formula':{'type':'string','maxLength':400},'domain':{'type':'array','items':LABEL,'minItems':2,'maxItems':2},'markers':{'type':'array','items':obj({'x':LABEL,'y':LABEL}),'maxItems':8}})
FUNCTION=obj({**COMMON,'kind':{'type':'string','enum':['function_plot']},'function':{'type':'string','enum':['linear','quadratic','cubic','square_root','absolute']},'a':NUM,'b':NUM,'c':NUM,'d':NUM,'domain':INTERVAL,'focus_interval':INTERVAL,'markers':{'type':'array','items':POINT,'maxItems':8}},['kind','title','basis','function','a','b','domain'])
FUNCTION['properties']['display']=DISPLAY
FUNCTION['properties']['axis_labels']=obj({'x':LABEL,'y':LABEL})
AREA=obj({**COMMON,'kind':{'type':'string','enum':['area_model']},'numerator':{'type':'integer','minimum':0,'maximum':24},'denominator':{'type':'integer','minimum':1,'maximum':24},'shape':{'type':'string','enum':['rectangle','circle']}},['kind','title','basis','numerator','denominator','shape'])


def coordinates(spec):
    points=[]
    for point in spec['points']:
        # 模型常将坐标写进label；界面还会附坐标，因此规范化为单个点名。
        import re
        suffix=re.search(r'\s*[（(]\s*([+-]?\d+(?:\.\d+)?)\s*[,，]\s*([+-]?\d+(?:\.\d+)?)\s*[)）]\s*$',point['label'])
        if suffix and (float(suffix[1]),float(suffix[2]))!=(point['x'],point['y']):raise ContractError('point label coordinates disagree with its actual position')
        label=point['label'][:suffix.start()].strip() if suffix else point['label']
        label=label or '点'
        points.append({**point,'label':label})
    count=len(points);segments=[];pairs=set()
    for segment in spec.get('segments',[]):
        a,b=segment['source'],segment['target']
        if a>=count or b>=count or a==b:raise ContractError('segment must join two different existing points')
        pair=tuple(sorted((a,b)))
        if pair in pairs:raise ContractError('duplicate segment')
        pairs.add(pair)
        length=math.hypot(points[a]['x']-points[b]['x'],points[a]['y']-points[b]['y'])
        if length<1e-9:raise ContractError('segment endpoints overlap')
        segments.append({**segment,'style':segment.get('style','solid'),'role':segment.get('role','edge'),'length':length})
    for polygon in spec.get('polygons',[]):
        vertices=polygon['vertices']
        if len(set(vertices))!=len(vertices) or any(i>=count for i in vertices):raise ContractError('polygon must use distinct existing points')
        area=abs(sum(points[a]['x']*points[b]['y']-points[b]['x']*points[a]['y'] for a,b in zip(vertices,vertices[1:]+vertices[:1])))/2
        if area<1e-9:raise ContractError('polygon must have positive area')
    for circle in spec.get('circles',[]):
        if circle['center']>=count:raise ContractError('circle center must be an existing point')
    extent=max(2,max(abs(p[k]) for p in points for k in ('x','y'))+1)
    for circle in spec.get('circles',[]):
        p=points[circle['center']];extent=max(extent,abs(p['x'])+circle['radius']+1,abs(p['y'])+circle['radius']+1)
    return {'points':points,'segments':segments,'polygons':spec.get('polygons',[]),'circles':spec.get('circles',[]),'extent':extent}


def function_plot(spec):
    lo,hi=spec['domain']
    if lo>=hi:raise ContractError('function domain must be increasing')
    a,b,c,d=spec['a'],spec['b'],spec.get('c',0),spec.get('d',0)
    if spec['function'] in {'quadratic','cubic'} and a==0:raise ContractError('polynomial leading coefficient must be nonzero')
    if spec['function']=='linear' and c:raise ContractError('linear function uses only a and b')
    if spec['function']!='cubic' and d:raise ContractError('only cubic functions use d')
    if spec['function'] in {'square_root','absolute'} and (not a or c):raise ContractError('outer function requires a nonzero affine coefficient and only a,b')
    if spec['function']=='square_root' and min(a*lo+b,a*hi+b)<-1e-10:raise ContractError('square root plotting domain must keep the radicand nonnegative')
    value=lambda x:math.sqrt(max(0,a*x+b)) if spec['function']=='square_root' else abs(a*x+b) if spec['function']=='absolute' else a*x+b if spec['function']=='linear' else a*x*x+b*x+c if spec['function']=='quadratic' else ((a*x+b)*x+c)*x+d
    if spec.get('focus_interval') and not lo<=spec['focus_interval'][0]<spec['focus_interval'][1]<=hi:raise ContractError('focus interval must be inside plotting domain')
    for marker in spec.get('markers',[]):
        if not lo<=marker['x']<=hi or not math.isclose(marker['y'],value(marker['x']),abs_tol=1e-8,rel_tol=1e-9):raise ContractError('function marker must lie on the actual curve')
    samples=[]
    for i in range(81):
        x=lo+(hi-lo)*i/80
        y=value(x)
        if not math.isfinite(y) or abs(y)>10000:raise ContractError('function values exceed bounded plotting range')
        samples.append({'x':x,'y':y})
    ymin,ymax=min(0,min(p['y'] for p in samples)),max(0,max(p['y'] for p in samples))
    padding=max(1,(ymax-ymin)*.12)
    return {'samples':samples,'y_range':[ymin-padding,ymax+padding],'c':c,'d':d}


def area_model(spec):
    if spec['numerator']>spec['denominator']:raise ContractError('fraction area numerator exceeds denominator')
    return {'ratio':spec['numerator']/spec['denominator']}
