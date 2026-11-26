"""Exact symbolic geometry for declared construction families, not model prose."""
from fractions import Fraction
from functools import lru_cache
from .contracts import obj,ContractError,ToolSpec,validate
from .geometry_lessons import helper_labels

LABEL={'type':'string','minLength':1,'maxLength':1}
LABELS=obj({key:LABEL for key in ('a','b','c','d','e','f')})
INPUT=obj({'construction':{'type':'string','enum':['right_isosceles_perpendicular']},'labels':LABELS,'scale':{'type':'string','maxLength':24},'ratio':{'type':'string','maxLength':24},'parameter':LABEL,'x_variable':LABEL,'y_variable':LABEL,'parts':{'type':'array','items':{'type':'string','enum':['midpoint','ratio','function']},'minItems':1,'maxItems':3}})
OUTPUT=obj({'status':{'type':'string','enum':['verified']},'labels':LABELS,'scale':{'type':'string'},'parameter':LABEL,'x_variable':LABEL,'y_variable':LABEL,'parts':{'type':'array','items':{'type':'string'}},'proof_checks':{'type':'object'},'midpoint':{'type':'object'},'ratio_proof':{'type':'object'},'elementary_proof':{'type':'object'},'function':{'type':'object'},'approved_visuals':{'type':'array','items':{'type':'object'},'maxItems':6}})
TOOL=ToolSpec('solve_geometry','Symbolically solve the owner-bound right-isosceles perpendicular-intersection construction. Computes and verifies identities, variable domain and approved animation parameters. No arbitrary expressions or code.',INPUT,OUTPUT,timeout=12,version='geometry_symbolic_v2')

@lru_cache(maxsize=1)
def prepare_geometry():
    # 冷启动的符号依赖和通用恒等式不属于某道题的12秒执行预算；只缓存不可变的符号族。
    import sympy as s
    a,r,t=s.symbols('a r t',positive=True);f,x=s.symbols('f x',real=True)
    d=s.Matrix([a/(1+r),a*r/(1+r)]);A=s.Matrix([a,0]);B=s.Matrix([0,a]);C=s.zeros(2,1);E=s.Matrix([t,0]);F=s.Matrix([0,f])
    vertical=s.solve((E-d).dot(F-d),f)[0]
    de2=s.expand((E-d).dot(E-d));df2=s.simplify((F-d).dot(F-d).subs(f,vertical))
    relation=s.simplify(de2-r*r*df2)==0
    function=s.factor((a-vertical).subs(t,a-x))
    midpoint_d=d.subs(r,1);turn=s.Matrix([[0,1],[-1,0]])
    def rotated(p):return midpoint_d+turn*(p-midpoint_d)
    matches=[all(s.simplify(v)==0 for v in rotated(p)-q) for p,q in ((A,C),(C,B),(E,F.subs(f,vertical.subs(r,1))))]
    right=s.simplify((A-midpoint_d).dot(C-midpoint_d))==0
    checks={'perpendicular_intersection':s.simplify((E-d).dot(F-d).subs(f,vertical))==0,'distance_ratio_identity':relation,'rotation_maps_a_to_c':matches[0],'rotation_maps_c_to_b':matches[1],'rotation_maps_e_to_f':matches[2],'midpoint_right_angle':right}
    checks['foot_lengths_match_division_ratio']=s.simplify((A-d).dot(A-d)/(B-d).dot(B-d)-(d[1]/d[0])**2)==0
    checks['right_triangle_leg_similarity']=s.simplify((t-d[0])**2*d[0]**2-(vertical-d[1])**2*d[1]**2)==0
    if not all(checks.values()):raise ContractError('symbolic geometry verification failed')
    return s,a,r,t,f,x,d,A,B,C,E,F,vertical,de2,function,tuple(checks.items())

def solve_geometry(**arguments):
    validate(arguments,INPUT)
    labels=arguments['labels'];parts=arguments['parts']
    if len(set(labels.values()))!=6 or any(not v.isascii() or not v.isupper() for v in labels.values()):raise ContractError('geometry labels must be six distinct capital letters')
    for key in ('parameter','x_variable','y_variable'):
        if not arguments[key].isascii() or not arguments[key].islower():raise ContractError('geometry variable must be a single lower-case letter')
    try:
        ratio=Fraction(arguments['ratio']);scale=Fraction(arguments['scale']) if arguments['scale']!='a' else None
    except (ValueError,ZeroDivisionError) as error:raise ContractError('invalid positive geometry parameters') from error
    if not Fraction(1,100000)<=ratio<=10000 or scale is not None and not Fraction(1,100)<=scale<=1000:raise ContractError('geometry parameter outside supported range')
    s,a,r,t,f,x,d,A,B,C,E,F,vertical,de2,function,check_items=prepare_geometry()
    checks=dict(check_items)
    aa=s.Rational(scale.numerator,scale.denominator) if scale else a;rr=s.Rational(ratio.numerator,ratio.denominator)
    fixed=s.expand(function.subs({a:aa,r:rr}))
    upper=s.simplify(2*aa*rr/(1+rr)) if ratio<1 else aa
    slope=s.simplify(s.diff(fixed,x));intercept=s.simplify(fixed.subs(x,0))
    y=s.symbols('y',real=True)
    dot=s.factor((E-d).dot(F-d).subs({t:a-x,f:a-y}).subs({a:aa,r:rr}))
    midpoint_angles={labels['e']+labels['c']+labels['d']:45,labels['a']+labels['d']+labels['c']:90,labels['d']+labels['a']+labels['e']:45,labels['d']+labels['c']+labels['f']:45}
    report={'status':'verified','labels':labels,'scale':str(aa),'parameter':arguments['parameter'],'x_variable':arguments['x_variable'],'y_variable':arguments['y_variable'],'parts':parts,'proof_checks':checks,
            'midpoint':{'angles':midpoint_angles,'rotation_degrees':-90},
            'elementary_proof':{'helpers':helper_labels(labels),'dh':s.latex(d[1]),'dk':s.latex(d[0])},
            'ratio_proof':{'d_x':s.latex(d[0]),'d_y':s.latex(d[1]),'f':s.latex(vertical),'de_squared':s.latex(s.factor(de2)),'identity':'DE^2 = r^2 DF^2'},
            'function':{'expression':s.latex(fixed),'slope':str(slope),'intercept':str(intercept),'upper':str(upper),'upper_closed':ratio<1,'side':str(aa),'ratio':str(rr),'d_x':s.latex(d[0].subs({a:aa,r:rr})),'d_y':s.latex(d[1].subs({a:aa,r:rr})),'perpendicular_equation':s.latex(dot)},'approved_visuals':[]}
    numerical_side=float(scale or 4);bound=float(upper) if scale else float(2*4*ratio/(1+ratio) if ratio<1 else 4)
    base={'kind':'animation_scene','duration':18}
    if 'midpoint' in parts:
        report['approved_visuals'].append({**base,'template':'triangle_rotation','title':'第（1）问：旋转证明的五个步骤','basis':'example','caption':'中点情形；两直角边均以'+str(numerical_side)+'作示意，E取一个合法位置。旋转保持长度，测量示例不代替证明。','params':{'side':numerical_side,'side_exact':str(scale or 4),'labels':labels,'ae':numerical_side*.4}})
    report['approved_visuals'].append({**base,'template':'geometry_motion','title':'动点关系：列式、轨迹与取值范围','basis':'problem' if 'function' in parts else 'example','caption':('本图取边长'+str(numerical_side)+'、比例'+str(ratio)+'作示例。' if 'function' not in parts else '')+'E在边内部，F在指定射线上，允许越过C。函数由垂直条件推导，动画用于观察。','params':{'side':numerical_side,'side_exact':str(scale or 4),'ratio':float(ratio),'ratio_exact':str(ratio),'parameter':arguments['parameter'],'labels':labels,'from_x':bound*.06,'to_x':bound if ratio<1 else bound*.94,'x_variable':arguments['x_variable'],'y_variable':arguments['y_variable']}})
    from .geometry_animation import scene_at
    from itertools import combinations
    scene=scene_at('geometry_motion',{'side':numerical_side,'ratio':float(ratio),'labels':labels,'from_x':bound/2,'to_x':bound/2},0)
    static={'kind':'coordinates','title':'原题构造示意','basis':'example','caption':'动点取定义域中的一个合法示例位置；位置不是题干新增条件。','points':[{k:v for k,v in p.items() if k in {'label','x','y'}} for p in scene['points']],'segments':scene['segments'],'polygons':[{'vertices':[0,1,2]}]}
    report['approved_visuals'].append(static)
    report['approved_visuals'].append({**static,'title':'连接示意图中的全部点','segments':[{'source':a,'target':b,'style':'solid','role':'connection'} for a,b in combinations(range(6),2)]})
    if 'midpoint' in parts:
        # 第（1）问的D必须是中点，不能拿第（3）问r=1/2的构造充当第一问示意图。
        midpoint=scene_at('triangle_rotation',{'side':numerical_side,'labels':labels,'ae':numerical_side*.4},0)
        figure={**static,'title':'第（1）问：中点构造示意','caption':'D是斜边中点，连接CD观察中线与直角。边长和动点位置只作示意，不是第一问新增的数值条件。','points':[{k:v for k,v in p.items() if k in {'label','x','y'}} for p in midpoint['points'][:6]],'segments':midpoint['segments']}
        report['approved_visuals'] += [figure,{**figure,'title':'第（1）问：连接中点构造中的所有点','segments':report['approved_visuals'][-1]['segments']}]
    return report
