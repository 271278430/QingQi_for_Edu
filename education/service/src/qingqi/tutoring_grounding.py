"""Speaker-separated teaching evidence; assistant explanations never prove student progress."""
import re
from .contracts import ContractError


INSTRUCTIONS=('dialogue_evidence严格区分学生文字、服务端核验和导师已给出的提示。'
              '导师讲过的结论不能说成学生自己发现；继续、不会、再提示和提示次数不证明学生已完成步骤。'
              '没有核验依据时不说“你已经抓住/理解/掌握/求出了”。可以中性说明“这里需要考虑…”或“我们继续看…”。'
              '只有current_assessment.status=correct能确认本轮对应步骤；它也不证明知识点已经掌握。'
              '连续求提示时参考teacher_hints和历史导师回复，增加当前卡点的具体帮助，不跳到假定完成的后续步骤。')


def evidence(payload,state):
    turns=payload.get('history') or []
    marker=state.get('practice_hint') or {}
    return {'student_messages':[t.get('question','') for t in turns],
            'teacher_messages':[t.get('reply','') for t in turns],
            'current_student_message':payload.get('question',''),
            'current_assessment':state.get('practice_assessment') or {'status':'unverified'},
            'teacher_hints':state.get('practice_hint_history',marker.get('hints',[])),
            'hint_level':min(marker.get('count',len(state.get('practice_hint_history',[]))),2),
            'rule':'Teacher messages/hint level are assistance offered, never student work or mastery.'}


def validate_attribution(text,payload,state):
    # 旧校验只拦confirm动作，ask/explain正文仍会虚构学生已掌握；同样约束自然文字。
    if re.search(r'你(?:已经?|已|现在|刚才)?(?:已经)?(?:基本|完全|确实|真正|很好地|正确地|终于)?(?:掌握了|理解了|明白了|抓住了|领会了|懂得了|学会了|懂了)',text):
        raise ContractError('Unsupported student mastery attribution: teacher hints are not student conclusions. Use neutral guidance without saying the student already understood.')
    assessment=state.get('practice_assessment') or {}
    verified=assessment.get('status')=='correct'
    if not verified and re.search(r'你(?:已经?|已|刚才|现在).{0,12}(?:求出|算出|得出|答对|做对)|(?:你的|这一步|刚才的)(?:答案|作答|计算|步骤)?(?:是|已经|完全|都|确实)?正确',text):
        raise ContractError('Unsupported student work confirmation: no verified current student step. Explain the condition without inventing completed work.')
    student=' '.join([payload.get('question',''),*[t.get('question','') for t in payload.get('history',[])]] )
    compact=lambda value:re.sub(r'[\s$，,。.!！“”"‘’]', '', value)
    for claim in re.finditer(r'你(?:刚才|已经?|已)?(?:说|提到|写下|指出)[^。！？\n]{0,8}[“"‘]([^”"’]+)[”"’]',text):
        if compact(claim[1]) not in compact(student):
            raise ContractError('Quoted conclusion came from the teacher rather than student messages. Attribute it to the condition or previous hint.')


def validate_identity_target(text,state):
    entry=state.get('practice_entry')
    if not entry:return
    from .practice_tutoring import identity_lesson
    info=identity_lesson(entry)
    if not info:return
    flat=re.sub(r'[\s$]', '',text).replace('−','-')
    for match in re.finditer(r'(?:由|根据|在)\(?([A-Za-z])([+\-])(\d+)=0\)?[，,:：]([+\-]?\d+)(?:应该|需要|必须|要)(?:等于|取|是)',flat):
        if match[1] in {info['variable'],info['other_variable']} and abs(int(match[3]))==abs(int(match[4])):
            # 数学对象错误先于格式/追问数量核验，避免修复循环只处理句式而丢失变量。
            raise ContractError('identity_variable_question: ask for the unknown variable, not the fixed known number')
