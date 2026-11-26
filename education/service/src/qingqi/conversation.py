from dataclasses import replace
import re

from .layered_routing import COMMANDS, preprocess
from .teaching_policy import FOLLOW_UP, normalize
from .domain_tools import number


def starts_new_problem(question):
    # “换一种方法/换个动画”只改变教学方式；只有题目、话题边界才解绑。
    pattern=r'换(?:一|个|道|一个|一道)?(?:新(?:的)?)?(?:题|问题|话题)|新(?:的)?(?:问题|题目|题|任务)|另一(?:题|个问题)|开始新题|取消|结束当前'
    return any(not re.search(r'(?:不是|没有|不要|不用|不需要|别|无需|不想)(?:再|去|重新|给我|我|说|要|的|这|个|一|道|\s){0,5}$',question[max(0,m.start()-20):m.start()]) for m in re.finditer(pattern,question))


def problem_followup(question):
    """Resolve short teaching requests, never a complete new expression/topic."""
    if starts_new_problem(question) or len(question)>180:return False
    from .presentation import references_problem,request_form
    if references_problem(question) or request_form(question):return True
    if not re.search(r'(?:[fy]\s*(?:\(x\))?\s*=)',question,re.I) and re.search(r'刚才|上面(?:那|这)?(?:一)?道?题|原题|这(?:道|一)?题|小数位|重新.*(?:图解|图示|动画)|(?:改成|改为|换成).*(?:分数|根号)',question):return True
    if re.search(r'(?:[fy]\s*(?:\(x\))?\s*=)|(?:已知|若函数|求解|解方程)|\d\s*[/／]\s*\d|(?:分数|勾股|绝对值|平方根).*\d',question,re.I):return False
    return bool(re.search(r'上面(?:那|这)?(?:一)?道?题|上(?:一|道|个)题|前面.*题|这(?:道|一)?题|刚才|这一步|继续|还是.*不(?:懂|明白)|画(?:个|一张)?图|可视化|图示|图解|动画|重(?:新)?(?:画|绘|给).{0,12}(?:图|动画|表)|(?:用|改成|改为|换成).{0,12}(?:分数|根号|精确)|小数位|不要算干净|换.*(?:方法|讲法|图)|再举.*例|^那.{1,50}呢|(?:直接|给出).*?(?:答案|解答)|完整.*(?:答案|解答)|怎么做|再讲|解释.*(?:上面|这)',question))


def prepare(request, snapshot, recent):
    # 查询保留在会话记录中，但不截断或冒充同题教学历史。
    recent=[turn for turn in recent if not turn.get('query_turn')]
    p = preprocess(request.question)
    task = replace(request, question=p['normalized'])
    new_task = starts_new_problem(task.question)
    pending = None if new_task else snapshot.get('pending')
    prior = snapshot.get('verified_work')
    active_recent = [] if new_task or snapshot.get('expired') or snapshot.get('active_task') is None else recent[:5]
    # Only a verified same-session binding may resolve "这题/刚才/还是不会".
    references = [{'run_id': prior['source_run_id'], 'request': prior}] if prior and not new_task else []
    task, provenance = normalize(task, references, allow_numeric=bool(pending and pending.get('slot') == 'expression'))
    signals = list(provenance)
    if prior and prior.get('expression') and not new_task and not task.expression and problem_followup(task.question):
        # 原题引用也包含画图、动画和“上面那道题”，不能只绑定旧的几句追问词。
        task=replace(task,expression=prior['expression'],steps=prior.get('steps',[]))
        signals.append({'source':'same_session_previous_work','run_id':prior['source_run_id'],'fields':['expression','steps']})
    if pending and pending.get('kind') == 'student_response' and prior and prior.get('expression') and not snapshot.get('expired') and not new_task and not request.expression and not request.steps:
        numeric_text = re.sub(r'[。！？!?]+$', '', task.question).strip()
        literal = r'[+-]?\d+(?:\.\d+)?(?:\s*/\s*[+-]?\d+)?'
        answer = re.fullmatch(r'(?:我的)?(?:答案|结果)(?:是|为|=|：|:)\s*(' + literal + r')', numeric_text)
        if answer:
            numeric_text = answer.group(1)
        equation = prior['expression'] + '=' + numeric_text if re.fullmatch(literal, numeric_text) else numeric_text
        if re.fullmatch(r'[\d\s.+\-*/×÷()（）=]+', equation) and equation.count('=') == 1 and len(equation) <= 120:
            try:
                for side in equation.split('='):
                    number(side.replace('（', '(').replace('）', ')'))
            except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
                pass
            else:
                # 追问中的短答案绑定到当前已核验原题，不能把学生分项重新当成新题。
                task = replace(task, expression=prior['expression'], steps=[{'equation': equation.replace('（', '(').replace('）', ')')}])
                signals.append({'source': 'pending_student_work', 'run_id': prior['source_run_id'], 'fields': ['expression', 'steps']})
    if prior and prior.get('course_query') and not new_task and not task.course_query and re.search(r'那个知识点|这个知识点|该知识点|刚才.*(?:知识点|章节)|它的先修', task.question):
        task = replace(task, course_query=prior['course_query'], subject=task.subject or prior.get('subject', ''))
        signals.append({'source': 'verified_same_session_graph_reference', 'run_id': prior['source_run_id'], 'node_id': prior['node_id'], 'fields': ['course_query', 'subject']})
    literal_command = re.sub(r'[。!?！？]+$', '', task.question) in COMMANDS
    if pending and pending.get('kind') == 'required_slot' and not literal_command and not new_task:
        slot = pending['slot']
        if slot == 'course_query' and not task.course_query and len(task.question) <= 200 and not re.search(r'删除|导出|上传|发送|聊天|你好|核对|数学|算式', task.question):
            task = replace(task, course_query=task.question)
            signals.append({'source': 'pending_slot_response', 'slot': slot, 'run_id': pending['run_id']})
        elif slot == 'history' and not task.history and re.search(r'我|不会|不懂|错|概念|步骤', task.question) and not task.expression:
            task = replace(task, history=[{'kind': 'self_report', 'text': request.question}])
            signals.append({'source': 'pending_slot_response', 'slot': slot, 'run_id': pending['run_id']})
    if literal_command or new_task:
        continuity = 'new_task'
    elif signals and any(s['source'] in {'same_session_previous_work', 'verified_same_session_graph_reference', 'pending_slot_response', 'pending_student_work'} for s in signals) or pending and task.expression and pending.get('slot') == 'expression':
        continuity = 'continuation'
    elif prior and task.expression and task.expression.replace(' ', '') == prior.get('expression', '').replace(' ', ''):
        continuity = 'continuation'
    else:
        continuity = 'new_task'
    context = {**snapshot, 'pending': pending, 'continuity': continuity, 'input_provenance': signals,
               'history_run_ids': [t['run_id'] for t in active_recent]}
    return task, context, active_recent
