import ast
import re

from .domain_tools import number


def heuristic_prompt(expression):
    """A next-step scaffold, without calculating or revealing a result."""
    if '(' in expression or '（' in expression:
        return '先处理最内层括号，把结果代回原式，保留括号外的运算；写出这一步让我核对。'
    if '/' in expression or '÷' in expression:
        return '先标出除法部分；含分数时保留精确分数，再按原式顺序处理其余项。请写出下一步等式。'
    if '*' in expression or '×' in expression:
        return '先处理乘法部分，保留其余加减项，再写出代回原式后的等式。'
    return '先判断数字的符号与运算顺序，再完成一小步；写出等式后我来核对。'


def completed_numeric_work(expression, steps):
    if not steps or steps[-1]['equation'].count('=') != 1:
        return False
    left, right = steps[-1]['equation'].split('=')
    if not re.fullmatch(r'\s*[+-]?\d+(?:\.\d+)?(?:\s*/\s*[+-]?\d+)?\s*', right):
        return False
    try:
        return number(left) == number(expression) == number(right)
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
        return False


def calculation_steps(expression, *, allow_final_answer=True):
    """Generate tutor explanation separately from the student's actual steps."""
    tree = ast.parse(expression.replace('×', '*').replace('÷', '/'), mode='eval')
    steps = []
    symbols = {ast.Add: '+', ast.Sub: '-', ast.Mult: '×', ast.Div: '÷'}
    def fmt(value):
        s = str(value)
        return '('+s+')' if value < 0 or value.denominator != 1 else s
    def walk(node):
        if isinstance(node, ast.BinOp):
            left, right = walk(node.left), walk(node.right)
            value = number(ast.unparse(node))
            steps.append(f'{fmt(left)} {symbols[type(node.op)]} {fmt(right)} = {value}')
            return value
        if isinstance(node, ast.UnaryOp):
            walk(node.operand)
        return number(ast.unparse(node))
    walk(tree.body)
    selected = steps if allow_final_answer else steps[:-1]
    text = '按原题的运算顺序逐步计算：\n'+'\n'.join(f'{i+1}. {step}' for i,step in enumerate(selected)) if selected else '先确定括号与乘除的顺序，再写出下一步等式。'
    if not allow_final_answer:
        text += '\n最后一步先留给你来算，写出结果后我再核对。'
    return text


def chat_reply(question):
    if re.search(r'谢谢|thanks', question, re.I):
        return '不客气！有新的问题或思路，随时告诉我。', 'greet'
    if re.search(r'笑话', question):
        return '讲个数学小笑话：为什么等号不担心吵架？因为它总能把两边摆平。', 'chat'
    if re.search(r'累|烦恼|心情不好', question):
        return '听起来今天有些疲惫。可以先休息一会儿；你也可以说说发生了什么，我们先聊聊。', 'chat'
    if re.search(r'你是谁', question):
        return '我是清启学习助手，可以陪你聊天，也能查询课程、检查作答并提供分步辅导。', 'chat'
    if re.search(r'你好|hello|你在吗', question, re.I):
        return '你好，我在。你想先聊聊，还是带着一道题一起看看？', 'greet'
    return '可以，我们先聊聊。你想说说今天的事情，还是聊一个感兴趣的话题？', 'chat'
