"""Compile the owned identity into mathematical steps, never model-created frames."""
import re
from .contracts import ContractError,obj
from .practice_tutoring import identity_lesson,identity_answer,linear

PARAMS=obj({'equation':{'type':'string','minLength':1,'maxLength':160},
            'lesson_mode':{'type':'string','enum':['hint','solution']},
            'power':{'type':'integer','minimum':0,'maximum':4096},'units':{'type':'boolean'},
            'scenario':{'type':'string','enum':['scorekeepers']}},['equation','lesson_mode'])


def specification(entry,allow_final_answer=False,scenario=None):
    info=identity_lesson(entry)
    if not info or 'x' in {info['variable'],info['other_variable']}:return None
    params={'equation':info['equation'],'lesson_mode':'solution' if allow_final_answer else 'hint'}
    exact=identity_answer(entry)
    if exact:params.update(power=exact['exponent'],units=exact['units'])
    if scenario:params['scenario']=scenario
    return {'kind':'animation_scene','template':'identity_probe','title':'双记录器的积分故事' if scenario else '用试值理解恒成立',
            'basis':'problem','params':params,'duration':14}


def render(params,duration):
    entry={'expression':'对任意x恒成立：$'+params['equation']+'$'}
    info=identity_lesson(entry)
    if not info or info['equation']!=params['equation'] or 'x' in {info['variable'],info['other_variable']}:
        raise ContractError('identity animation requires a complete supported equation')
    relation=info['rearranged'];left,right=relation.split('=')
    coefficient=left[:-1].strip('()');constant=right
    conditions=[coefficient+'=0',constant+'=0']
    steps=[
      {'at':0,'title':'把随x变化的项放在一起','phase':'rearrange','explanation':'把含x的项移到左边，常数移到右边；这一步保持原方程的条件。','formula':info['equation']+r'\quad\Longrightarrow\quad '+relation},
      {'at':.2,'title':'先用x=0检验','phase':'probe','probe':0,'explanation':'恒成立包括x=0。此时左边为0，所以右边这个固定常数也必须为0。','formula':'0='+constant},
      {'at':.4,'title':'再用x=1检验','phase':'probe','probe':1,'explanation':'x=1时，左边是一份系数，右边仍是同一个固定常数。','formula':coefficient+'='+constant},
      {'at':.6,'title':'对照x=2的情况','phase':'probe','probe':2,'explanation':'左边变成两份同样的系数，右边仍不改变。一份和两份都要等于这个常数，系数只能为0。','formula':f'2({coefficient})={constant}'},
      {'at':1 if params['lesson_mode']=='hint' else .8,'title':'得到两个参数条件','phase':'conditions','explanation':'当系数和常数都为0，方程化为0·x=0，所以对所有x都成立。再根据两个条件求参数。','formula':r'\begin{cases}'+conditions[0]+r'\\'+conditions[1]+r'\end{cases}'}]
    if params['lesson_mode']=='solution':
        formula=f"{info['variable']}={info['known']},\\quad {info['other_variable']}={info['other_known']}"
        explanation='分别对两个条件做相同的运算，得到参数。'
        if 'power' in params:
            entry['expression']+=f"求 $({info['variable']}+{info['other_variable']})^{{{params['power']}}}$"+('的个位数字' if params.get('units') else '')
            exact=identity_answer(entry)
            if not exact:raise ContractError('identity power exceeds exact animation limits')
            formula+=r'\quad\Longrightarrow\quad '+exact['display']
            explanation+=' 本题仅求个位，取个位数字。' if params.get('units') else ' 对原题的所求保留精确乘方，不展开长串数字。'
        steps.append({'at':1,'title':'回到原题的所求','phase':'solution','explanation':explanation,'formula':formula})
    story=None
    if params.get('scenario')=='scorekeepers':
        # 故事按原式编译，不把有符号输入x误改成非负次数，也不改变常数的负号。
        lhs,rhs=info['equation'].split('=')
        lr,lo=lhs.split('x');rr,ro=rhs.split('x')
        lr=lr or '1';rr=rr or '1';lo=lo.lstrip('+') or '0';ro=ro.lstrip('+') or '0'
        def account(rate,offset,x):
            if x==0:return offset
            if rate.lstrip('+-').isdigit():term=str(int(rate)*x)
            else:term=rate if x==1 else str(x)+rate
            if term=='0':return offset
            if offset.lstrip('+-').isalpha() and term.lstrip('+-').isdigit():return offset+('' if term.startswith('-') else '+')+term
            return term if offset=='0' else term+('' if offset.startswith('-') else '+')+offset
        story={'title':'双记录器的积分故事',
               'setup':'小林设计了两台积分记录器，接受同一个输入x。任务是调整未知设置，让无论输入怎样变化，两台记录器的积分始终相同。',
               'left':{'name':'蓝色记录器','rate':lr,'offset':lo,'expression':lhs},
               'right':{'name':'紫色记录器','rate':rr,'offset':ro,'expression':rhs},
               'domain_note':'x只是数值输入，可以为负数或分数；0、1、2是观察例子，原题仍要求对所有x成立。'}
        steps[0].update(title='给两台记录器设置规则',explanation='蓝色和紫色记录器接受相同输入。每次按各自规则计算积分；我们要让两边对所有输入都一致。',formula=info['equation'],accounts=[lhs,rhs])
        for step in steps[1:4]:
            x=step['probe'];a,b=account(lr,lo,x),account(rr,ro,x)
            step.update(accounts=[a,b],formula=a+'='+b)
            step['title']=f'输入x={x}，对照两本积分账'
            step['explanation']=('没有输入变化时，只剩两台记录器的初始积分。先让固定部分一致。' if x==0 else '同样增加一份输入，两本账必须增加相同的积分。对照x=0的账单，找出变化率的条件。' if x==1 else '输入从1增加到2，再增加同样的一份。只有变化率和初始积分都相同，才能保证所有输入下两本账都一致。')
        steps[4].update(title='把故事转回两个数学条件',explanation='两台记录器的变化率必须相同，初始积分也必须相同。把这两个要求写回原方程，再求参数。',accounts=[lhs,rhs])
    return {'duration':duration,'range':[0,2],'extent':2,
            'frames':[{'at':s['at']*duration,'values':{'phase':i,'probe':s.get('probe',0)}} for i,s in enumerate(steps)],
            'algebra_lesson':{'version':'identity_lesson_v1','mode':params['lesson_mode'],'equation':info['equation'],
                              'rearranged':relation,'coefficient_symbol':coefficient,'constant_symbol':constant,
                              'conditions':conditions,'steps':steps,**({'story':story} if story else {})}}


def story_text(entry,allow_final_answer=False):
    spec=specification(entry,allow_final_answer,scenario='scorekeepers')
    if not spec:return None
    lesson=render(spec['params'],spec['duration'])['algebra_lesson'];story=lesson['story']
    text='可以，沿用这道题来讲一个积分故事。'+story['setup']+'恒成立意味着两台记录器对每个输入都要给出相同积分。\n'
    text+=f"蓝色记录器的积分是 ${story['left']['expression']}$，紫色记录器是 ${story['right']['expression']}$。\n"
    text+='先输入 $x=0$，两本账分别记为 $'+lesson['steps'][1]['accounts'][0]+'$ 和 $'+lesson['steps'][1]['accounts'][1]+'$；再输入 $x=1$，两本账分别变为 $'+lesson['steps'][2]['accounts'][0]+'$ 和 $'+lesson['steps'][2]['accounts'][1]+'$。'
    text+='让初始积分相同、每份输入带来的变化也相同，就是这道恒等式的关键。'
    text+='\n'+lesson['steps'][-1]['explanation']+' $'+lesson['steps'][-1]['formula']+'$。' if allow_final_answer else '\n你可以先比较这两次账单，列出求参数的条件，最终乘方先保留。'
    return text


def struggle_reply(entry,assessment,question,*,no_questions=False):
    info=identity_lesson(entry)
    if not info or not re.search(r'还是|仍然|依然|不懂|没懂|不明白|不会|解释这一步',question):return None
    if re.search(r'乘方|指数|幂|偶次|奇次|最后结果',question):return None
    stage=assessment['stage'];variable=info['other_variable'] if stage==1 else info['variable']
    value=info['other_known'] if stage==1 else info['known']
    relation=info['rearranged'];left,right=relation.split('=');coefficient=left[:-1].strip('()')
    condition=right+'=0' if stage==1 else coefficient+'=0'
    c,d=linear(condition.split('=')[0])
    text=f'我们把这一步说具体：${relation}$ 要对所有 $x$ 成立。取 $x=0$ 得到 $0={right}$；再取 $x=1$，说明 ${coefficient}=0$。\n'
    operation=f'等式两边同时减去 ${d}$' if d>0 else f'等式两边同时加上 ${-d}$'
    if c[variable]!=1:operation+=f'，再将两边同时除以 ${c[variable]}$'
    text+=f'现在看 ${condition}$，要找的是变量 ${variable}$。{operation}，得到 ${variable}={value}$。'
    if not no_questions:text+='\n你可以照这个方法，试着处理另一个参数的条件吗？'
    return text
