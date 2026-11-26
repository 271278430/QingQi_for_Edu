"""Isolated real HTTP owner with a durable interruption for browser acceptance."""
import json
import uuid
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service/src"))
from qingqi.agent import Agent, InjectedInterruption, PROJECT
from qingqi.contracts import Identity, Request
from qingqi.product import server
from qingqi.web_store import WebStore

root = PROJECT / "runs/browser-recovery" / uuid.uuid4().hex
instance = server(0, root=root)
store = WebStore(root)
agent = Agent(root, PROJECT / "data/curriculum.sqlite")
cases = []
try:
    for name, question, expected in (
        ("inline_expression", "直接核对 2+3*4 的答案", "give_answer"),
        ("same_session_followup", "这道题还是不会，请再给一点提示", "ask"),
    ):
        session = store.create("edu-student-a", name)["id"]
        identity = Identity("edu-student-a", session)
        if name == "same_session_followup":
            seed = Request.parse({"request_id": uuid.uuid4().hex, "question": "请给我提示", "expression": "2+3*4", "steps": [{"equation": "2+3*4=20"}], "mode": "socratic"})
            agent.run(identity, seed)
        request = Request.parse({"request_id": uuid.uuid4().hex, "question": question})
        try:
            agent.run(identity, request, interrupt_after_tool=True)
        except InjectedInterruption:
            pass
        else:
            raise AssertionError("fixture must stop after durable tool completion")
        message = store.detail("edu-student-a", session)["messages"][-1]
        assert message["response"] is None
        assert message["input"] != message["original_input"]
        assert message["original_input"] == request.dump()
        cases.append({"name": name, "session": session, "request": request.dump(), "expected": expected})
finally:
    agent.close()
    store.close()

print(json.dumps({"base": f"http://127.0.0.1:{instance.server_port}", "cases": cases}), flush=True)
try:
    instance.serve_forever()
finally:
    instance.server_close()
