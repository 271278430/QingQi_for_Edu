"""Exact educational labels; numeric sampling never becomes mathematical truth."""
import re
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

def compact_response(text):
    """Unknown model decimals are approximations, never invented exact fractions."""
    def compact(match):
        prefix=match[1] or '';n=float(match[2]);value=format(n,'.2f').rstrip('0').rstrip('.')
        return ('≈' if prefix in ('=','≈') else '\\approx ' if prefix=='\\approx ' else '≈')+value
    # 仅压缩助手生成的数值，不改变学生原题。分段保留代码/URL，避免改写标识符。
    pieces=re.split(r'(```[\s\S]*?```|`[^`\n]*`|https?://\S+)',text)
    for i in range(0,len(pieces),2):pieces[i]=re.sub(r'(=|≈|\\approx )?(?<![A-Za-z0-9_])(-?\d+\.\d{3,})(?![A-Za-z0-9_])',compact,pieces[i])
    return ''.join(pieces)
