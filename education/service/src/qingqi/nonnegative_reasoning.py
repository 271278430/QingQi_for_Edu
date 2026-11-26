"""Exact expression-bound contradiction, equation operations and substitution scenes."""
import re
from fractions import Fraction
from .contracts import obj,ContractError
from .nonnegative_teaching import identify
from .practice_tutoring import linear

PARAMS=obj({'equation':{'type':'string','minLength':1,'maxLength':160},'target':{'type':'string','maxLength':120},
            'lesson_mode':{'type':'string','enum':['hint','solution']}},['equation','lesson_mode'])

def tex(value):
    n=Fraction(value)
    return str(n.numerator) if n.denominator==1 else ('-' if n<0 else '')+r'\frac{'+str(abs(n.numerator))+'}{'+str(n.denominator)+'}'

def target_of(entry,info):
    for value in reversed(re.findall(r'\$([^$]+)\$',entry.get('expression',''))):
        try:c,_=linear(value)
        except (ValueError,SyntaxError,ZeroDivisionError):continue
        if c and set(c)<=set(info['solutions']):return value.strip()
    return ''

def specification(entry,solution=False):
    info=identify(entry)
    if not info:return None
    # 两种许可共用同一受支持题型；不能提示版能建图、解答版却提交None造成协议失败。
    try:term_specs(info,solution);term_specs(info,True)
    except ContractError:return None
    return {'kind':'animation_scene','template':'nonnegative_reasoning','basis':'problem','title':'从非负和为零逐步推到所求',
            'params':{'equation':info['equation'],'target':target_of(entry,info),'lesson_mode':'solution' if solution else 'hint'},'duration':20,
            'caption':'每次图形变化对应本题的一条推理；变量值与表达式的非负性分开。'}


def term_specs(info,solution):
    """Same expression, explicit coordinate meaning, exact zero and valid domain."""
    specs=[]
    for i,condition in enumerate(info['conditions']):
        expression=condition.split('=')[0];coefficients,constant=linear(expression)
        name,coefficient=next(iter(coefficients.items()));root=info['solutions'][name]
        # 提示横轴是原题内部一次式u，不把未求a、b的数值作为轴刻度展示。
        a,b=(float(coefficient),float(constant)) if solution else (1,0)
        zero=float(root) if solution else 0
        root_exact=root if solution else Fraction(0)
        span=Fraction(4)/abs(coefficient) if solution else Fraction(4)
        exact_domain=[root_exact,root_exact+span] if i==0 and a>0 else [root_exact-span,root_exact] if i==0 else [root_exact-span,root_exact+span]
        domain=[float(v) for v in exact_domain]
        if not -20<=domain[0]<domain[1]<=20:raise ContractError('nonnegative curve domain exceeds supported range')
        axis=name if solution else expression.replace('-', '−')
        specs.append({'kind':'function_plot','function':'square_root' if i==0 else 'absolute','basis':'problem',
             'title':('根式：从定义域边界开始' if i==0 else '绝对值：V形最低点为零'),
             'caption':('横轴是原变量 '+name+'；圆点为使这一项归零的位置。' if solution else '横轴是原题内部的一次式 '+axis+'，不是变量 '+name+' 本身；内部量为零时外层才为零。'),
             'a':a,'b':b,'domain':domain,'axis_labels':{'x':axis,'y':'根式值' if i==0 else '绝对值'},
             'markers':[{'x':zero,'y':0,'label':'表达式等于零'}],
             'display':{'formula':info['first'] if i==0 and solution else info['second'] if solution else r'\sqrt{u},\ u='+expression if i==0 else r'|v|,\ v='+expression,
                        'domain':[tex(v) for v in exact_domain],'markers':[{'x':tex(root) if solution else '0','y':'0'}]}})
    return specs


def static_specifications(entry,solution=False):
    info=identify(entry)
    return term_specs(info,solution) if info else []


def explanation(entry,solution=False):
    info=identify(entry)
    if not info:return None
    text=f"根式 ${info['first']}$ 只在被开方数非负时有实数值，且函数值不小于0；绝对值 ${info['second']}$ 的图像是V形，函数值也不小于0。任一项为正，总和就大于0，所以总和为0只能使两项同时为0。"
    text+='因此得到 $'+r',\quad '.join(info['conditions'])+'$。'
    if solution:
        text+='解得 $'+r',\quad '.join(name+'='+tex(value) for name,value in info['solutions'].items())+'$。'
        target=target_of(entry,info)
        if target:
            cs,c=linear(target);value=c+sum(v*info['solutions'][name] for name,v in cs.items())
            text+='代回所求：$'+target+'='+tex(value)+'$。'
    else:text+='先从这两个一次方程求变量，最后所求留给你完成。'
    return text

def render(params,duration):
    info=identify({'expression':'$'+params['equation']+'$'})
    if not info or info['equation']!=params['equation']:raise ContractError('nonnegative reasoning requires the complete owned supported equation')
    mode=params['lesson_mode'];solution=mode=='solution';target=params.get('target','')
    def step(at,title,scene,given,action,rule,formula):return {'at':at,'title':title,'scene':scene,'given':given,'action':action,'rule':rule,'formula':formula}
    lesson={'version':'problem_reasoning_v1','kind':'nonnegative','mode':mode,'problem':info['equation'],'target':target,
            'goal':'求 $'+target+'$' if target else '由条件求参数','terms':[info['first'],info['second']]}
    from .advanced_visuals import function_plot
    lesson['term_curves']=[]
    for spec in term_specs(info,solution):
        compiled=function_plot(spec);lo,hi=spec['domain'];zero=spec['markers'][0]
        positive_x=lo+.7*(hi-lo) if zero['x']==lo else lo+.3*(hi-lo)
        inner=spec['a']*positive_x+spec['b'];positive_y=inner**.5 if spec['function']=='square_root' else abs(inner)
        lesson['term_curves'].append({'expression':spec['display']['formula'],
            'curve':{'domain':spec['domain'],'y_range':compiled['y_range'],'samples':compiled['samples'],'markers':[],
                     'formula':spec['display']['formula'],'axis_labels':spec['axis_labels'],'note':spec['caption'],
                     'x_ticks':[{'value':zero['x'],'label':spec['display']['markers'][0]['x']}],
                     'y_ticks':[{'value':v,'label':str(v)} for v in (0,1,2)]},
            'zero':{'x':zero['x'],'y':0},'positive':{'x':positive_x,'y':positive_y}})
    steps=[step(0,'先确认哪些量非负','read','原题是两个表达式相加等于零。','分别标明根式与绝对值的非负性。','非负的是表达式的值，变量本身可能为负。',info['first']+r'\ge0,\quad '+info['second']+r'\ge0'),
           step(.12 if solution else .25,'假设根式这一项为正','positive_left','另一项不能为负。','突出一项为正时总和也必为正。','正数加非负数大于零，与原题总和为零矛盾。',info['first']+'>0'+r'\quad\Rightarrow\quad '+info['equation'].split('=')[0]+'>0'),
           step(.24 if solution else .5,'交换两项再检查','positive_right','根式这一项不能为负。','假设绝对值这一项为正，观察同样的矛盾。','所以任意一项为正都不满足原题。',info['second']+'>0'+r'\quad\Rightarrow\quad '+info['equation'].split('=')[0]+'>0'),
           step(.36 if solution else .75,'两项必须同时归零','zero','两项各自不小于零，任一项为正都矛盾。','把两个表达式分别写成等于零。','不能用一正一负抵消，因为两项都不允许为负。',r'\begin{cases}'+info['first']+r'=0\\'+info['second']+r'=0\end{cases}'),
           step(.48 if solution else 1,'去掉外层，得到一次方程','conditions','根式和绝对值都为零。','根式为零则被开方数为零；绝对值为零则内部量为零。','外层为零的依据来自各自定义，不是把符号随意删除。',r'\begin{cases}'+info['conditions'][0]+r'\\'+info['conditions'][1]+r'\end{cases}')]
    if solution:
        variables=[]
        for i,condition in enumerate(info['conditions']):
            expression=condition.split('=')[0];coefficients,constant=linear(expression);name,coefficient=next(iter(coefficients.items()));value=info['solutions'][name]
            operation=f'两边同时减去 {tex(constant)}' if constant>0 else f'两边同时加上 {tex(-constant)}' if constant<0 else '合并当前等式'
            if coefficient!=1:operation+=f'，再除以 {tex(coefficient)}'
            middle=(tex(coefficient) if coefficient!=1 else '')+name+'='+tex(-constant)
            formula=condition+r'\quad\Longrightarrow\quad '+middle+r'\quad\Longrightarrow\quad '+name+'='+tex(value)
            steps.append(step(.60+.12*i,'求出'+name,'solve_variable','使用刚才从原条件得到的方程。',operation,'等式两边执行相同运算，参数可以为负或分数。',formula))
            variables.append({'name':name,'value':float(value),'label':tex(value),'equation':condition,
              'intermediate':middle,'solved_equation':name+'='+tex(value),'operation1':('+' if constant<=0 else '-')+tex(abs(constant)),
              'operation2':r'\div '+tex(coefficient) if coefficient!=1 else ''})
        solved={'variables':{name:tex(value) for name,value in info['solutions'].items()}}
        if target:
            coefficients,constant=linear(target)
            if not set(coefficients)<=set(info['solutions']):raise ContractError('target variables must belong to this owned nonnegative equation')
            contributions=[constant] if constant else []
            contributions.extend(coefficient*info['solutions'][name] for name,coefficient in sorted(coefficients.items()))
            positions=[Fraction(0)]
            for value in contributions:positions.append(positions[-1]+value)
            result=positions[-1];substitution='+'.join('('+tex(value)+')' for value in contributions)
            solved['result']=tex(result)
            steps.extend([step(.86,'把参数代回真正所求','combine','两个参数已由原条件求出。','按所求表达式的系数代入，数轴依次显示各项贡献。','负数向左，正数向右；这里计算所求，不把变量值相加到无关目标。',target+'='+substitution),
                          step(1,'核对原条件与最终结果','result','所有参数与所求都来自同一原题。','把已求变量代回原条件检查，再写所求的精确值。','两项确实都为零，所求保留精确分数或整数。',target+'='+tex(result))])
            span=max(Fraction(1),max(positions)-min(positions));pad=span/4
            lesson['number_line']={'range':[float(min(positions)-pad),float(max(positions)+pad)],
              'positions':[float(value) for value in positions],
              'ticks':[{'value':float(value),'label':str(value).replace('-','−')} for value in sorted(set(positions))]}
        lesson['solved']=solved;lesson['variables']=variables
    lesson['steps']=steps
    return {'duration':duration,'range':[0,1],'extent':1,'frames':[{'at':step['at']*duration,'values':{'phase':i}} for i,step in enumerate(steps)],'reasoning_lesson':lesson}
