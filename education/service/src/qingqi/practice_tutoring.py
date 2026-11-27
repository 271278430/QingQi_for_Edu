"""Pure, bounded tutoring scaffolds and exact linear checks over an owned question."""
import ast
import re
from fractions import Fraction

LIMIT = 10 ** 9


def linear(value):
    value = value.replace('×', '*').replace('÷', '/').replace('（', '(').replace('）', ')').replace(' ', '')
    if len(value) > 120 or not re.fullmatch(r'[0-9a-zA-Z.+*/()\-]+', value):
        raise ValueError('unsupported linear expression')
    value = re.sub(r'(?<=\d)(?=[a-zA-Z(])|(?<=\))(?=[a-zA-Z(])', '*', value)
    tree = ast.parse(value, mode='eval')
    if len(list(ast.walk(tree))) > 80:
        raise ValueError('linear expression budget exceeded')
    def walk(node):
        if isinstance(node, ast.Constant) and type(node.value) in {int, float}:
            return {}, Fraction(str(node.value))
        if isinstance(node, ast.Name) and re.fullmatch('[a-zA-Z]', node.id):
            return {node.id: Fraction(1)}, Fraction(0)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            a, b = walk(node.operand)
            sign = -1 if isinstance(node.op, ast.USub) else 1
            return {k: v * sign for k, v in a.items()}, b * sign
        if isinstance(node, ast.BinOp):
            a, b = walk(node.left)
            c, d = walk(node.right)
            if isinstance(node.op, (ast.Add, ast.Sub)):
                sign = -1 if isinstance(node.op, ast.Sub) else 1
                result = {k: a.get(k, 0) + sign * c.get(k, 0) for k in a.keys() | c.keys()}
                return {k: v for k, v in result.items() if v}, b + sign * d
            if isinstance(node.op, ast.Mult) and not (a and c):
                return ({k: v * d for k, v in a.items()}, b * d) if a else ({k: v * b for k, v in c.items()}, b * d)
            if isinstance(node.op, ast.Div) and not c and d:
                return {k: v / d for k, v in a.items()}, b / d
        raise ValueError('nonlinear or unsupported expression')
    coefficients, constant = walk(tree.body)
    if any(abs(v.numerator) > LIMIT or v.denominator > LIMIT for v in [constant, *coefficients.values()]):
        raise ValueError('linear number budget exceeded')
    return coefficients, constant


def equation(value):
    left, right = value.split('=')
    a, b = linear(left)
    c, d = linear(right)
    coefficients = {k: a.get(k, 0) - c.get(k, 0) for k in a.keys() | c.keys()}
    return {k: v for k, v in coefficients.items() if v}, d - b


def equations(question):
    pieces = re.findall(r'\$([^$]{1,120})\$', question)
    # 真实题库的方程组放在 cases 内；整段含多个等号不能被当成一条方程跳过。
    pieces = [part.strip() for value in pieces for part in value.replace(r'\begin{cases}', '').replace(r'\end{cases}', '').split(r'\\')]
    if not pieces:
        pieces = re.findall(r'[\da-zA-Z(（][\da-zA-Z\s.+*/×÷()（）\-]*=[\da-zA-Z\s.+*/×÷()（）\-]+', question)
    found = []
    for value in pieces:
        if value.count('=') != 1:
            continue
        try:
            coeff, total = equation(value.strip())
        except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
            continue
        if coeff:
            found.append((value.strip(), coeff, total))
    return found


def free_entry(question):
    found = equations(question)
    if len(found) != 1 or len(found[0][1]) != 1:
        return None
    raw, coefficients, total = found[0]
    if re.fullmatch(r'\s*[a-zA-Z]\s*=\s*[+\-\d./\s]+\s*', raw) and not re.search('解方程|求解', question):
        return None
    # 复杂题的一条局部等式不能代表整题；只为明确的单方程请求建立核验上下文。
    rest = question.replace(raw, '').replace('$', '')
    if re.search(r'如果|已知|当|同时|且|面积|周长|至少|至多|两个|两种', rest):
        return None
    if rest.strip(' ，,。.!！?？:：;；') and not re.search(r'解方程|求解|方程.*(?:解|提示)|核对.*方程', rest):
        return None
    variable, coefficient = next(iter(coefficients.items()))
    if not coefficient:
        return None
    return {'id': 'student-linear', 'expression': question, 'linear_equation': raw, 'title': '一元一次方程', 'target': variable,
            'answer_kind': 'numeric', 'key': {'kind': 'numeric', 'values': [str(total / coefficient)]}, 'options': []}


def uses_question(question, entry):
    from .teaching_goals import refers_to_owned,goal,separate_calculation
    from .conversation import starts_new_problem
    from .presentation import references_problem,request_form
    if separate_calculation(question,entry):return False
    if starts_new_problem(question) or re.search(r'讲.*笑话', question) or goal(question)=='chat':
        return False
    if references_problem(question) or request_form(question):return True
    # 有效所属题上的概念困惑使用同一题面；不要求学生重说固定的“这道题”。
    if refers_to_owned(question,entry):return True
    if len(question) > 180 and entry['expression'] not in question:
        return False
    # 选题后第一句话也可以直接改变教学形式，不要求先发送一轮固定提示词。
    if re.search(r'动画|动态|演示|图示|可视化|画.{0,8}(?:图|线)',question):return True
    # 图示请求也是同题追问；只认当前题引用，不把新的完整题面绑定到旧题。
    if re.search(r'这(?:道(?:历史)?题|题|一步)|这(?:两个|组).*角|∠[A-Z]{3}|相似|垂足|锐角|重合|退化|对应边|当前题目|(?:数轴|坐标图|情景图|柱状图|示意图|图示).*(?:理解|讲解|说明)|原(?:题|练习)|提示|引导|追问|启发|解题(?:思路|步骤|过程)|讨论|复习|答案|结果|方程的解|继续|接下来|下一步|还是|不会|不懂|代入|移项|为什么|怎么理解', question):
        return True
    if re.fullmatch(r'\s*(?:[a-zA-Z]\s*=\s*)?[+\-\d./\s]+\s*|\s*[A-Da-d]\s*', question):
        return True
    return entry['expression'] in question


def equation_step(question):
    found = equations(question)
    if len(found) != 1 or len(found[0][1]) != 1:
        return False
    rest = question.replace(found[0][0], '').replace('$', '').strip(' ，,。.!！?？:：;；')
    return rest in {'', '我得到', '移项后', '合并后', '这一步是'}


def lesson(entry):
    identity=identity_lesson(entry)
    if identity:return identity
    found = equations(entry['expression'])
    target = entry.get('target')
    if not target:
        matches = re.findall(r'\$\s*([a-zA-Z])\s*=\s*\$', entry['expression'])
        target = matches[-1] if matches else None
    univariate = [e for e in found if len(e[1]) == 1 and (not target or target not in e[1])]
    if re.search('和谐方程|解互为相反数', entry['expression']) and univariate and target:
        raw, coefficients, total = univariate[-1]
        var, coefficient = next(iter(coefficients.items()))
        return {'kind': 'opposite', 'equation': raw, 'variable': var, 'known': total / coefficient, 'target': target}
    if entry.get('id') == 'student-linear':
        return {'kind': 'linear', 'equation': entry.get('linear_equation', entry['expression']), 'variable': target, 'known': Fraction(entry['key']['values'][0]), 'target': target}
    if '遮住' in entry['expression'] and '★' in entry['expression'] and '■' in entry['expression']:
        # 仅从原题的已知值和完整方程推出中间量，不用选择题答案倒推解题步骤。
        knowns = [(next(iter(c)), total / next(iter(c.values()))) for _, c, total in found if len(c) == 1]
        for given_var, given in knowns:
            for raw, c, total in found:
                if len(c) != 2 or given_var not in c:
                    continue
                variable = next(v for v in c if v != given_var)
                value = (total - c[given_var] * given) / c[variable]
                masked = re.search(r'([a-zA-Z0-9+\- ]+)\s*=\s*★', entry['expression'])
                if masked:
                    a, constant = linear(masked[1].strip())
                    if set(a) <= {given_var, variable}:
                        return {'kind':'substitution','equation':raw,'variable':variable,'known':value,'given_variable':given_var,'given':given,
                                'masked_expression':masked[1].strip(),'masked_known':constant + a.get(given_var,0)*given + a.get(variable,0)*value,'target':None}
    roots = re.findall(r'\$([^$]+)\$', entry['expression'])
    if '两个不同的平方根' in entry['expression']:
        affine = []
        for value in roots:
            try:
                c, d = linear(value)
                if len(c) == 1 and 'x' in c:
                    affine.append((value, c['x'], d))
            except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
                continue
        if len(affine) >= 2 and affine[0][1] + affine[1][1]:
            return {'kind': 'roots', 'variable': 'x', 'known': -(affine[0][2] + affine[1][2]) / (affine[0][1] + affine[1][1]), 'target': None,
                    'terms': [affine[0][0], affine[1][0]]}
    return {'kind': 'generic', 'target': target}


def identity_lesson(entry):
    """Recognize a bounded identity from its actual equation, never from a topic label."""
    text=entry['expression'];compact=re.sub(r'[\s$]', '', text)
    if not re.search(r'恒成立|恒等|任意|无论.*取',text):return None
    match=re.search(r'([a-zA-Z])x([+\-]\d+)=([+\-]?\d+)x([+\-])([a-zA-Z])',compact)
    if not match or match[1]==match[5]:return None
    m,b,k,sign,n=match.groups();b=int(b);k=int(k)
    if abs(b)>LIMIT or abs(k)>LIMIT:return None
    left=f'({m}{-k:+d})x' if k else f'{m}x'
    right=(n if sign=='+' else '-'+n)+(f'{-b:+d}' if b else '')
    return {'kind':'identity','equation':match[0],'variable':m,'other_variable':n,
            'known':Fraction(k),'other_known':Fraction(b if sign=='+' else -b),
            'rearranged':left+'='+right,'target':None}


def identity_answer(entry):
    info=identity_lesson(entry)
    if not info:return None
    text=re.sub(r'[\s$]', '', entry['expression'])
    m,n=info['variable'],info['other_variable']
    found=re.search(r'\('+re.escape(m)+r'\+'+re.escape(n)+r'\)\^\{?(\d{1,4})\}?',text)
    if not found:return None
    exponent=int(found[1]);base=info['known']+info['other_known']
    if exponent>4096 or max(abs(base.numerator).bit_length(),base.denominator.bit_length())*exponent>4096:return None
    value=base**exponent
    units='个位' in text
    if units and value.denominator!=1:return None
    return {'value':Fraction(abs(value.numerator)%10) if units else value,'exponent':exponent,
            'display':str(abs(value.numerator)%10) if units else f'({base})^{{{exponent}}}', 'units':units}


def assessment(entry, question, stage, grader):
    info = lesson(entry)
    number = r'[+-]?\d+(?:\.\d+)?(?:\s*/\s*[+-]?\d+)?'
    if info['kind']=='identity':
        match=re.fullmatch(r'\s*([a-zA-Z])\s*=\s*('+number+r')\s*[。.!！]?\s*',question)
        if match and match[1] in {info['variable'],info['other_variable']}:
            try:correct=Fraction(match[2].replace(' ',''))==(info['known'] if match[1]==info['variable'] else info['other_known'])
            except (ValueError,ZeroDivisionError):return {'status':'unverified','complete':False,'stage':stage}
            return {'status':'correct' if correct else 'incorrect','complete':False,'stage':stage | (1 if match[1]==info['variable'] else 2) if correct else stage}
    if info['kind'] == 'substitution':
        step = re.fullmatch(r'\s*([a-zA-Z★■])\s*=\s*(' + number + r')\s*[。.!！]?\s*', question)
        if step and step[1] in {info['variable'],'■','★'}:
            try:
                correct = Fraction(step[2].replace(' ','')) == (info['masked_known'] if step[1]=='★' else info['known'])
            except (ValueError, ZeroDivisionError, OverflowError):
                return {'status':'unverified','complete':False,'stage':stage}
            return {'status':'correct' if correct else 'incorrect','complete':False,'stage':max(stage, 2 if step[1]=='★' else 1) if correct else stage}
    match = re.search(r'\b([a-zA-Z])\s*=\s*(' + number + r')\s*[。.!！]?$', question.strip())
    if match and info['kind'] in {'opposite', 'roots'} and match[1] == info['variable']:
        expected = -info['known'] if info['kind'] == 'opposite' and stage >= 1 else info['known']
        try:
            correct = Fraction(match[2].replace(' ', '')) == expected
        except (ValueError, ZeroDivisionError, OverflowError):
            return {'status': 'unverified', 'complete': False, 'stage': stage}
        return {'status': 'correct' if correct else 'incorrect', 'complete': False, 'stage': min(2, stage + 1) if correct else stage}
    submitted = None
    if match and info.get('target') == match[1]:
        submitted = match[2]
    else:
        bare = re.fullmatch(number + r'(?:\s*[;；]\s*' + number + r')*|[A-Da-d]|\(?[+\-]?\d+\)?\s*\^\s*\d{1,4}', question.strip())
        stated = re.search(r'(?:最终答案|答案|结果|选项)(?:是|为|=|：|:)?\s*(' + number + r'|[A-Da-d])\s*[。.!！]?$', question.strip())
        submitted = bare[0] if bare else stated[1] if stated else None
    if submitted is not None:
        try:
            correct = grader(entry, submitted)
        except (ValueError, ZeroDivisionError, OverflowError):
            return {'status': 'unverified', 'complete': False, 'stage': stage}
        if not correct and not match and not stated and re.fullmatch(number, submitted) and info['kind'] in {'opposite', 'roots'} and stage < 2:
            expected = -info['known'] if info['kind'] == 'opposite' and stage == 1 else info['known']
            # 简短数值回应当前追问，不能把正确中间量当作整题成绩。
            if stage == 0 or info['kind'] == 'opposite':
                step_correct = Fraction(submitted.replace(' ', '')) == expected
                return {'status': 'correct' if step_correct else 'incorrect', 'complete': False, 'stage': stage + 1 if step_correct else stage}
        return {'status': 'correct' if correct else 'incorrect', 'complete': True, 'stage': 3 if correct else stage, 'submitted': submitted}
    if equation_step(question) and info['kind'] in {'linear', 'opposite', 'roots', 'substitution'}:
        _, coefficients, total = equations(question)[0]
        if info['variable'] in coefficients:
            expected = -info['known'] if info['kind'] == 'opposite' and stage >= 1 else info['known']
            correct = total / coefficients[info['variable']] == expected
            return {'status': 'correct' if correct else 'incorrect', 'complete': False, 'stage': stage, 'equivalent_step': True}
    return {'status': 'unverified', 'complete': False, 'stage': stage}


def guidance(entry, mode, stage=0, *, help_level=0, interactive=True):
    info = lesson(entry)
    if not interactive:
        # 提示按钮提供行动线索；同题的苏格拉底对话仍使用下面的互动支架。
        if info['kind']=='identity':
            if stage==1:return f"回到原式 ${info['equation']}$，比较不含 $x$ 的常数项，整理求 ${info['other_variable']}$ 的等式。先保留最后的乘方。"
            if stage==2:return f"回到原式 ${info['equation']}$，比较两边含 $x$ 的系数，整理求 ${info['variable']}$ 的等式。先保留最后的乘方。"
            if stage==0 and help_level==0:return f"先把 ${info['equation']}$ 整理成 ${info['rearranged']}$。等式要对所有 $x$ 成立，比较含 $x$ 的项与常数项是切入点。"
            if stage==0 and help_level==1:return f"对 ${info['rearranged']}$ 分别代入 $x=0$、$x=1$，再把两个等式相减。这样可以消去不随 $x$ 改变的部分，确定含 $x$ 的系数。"
            return f"回到 ${info['equation']}$，分别比较 $x$ 的系数和常数项。只整理当前参数关系，先不计算最后的乘方。"
        if info['kind']=='opposite':
            return f"先解不含参数的方程 ${info['equation']}$：把未知数项移到一边、常数项移到另一边，并注意移项变号。再用‘两个解互为相反数’把这个解与含参数方程联系起来。"
        if info['kind']=='substitution':
            return f"题目给出 ${info['given_variable']}={info['given']}$。先将这个值代入 ${info['equation']}$，得到只含另一个未知数的方程；把遮住的量留到后一步处理。"
        if info['kind']=='linear':return f"从 ${info['equation']}$ 入手，把含 ${info['variable']}$ 的项与常数项分开，移项后合并同类项，再处理未知数的系数。"
        if info['kind']=='roots':return f"同一个正数的两个平方根互为相反数，所以题中的 ${info['terms'][0]}$ 与 ${info['terms'][1]}$ 相加为零。先用这条关系整理当前未知数，再回到原题的所求。"
    if info['kind']=='identity':
        equation=info['equation'];relation=info['rearranged'];m=info['variable'];n=info['other_variable']
        if stage==0:
            if help_level==0:return f'题目要求 ${equation}$ 对所有 $x$ 都成立。先整理为 ${relation}$，右边不随 $x$ 改变；左边的 $x$ 系数需要满足什么条件？'
            if help_level==1:return f'继续看 ${relation}$。分别令 $x=0$、$x=1$，把得到的两个等式相减；这能帮助确定含 $x$ 的系数，而不需要猜 ${m}$。'
            return f'由 ${relation}$ 对任意 $x$ 成立，可以比较 $x$ 的系数与常数项：含 $x$ 的系数必须为零，两边常数也要相同。请据此分别列出求 ${m}$、${n}$ 的等式。'
        if stage==1:return f'接着回到原式 ${equation}$，比较不含 $x$ 的常数项，写出求 ${n}$ 的等式。'
        if stage==2:return f'回到 ${equation}$ 中含 $x$ 的项，比较两边系数，写出求 ${m}$ 的等式。'
        return f'回到 ${equation}$ 核对两个参数，再按原题所求计算。若所求是大整数乘方，保留精确乘方形式；只有问个位数字时才使用个位循环。'
    if info['kind'] == 'substitution':
        if stage == 0:
            return f"原题已经给出 ${info['given_variable']}={info['given']}$。先看第二个方程 ${info['equation']}$：把这个已知值代进去，剩下哪个未知数？你能写出代入后的等式吗？"
        if stage == 1:
            return f"这个中间值与原方程一致。现在把 ${info['given_variable']}={info['given']}$、${info['variable']}={info['known']}$ 放进第一个关系 ${info['masked_expression']}=\\bigstar$，星号应是多少？"
        return '两个遮住的数都已求出。按原题“星号、方块”的顺序检查选项，你选择哪一项？'
    if info['kind'] == 'opposite':
        if stage == 0:
            return (f"先看不含参数的方程 ${info['equation']}$。把含 ${info['variable']}$ 的项移到一边，常数项移到另一边，再合并同类项。你得到的解是多少？" if mode == 'heuristic'
                    else f"先从不含参数的方程 ${info['equation']}$ 入手。你能先求出它的解吗？")
        if stage == 1:
            return '这一步正确。两个方程的解互为相反数，另一个方程的解应该是什么？'
        return f"把刚才得到的另一个解代入含 ${info['target']}$ 的方程，接着整理参数。你得到的最终结果是多少？"
    if info['kind'] == 'linear':
        return f"先看 ${info['equation']}$。把含 ${info['variable']}$ 的项和常数项分开，移项时注意符号，再合并同类项。你愿意先写一步吗？"
    if info['kind'] == 'roots':
        if stage == 0:
            return f"同一个正数的两个平方根互为相反数。题中 ${info['terms'][0]}$ 与 ${info['terms'][1]}$ 相加应等于多少？你能据此求出 $x$ 吗？"
        if stage == 1:
            return '这一步正确。把 $x$ 代回一个平方根表达式，再把它平方，就能求出原来的正数。你准备怎样算？'
        return '现在把已求出的量代回所求表达式，最后判断立方根的符号和数值。请给出最终答案。'
    # 未识别出整题结构时不能按“有理数”等宽泛标签猜算法，更不能按提示次数假定已完成。
    text=entry['expression'];parts=re.findall(r'\$([^$]+)\$',text)
    anchor=next((p for p in parts if '=' in p or '<' in p or '>' in p),parts[0] if parts else '')
    goal=parts[-1] if len(parts)>1 else ''
    if anchor:
        lead=f'先看本题给出的 ${anchor}$。'
        if help_level==0:return lead+('对照其中的已知量与未知量，先写出能连接已知条件的一条关系。' if not goal or goal==anchor else f'所求涉及 ${goal}$；先确定这个量需要哪些已知条件，保留其他条件再整理。')
        if help_level==1:return lead+'可以先把题目明确给出的数值代入这条关系，只整理当前一步；不要把还没求出的量当成已知。'
        return lead+'如果仍然卡住，可点“和导师一起做”说明具体哪一项看不懂，导师会沿这道题继续解释。'
    excerpt=text[:100].strip()
    return f'先对照原题：“{excerpt}”。把已知条件与最后要求的量分开，先选一条能直接使用的条件；需要进一步解释时可以与导师讨论当前题。'


def hint_projection(entry, result):
    from .teaching_plan import hint_requires_repair
    # 旧版提示包含追问；只修正原题的展示投影，原事件和学生成绩保持原样。
    if result.get('style')!='explain' and hint_requires_repair(result.get('text','')):
        return {**result,'text':guidance(entry,'heuristic',0,help_level=max(0,result.get('hint_count',1)-1),interactive=False)}
    return result


def reply_for(entry, question, decision, checked):
    from .planning import reply
    mode, stage = decision['mode'], checked['stage']
    if checked['status'] == 'correct':
        if decision.get('no_questions'):return reply('当前作答与参考结果一致，已通过核对。','confirm')
        if checked.get('equivalent_step'):
            return reply('这一步与当前方程等价，变形正确。继续化简系数，看看未知数应等于多少。', 'confirm')
        return reply('最终作答与参考答案一致，已记录这次练习。你能用一句话说明关键依据吗？' if checked['complete'] and entry['id'] != 'student-linear' else '方程的解正确。代回原方程，两边相等。' if checked['complete'] else guidance(entry, mode, stage), 'confirm')
    if checked['status'] == 'incorrect':
        return reply('这一步还需要调整。' + guidance(entry, 'heuristic', stage), 'ask')
    if mode == 'answer' and decision['allow_final_answer']:
        exact=identity_answer(entry)
        if exact:return reply('由恒等关系比较系数和常数项，再代入所求，参考结果为 $'+exact['display']+'$。'+('这里仅取个位数字。' if exact['units'] else '这是精确乘方形式，不把它展开成长串数字。'),'give_answer')
        values=entry['key']['values'];text='参考结果是 $'+'；'.join(values)+'$。'
        if entry['key']['kind']=='choice' and len(values[0])==1 and entry.get('options'):
            index=ord(values[0])-65
            if 0<=index<len(entry['options']):text+='对应选项内容：'+entry['options'][index]+'。'
        if decision.get('full_walkthrough_requested') and entry.get('analysis'):
            text+='\n'+entry['analysis']
        return reply(text+'如果想理解关键步骤，可以继续问我。', 'give_answer')
    if mode == 'explain':
        text = guidance(entry, 'heuristic', stage)
        if decision['allow_final_answer']:
            exact=identity_answer(entry)
            text = (text if exact else entry.get('analysis') or text) + '\n参考结果：$' + (exact['display'] if exact else '；'.join(entry['key']['values'])) + '$。'
        return reply(text, 'explain')
    return reply(guidance(entry, mode, stage), 'ask')
