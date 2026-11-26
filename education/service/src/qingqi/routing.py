from __future__ import annotations

import re

from .contracts import Request, Route


class Router:
    """Two-stage routing: explicit task data, then lexical evidence/clarification.

    No scorer labels enter here. Rule matches are evidence, not probability.
    Authorization is handled by a separate registry gate.
    """

    def route(self, request: Request) -> Route:
        q = request.question.casefold()
        from .teaching_goals import is_teaching
        if is_teaching(q) and not request.expression and not request.steps and not request.course_query:
            return Route(('tutor',),('clear_concept_or_step_request',))
        intents, basis = [], []
        if request.course_query or re.search(r"课标|教材|章节|哪[一]?章|先修|前置|课程|prerequisite|curriculum", q):
            intents.append("course")
            basis.append("course_query" if request.course_query else "curriculum_terms")
        review_terms = re.search(r"作答|第几步|算错|检查.*步骤|核验|核对|怎么(?:做|算)|分步讲|一步一步|review.*step", q)
        catalog_check = re.search(r"(?:核对|核验).*(?:课程|教材|章节|课标|关联|图谱)|(?:课程|教材|章节|课标|关联|图谱).*(?:核对|核验)", q)
        explicit_work = re.search(r"作答|答案|算式|等式|步骤|计算|算错|怎么(?:做|算)|review.*step", q)
        # “核对教材关联”不是核对学生作答；按对象消歧，保留真实作答的复合意图。
        if request.steps or request.expression or (review_terms and (not catalog_check or explicit_work)):
            intents.append("review")
            basis.append("structured_work" if request.steps or request.expression else "review_terms")
        if request.history or re.search(r"哪里薄弱|学情|学习困难|总是.*错|为什么.*不会|learning.*difficulty", q):
            intents.append("diagnosis")
            basis.append("learning_history" if request.history else "difficulty_terms")
        if re.search(r"个性化|辅导|提示|引导|追问|苏格拉底|hint|tutor", q):
            intents.append("tutor")
            basis.append("teaching_request")
        if "review" in intents and not request.expression:
            return Route(tuple(dict.fromkeys(intents)), tuple(basis), "请提供原题的数值算式；如有作答，请逐步填写等式。")
        if "diagnosis" in intents and not request.history and not request.steps:
            return Route(tuple(dict.fromkeys(intents)), tuple(basis), "请提供最近的实际作答或学习记录，我会据此分析困难候选。")
        if "course" in intents and not request.course_query:
            return Route(tuple(dict.fromkeys(intents)), tuple(basis), "请提供要查询的知识点名称，并尽量说明学科或教材版本。")
        if not intents:
            if re.search(r"你好|谢谢|hello|thanks|聊(?:天|聊)|你在吗|你是谁|讲.*笑话|今天.*(?:开心|累|心情)|有点累|烦恼", q):
                return Route(("chat",), ("greeting",))
            return Route(("clarify",), ("insufficient_task",), "请说一下你想理解的数学概念，或贴出题目和卡住的一步。")
        if "tutor" in intents and len(intents) == 1:
            return Route(("tutor",), tuple(basis), "请提供具体问题或学生作答，才能给出针对性的分步引导。")
        return Route(tuple(dict.fromkeys(intents)), tuple(basis))
