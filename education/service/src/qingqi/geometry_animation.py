"""Pure coordinates for continuous, constraint-preserving geometry animation."""
import math
from .contracts import obj,ContractError
from .geometry_solver import LABELS

SIDE={'type':'number','minimum':.01,'maximum':1000}
POSITION={'type':'number','minimum':.000000001,'maximum':1000}
MODE={'type':'string','enum':['hint','solution']}
TEACHING_MODE={'type':'string','enum':['socratic','heuristic','explain','answer']}
VARIABLE={'type':'string','pattern':'^[a-z]$'}
EXACT={'type':'string','maxLength':48,'pattern':'^[0-9]+(?:/[0-9]+)?$'}
GOAL={'type':'string','enum':['ratio','function']}
PARAMS={'triangle_rotation':obj({'side':SIDE,'labels':LABELS,'ae':POSITION,'lesson_mode':MODE,'teaching_mode':TEACHING_MODE,'side_exact':EXACT},['side','labels','ae']),
        'geometry_motion':obj({'side':SIDE,'labels':LABELS,'ratio':{'type':'number','minimum':.00001,'maximum':10000},'from_x':POSITION,'to_x':POSITION,'lesson_mode':MODE,'teaching_mode':TEACHING_MODE,'lesson_goal':GOAL,'parameter':VARIABLE,'x_variable':VARIABLE,'y_variable':VARIABLE,'side_exact':EXACT,'ratio_exact':EXACT},['side','labels','ratio','from_x','to_x'])}

def label_coordinates(points):
    from fractions import Fraction
    def label(value):
        if value==0:return '0'
        coefficient=Fraction(value/math.sqrt(2)).limit_denominator(100000)
        if not math.isclose(float(coefficient)*math.sqrt(2),value,rel_tol=1e-12,abs_tol=1e-12):return None
        sign='-' if coefficient<0 else '';n=abs(coefficient.numerator);d=coefficient.denominator
        top=('' if n==1 else str(n))+r'\sqrt{2}'
        return sign+(top if d==1 else r'\frac{'+top+'}{'+str(d)+'}')
    # 仅固定几何族的45度坐标变换使用该标签；一般曲线采样仍是近似测量。
    return [{**p,**{key+'_tex':text for key in ('x','y') if (text:=label(p[key])) is not None}} for p in points]

def scene_at(template,p,progress):
    a=p['side'];names=p['labels'];r=1 if template=='triangle_rotation' else p['ratio']
    x=p['ae'] if template=='triangle_rotation' else p['from_x']+(p['to_x']-p['from_x'])*progress
    limit=min(a,2*a*r/(1+r))
    if not 0<x<a or x>limit+1e-9:raise ContractError('moving point is outside the edge or intersection outside the specified ray')
    t=a-x;dx=a/(1+r);dy=a*r/(1+r);f=(dx*dx+dy*dy-dx*t)/dy
    canonical=[(a,0),(0,a),(0,0),(dx,dy),(t,0),(0,f)]
    def display(point):
        u,v=point
        return ((a-u+v)/math.sqrt(2),(a-u-v)/math.sqrt(2))
    points=[{'label':names[key],'x':display(point)[0],'y':display(point)[1]} for key,point in zip(('a','b','c','d','e','f'),canonical)]
    de=math.hypot(t-dx,dy);df=math.hypot(dx,f-dy)
    if abs((t-dx)*(-dx)+(-dy)*(f-dy))>1e-6*max(1,a*a):raise ContractError('generated geometry violates perpendicular constraint')
    if template=='triangle_rotation':
        angle=-math.pi/2*progress
        for index in (0,4,2):
            u,v=canonical[index];du,dv=u-dx,v-dy
            q=(dx+du*math.cos(angle)-dv*math.sin(angle),dy+du*math.sin(angle)+dv*math.cos(angle))
            points.append({'label':points[index]['label']+'′','x':display(q)[0],'y':display(q)[1]})
    segments=[{'source':u,'target':v,'role':role,'style':style} for u,v,role,style in ((0,1,'edge','solid'),(1,2,'edge','solid'),(2,0,'edge','solid'),(3,4,'connection','solid'),(3,5,'connection','solid'),(2,3,'auxiliary','dashed'))]
    for line,label in zip(segments[3:6],('de','df','cd')):line['label']=names[label[0]]+names[label[1]]
    if progress==0:points=label_coordinates(points)
    return {'points':points,'segments':segments,'x':x,'y':a-f,'de':de,'df':df,'ratio':de/df,'angle':-90*progress if template=='triangle_rotation' else 90}

def render(template,p,duration):
    from fractions import Fraction
    for key in ('side','ratio'):
        if p.get(key+'_exact'):
            try:value=Fraction(p[key+'_exact'])
            except (ValueError,ZeroDivisionError) as error:raise ContractError('invalid exact geometry parameter') from error
            if value<=0 or not math.isclose(float(value),p[key],rel_tol=1e-12,abs_tol=1e-12):raise ContractError('exact geometry value must match its approved numeric parameter')
    from .geometry_lessons import build,motion_progress
    lesson=build(template,p)
    scenes=[scene_at(template,p,motion_progress(lesson,i/80)) for i in range(81)]
    extent=max(2,max(abs(point[k]) for scene in scenes for point in scene['points'] for k in ('x','y'))+1)
    points=[point for scene in scenes for point in scene['points']]
    b,c=(scenes[0]['points'][i] for i in (1,2));length=math.hypot(c['x']-b['x'],c['y']-b['y']);ux=(c['x']-b['x'])/length;uy=(c['y']-b['y'])/length
    beyond=max(0,max((scene['points'][5]['x']-c['x'])*ux+(scene['points'][5]['y']-c['y'])*uy for scene in scenes))+.18*p['side']
    ray={'x':c['x']+beyond*ux,'y':c['y']+beyond*uy};points.append(ray)
    bounds={key:fn(point[axis] for point in points) for key,axis,fn in (('xmin','x',min),('xmax','x',max),('ymin','y',min),('ymax','y',max))}
    helpers=[]
    if lesson.get('helper_labels'):
        aa=p['side'];rr=p['ratio'];ddx=aa/(1+rr);ddy=aa*rr/(1+rr)
        helpers=[{'label':lesson['helper_labels'][key],'x':(aa-u+v)/math.sqrt(2),'y':(aa-u-v)/math.sqrt(2)} for key,u,v in (('h',ddx,0),('k',0,ddy))]
    result={'frames':[{'at':duration*i/80,'values':{key:scene[key] for key in ('x','y','de','df','ratio','angle')}} for i,scene in enumerate(scenes)],'duration':duration,'extent':extent,'range':[0,extent],'geometry':{'points':scenes[0]['points'],'segments':scenes[0]['segments'],'extent':extent,'bounds':bounds,'ray_end':ray,'helpers':helpers},'lesson':lesson}
    if template=='geometry_motion':result['title']='相似与长度比' if lesson.get('goal')=='ratio' else '从相似到函数：长度关系与范围'
    if lesson.get('coefficients'):
        plot={'function':'linear',**lesson['coefficients'],'c':0,'domain':[0,lesson['domain']['upper']]}
        # 几何中很小的正比例会产生大斜率但很小的x范围；不能被通用函数输入界限误拒绝。
        samples=[{'x':plot['domain'][1]*i/80,'y':plot['b']+plot['a']*plot['domain'][1]*i/80} for i in range(81)]
        ys=[v['y'] for v in samples];padding=max(1e-9,(max(ys)-min(ys))*.12,max(abs(v) for v in ys)*.06)
        result['plot']={**plot,'samples':samples,'y_range':[min(ys)-padding,max(ys)+padding]}
    return result
