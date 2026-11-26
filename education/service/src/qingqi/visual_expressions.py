"""Bounded polynomial data extraction, never Python eval or arbitrary function calls."""
import ast
import re
from fractions import Fraction
from .contracts import ContractError


def polynomial(expression):
    text=expression.replace('²','**2').replace('³','**3').replace('^','**').replace('−','-').replace('×','*').replace('÷','/')
    text=re.sub(r'\s+','',text)
    text=re.sub(r'(?<=[0-9)])(?=x|\()', '*',text)
    if len(text)>160:raise ContractError('函数表达式过长。')
    try:tree=ast.parse(text,mode='eval')
    except SyntaxError as error:raise ContractError('请提供清晰的一次或二次函数表达式。') from error
    if len(list(ast.walk(tree)))>64:raise ContractError('函数表达式过于复杂。')
    def add(a,b,sign=1):return {i:a.get(i,Fraction(0))+sign*b.get(i,Fraction(0)) for i in set(a)|set(b)}
    def multiply(a,b):
        result={}
        for i,x in a.items():
            for j,y in b.items():
                if i+j>3:raise ContractError('目前函数图支持最高三次多项式。')
                result[i+j]=result.get(i+j,Fraction(0))+x*y
        return result
    def visit(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)) and not isinstance(n.value,bool) and abs(n.value)<=10000:return {0:Fraction(str(n.value))}
        if isinstance(n,ast.Name) and n.id=='x':return {1:Fraction(1)}
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):return {i:v*(-1 if isinstance(n.op,ast.USub) else 1) for i,v in visit(n.operand).items()}
        if isinstance(n,ast.BinOp):
            if isinstance(n.op,ast.Pow):
                if not isinstance(n.right,ast.Constant) or n.right.value not in {0,1,2,3}:raise ContractError('目前函数图支持最高三次多项式。')
                a=visit(n.left);result={0:Fraction(1)}
                for _ in range(n.right.value):result=multiply(result,a)
                return result
            a,b=visit(n.left),visit(n.right)
            if isinstance(n.op,ast.Add):return add(a,b)
            if isinstance(n.op,ast.Sub):return add(a,b,-1)
            if isinstance(n.op,ast.Mult):return multiply(a,b)
            if isinstance(n.op,ast.Div) and set(b)<={0} and b.get(0):return {i:v/b[0] for i,v in a.items()}
        raise ContractError('目前函数图支持最高三次多项式，不执行函数调用或代码。')
    result=visit(tree.body)
    if any(abs(v)>10000 for v in result.values()):raise ContractError('函数系数超出当前绘图范围。')
    return result


def specified_functions(text):
    # Unicode词边界会漏掉“函数y=”；只排除ASCII标识符前缀。
    pattern=r'(?<![A-Za-z0-9_])(?:y|f\s*\(x\))\s*[=＝]\s*([0-9xX.+*/^()\-−²³×÷\s]+)'
    return [m[1].strip().lower().rstrip('. ') for m in re.finditer(pattern,text,re.I)]
