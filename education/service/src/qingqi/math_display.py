"""Exact educational labels; numeric sampling never becomes mathematical truth."""
import re
from decimal import Decimal
import sympy as s
from sympy.printing.latex import LatexPrinter

class ExactPrinter(LatexPrinter):
    def _print_Pow(self,expr):
        base,power=expr.as_base_exp()
        if power.is_Rational and power.q==3 and power.p in (1,2):
            return r'\sqrt[3]{'+self._print(base**power.p)+'}'
        return super()._print_Pow(expr)

def exact(value):
    value=s.simplify(value)
    if value.is_Rational and (100 % int(value.q)==0):
        return (format(float(value),'.2f').rstrip('0').rstrip('.') if value.q!=1 else str(value)).replace('-','−')
    return ExactPrinter().doprint(value)

def source_numbers(source):
    return {Decimal(value.replace('−','-')) for value in re.findall(r'(?<![A-Za-z0-9_])[-−]?\d+\.\d+(?![A-Za-z0-9_])',source)}


def teaching_source(payload,state):
    problem=payload.get('problem') or {}
    return ' '.join(str(v) for v in (problem.get('text','') if isinstance(problem,dict) else problem,
                    (state.get('practice_entry') or {}).get('expression',''),
                    (state.get('image_question') or state.get('problem_question') or {}).get('text',''),
                    state.get('effective_request',{}).get('expression','')))


def unknown_decimals(text,source=''):
    known=source_numbers(source)
    return [m.group() for m in re.finditer(r'-?\d+\.\d{3,}',text) if Decimal(m.group()) not in known]


def invalid_teacher_reply(text,question=''):
    if re.search(r'(?:√|\\sqrt\s*\{?)\s*(?:≈|\\approx)',text):return 'radicand_approximation'
    from .request_controls import answer_directives
    commands=answer_directives(question)
    if commands and commands[-1]['allowed'] and re.search(r'不能直接(?:报出|报|给出|给|提供)(?:最终)?(?:结果|答案)',text):return 'missed_answer_request'
    return None


def model_history(history):
    result=[];omitted=[]
    for i,turn in enumerate(history):
        if invalid_teacher_reply(turn.get('reply',''),turn.get('question','')):
            result.append({**turn,'reply':''});omitted.append(i)
        else:result.append(turn)
    return result,omitted


def compact_response(text,*,source=''):
    """Unknown model decimals are approximations, never invented exact fractions."""
    known=source_numbers(source)
    def compact(match):
        # 原题的2.061和已知近似1.436是条件，不能在输出里改成2.06和1.44再用于推导。
        if Decimal(match[2]) in known:return match[0]
        prefix=match[1] or '';n=float(match[2]);value=format(n,'.2f').rstrip('0').rstrip('.')
        if n and abs(n)<.01:value=format(n,'.1e').replace('e-0','e-').replace('e+0','e+')
        return ('≈' if prefix in ('=','≈') else '\\approx ' if prefix=='\\approx ' else '≈')+value
    # 仅压缩助手生成的数值，不改变学生原题。分段保留代码/URL，避免改写标识符。
    pieces=re.split(r'(```[\s\S]*?```|`[^`\n]*`|https?://\S+)',text)
    for i in range(0,len(pieces),2):pieces[i]=re.sub(r'(=|≈|\\approx )?(?<![A-Za-z0-9_])(-?\d+\.\d{3,})(?![A-Za-z0-9_])',compact,pieces[i])
    return ''.join(pieces)
