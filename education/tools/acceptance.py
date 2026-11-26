"""Web-only HTTP and authentication acceptance with native internal runtime; no remote model calls."""
import http.cookiejar
import json
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service/src"))
from qingqi.agent import PROJECT, Agent, InjectedInterruption
from qingqi.contracts import Identity, Request
from qingqi.product import Deployment, password_hash, server

results = []
def assertion(condition):
    assert condition
def record(name, function):
    function()
    results.append({"name": name, "passed": True})

def start(deployment=None):
    acceptance_root = PROJECT / "runs/acceptance" / uuid.uuid4().hex
    instance = server(0, root=acceptance_root, deployment=deployment)
    instance.acceptance_root = acceptance_root
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    return instance, thread

class Client:
    def __init__(self, port):
        self.base = f"http://127.0.0.1:{port}"
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.bootstrap = self.get("/api/bootstrap")
    def get(self, path):
        with self.opener.open(self.base + path, timeout=30) as response:
            return json.load(response)
    def post(self, path, body, csrf=True):
        headers = {"Content-Type": "application/json", "Origin": self.base}
        if csrf:
            headers["X-Qingqi-CSRF"] = self.bootstrap["csrf"]
        request = urllib.request.Request(self.base + path, data=json.dumps(body).encode(), headers=headers)
        with self.opener.open(request, timeout=30) as response:
            value = json.load(response)
        if path in {"/api/profile", "/api/login"}:
            self.bootstrap = value
        return value

def denied(action, code):
    try:
        action()
    except urllib.error.HTTPError as error:
        assert error.code == code, (error.code, code)
        return
    raise AssertionError("operation should have failed")

instance, thread = start()
try:
    client = Client(instance.server_port)
    session = client.post("/api/sessions", {})["id"]
    request = {"request_id": "work-1", "question": "请检查并给我提示", "expression": "2+3*4", "steps": [{"equation": "2+3*4=20"}], "mode": "socratic"}
    response = client.post("/api/teach", {"session": session, "request": request})
    record("incorrect_work_and_actual_step_evidence", lambda: (assertion(response["response"]["teaching_action"] == "ask" and response["response"]["step_refs"] == [0] and "14" not in response["response"]["text"])))
    record("refresh_and_idempotent_retry", lambda: assertion(client.post("/api/teach", {"session": session, "request": request})["response"]["cache_hit"] and len(client.get("/api/session?id=" + session)["messages"]) == 1))
    record("csrf_rejected", lambda: denied(lambda: client.post("/api/sessions", {}, csrf=False), 403))
    record("input_fingerprint_conflict", lambda: denied(lambda: client.post("/api/teach", {"session": session, "request": {**request, "question": "changed"}}), 403))
    record("student_cannot_confirm_teacher_fact", lambda: denied(lambda: client.post("/api/teacher/facts", {"student": "student-a", "key": "算术", "value": "掌握", "source": "class"}), 403))
    client.post("/api/profile", {"profile": "student-b"})
    record("student_scope_isolation", lambda: (assertion(client.get("/api/sessions")["sessions"] == []), denied(lambda: client.get("/api/session?id=" + session), 403)))
    client.post("/api/profile", {"profile": "teacher-demo"})
    record("teacher_fact_versioned", lambda: assertion(client.post("/api/teacher/facts", {"student": "student-a", "key": "四则运算", "value": "课堂确认", "source": "课堂作答"})["ok"]))
    client.post("/api/profile", {"profile": "student-a"})
    record("teacher_fact_visible_to_own_student", lambda: assertion(client.get("/api/memory")["facts"][0]["version"] == 1))
    record("real_curriculum_search", lambda: assertion(len(client.get("/api/courses?q=" + urllib.parse.quote("分数"))["matches"]) > 0))
    course_session = client.post("/api/sessions", {"title": "course routing"})["id"]
    course_checked = client.post("/api/teach", {"session": course_session, "request": {"request_id": "course-routing-1", "question": "请核对教材的课程关联", "course_query": "一氧化碳", "subject": "化学"}})
    record("course_verification_does_not_require_student_arithmetic", lambda: assertion(course_checked["response"]["route"]["intents"] == ["course"] and course_checked["response"]["evidence_refs"]))
    recovery_session = client.post("/api/sessions", {"title": "persisted recovery"})["id"]
    recovery_input = {"request_id": "recover-1", "question": "核对作答", "expression": "2+2", "steps": [{"equation": "2+2=4"}], "mode": "explain"}
    interrupted = Agent(instance.acceptance_root, PROJECT / "data/curriculum.sqlite")
    try:
        try:
            interrupted.run(Identity("edu-student-a", recovery_session), Request.parse(recovery_input), interrupt_after_tool=True)
        except InjectedInterruption:
            pass
    finally:
        interrupted.close()
    refreshed = client.get("/api/session?id=" + recovery_session)
    resumed = client.post("/api/teach", {"session": recovery_session, "request": refreshed["messages"][0]["input"]})
    record("persisted_input_resumes_after_durable_tool_completion", lambda: assertion(resumed["response"]["teaching_action"] == "confirm" and len(resumed["session"]["messages"]) == 1))

finally:
    instance.shutdown(); instance.server_close(); thread.join(2)

accounts = PROJECT / "runs/acceptance/accounts.json"
accounts.parent.mkdir(parents=True, exist_ok=True)
accounts.write_text(json.dumps({"accounts": {"a": {"name": "A", "role": "student", "password_hash": password_hash("acceptance-password")}}}), encoding="utf-8")
instance, thread = start(Deployment(accounts=accounts))
try:
    client = Client(instance.server_port)
    record("account_mode_requires_login", lambda: (assertion(not client.bootstrap["authenticated"]), denied(lambda: client.get("/api/memory"), 403)))
    record("wrong_password_rejected", lambda: denied(lambda: client.post("/api/login", {"username": "a", "password": "wrong"}), 403))
    record("pbkdf2_login_and_no_demo_impersonation", lambda: (assertion(client.post("/api/login", {"username": "a", "password": "acceptance-password"})["profile"] == "a"), denied(lambda: client.post("/api/profile", {"profile": "student-a"}), 403)))
finally:
    instance.shutdown(); instance.server_close(); thread.join(2)
target = PROJECT.parent / ".local/reports/product-acceptance.json"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps({"passed": len(results), "tests": results, "mode": "Web-only real HTTP + native internal runtime + offline teaching; no remote inference"}, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"passed": len(results), "report": str(target)}, ensure_ascii=False))
