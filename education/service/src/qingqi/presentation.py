"""Pure presentation preferences, separate from pedagogy and problem ownership."""
import re


def request_form(question):
    # 能力反问“你不能创建故事吗”是请求，不能误当成“不要故事”。
    from .request_controls import strip_denied
    positive,negative=strip_denied(question,r'故事|情景|情境|场景')
    if re.search(r'故事|情景|情境|场景',positive):
        from .visual_tasks import refuses_animation,wants_animation
        animation='off' if refuses_animation(question) or '文字' in question and not wants_animation(question) else 'on'
        return {'kind':'story','animation':animation,'requested':True,'source':'current_student_request'}
    if negative:return {'kind':'text','requested':True,'source':'current_student_request'}
    return None


def references_problem(question):
    return bool(re.search(r'上(?:一(?:个|道|次)?|个|道)(?:题目|题|问题|练习)|同一(?:道|个)?(?:题目|题|问题)|题目(?:就是|还是|没换)|刚才|原题',question))


def resolve(question,snapshot,recent,*,continuing=False):
    current=request_form(question)
    if current:return current
    if not continuing:return {'kind':'text','requested':False,'source':'default'}
    if snapshot.get('presentation'):
        return {**snapshot['presentation'],'requested':False,'source':'same_problem_preference'}
    if references_problem(question):
        # 旧版误澄清没有接受呈现偏好；只从同题学生请求恢复，不读导师推断。
        from .conversation import starts_new_problem
        for turn in recent:
            if turn.get('command') in {'cancel','new_task'} or starts_new_problem(turn['student_question']):break
            form=request_form(turn['student_question'])
            if form:return {**form,'requested':False,'source':'same_problem_student_request'}
    return {'kind':'text','requested':False,'source':'default'}


def story_basis(entry,allow_final_answer=False):
    """Compile a supported problem's quantitative story; the model supplies prose only."""
    from .practice_tutoring import lesson,linear
    info=lesson(entry)
    if info['kind']!='substitution':return None
    x,y=info['given_variable'],info['variable']
    colors={x:'蓝色',y:'紫色'}
    def rule(expression):
        coefficients,offset=linear(expression)
        parts=[f"{colors[var]}积分计入 ${value}$ 份" for var,value in sorted(coefficients.items())]
        if offset:parts.append(f'另调整 ${offset}$ 积分')
        return '，'.join(parts)
    lhs,total=info['equation'].split('=')
    # 真实模型曾把2x+y说成两个人都翻倍；规则由当前原式系数编译，不能自由改写。
    text=f'在这个故事里，蓝色记录器的积分记为 ${x}$，紫色记为 ${y}$。\n'
    text+='方程组的解表示：同一对积分必须同时满足这两种记账规则，因此要用同一组已知值核对各条规则。\n'
    text+=f"第一种记账规则：{rule(info['masked_expression'])}，合计为 $★$，对应 ${info['masked_expression']}=★$。\n"
    text+=f"第二种记账规则：{rule(lhs)}，合计为 ${total}$，对应 ${info['equation']}$。\n"
    text+=f"题目已知蓝色积分 ${x}={info['given']}$。先把它放入第二种规则，求紫色积分，再回到第一种规则求 $★$。"
    if allow_final_answer:
        values=entry['key']['values'];text+='\n按原题顺序，参考答案为 $'+'；'.join(values)+'$。'
    else:text+='最终的两个数先保留，让你尝试计算。'
    compact=f"蓝色记录器记为 ${x}$，紫色记为 ${y}$。方程组的解表示同一对积分同时符合两条记账规则。"
    compact+=f"第二条规则：{rule(lhs)}，合计 ${total}$，即 ${info['equation']}$。已知 ${x}={info['given']}$，先代入这一条，再回到第一条记账规则。"
    compact+=('参考答案为 $'+'；'.join(entry['key']['values'])+'$。') if allow_final_answer else '两个最终数先保留，请尝试写出代入后的等式。'
    return {'setup':'小林正在设计一个彩色积分小游戏，要用不同的记账规则记录积分。我们来帮他看懂这份账本。','compact_text':compact,
            'text':text,'equation':info['equation'],'source':'owned_equation_coefficients'}


def story_opening_ok(text):
    # 模型只补充场景开场；数字、公式和定量关系必须由原题编译器负责。
    return bool(text.strip() and len(text)<=200 and not re.search(r'\d|\$|[=<>]|倍|双份|均分|相加|相减|相等|等于|总数|总和|乘以|除以|平方|根号|每[^。]{0,12}份|你已经|掌握|抓住|做对|正确答案',text))
