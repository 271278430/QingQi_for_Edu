from __future__ import annotations

import ast
import copy
from fractions import Fraction

from .contracts import EVIDENCE, HISTORY, SHORT, STEP, TEXT, ToolSpec, obj


def number(expression: str) -> Fraction:
    """Bounded AST arithmetic, no eval, names, attributes, calls or powers."""
    if len(expression) > 120:
        raise ValueError("expression too long")
    tree = ast.parse(expression.replace("×", "*").replace("÷", "/"), mode="eval")
    if len(list(ast.walk(tree))) > 80:
        raise ValueError("expression too complex")

    def walk(n):
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            value = Fraction(str(n.value))
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.UAdd, ast.USub)):
            value = walk(n.operand) * (-1 if isinstance(n.op, ast.USub) else 1)
        elif isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            left, right = walk(n.left), walk(n.right)
            if isinstance(n.op, ast.Add):
                value = left + right
            elif isinstance(n.op, ast.Sub):
                value = left - right
            elif isinstance(n.op, ast.Mult):
                value = left * right
            else:
                value = left / right
        else:
            raise ValueError("only finite numeric + - * / expressions are supported")
        if abs(value.numerator) > 10**15 or value.denominator > 10**15:
            raise ValueError("numeric bound exceeded")
        return value

    return walk(tree.body)


def review(expression: str, steps: list[dict], mode: str) -> dict:
    expected = number(expression)
    checks, first, unsupported = [], -1, False
    working = ast.parse(expression.replace("×", "*").replace("÷", "/"), mode="eval").body
    for i, step in enumerate(steps):
        try:
            pieces = step["equation"].split("=")
            if len(pieces) != 2:
                raise ValueError("a step must contain exactly one equality")
            left, right = [number(p) for p in pieces]
            equal = left == right
            lhs = ast.parse(pieces[0].replace("×", "*").replace("÷", "/"), mode="eval").body
            rhs = ast.parse(pieces[1].replace("×", "*").replace("÷", "/"), mode="eval").body
            matched = False
            key = ast.dump(lhs, include_attributes=False)
            class ReplacePart(ast.NodeTransformer):
                def generic_visit(self, node):
                    nonlocal matched
                    if not matched and ast.dump(node, include_attributes=False) == key:
                        matched = True
                        return copy.deepcopy(rhs)
                    return super().generic_visit(node)
            candidate = ReplacePart().visit(copy.deepcopy(working))
            # 正确分项可替换当前原题的子表达式；无关等式仍不能凭数值相等获得授权。
            preserved = matched or left == number(ast.unparse(working))
            valid = equal and preserved
            checks.append({"index": i, "valid": valid, "reason": "valid" if valid else "false_equality" if not equal else "changed_problem_value"})
            if not valid and first == -1:
                first = i
            if matched:
                working = candidate
            elif preserved:
                working = rhs
        except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as exc:
            unsupported = True
            checks.append({"index": i, "valid": False, "reason": "unsupported_step:" + str(exc)[:100]})
            if first == -1:
                first = i
    status = "unsupported" if unsupported else "no_steps" if not steps else "correct" if first == -1 else "incorrect"
    if unsupported:
        first = -1
    return {"status": status, "first_error": first, "answer": str(expected), "checks": checks,
            "mode": mode, "domain": "exact_numeric_value_preserving_equalities",
            "evidence": [{"ref": f"step:{i}", "text": s["equation"], "source": "current_student_work"} for i, s in enumerate(steps)]}


def difficulty(history: list[dict], review: dict | None = None) -> dict:
    evidence, labels = [], []
    if review and review.get("first_error", -1) >= 0:
        i = review["first_error"]
        labels.append("calculation_or_procedure")
        evidence.append({"ref": f"step:{i}", "text": "数值等式未通过核验；仍需追问原因", "source": "symbolic_review"})
    for i, event in enumerate(history):
        text = event["text"]
        if any(t in text for t in ("不理解", "概念", "什么意思")):
            labels.append("concept_candidate")
        if any(t in text for t in ("顺序", "先算", "步骤", "漏", "算错")):
            labels.append("procedure_candidate")
        evidence.append({"ref": f"history:{i}", "text": text[:1000], "source": event["kind"]})
    if not labels:
        labels = ["insufficient_evidence"]
    strategy = "请解释你怎样确定运算顺序，我会根据你的理由给一项提示。"
    if "concept_candidate" in labels:
        strategy = "请先用自己的话解释这个概念并举一个例子，我再给你一项提示。"
    elif labels == ["insufficient_evidence"]:
        strategy = "请提供一道最近做过的题和你的实际步骤，我再给针对性的建议。"
    return {"candidates": list(dict.fromkeys(labels)), "certainty": "candidate_requires_confirmation",
            "strategy": strategy, "evidence": evidence}


ARRAY_EVIDENCE = {"type": "array", "items": EVIDENCE, "maxItems": 40}
MATCH = obj({"id": SHORT, "title": TEXT, "scope": SHORT, "type": SHORT, "source": TEXT})
SEARCH_OUT = obj({"matches": {"type": "array", "items": MATCH, "maxItems": 5}, "ambiguous": {"type": "boolean"}, "method": SHORT})
CONTEXT_OUT = obj({"node_id": SHORT, "title": TEXT, "scope": SHORT,
    "ancestors": {"type": "array", "items": obj({"id": SHORT, "title": TEXT, "type": SHORT, "relation": SHORT}), "maxItems": 12},
    "prerequisite_candidates": {"type": "array", "items": obj({"id": SHORT, "title": TEXT, "status": SHORT}), "maxItems": 12},
    "evidence": ARRAY_EVIDENCE, "prerequisite_status": SHORT})
REVIEW_OUT = obj({"status": {"type": "string", "enum": ["no_steps", "correct", "incorrect", "unsupported"]}, "first_error": {"type": "integer", "minimum": -1, "maximum": 29}, "answer": SHORT,
    "checks": {"type": "array", "items": obj({"index": {"type": "integer", "minimum": 0}, "valid": {"type": "boolean"}, "reason": SHORT}), "maxItems": 30},
    "mode": {"type": "string", "enum": ["socratic", "explain", "answer"]}, "domain": SHORT, "evidence": ARRAY_EVIDENCE})
DIAG_OUT = obj({"candidates": {"type": "array", "items": SHORT, "maxItems": 8}, "certainty": SHORT, "strategy": TEXT, "evidence": ARRAY_EVIDENCE})
SPECS = {
    "course_search": ToolSpec("course_search", "Search actual curriculum KG titles; returns ambiguity and original node IDs.", obj({"query": SHORT, "subject": TEXT}), SEARCH_OUT, "mcp"),
    "course_context": ToolSpec("course_context", "Read textbook/standard ancestors and explicitly unverified prerequisite candidates.", obj({"node_id": SHORT}), CONTEXT_OUT, "mcp"),
    "review_arithmetic": ToolSpec("review_arithmetic", "Symbolic check of numeric value-preserving equalities ONLY. Not a 27B model.", obj({"expression": SHORT, "steps": {"type": "array", "items": STEP, "maxItems": 30}, "mode": {"type": "string", "enum": ["socratic", "explain", "answer"]}}), REVIEW_OUT, "mcp"),
    "difficulty_candidates": ToolSpec("difficulty_candidates", "Rule-based local learning-difficulty candidates; never confirmed mastery.", obj({"history": {"type": "array", "items": HISTORY, "maxItems": 20}, "review": REVIEW_OUT}, ["history"]), DIAG_OUT),
}
