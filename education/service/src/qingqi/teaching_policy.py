"""Auditable teaching-mode selection; no remote classifier is used by default.

Route WHAT needs doing separately from HOW to help. Request identity, tool
permissions and input provenance are not controlled by a model or by memory.
"""
from __future__ import annotations

import re
from dataclasses import replace

from .domain_tools import number
from .request_controls import NEGATION,negated_before,strip_denied,answer_directives

VERSION = 'teaching_policy_v20'
LABELS = {'socratic': '苏格拉底式教学', 'heuristic': '启发式提示', 'explain': '分步讲解', 'answer': '参考解答',
          'confirm': '确认正确作答', 'chat': '闲聊', 'course': '课程查询', 'clarify': '先澄清问题'}
LABELS.update({'recommend':'相似练习','learning_path':'学习路径','learning_dashboard':'学情摘要','unsupported':'需求说明'})
PREFERENCES = {
    'socratic': r'苏格拉底|追问|引导我',
    'heuristic': r'启发式(?:提示|教学)?|(?:给|来|要|先).*?(?:提示|启发)|只(?:需|要).*?提示|hint',
    'explain': r'分步讲解|分步讲|一步一步|一步步|逐步讲|从头.{0,4}(?:讲|解)|完整(?:讲解|解答|解法|解题步骤|解题过程)|详细(?:讲|解释)|讲(?:清楚|明白)|解释.*(?:步骤|顺序)|从基础',
}
FULL_WALKTHROUGH = r'完整[^，,。；;！？\n]{0,12}(?:解法|解答|讲解|解题步骤|解题过程)|从头讲|全过程|所有步骤'
STRUGGLE = r'还是(?:不会|不懂|不明白|没懂)|仍(?:然)?(?:不会|不懂|不明白)|没听懂|听不懂|提示.*(?:不够|没用)|卡住|再讲|不明白'
FOLLOW_UP = r'这(?:道题|一步|题)|刚才|上一(?:题|步)|还是(?:不会|不懂|不明白|没懂)|继续|再讲|没听懂|仍然不懂|从头讲|讲清楚|讲明白|分步讲解'
MATH_TEXT = r'算|数学|答案|结果|等于|怎么做|步骤|运算|对吗|对不对|检查|核对|提示|讲解'
NUMERIC_CHUNK = re.compile(r'(?<![A-Za-z0-9_.])[-+\d(（][\d\s.+\-*/×÷()（）=]{1,119}')


def normalize(request, recent, *, allow_numeric=False):
    """Parse bounded numeric expressions actually written in the current message.

    Otherwise reuse prior work ONLY for an explicit same-session reference.
    A numeric expression is not guessed from unrelated cross-session memory.
    """
    provenance = []
    expression, steps = request.expression, request.steps
    if not expression and (allow_numeric or re.search(MATH_TEXT, request.question) or re.fullmatch(r'[\d\s.+\-*/×÷()（）=]+', request.question.strip())):
        chunks = []
        for match in NUMERIC_CHUNK.finditer(request.question):
            text = match.group().strip().replace('（', '(').replace('）', ')')
            if not re.search(r'[+\-*/×÷]', text) or len(re.findall(r'\d+', text)) < 2:
                continue
            if match.end() < len(request.question) and re.match(r'[A-Za-z_]', request.question[match.end()]):
                continue
            pieces = [p.strip() for p in text.split('=')]
            if len(pieces) not in {1, 2}:
                continue
            try:
                for p in pieces:
                    number(p)
            except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
                continue
            chunks.append((pieces[0], text if len(pieces) == 2 else None))
        # Multiple different parent expressions are ambiguous; ask instead.
        if chunks and len({c[0] for c in chunks}) == 1:
            expression = chunks[0][0]
            if not steps:
                steps = [{'equation': eq} for _, eq in chunks if eq]
            provenance.append({'source': 'current_message_numeric_text', 'fields': ['expression', 'steps']})
    if not expression and recent and re.search(FOLLOW_UP, request.question):
        prior = recent[0]['request']
        if prior.get('expression'):
            expression = prior['expression']
            steps = steps or prior.get('steps', [])
            provenance.append({'source': 'same_session_previous_work', 'run_id': recent[0]['run_id'], 'fields': ['expression', 'steps']})
    return replace(request, expression=expression, steps=steps), provenance


def _positive_preferences(question):
    found = []
    for mode, pattern in PREFERENCES.items():
        for m in re.finditer(pattern, question, re.IGNORECASE):
            if negated_before(question,m.start()):
                continue
            if mode == 'explain' and m.group().startswith('怎么') and re.search(r'检查|核验', question):
                continue
            found.append((m.start(), mode, m.group()))
    found.extend((event['at'],'answer',event['text']) for event in answer_directives(question) if event['allowed'])
    return sorted(found)


def choose(request, route, recent, *, continuing_problem=False, prior_no_answer=False, learner=None, problem=None, prior_no_questions=False, prior_mode=None, current_part=None, prior_disclosed=False):
    from .teaching_goals import goal
    from .teaching_plan import build
    q = request.question
    preferences = _positive_preferences(q)
    directives=answer_directives(q)
    explicit_answer = request.mode == 'answer' or bool(directives and directives[-1]['allowed'])
    # 被否定的完整解答不能反向授权长解或答案，完整讲解许可必须来自正向命令。
    positive_walkthrough=strip_denied(q,FULL_WALKTHROUGH,distance=16)[0]
    full_walkthrough = request.mode=='explain' or bool(re.search(FULL_WALKTHROUGH,positive_walkthrough)) or bool(directives and directives[-1]['allowed'] and re.search(r'全部|所有|完整',directives[-1]['text']))
    # 最新命令优先于旧教学偏好；不能漏掉“答案全部给我”，或让较早的否定锁死后续授权。
    no_answer = not directives[-1]['allowed'] if directives else bool(prior_no_answer and continuing_problem and not (explicit_answer or full_walkthrough))
    purpose=goal(q)
    # 否定只能修饰邻近的追问，不能把“不要答案，请追问”错误理解成禁止追问。
    no_questions=bool(re.search(NEGATION+r'(?:再|一直|总是|总|给我|继续|那么多|老是|先){0,4}(?:反问|追问|问我)',q))
    no_questions=no_questions or bool(prior_no_questions and continuing_problem and not any(p[1] in {'socratic','heuristic'} for p in preferences))
    automatic_scaffold = False
    # 教法与答案许可分开：未授权完整答案可以解释当前一步，不必把所有情形都退回追问。
    mode, reason, evidence = 'heuristic', '先给一条与当前题有关的线索，让学生有可执行的起点。', []
    mode_source='adaptive_context'
    old_mode=(prior_mode or {}) if continuing_problem else {}
    if current_part is not None and old_mode.get('part') not in {None,current_part}:old_mode={}
    if request.mode != 'auto':
        mode, reason = request.mode, '学生手动指定了本次辅导方式。'
        evidence = [{'source': 'request_mode', 'value': request.mode}]
        mode_source='current_request'
    else:
        if preferences:
            _, mode, phrase = preferences[-1]
            if mode=='heuristic' and any(p[1]=='socratic' and re.search('苏格拉底|追问',p[2]) for p in preferences) and not re.search('改成|改为|切换|启发式',q):
                _,mode,phrase=next(p for p in reversed(preferences) if p[1]=='socratic')
            reason = {'socratic': '学生明确请求提示或追问，先保留思考空间。',
                      'heuristic': '学生明确请求启发式提示，给出可执行的思考线索。',
                      'explain': '学生明确请求从头或逐步讲解。', 'answer': '学生明确请求直接核对答案。'}[mode]
            evidence = [{'source': 'current_question', 'text': phrase}]
            mode_source='current_request'
        elif no_questions:
            mode,reason='explain','学生要理解概念或要求直接解释，先回答当前卡点。'
            automatic_scaffold=True
            evidence=[{'source':'current_learning_goal','value':purpose}]
        elif re.search(STRUGGLE,q) and continuing_problem:
            mode,reason='explain','学生反馈仍未理解，改为解释当前步骤的操作与依据。'
            automatic_scaffold=True
            evidence=[{'source':'same_session_feedback','run_id':t['run_id']} for t in recent[:2]]
        elif purpose=='hint':
            mode,reason='heuristic','当前需要提示，给出一条能动手尝试的线索。'
            automatic_scaffold=True
        elif purpose=='concept' or purpose=='step' and re.search(r'为什么|解释|讲清楚|讲明白|不懂|不会|不明白',q):
            mode,reason='explain','先回答当前概念或为什么成立，再解释一小步。'
            automatic_scaffold=True
        elif old_mode.get('mode') in {'socratic','heuristic','explain','answer'}:
            mode=old_mode['mode'] if old_mode['mode']!='answer' else 'explain'
            reason='沿用同一题当前小问的教学方式，继续处理当前步骤。'
            mode_source='same_problem_context'
            evidence=[{'source':'teaching_mode','run_id':old_mode.get('source_run_id')}]
        elif request.expression or continuing_problem:
            # 所属题与图片辅导已绑定完整题干，不必有数值 expression 才能升级帮助。
            related = [t for t in recent if t['request'].get('expression', '').replace(' ', '') == request.expression.replace(' ', '')] if request.expression else recent
            prompted = [t for t in related if t['response']['teaching_action'] == 'ask']
            inherited = None
            if re.fullmatch(r'[\d\s.+\-*/×÷()（）=]+', q.strip()):
                for turn in related:
                    explicit = _positive_preferences(turn['request']['question'])
                    prior_mode = turn['request'].get('mode', 'auto')
                    selected = prior_mode if prior_mode != 'auto' else explicit[-1][1] if explicit else None
                    if selected:
                        inherited = (selected, turn['run_id'])
                        break
            # 撤掉模式表单后，短作答仍须保留学生同题明确的提示偏好。
            if inherited and inherited[0] in {'socratic', 'heuristic'}:
                mode, reason = inherited[0], '沿用同一题最近明确的提示偏好，先核对当前作答。'
                evidence = [{'source': 'same_session_teaching_preference', 'run_id': inherited[1]}]
            elif prompted and re.search(STRUGGLE, q):
                mode, reason = 'explain', '学生仍不理解，解释当前步骤的操作与依据。'
                automatic_scaffold = True
                evidence = [{'source': 'same_session_feedback', 'run_id': t['run_id']} for t in prompted[:2]]
            elif len(prompted) >= 2 and request.steps:
                mode, reason = 'explain', '已有多次提示，补充当前卡点的依据，保留最终结果。'
                automatic_scaffold = True
                evidence = [{'source': 'same_session_feedback', 'run_id': t['run_id']} for t in prompted[:2]]
            else:
                reason = '根据已提交的题目或步骤先定位问题，首次辅导优先提示。'
    if no_answer and mode == 'answer':
        mode, reason = 'heuristic', '学生要求不直接给答案，改为给当前步骤的线索。'
        evidence.append({'source': 'current_question', 'text': '不直接给答案'})
    if no_questions and mode in {'socratic','heuristic'}:
        mode,reason='explain','学生要求停止反问，直接解释当前问题。'
    # 逐步是内容组织，苏格拉底是互动方式，二者不能因关键词顺序互相覆盖。
    combined=bool(not no_questions and mode!='answer' and request.mode in {'auto','socratic'} and any(p[1]=='socratic' for p in preferences)
                  and re.search(r'逐步|分步|一步一步|一步步|从头',q))
    if combined:
        mode,reason='socratic','按逐步引导组织内容：简短解释当前一步，再给一个学生推理任务。'
        automatic_scaffold=True
    p=(learner or {}).get('current_topic') or {}
    if request.mode=='auto' and not preferences and purpose=='solve' and p.get('recent_independent_attempts',0)>=3 and (p.get('accuracy') or 0)<60:
        mode='explain'
        reason='相关近期作答需要更多支撑，先给可执行线索或拆解当前步骤。'
        automatic_scaffold=True
        evidence=[{'source':'recent_independent_work','attempts':p['recent_independent_attempts'],'accuracy':p['accuracy']}]
    elif request.mode=='auto' and not preferences and not old_mode and purpose=='solve' and p.get('recent_independent_attempts',0)>=3 and (p.get('accuracy') or 0)>=80:
        mode='socratic';reason='相关近期独立作答较熟练，用一个针对性的推理问题帮助迁移。'
        evidence=[{'source':'recent_independent_work','attempts':p['recent_independent_attempts'],'accuracy':p['accuracy']}]
    if automatic_scaffold and recent and re.search(STRUGGLE,q):
        prior=[{'source':'same_session_feedback','run_id':t['run_id']} for t in recent if t['response']['teaching_action']=='ask'][:2]
        evidence=prior+evidence
    display = mode
    if route.clarify:
        display, reason = 'clarify', '缺少完成任务所需的题目、作答或课程信息，先补充信息。'
    elif route.intents == ('chat',):
        display, reason = 'chat', '当前是日常交流，没有需要核验的教学任务。'
    elif route.intents == ('course',):
        display, reason = 'course', '当前需要查询课程与教材依据。'
    if mode!='answer' and (purpose=='concept' or no_questions):automatic_scaffold=True
    result={'version': VERSION, 'requested_mode': request.mode, 'mode': mode, 'display_mode': display,
            'label': LABELS[display], 'reason': reason, 'evidence': evidence,'source':mode_source,
            'goal':purpose,'no_questions':no_questions,'no_questions_requested':no_questions,
            'no_final_requested': no_answer, 'automatic_scaffold': automatic_scaffold,
            'full_walkthrough_requested':full_walkthrough,
            'allow_final_answer': mode in {'answer', 'explain'} and not no_answer and (explicit_answer or full_walkthrough or continuing_problem and prior_disclosed)}
    if result['allow_final_answer'] and prior_disclosed and not explicit_answer and not full_walkthrough:
        result['evidence'].append({'source':'same_problem_already_published_solution','part':current_part})
    result['plan']=build(request,result,learner,problem)
    result['budget']=result['plan']['budget']
    if result['plan']['content_style']=='stepwise' and result['plan']['interaction_style']=='guided_question':result['label']='逐步引导'
    return result


def final_decision(initial, result, checked):
    decision = dict(initial)
    action = result['teaching_action']
    mode = {'ask':'socratic','explain':'explain','give_answer':'answer','clarify':'clarify','greet':'chat','chat':'chat','confirm':'confirm',
            'recommend':'recommend','learning_path':'learning_path','learning_dashboard':'learning_dashboard'}[action]
    if action == 'ask' and initial['mode'] == 'heuristic':
        mode = 'heuristic'
    if initial['display_mode'] == 'course' and action != 'clarify':
        mode = 'course'
    decision.update(display_mode=mode, label=LABELS[mode])
    if (initial.get('plan') or {}).get('content_style')=='stepwise' and (initial.get('plan') or {}).get('interaction_style')=='guided_question' and action in {'ask','explain'}:
        decision['label']='逐步引导'
    elif initial.get('label') in {'图示辅助','图片内容解读'} and action=='explain':decision['label']=initial['label']
    elif (initial.get('plan') or {}).get('goal')=='concept' and action=='explain':decision['label']='概念解释'
    elif (initial.get('plan') or {}).get('goal')=='check' and action in {'ask','confirm','explain'}:decision['label']='作答核对'
    if action == 'confirm':
        decision['reason'] = '实际作答已经通过核验，先确认正确，不制造错误。'
    elif checked and checked['status'] == 'unsupported':
        decision['reason'] = '当前工具无法判断该题型，先澄清而不猜测答案。'
    return decision
