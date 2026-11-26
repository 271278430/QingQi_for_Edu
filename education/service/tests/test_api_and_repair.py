from __future__ import annotations

import uuid

import pytest

from qingqi.agent import Agent, InjectedInterruption, PROJECT
from qingqi.contracts import Denied, Identity, Request
from qingqi.planning import OfflineController


class RepairFixture(OfflineController):
    name = "repair_fixture_not_llm"

    def next(self, request, state, *args):
        if not state["repairs"]:
            return {"kind": "call"}  # Discriminator-valid but missing tool arguments.
        return super().next(request, state, *args)


def test_bad_action_schema_is_repaired_and_real_tool_runs():
    a = Agent(PROJECT / "runs/tests" / uuid.uuid4().hex, PROJECT / "data/curriculum.sqlite", controller=RepairFixture())
    try:
        q = Request.parse({"request_id": "repair", "question": "检查作答", "expression": "2+2", "steps": [{"equation": "2+2=4"}]})
        r = a.run(Identity("a", "s"), q)
        assert r["repairs"] == 1 and r["teaching_action"] == "confirm"
        assert r["model_inference"] is False
    finally:
        a.close()


def test_resume_refuses_changed_budgets():
    path = PROJECT / "runs/tests" / uuid.uuid4().hex
    q = Request.parse({"request_id": "resume", "question": "检查作答", "expression": "2+2", "steps": [{"equation": "2+2=4"}]})
    a = Agent(path, PROJECT / "data/curriculum.sqlite", max_calls=8)
    with pytest.raises(InjectedInterruption):
        a.run(Identity("a", "s"), q, interrupt_after_tool=True)
    a.close()
    b = Agent(path, PROJECT / "data/curriculum.sqlite", max_calls=10)
    try:
        with pytest.raises(Denied, match="budgets"):
            b.run(Identity("a", "s"), q)
    finally:
        b.close()
