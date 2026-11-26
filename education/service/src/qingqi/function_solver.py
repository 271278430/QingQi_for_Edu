"""Read-only, bounded analysis of an explicitly stated positive-double-root cubic."""
import math
import re
from .contracts import obj, ContractError
from .domain_tools import ToolSpec

NUM={'type':'number','minimum':-100,'maximum':100}
INPUT=obj({'k':{'type':'number','exclusiveMinimum':0,'maximum':20},'constant':{'type':'number','exclusiveMinimum':0,'maximum':100},'parameter':{'type':'string','enum':['a','b','p']},'interval':{'type':'array','items':NUM,'minItems':2,'maxItems':2}})
OUTPUT=obj({'parameter_value':{'type':'number'},'positive_root':{'type':'number'},'negative_root':{'type':'number'},'minimum':{'type':'number'},'maximum':{'type':'number'},'sum':{'type':'number'},'formula':{'type':'string'},'factorization':{'type':'string'},'derivative':{'type':'string'},'candidates':{'type':'array','items':{'type':'object'}},'approved_solution_visuals':{'type':'array','items':{'type':'object'}},'approved_hint_visuals':{'type':'array','items':{'type':'object'}},'verified':{'type':'boolean'}})
OUTPUT['properties']['exact_values']={'type':'object'}
OUTPUT['properties']['approved_problem_hint_visuals']={'type':'array','items':{'type':'object'}}
OUTPUT['properties']['approved_problem_solution_visuals']={'type':'array','items':{'type':'object'}}
TOOL=ToolSpec('analyze_function','Analyze owned kx^3-px^2+c (k,c>0), exactly one positive zero and closed-interval extrema. Read-only SymPy facts and approved visuals; no grading.',INPUT,OUTPUT)

def identify(source):
    q=source.replace('−','-').replace('³','^3').replace('²','^2').replace('（','(').replace('）',')').replace('，',',').replace('［','[').replace('］',']')
    q=re.sub(r'\\(?:left|right)', '',q);q=re.sub(r'\^\{([23])\}',r'^\1',q);q=re.sub(r'\s+','',q)
    if not re.search(r'(?:有且仅有|恰有|只有|仅有)一个零点',q) or not re.search(r'\(0,(?:∞|\\infty|\+∞)\)',q):return None
    n=r'\d+(?:\.\d+)?';matches=list(re.finditer(r'f\(x\)=('+n+r')?\*?x\^3-([abp])\*?x\^2\+('+n+r')(?![\d.x+*/^−-])',q));m=matches[0] if len(matches)==1 else None
    intervals=re.findall(r'\[([+-]?'+n+r'),([+-]?'+n+r')\]',q)
    if not m or len(intervals)!=1:return None
    k=float(m[1] or 1);c=float(m[3]);lo,hi=map(float,intervals[0])
    if not 0<k<=20 or not 0<c<=100 or not -10<=lo<hi<=10:return None
    if (2*c/k)**(1/3)>8:return None
    return {'arguments':{'k':k,'constant':c,'parameter':m[2],'interval':[lo,hi]}}

def _visuals(k,c,parameter,interval,basis):
    import sympy as s
    from .math_display import exact
    k=s.Rational(str(k));c=s.Rational(str(c));r=s.real_root(2*c/k,3);p=3*k*r/2;left,right=map(lambda n:s.Rational(str(n)),interval)
    lo=min(left,-r/2)-s.Rational(3,10);hi=max(right,r)+s.Rational(3,10)
    if not -20<=lo<hi<=20:raise ContractError('function inspection domain exceeds supported range')
    f=lambda x:k*x**3-p*x*x+c
    marker_x=sorted({left,right,-r/2,0,r})
    def label(x):
        roles=[]
        if x==left:roles.append('区间左端点：参与最值比较')
        if x==right:roles.append('区间右端点：参与最值比较')
        if x==-r/2:roles.append('负零点：不计入正零点条件')
        if x==0:roles.append('驻点 x=0：导数变号')
        if x==r:roles.append('唯一正零点：相切不穿轴')
        if not left<=x<=right:roles.append('不在求最值区间')
        return '；'.join(roles)
    markers=[{'x':float(x),'y':float(s.simplify(f(x))),'label':label(x)} for x in marker_x]
    caption=('当前原题，参数 $'+parameter+' = '+exact(p)+'$。' if basis=='problem' else '不同参数的相似例子，不是原题答案。')+'阴影为求最值区间；负零点不计入正零点条件，区间外值不参与最值比较。'
    X=s.Symbol('x');domain=[float(lo),float(hi)]
    display={'formula':exact(f(X)),'domain':[exact(lo),exact(hi)],'markers':[{'x':exact(x),'y':exact(f(x))} for x in marker_x]}
    curve={'function':'cubic','a':float(k),'b':float(-p),'c':0,'d':float(c),'domain':domain,'focus_interval':interval,'markers':markers,'display':display}
    derivative={'function':'quadratic','a':float(3*k),'b':float(-2*p),'c':0,'domain':domain,'focus_interval':interval,'markers':[{'x':float(x),'y':0,'label':'导数为零：检查左右变号'} for x in (0,r)],'display':{'formula':exact(3*k*X**2-2*p*X),'domain':display['domain'],'markers':[{'x':exact(x),'y':'0'} for x in (0,r)]}}
    return [{'kind':'animation_scene','basis':basis,'title':('原题函数：零点与区间最值' if basis=='problem' else '相似例子：观察相切与最值'),'caption':caption,'template':'function_trace','params':curve,'duration':12},
            {'kind':'animation_scene','basis':basis,'title':'导函数：变号决定增减','caption':('原题导函数。' if basis=='problem' else '相似例子的导函数。')+'导数为零只是候选；最值还需比较区间端点。','template':'function_trace','params':derivative,'duration':12}]


def static_visuals(visuals):
    """Static projection of the same approved symbolic curves; no new parameters."""
    return [{'kind':'function_plot','basis':v['basis'],'title':v['title'],'caption':v['caption'],**v['params']} for v in visuals]


def hint_visuals(k,c,parameter,interval):
    """An explicitly unresolved trial of the ORIGINAL family, not a different exercise."""
    import sympy as s
    from .math_display import exact
    X=s.Symbol('x');K,C=s.Rational(str(k)),s.Rational(str(c))
    lo,hi=min(interval[0],0)-.2,max(interval[1],1)+.2
    return [{'kind':'animation_scene','basis':'problem','template':'function_trace','duration':12,
             'title':'原题函数族：先观察参数未定的情况',
             'caption':f'保持原题系数和求最值区间，仅取 {parameter}=0 作试探；这时正半轴没有零点，不是满足条件的解。改变参数后，最低点与横轴的位置决定正零点数量。',
             'params':{'function':'cubic','a':k,'b':0,'c':0,'d':c,'domain':[lo,hi],'focus_interval':interval,
                       'markers':[{'x':0,'y':c,'label':'原题给定 f(0)>0'}],
                       'display':{'formula':exact(K*X**3+C),'domain':[exact(s.Rational(str(lo))),exact(s.Rational(str(hi)))],
                                  'markers':[{'x':'0','y':exact(C)}]}}}]

def analyze_function(*,k,constant,parameter,interval):
    import sympy as s
    K,C=s.Rational(str(k)),s.Rational(str(constant));x=s.Symbol('x',real=True)
    r=s.real_root(2*C/K,3);p=3*K*r/2;f=K*x**3-p*x*x+C;factor=K*(x-r)**2*(x+r/2);derivative=s.diff(f,x)
    if s.simplify(f-factor)!=0 or s.simplify(f.subs(x,r))!=0 or s.simplify(derivative.subs(x,r))!=0 or not bool(r>0):raise ContractError('positive double root could not be verified')
    left,right=(s.Rational(str(v)) for v in interval)
    if left>=right:raise ContractError('closed interval must be increasing')
    candidates=sorted({left,right,*[v for v in (s.Integer(0),r) if left<=v<=right]},key=float)
    exact_values=[s.simplify(f.subs(x,v)) for v in candidates];low=min(exact_values);high=max(exact_values)
    values=[float(v) for v in exact_values];minimum=float(low);maximum=float(high)
    if not all(math.isfinite(v) for v in values):raise ContractError('extrema must be finite')
    from .math_display import exact
    from .function_reasoning import specification as reasoning_specification
    arguments={'k':k,'constant':constant,'parameter':parameter,'interval':interval}
    return {'parameter_value':float(p),'positive_root':float(r),'negative_root':float(-r/2),'minimum':minimum,'maximum':maximum,'sum':float(low+high),'formula':exact(f),'factorization':exact(factor),'derivative':exact(derivative),'candidates':[{'x':float(v),'y':float(f.subs(x,v)),'x_exact':exact(v),'y_exact':exact(f.subs(x,v))} for v in candidates],'exact_values':{'parameter_value':exact(p),'positive_root':exact(r),'negative_root':exact(-r/2),'minimum':exact(low),'maximum':exact(high),'sum':exact(low+high)},
            'approved_solution_visuals':_visuals(float(K),float(C),parameter,interval,'problem'),'approved_hint_visuals':hint_visuals(float(K),float(C),parameter,interval),
            'approved_problem_hint_visuals':[reasoning_specification(arguments)],'approved_problem_solution_visuals':[reasoning_specification(arguments,True)],'verified':True}

class FunctionTutorController:
    name='grounded_symbolic_function_v1';uses_model=False;deployment_signature='positive_double_root_cubic_reasoning_v2'
    def next(self,request,state,context,registry):
        from .planning import find,reply
        report=find(state,'analyze_function')
        if report is None:return {'kind':'call','tool':'analyze_function','arguments':state['function_task']['arguments']}
        q=state['function_question'];allowed=state['route']['teaching']['allow_final_answer']
        from .visual_tasks import refuses_drawing
        # 函数题本身已提供绘图依据；不能把是否画图完全交给关键词，更不能改成另一道题。
        drawing=state['teaching_plan']['visual']['delivery']!='text'
        animated=not state['teaching_plan']['visual']['forbid_animation']
        story=(state.get('presentation') or {}).get('kind')=='story'
        if drawing and not find(state,'render_teaching_visual'):
            approved=report['approved_solution_visuals' if allowed else 'approved_hint_visuals']
            if animated:approved=report['approved_problem_solution_visuals' if allowed else 'approved_problem_hint_visuals']
            # 否定策略与执行使用同一plan；“不用动画”可给静态图，不能反复制造冲突动作。
            return {'kind':'call','tool':'render_teaching_visual','arguments':{'visuals':approved if animated else static_visuals(approved)}}
        narrative='情景教学：把函数曲线想象成小车的高度路线，横轴代表地面。原题 $f(0)>0$，正半轴远处又会上升；要只有一个正零点，路线必须刚好碰到地面后抬起，也就是在正驻点与横轴相切。因此接触点同时满足 $f(r)=0$ 和 $f\\prime(r)=0$。区间最值再比较题目区间内的端点和驻点。\n\n' if story else ''
        if not allowed:
            figure='先看这道题的函数图：正半轴最低点高于、接触、低于横轴，分别对应0、1、2个正零点。这里只比较条件，横轴用尚未知的正驻点r作尺度；参数与最后所求先保留。'
            return reply(narrative+(figure if drawing else '原题在零点右侧最终上升，且 f(0)>0；正半轴若只有一个零点，极小值必须恰好等于零。先求导数，找到正驻点。')+('你能把这个驻点代回函数写出方程吗？' if not state['route']['teaching'].get('no_questions') else '原题参数与最终结果留给你完成。'),'ask' if not state['route']['teaching'].get('no_questions') else 'explain')
        from .math_display import exact
        import sympy as s
        def fmt(n):return exact(s.Rational(str(n)))
        def value(key):return report['exact_values'][key]
        param=state['function_task']['arguments']['parameter'];lo,hi=state['function_task']['arguments']['interval']
        if drawing:
            label='动画' if animated else '静态图'
            ending='逐步查看时，图形和公式会同步突出当前依据。' if animated else '静态图分别展示原函数与导数，最值只比较题目区间内的候选点。'
            return reply(narrative+f'原题曲线在正零点 $r={value("positive_root")}$ 处与横轴相切，所以同时满足 $f(r)=0$ 与 $f\\prime(r)=0$，得到 ${param}={value("parameter_value")}$。阴影是求最值区间，比较端点与区间内驻点：最小值 ${value("minimum")}$，最大值 ${value("maximum")}$，和为 ${value("sum")}$。'+ending,'explain')
        comparisons='，'.join(f'$f({v["x_exact"]})={v["y_exact"]}$' for v in report['candidates'])
        return reply(narrative+f'正半轴唯一零点必须是极小值处的重根：若极小值小于零会有两次穿轴，大于零则无零点。联立 $f(r)=0$ 与 $f\\prime(r)=0$，得到 ${param}={value("parameter_value")}$、$r={value("positive_root")}$。\n\n代入后 $$f(x)={report["formula"]}={report["factorization"]}.$$ 负根 ${value("negative_root")}$ 不在正半轴。\n\n在 $[{fmt(lo)},{fmt(hi)}]$ 中比较端点和驻点：{comparisons}。因此最小值 ${value("minimum")}$，最大值 ${value("maximum")}$，两者之和 $\\boxed{{{value("sum")}}}$。','give_answer')
