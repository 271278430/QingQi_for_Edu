"""Real HTTP + native ZCode runtime, specialist protocol fixtures, isolated data."""
import http.cookiejar
import json
import os
import socket
import sys
import threading
import urllib.error
import urllib.request
import uuid
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service/src"))
from qingqi.agent import Agent, PROJECT
from qingqi.contracts import Denied, Identity, Request
from qingqi.domain_tools import review, difficulty
from qingqi.product import Deployment, server
from qingqi.providers import Endpoint, JSONModel, GLMController
from qingqi.storage import Store
from qingqi.workers import make_workers
from qingqi.planning import OfflineController
from qingqi.zcode_runtime import RuntimeFailure

KEY_ENV = "QINGQI_RUNTIME_FIXTURE_KEY"
os.environ[KEY_ENV] = "isolated-protocol-fixture"
calls = Counter()
entered, release = threading.Event(), threading.Event()
checks = []

class ModelHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        model = body["model"]
        calls[model] += 1
        payload = json.loads(body["messages"][-1]["content"])["input"]
        if model == "fixture-glm-unknown":
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            return
        if model == "fixture-review-busy" and calls[model] == 1:
            self.send_response(429)
            self.end_headers()
            return
        if model == "fixture-glm-held":
            entered.set()
            if not release.wait(15):
                self.send_response(503)
                self.end_headers()
                return
        if "review" in model:
            result = review(**payload)
        elif "course" in model:
            result = {"suggested_titles": [item["title"] for item in payload["candidates"]], "status": "candidate_requires_graph_confirmation"}
        elif "difficulty" in model:
            result = difficulty(**payload)
        else:
            observed = payload.get("state", {}).get("observations", [])
            checked = next((item["result"] for item in observed if "review" in item["tool"]), None)
            action = "confirm" if checked and checked["status"] == "correct" else "ask" if observed else "chat"
            # 故意让合法引用搭配泄答正文；服务端必须用核验证据重新构造教学结论。
            result = {"kind": "respond", "reply": {"text": "最终答案是14。伪造的结论。", "teaching_action": action,
                "step_refs": [checked["first_error"]] if checked and checked["first_error"] >= 0 else [], "evidence_refs": payload.get("observed_evidence_refs", [])}}
        encoded = json.dumps({"choices": [{"message": {"content": json.dumps(result, ensure_ascii=False)}}], "usage": {"prompt_tokens": 20, "completion_tokens": 10}}).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(encoded)

model_server = ThreadingHTTPServer(("127.0.0.1", 0), ModelHandler)
model_thread = threading.Thread(target=model_server.serve_forever, daemon=True)
model_thread.start()
base_model = f"http://127.0.0.1:{model_server.server_port}/v1"

class FixtureDeployment(Deployment):
    def __init__(self, glm="fixture-glm", review_model="fixture-review", specialists=True):
        super().__init__()
        self.glm, self.review_model, self.specialists = glm, review_model, specialists
    def agent(self, root):
        def model(role, name):
            return JSONModel(Endpoint(role, base_model, name, KEY_ENV, enabled=True, allowed_hosts=("127.0.0.1",), timeout=15))
        glm = GLMController(model("glm", self.glm))
        workers = make_workers({"review27b": model("review27b", self.review_model), "course8b": model("course8b", "fixture-course"), "difficulty8b": model("difficulty8b", "fixture-difficulty")}) if self.specialists else {}
        return Agent(root, PROJECT / "data/curriculum.sqlite", controller=glm, router=glm, workers=workers)

class Client:
    def __init__(self, instance):
        self.base = f"http://127.0.0.1:{instance.server_port}"
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.csrf = self.get("/api/bootstrap")["csrf"]
    def get(self, path):
        return json.load(self.opener.open(self.base + path, timeout=30))
    def post(self, path, body):
        request = urllib.request.Request(self.base + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "Origin": self.base, "X-Qingqi-CSRF": self.csrf})
        try:
            with self.opener.open(request, timeout=40) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, json.load(error)
    def session(self):
        return self.post("/api/sessions", {})[1]["id"]

instances = []
def start(deployment):
    root = PROJECT / "runs/runtime-acceptance" / uuid.uuid4().hex
    instance = server(0, root=root, deployment=deployment)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    instances.append((instance, thread))
    return Client(instance), root
def check(name, passed):
    if not passed:
        raise AssertionError(name)
    checks.append({"name": name, "passed": True})

try:
    client, root = start(FixtureDeployment())
    session = client.session()
    request = {"request_id": "native-review", "question": "检查我的作答，先不要给答案", "expression": "2+3*4", "steps": [{"equation": "2+3*4=20"}], "mode": "socratic"}
    status, result = client.post("/api/teach", {"session": session, "request": request})
    check("native_specialist_teaching_http", status == 200 and result["response"]["teaching_action"] == "ask")
    detail = client.get("/api/session?id=" + session)
    text = json.dumps(detail, ensure_ascii=False)
    check("student_projection_and_grounded_reply", '"answer"' not in text and '"content"' not in text and "伪造" not in text and "最终答案是14" not in text)
    store = Store(root)
    try:
        state = json.loads(store.db.execute("SELECT state FROM runs WHERE request_id='native-review'").fetchone()[0])
        observations = state["observations"]
        child = next(item for item in observations if item["tool"] == "worker_review27b")["runtime"]
        check("actual_upstream_subagent_lifecycle", bool(child["subagent"]["agent_id"] and child["subagent"]["child_session_id"]) and any("subagent" in str(event["type"]).lower() for event in child["events"]))
        check("native_skill_and_scheduler", "work-review" in state["skill_hashes"] and state["native_schedule"]["source"] == "@zcode/core/ToolScheduler")
        check("model_journal_completed", store.db.execute("SELECT count(*) FROM model_invocations WHERE status='done'").fetchone()[0] >= 2)
    finally:
        store.close()
    status, repeated = client.post("/api/teach", {"session": session, "request": request})
    check("same_id_replay_no_worker_call", status == 200 and repeated["response"]["cache_hit"] and calls["fixture-review"] == 1)
    status, partial = client.post("/api/teach", {"session": client.session(), "request": {"request_id": "partial", "question": "检查作答", "expression": "2+3*4", "steps": [{"equation": "3*4=12"}, {"equation": "2+12=14"}]}})
    check("correct_subexpression_steps", status == 200 and partial["response"]["teaching_action"] == "confirm")
    for name, expression in (("algebra", "2*x+1"), ("division_zero", "1/0")):
        before = sum(calls.values())
        status, unsupported = client.post("/api/teach", {"session": client.session(), "request": {"request_id": name, "question": "检查作答", "expression": expression}})
        check(name + "_clarifies_before_models", status == 200 and unsupported["response"]["teaching_action"] == "clarify" and sum(calls.values()) == before)
    before_glm = calls["fixture-glm"]
    status, course = client.post("/api/teach", {"session": client.session(), "request": {"request_id": "course", "question": "核对教材课程关联", "course_query": "一氧化碳", "subject": "化学"}})
    check("native_mcp_course_worker_grounded_plan", status == 200 and course["response"]["evidence_refs"] and calls["fixture-course"] == 1 and calls["fixture-glm"] == before_glm)
    status, diagnostic = client.post("/api/teach", {"session": client.session(), "request": {"request_id": "difficulty", "question": "分析学情", "history": [{"kind": "self_report", "text": "我总是漏步骤"}]}})
    check("native_difficulty_specialist", status == 200 and calls["fixture-difficulty"] == 1)
    compound_input = {"request_id": "compound-scheduled", "question": "核对教材课程并检查作答、分析学情", "course_query": "一氧化碳", "subject": "化学", "expression": "2+2", "steps": [{"equation": "2+2=4"}], "history": [{"kind": "self_report", "text": "我总是漏步骤"}]}
    status, compound = client.post("/api/teach", {"session": client.session(), "request": compound_input})
    observed=[item['tool'] for item in compound['session']['messages'][-1]['trace']['observations']] if status==200 else []
    check("native_schedule_drives_compound_execution", status == 200 and observed[:5] == ["course_search", "worker_course8b", "course_context", "worker_review27b", "worker_difficulty8b"] and observed[5:] in ([],['render_teaching_visual']))
    class OutOfOrderController(OfflineController):
        name = "deliberate_order_violation_fixture"
        def next(self, request, state, context, registry):
            return {"kind": "call", "tool": "difficulty_candidates", "arguments": {"history": state["diagnosis_history"]}}
    order_agent = Agent(root / "order-negative", PROJECT / "data/curriculum.sqlite", controller=OutOfOrderController())
    try:
        try:
            order_agent.run(Identity("fixture", "s"), Request.parse({"request_id": "out-of-order", "question": "检查作答并分析学情", "expression": "2+2", "steps": [{"equation": "2+2=4"}], "history": [{"kind": "self_report", "text": "我总是漏步骤"}]}))
        except Denied as error:
            check("native_schedule_rejects_dependency_bypass", "native DAG" in str(error) and order_agent.store.db.execute("SELECT count(*) FROM calls").fetchone()[0] == 0)
        else:
            raise AssertionError("out-of-order tool must be denied before execution")
    finally:
        order_agent.close()
    offline, offline_root = start(Deployment())
    status, local = offline.post("/api/teach", {"session": offline.session(), "request": {"request_id": "local", "question": "分析学情", "history": [{"kind": "self_report", "text": "私有记忆A，我不理解概念"}]}})
    owner = Store(offline_root)
    try:
        record = json.loads(owner.db.execute("SELECT state FROM runs WHERE request_id='local'").fetchone()[0])
        check("native_local_tool_executor", status == 200 and record["observations"][0]["runtime"]["source"] == "@zcode/core/ToolExecutor")
        bridge_agent = Agent(offline_root, PROJECT / "data/curriculum.sqlite")
        try:
            memories = bridge_agent.registry.runtime.rpc("recall", owner.retrieve(Identity("edu-student-b", "s"), "私有记忆"))
            bounded = bridge_agent.registry.runtime.rpc("recall", {"facts": [], "episodes": [{"text": str(i), "kind": "self_report"} for i in range(12)]})
            oversized = bridge_agent.registry.runtime.rpc("recall", {"facts": [{"value": "x" * 70000}], "episodes": []})
            check("native_memory_scope_and_budget", memories["episodes"] == [] and bounded["recall_metrics"]["selected"] == 5 and bounded["recall_metrics"]["source"] == "@zcode/core/memory" and oversized["facts"] == [] and oversized["recall_metrics"]["selected"] == 0)
            process = bridge_agent.registry.runtime.process
            process.stdin.close()
            process.wait(timeout=5)
            try:
                bridge_agent.registry.runtime.rpc("contracts", {"names": []}, start=False)
            except RuntimeFailure as error:
                check("closed_native_pipe_has_stable_failure", error.code == "runtime_unavailable" and error.recoverable)
            else:
                raise AssertionError("closed native pipe must not appear successful")
        finally:
            bridge_agent.close()
    finally:
        owner.close()
    fault, fault_root = start(FixtureDeployment(glm="fixture-glm-unknown", specialists=False))
    payload = {"session": fault.session(), "request": {"request_id": "unknown", "question": "你好"}}
    first = fault.post("/api/teach", payload)
    second = fault.post("/api/teach", payload)
    check("unknown_model_outcome_never_replayed", first[0] == second[0] == 409 and second[1]["error"] == "model_unknown" and fault.get("/api/session?id=" + payload["session"])["messages"][-1]["trace"]["error_code"] == "model_unknown" and calls["fixture-glm-unknown"] == 1)
    busy, _ = start(FixtureDeployment(review_model="fixture-review-busy"))
    payload = {"session": busy.session(), "request": {"request_id": "busy", "question": "检查作答", "expression": "2+2", "steps": [{"equation": "2+2=4"}]}}
    first, second = busy.post("/api/teach", payload), busy.post("/api/teach", payload)
    check("known_specialist_busy_same_id_recovers", first[0] == 429 and first[1]["error"] == "model_busy" and first[1]["retry_after"] == 3 and second[0] == 200 and calls["fixture-review-busy"] == 2)
    held, _ = start(FixtureDeployment(glm="fixture-glm-held", specialists=False))
    session = held.session()
    completed = []
    thread = threading.Thread(target=lambda: completed.append(held.post("/api/teach", {"session": session, "request": {"request_id": "held", "question": "你好"}})), daemon=True)
    thread.start()
    try:
        check("first_request_entered_model", entered.wait(15))
        second = held.post("/api/teach", {"session": session, "request": {"request_id": "concurrent", "question": "你好"}})
        check("same_session_concurrent_admission_rejected", second[0] == 429)
    finally:
        release.set()
        thread.join(20)
    check("accepted_owner_completes", bool(completed) and completed[0][0] == 200)
finally:
    release.set()
    for instance, thread in instances:
        instance.shutdown()
        instance.server_close()
        thread.join(2)
    model_server.shutdown()
    model_server.server_close()
    model_thread.join(2)
    os.environ.pop(KEY_ENV, None)
    report = {"passed": len(checks), "checks": checks, "actualHTTP": True, "actualZCodeRuntime": True, "modelProtocolFixtures": True, "remoteInference": False, "modelCalls": dict(calls)}
    target = PROJECT.parent / ".local/reports/runtime-reuse-acceptance.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"passed": len(checks), "report": str(target)}, ensure_ascii=False))
