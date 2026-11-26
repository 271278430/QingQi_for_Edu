"""Bounded nonnegative-expression story compiler, never a claim about the variables."""
import re
from .practice_tutoring import linear


def identify(entry):
    source=entry.get('expression','');parts=re.findall(r'\$([^$]+)\$',source) or [source]
    # 只承接完整两项的非负和，不能从含减号或其他项的题里截取片段猜教学条件。
    for part in parts:
        compact=re.sub(r'\s+|\\(?:left|right)','',part).replace('−','-')
        match=re.fullmatch(r'\\sqrt\{([^{}]+)\}\+\|([^|]+)\|=0',compact)
        if not match:continue
        try:
            fields=[linear(value) for value in match.groups()]
        except (ValueError,SyntaxError,ZeroDivisionError):continue
        if not all(len(coefficients)==1 for coefficients,_ in fields):continue
        solutions={}
        for coefficients,constant in fields:
            variable,coefficient=next(iter(coefficients.items()));value=-constant/coefficient
            if variable in solutions and solutions[variable]!=value:break
            solutions[variable]=value
        else:
            return {'equation':compact,'first':r'\sqrt{'+match[1]+'}','second':'|'+match[2]+'|',
                    'conditions':[match[1]+'=0',match[2]+'=0'],'solutions':solutions}
    return None


def story_text(entry,allow_final_answer=False):
    info=identify(entry)
    if not info:return None
    text=f"情景教学：两台记录器分别记录甲、乙两项积分，积分都不小于零。在原题中，甲项表示 ${info['first']}$，乙项表示 ${info['second']}$。\n"
    text+='非负的是这两个表达式的值，变量本身仍由原题条件确定。总积分为零时，任何一项为正都会使总量大于零，因此两项只能同时为零。\n'
    text+='于是分别列出 $'+info['conditions'][0]+'$ 和 $'+info['conditions'][1]+'$，再求变量。'
    if allow_final_answer:
        text+='\n由条件得到 $'+r',\quad '.join(f'{variable}={value}' for variable,value in sorted(info['solutions'].items()))+'$。'
        if entry.get('key'):
            text+='按原题要求，参考结果为 $'+'；'.join(entry['key']['values'])+'$。'
        else:
            for target in reversed(re.findall(r'\$([^$]+)\$',entry['expression'])):
                try:coefficients,constant=linear(target)
                except (ValueError,SyntaxError,ZeroDivisionError):continue
                if coefficients and set(coefficients)<=set(info['solutions']):
                    value=constant+sum(c*info['solutions'][var] for var,c in coefficients.items())
                    text+=f'代回原题所求，${target}={value}$。';break
    else:text+='最后的所求先保留。'
    return text
