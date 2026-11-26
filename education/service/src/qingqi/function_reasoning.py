"""Owner-bound function reasoning scenes, with symbolic steps and meaningful comparison."""
from .contracts import obj
from .function_solver import INPUT,analyze_function

PARAMS=obj({**INPUT['properties'],'lesson_mode':{'type':'string','enum':['hint','solution']}},['k','constant','parameter','interval','lesson_mode'])


def specification(arguments,solution=False):
    return {'kind':'animation_scene','template':'function_reasoning','title':'从唯一正零点推到区间最值','basis':'problem',
            'params':{**arguments,'lesson_mode':'solution' if solution else 'hint'},'duration':20,
            'caption':'按本题条件比较可能情形、推导参数，再检查区间内的候选点。' if solution else '先演示原题的约束与推理条件，参数及最终结果留给你完成。'}


def curve(k,c,a,domain,y_range,markers=()):
    lo,hi=domain
    return {'domain':domain,'y_range':y_range,'samples':[{'x':x,'y':k*x**3-a*x*x+c} for x in [lo+(hi-lo)*i/100 for i in range(101)]],
            'markers':list(markers)}


def render(params,duration):
    import sympy as s
    from .math_display import exact
    report=analyze_function(k=params['k'],constant=params['constant'],parameter=params['parameter'],interval=params['interval'])
    k,c=params['k'],params['constant'];a=report['parameter_value'];r=report['positive_root'];p=params['parameter'];lo,hi=params['interval']
    K,C=s.Rational(str(k)),s.Rational(str(c))
    exact_root=s.real_root(2*C/K,3)
    exact_parameter=3*K*exact_root/2
    fmt=exact;mode=params['lesson_mode'];solution=mode=='solution'
    expression=(fmt(K) if K!=1 else '')+'x^{3}-'+p+'x^{2}+'+fmt(C)
    original='f(x)='+expression
    # 提示图以未知r为横轴尺度，不能用数值刻度间接泄露已经求出的r。
    scale=r if solution else 1
    case_domain=[0,2.25*scale];case_range=[-1.3*c,2*c]
    graph_k=k if solution else 2*c
    graph_a=a if solution else 3*c
    exact_scale=exact_root if solution else s.Integer(1)
    exact_graph_a=exact_parameter if solution else 3*C
    def annotate(data,formula='',symbolic=False):
        data.update(formula=formula,axis_labels={'x':'x' if not symbolic else 'x / r','y':'f(x)'},
                    x_ticks=[{'value':scale*i,'label':fmt(exact_scale*i) if not symbolic else ('0' if i==0 else str(i))} for i in range(3)],
                    y_ticks=[{'value':v*c,'label':fmt(s.Rational(str(v))*C)} for v in (-1,0,1,2)])
        if symbolic:data['note']='横轴以尚未求出的正接触点r为尺度（x/r）；展示原题函数族的形状比较，不是已确定参数的函数图。'
        return data
    cases=[]
    # 比例是已知精确4/5、1、6/5；先乘float再转Rational会显示89999…等伪精确长分数。
    for ratio_exact,label,count in [(s.Rational(4,5),'最低点高于横轴',0),(s.Integer(1),'最低点接触横轴',1),(s.Rational(6,5),'最低点低于横轴',2)]:
        ratio=float(ratio_exact)
        x=scale*ratio;y=c*(1-ratio**3)
        if ratio==1:y=0
        cases.append({'label':label,'root_count':count,'minimum':{'x':x,'y':y},
                      'curve':annotate(curve(graph_k,c,float(exact_graph_a*ratio_exact),case_domain,case_range),r'f(x)='+fmt(K*s.Symbol('x')**3-exact_graph_a*ratio_exact*s.Symbol('x')**2+C) if solution else original,not solution)})
        if solution:cases[-1]['curve']['note']='原题函数族的参数试探：只改变参数，保持三次项系数和常数；比较正零点数量。'
        def zero_between(left,right):
            f=lambda z:graph_k*z**3-graph_a*ratio*z*z+c
            before=f(left)
            for _ in range(60):
                middle=(left+right)/2
                if before*f(middle)<=0:right=middle
                else:left=middle;before=f(left)
            return (left+right)/2
        cases[-1]['zeros']=[] if count==0 else [scale] if count==1 else [zero_between(0,x),zero_between(x,case_domain[1])]
    domain=[min(lo,-r/2)-.3*r,max(hi,r)+.3*r]
    # 显示范围围绕题目区间及合法候选值，防止远处三次项把重要零点压成一条直线。
    samples=[v['y'] for v in report['candidates']]+[0,c]
    pad=max(.3*c,(max(samples)-min(samples))*.15)
    full_range=[min(samples)-pad,max(samples)+pad]
    marker_data=[{'x':v['x'],'y':v['y'],'label':f'f({v["x_exact"]})={v["y_exact"]}'} for v in report['candidates']]
    lesson={'version':'problem_reasoning_v1','kind':'function','mode':mode,'problem':original,
            'goal':f'求区间 $[{fmt(s.Rational(str(lo)))},{fmt(s.Rational(str(hi)))}]$ 上的最大值与最小值之和',
            'given':{'k':k,'constant':c,'parameter':p,'interval':[lo,hi]},'cases':cases,
            'root_curve':annotate(curve(graph_k,c,graph_a,[-.9*scale,2.25*scale],case_range),'f(x)='+report['formula'] if solution else original,not solution),
            'positive_stationary':{'x':scale,'y':0}}
    def step(at,title,scene,given,action,rule,formula):
        return {'at':at,'title':title,'scene':scene,'given':given,'action':action,'rule':rule,'formula':formula}
    steps=[step(0,'读清“正零点”与求值区间','read','原题要求正半轴恰好一个零点；求最值只看指定闭区间。','区分零点条件和最值区间。','横轴上的交点是零点；负零点不计入正零点数量。',original),
           step(.14 if solution else .32,'比较三种最低点位置','cases',f'$f(0)={fmt(C)}>0$，正半轴远处会上升。','对照最低点高于、接触、低于横轴时的交点数。','没有正驻点时正侧保持正值；存在正驻点时，最低点接触横轴才只有一个正零点。',r'f(0)>0,\quad f(x)\to+\infty\ (x\to+\infty)'),
           step(.30 if solution else .68,'把“相切”写成两个方程','conditions','唯一正零点在正驻点 $r>0$。','在同一个r处同时使用函数值为零和导数为零。','接触横轴给出f(r)=0；切线水平给出导数为零。',r'\begin{cases}f(r)=0\\f\prime(r)=0\end{cases},\quad r>0')]
    if not solution:
        steps.append(step(1,'接下来求哪个未知量','conditions','r和参数仍未求出。','先由导数条件表示参数，再代回函数值条件。','两条条件必须由同一个正数r满足，不能分别猜解。',r'f\prime(x)='+fmt(3*K)+r'x^2-2'+p+r'x,\quad f\prime(r)=0'))
    else:
        # 提示版不携带未展示的完整区间解答数据，避免额外透露候选值与负根。
        lesson['curve']=curve(k,c,a,domain,full_range,marker_data)
        X=s.Symbol('x')
        tick_values=sorted({s.Rational(str(lo)),s.Rational(str(hi)),s.Integer(0),s.real_root(2*C/K,3),-s.real_root(2*C/K,3)/2},key=float)
        lesson['curve'].update(formula=report['formula'],axis_labels={'x':'x','y':'f(x)'},
             x_ticks=[{'value':float(v),'label':fmt(v)} for v in tick_values if domain[0]<=float(v)<=domain[1]],
             y_ticks=[{'value':v['y'],'label':v['y_exact']} for v in report['candidates']]+[{'value':0,'label':'0'}],
             note='阴影为原题求最值区间；标记显示端点或区间内驻点的精确函数值。负零点不计入正半轴的零点条件。')
        lesson['negative_root']={'x':-r/2,'y':0}
        lesson['elimination']=[
          {'title':'由导数条件表示参数','action':'利用r>0，把导数等式两边除以r，再整理参数。','formula':fmt(3*K)+r'r^2-2'+p+r'r=0\quad\Longrightarrow\quad '+p+'='+fmt(3*K/2)+'r'},
          {'title':'回到函数条件消元','action':'把同一个参数表达式代入f(r)=0，整理立方项。','formula':fmt(K)+r'r^3-('+fmt(3*K/2)+r'r)r^2+'+fmt(C)+r'=0\quad\Longrightarrow\quad r^3='+fmt(2*C/K)},
          {'title':'取正根并回代参数','action':'r必须为正，取正立方根，再回代参数关系。','formula':'r='+report['exact_values']['positive_root']+r'>0,\quad '+p+'='+report['exact_values']['parameter_value']}]
        steps.extend([
          step(.43,'求导与消元，确定参数','solve',r'$r>0$，所以导数条件可以除以r。','由导数条件表示参数，再代入函数条件消元。','在两个等式中代入同一个r与同一个参数。',p+'='+fmt(3*K/2)+r'r\quad\Longrightarrow\quad r^3='+fmt(2*C/K)+r'\quad\Longrightarrow\quad r='+report['exact_values']['positive_root']+r',\ '+p+'='+report['exact_values']['parameter_value']),
          step(.57,'区分负零点与正重根','factor','参数已由两个条件确定。','把原函数因式分解，对照穿轴与接触的位置。','重根处相切，负根只用于理解图形，不计入正半轴条件。',r'f(x)='+report['factorization']),
          step(.70,'用导数符号判断增减','derivative','最值只比较指定区间。','沿区间观察导数为正、为负和为零的位置。','导数为正函数增加，为负函数减少；端点与区间内驻点才是候选。',r'f\prime(x)='+report['derivative']),
          step(.84,'逐个比较合法候选点','extrema','区间外的零点或驻点不参与最值比较。','依次突出端点与区间内驻点并核对精确函数值。','最小值和最大值必须从同一组合法候选中选择。',r'\quad '.join(f'f({v["x_exact"]})={v["y_exact"]}' for v in report['candidates'])),
          step(1,'回到原题所求','result','候选值已完成比较。','把最大值与最小值相加。','这里求最值之和，不是零点的和。',r'\max f+\min f='+report['exact_values']['maximum']+'+('+report['exact_values']['minimum']+')='+report['exact_values']['sum'])])
        derivative=lambda x:3*k*x*x-2*a*x
        ds=[derivative(x) for x in [domain[0]+(domain[1]-domain[0])*i/100 for i in range(101)]]
        dp=max(c,.1*(max(ds)-min(ds)))
        lesson['derivative_curve']={'domain':domain,'y_range':[min(ds)-dp,max(ds)+dp],
          'samples':[{'x':domain[0]+(domain[1]-domain[0])*i/100,'y':y} for i,y in enumerate(ds)],'markers':[],
          'formula':report['derivative'],'axis_labels':{'x':'x','y':'f′(x)'},'x_ticks':lesson['curve']['x_ticks']}
        boundaries=sorted({lo,hi,*[x for x in (0,r) if lo<x<hi]})
        lesson['signs']=[{'from':left,'to':right,'sign':'+' if derivative((left+right)/2)>0 else '-'} for left,right in zip(boundaries,boundaries[1:])]
        lesson['candidates']=[{'x':v['x'],'y':v['y'],'x_label':v['x_exact'],'y_label':v['y_exact'],
                               'role':'端点' if v['x'] in {lo,hi} else '区间内驻点'} for v in report['candidates']]
        lesson['solved']={'parameter':report['exact_values']['parameter_value'],'root':report['exact_values']['positive_root'],
                         'negative_root':report['exact_values']['negative_root'],'minimum':report['exact_values']['minimum'],
                         'maximum':report['exact_values']['maximum'],'sum':report['exact_values']['sum']}
    lesson['steps']=steps
    return {'duration':duration,'range':domain,'extent':max(abs(v) for v in full_range),
            'frames':[{'at':step['at']*duration,'values':{'phase':i}} for i,step in enumerate(steps)],'reasoning_lesson':lesson}
