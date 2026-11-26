from __future__ import annotations

from .contracts import SHORT, TEXT, obj
from .teaching_responses import calculation_steps, chat_reply, heuristic_prompt, completed_numeric_work


REPLY_SCHEMA = obj({"text": {"type":"string","maxLength":6000}, "teaching_action": {"type": "string", "enum": ["ask", "confirm", "explain", "give_answer", "clarify", "greet", "chat", "recommend", "learning_path", "learning_dashboard"]},
    "evidence_refs": {"type": "array", "items": SHORT, "maxItems": 40},
    "step_refs": {"type": "array", "items": {"type": "integer", "minimum": 0, "maximum": 29}, "maxItems": 30}})
ACTION_SCHEMA = obj({"kind": {"type": "string", "enum": ["call", "respond", "clarify"]}, "tool": SHORT, "arguments": {"type": "object"}, "reply": REPLY_SCHEMA}, ["kind"])


def find(state: dict, name: str):
    return next((o["result"] for o in state["observations"] if o["tool"] == name), None)


TOOL_INTENTS = {"course_search": "course", "worker_course8b": "course", "course_context": "course",
                "review_arithmetic": "review", "worker_review27b": "review",
                "difficulty_candidates": "diagnosis", "worker_difficulty8b": "diagnosis"}
TOOL_INTENTS.update({'recommend_practice':'recommend','preview_learning_path':'learning_path','read_learning_dashboard':'learning_dashboard'})


def next_tool_intent(state):
    # 原先只记录上游调度结果，领域计划仍用硬编码顺序；现在使用其真实拓扑顺序选择节点。
    tasks = {node["id"]: node["intent"] for node in state["route"]["task_dag"]["nodes"]}
    done = {"course": find(state, "course_context") is not None,
            "review": find(state, "review_arithmetic") is not None or find(state, "worker_review27b") is not None,
            "diagnosis": find(state, "difficulty_candidates") is not None or find(state, "worker_difficulty8b") is not None,
            "recommend":find(state,'recommend_practice') is not None,
            "learning_path":find(state,'preview_learning_path') is not None,
            "learning_dashboard":find(state,'read_learning_dashboard') is not None}
    for node_id in state["native_schedule"]["order"]:
        intent = tasks[node_id]
        if intent in done and not done[intent]:
            return intent
    return None


class OfflineController:
    name = "offline_rules_and_symbolic_v2"
    uses_model = False

    def next(self, request, state, context, registry):
        intents = state["route"]["intents"]
        command = state['route'].get('command')
        if command in {'cancel', 'new_task'}:
            return reply('已结束当前任务。你可以直接提出新问题，我会重新判断需要哪种帮助。', 'chat')
        if command == 'capabilities':
            return reply('我可以自动判断是否需要课程查询、作答检查、启发式追问、分步讲解或闲聊。请直接描述需求；检查作答时提供原题与步骤。', 'chat')
        if intents == ('chat',) or intents == ['chat']:
            text, action = chat_reply(request.question)
            return reply(text, action)
        search = find(state, "course_search")
        course = find(state, "course_context")
        checked = find(state, "review_arithmetic") or find(state, "worker_review27b")
        diagnosed = find(state, "difficulty_candidates") or find(state, "worker_difficulty8b")
        current_intent = next_tool_intent(state)
        if current_intent == "course":
            if search is None:
                return {"kind": "call", "tool": "course_search", "arguments": {"query": request.course_query, "subject": request.subject}}
            if not search["matches"]:
                return reply("图谱中没有找到该知识点。请补充准确名称、学科或教材版本。", "clarify")
            if search["ambiguous"]:
                choices = "；".join(f'{m["title"]}（{m["scope"]}）' for m in search["matches"])
                return reply("找到多个候选，请说明你使用的教材或知识点：" + choices, "clarify")
            if course is None:
                return {"kind": "call", "tool": "course_context", "arguments": {"node_id": search["matches"][0]["id"]}}
        if current_intent == "review" and checked is None:
            tool = "worker_review27b" if "worker_review27b" in state["allowed_tools"] else "review_arithmetic"
            return {"kind": "call", "tool": tool, "arguments": {"expression": request.expression, "steps": request.steps, "mode": request.mode}}
        if current_intent == "diagnosis" and diagnosed is None:
            tool = "worker_difficulty8b" if "worker_difficulty8b" in state["allowed_tools"] else "difficulty_candidates"
            args = {"history": state["diagnosis_history"]}
            if checked:
                args["review"] = checked
            return {"kind": "call", "tool": tool, "arguments": args}
        refs = [e["ref"] for o in state["observations"] for e in o["result"].get("evidence", [])]
        fragments, action, steps = [], "ask", []
        if course:
            mapping = "、".join(a["title"] for a in course["ancestors"] if a["type"] in {"Chapter", "Section", "SubSection"})
            fragments.append(f'课程定位：{course["title"]}（{course["scope"]}）' + (f'，教材关联：{mapping}。' if mapping else "。当前未找到可确认的章节关联。"))
            if course["prerequisite_candidates"]:
                fragments.append("公开论文图谱提供先修候选：" + "、".join(p["title"] for p in course["prerequisite_candidates"]) + "；同名对齐尚未专家确认，只用于参考。")
            else:
                fragments.append("该节点暂无可确认的先修关系证据。")
        if checked:
            complete = checked['status'] == 'correct' and completed_numeric_work(request.expression, request.steps)
            if checked["status"] == "unsupported":
                return reply("当前工具只能核验数值等式，无法判断这份作答。请提供原题的数值算式和对应步骤，或使用支持该题型的审查服务。", "clarify", refs)
            if checked["status"] == "correct":
                fragments.append("你提供的数值等式均通过核验，无需纠正。")
                if not complete:
                    fragments.append('这一步正确。请把结果代回原题，继续写出剩余运算与最终数值，我再核对。')
                elif request.mode == 'socratic':
                    fragments.append('能解释一下为什么按这个顺序计算吗？')
                action = "confirm"
                steps = list(range(len(request.steps)))
            elif checked["status"] == "incorrect":
                i = checked["first_error"]
                prompt = heuristic_prompt(request.expression) if state['route']['teaching']['mode'] == 'heuristic' else '请分别算等号两边，并与原题数值比较：它们是否相等？'
                fragments.append(f'先看第 {i + 1} 步「{request.steps[i]["equation"]}」。' + (prompt if request.mode == 'socratic' else '这一步没有保持原式的数值。'))
                steps = [i]
            else:
                if request.mode == 'socratic':
                    fragments.append(heuristic_prompt(request.expression) if state['route']['teaching']['mode'] == 'heuristic' else "你准备先做哪一步？请写出等式，我再检查。")
                elif request.mode == 'explain':
                    fragments.append('还没有提交作答步骤，我先按原题讲解。')
            if request.mode == "answer" and not complete:
                fragments.append("原题的精确数值结果是 " + checked["answer"] + "。")
                action = "give_answer"
            elif request.mode == "explain" and checked['status'] != 'correct':
                fragments.append(calculation_steps(request.expression, allow_final_answer=state['route']['teaching']['allow_final_answer']))
                action = "explain"
        if diagnosed:
            names = {"calculation_or_procedure": "计算或步骤问题", "concept_candidate": "概念理解困难", "procedure_candidate": "运算顺序或步骤困难", "insufficient_evidence": "暂时缺少判断依据",
                     "recall_failure_candidate": "知识回忆困难候选", "conceptual_gap_candidate": "概念理解困难候选",
                     "procedural_error_candidate": "解题步骤困难候选", "transfer_deficit_candidate": "知识迁移困难候选"}
            fragments.append("当前需要确认的问题：" + "、".join(names.get(c, "其他学习困难") for c in diagnosed["candidates"]) + "。请解释你的作答思路，我再判断是否需要相应提示。")
            fragments.append(diagnosed["strategy"])
        if not fragments:
            fragments = ["你好，我可以查询课程、核验数值作答，并根据学习记录提供分步引导。"]
            action = "greet"
        if state['route'].get('unresolved_clauses'):
            fragments.append('另有一项需求尚未支持或识别：'+'；'.join(state['route']['unresolved_clauses'])+'。这部分没有执行，请明确需要的功能。')
        if 'chat' in intents and len(intents) > 1:
            fragments.append(chat_reply(request.question)[0])
        return reply("\n".join(fragments), action, refs, steps)


def reply(text, action, refs=None, steps=None):
    return {"kind": "clarify" if action == "clarify" else "respond", "reply": {"text": text, "teaching_action": action, "evidence_refs": list(dict.fromkeys(refs or [])), "step_refs": steps or []}}
