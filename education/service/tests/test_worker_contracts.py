"""Worker stubs verify contracts only, never model ability."""
import pytest

from qingqi.contracts import ContractError, Denied
from qingqi.domain_tools import review
from qingqi.workers import make_workers


class Stub:
    def __init__(self, result):
        self.result = result

    def generate(self, *args):
        return self.result


def test_review_worker_preserves_exact_input_references():
    args = {"expression": "2+3", "steps": [{"equation": "2+3=6"}], "mode": "socratic"}
    output = review(**args)
    tool = make_workers({"review27b": Stub(output)})["worker_review27b"][1]
    assert tool(**args)["first_error"] == 0
    output["evidence"][0]["text"] = "2+3=5"
    with pytest.raises(Denied, match="actual student"):
        tool(**args)


def test_review_worker_first_error_agrees_with_checklist():
    args = {"expression": "2+3", "steps": [{"equation": "2+3=6"}], "mode": "socratic"}
    output = review(**args)
    output["first_error"] = -1
    with pytest.raises(Denied, match="contradicts"):
        make_workers({"review27b": Stub(output)})["worker_review27b"][1](**args)


def test_difficulty_worker_cannot_invent_history_or_mastery():
    output = {"candidates": ["concept_candidate"], "certainty": "candidate_requires_confirmation", "strategy": "追问", "evidence": [{"ref": "history:7", "text": "错了七次", "source": "student_work"}]}
    tool = make_workers({"difficulty8b": Stub(output)})["worker_difficulty8b"][1]
    with pytest.raises(Denied, match="nonexistent"):
        tool(history=[{"text": "我不理解概念", "kind": "self_report"}])
    output["certainty"] = "mastered"
    with pytest.raises(Denied, match="mastery"):
        tool(history=[])


def test_course_worker_cannot_authorize_node_ids():
    tool = make_workers({"course8b": Stub({"candidate_node_id": "invented", "rationale": "猜测"})})["worker_course8b"][1]
    with pytest.raises(ContractError, match="missing"):
        tool(query="分数", candidates=[{"id": "real", "title": "分数"}])
