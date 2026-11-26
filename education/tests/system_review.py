"""Independent review: isolated real HTTP probes plus bounded live-model evaluation.

Controlled endpoints simulate faulty outputs; those probes do NOT measure model accuracy.
Gold labels stay outside model requests. No product code or live student DB is modified.
"""
from __future__ import annotations
import argparse
import datetime
from fractions import Fraction
import http.cookiejar
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import sqlite3
import statistics
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid

EDUCATION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EDUCATION / "service/src"))
from qingqi.agent import Agent, PROJECT
from qingqi.contracts import Request
from qingqi.domain_tools import review
from qingqi.layered_routing import LayeredRouter
from qingqi.planning import OfflineController, find, reply
from qingqi.product import Deployment, server
from qingqi.providers import Endpoint, GLMController, JSONModel
from qingqi.workers import make_workers

ROOT = PROJECT / "runs/system-review" / uuid.uuid4().hex
REPORT = EDUCATION / ".local/reports/system-review.json"
GRAPH = PROJECT / "data/curriculum.sqlite"
RESULTS = {"date": datetime.datetime.now().astimezone().isoformat(), "scope": "isolated synthetic audit; no live student records", "run_directory": str(ROOT.relative_to(PROJECT)), "probes": [], "real": {"executed": False}}

def save():
    REPORT.write_text(json.dumps(RESULTS, ensure_ascii=False, indent=2), encoding="utf-8")

def emit(value):
    print(json.dumps(value, ensure_ascii=False), flush=True)

class Client:
    def __init__(self, port):
        self.base = f"http://127.0.0.1:{port}"
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.boot = self.get("/api/bootstrap")
    def get(self, path):
        with self.opener.open(self.base + path, timeout=20) as response:
            return json.load(response)
    def post(self, path, value):
        request = urllib.request.Request(self.base + path, data=json.dumps(value).encode(), headers={"Content-Type": "application/json", "Origin": self.base, "X-Qingqi-CSRF": self.boot["csrf"]})
        try:
            with self.opener.open(request, timeout=360) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, json.load(error)
    def job(self, value):
        _, session = self.post("/api/sessions", {"title": "独立审查评测"})
        return {"session": session["id"], "request": {"request_id": uuid.uuid4().hex, **value}}

class FixtureDeployment(Deployment):
    def __init__(self, factory):
        super().__init__()
        self.factory = factory
    def agent(self, root):
        return self.factory(root)

def start(name, deployment=None):
    root = ROOT / name
    instance = server(0, root=root, deployment=deployment)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    return instance, thread, root

def stop(instance, thread):
    instance.shutdown()
    instance.server_close()
    thread.join(2)

def add_probe(value):
    RESULTS["probes"].append(value)
    emit(value)
    save()

WORK = {"question": "请核对我的实际步骤，先只给提示，不给答案。", "expression": "2+3*4", "steps": [{"equation": "2+3*4=20"}], "mode": "socratic"}

def controlled_probes():
    instance, thread, root = start("student_trace")
    try:
        client = Client(instance.server_port)
        job = client.job(WORK)
        code, value = client.post("/api/teach", job)
        assert code == 200
        observations = value["session"]["messages"][-1]["trace"]["observations"]
        # 规范学生投影已删除工具内部答案；独立审查检查当前API边界，浏览器由统一清单另行覆盖。
        exposed = [item["result"].get("answer") for item in observations if item["tool"] == "review_arithmetic"]
        add_probe({"id": "R1", "name": "socratic_student_trace", "scope": "real isolated HTTP with current safe projection", "reply_withholds_14": "14" not in value["response"]["text"], "trace_answers": exposed, "protection_satisfied": all(v is None for v in exposed) and "14" not in value["response"]["text"]})
    finally:
        stop(instance, thread)

    class LeakingController(OfflineController):
        name = "controlled_reply_fault"
        def next(self, request, state, context, registry):
            if find(state, "review_arithmetic"):
                return reply("先想一想：这道题的最终答案是14。你应该先做哪一步？", "ask", ["step:0"], [0])
            return super().next(request, state, context, registry)
    instance, thread, _ = start("reply_fault", FixtureDeployment(lambda root: Agent(root, GRAPH, controller=LeakingController())))
    try:
        client = Client(instance.server_port)
        code, value = client.post("/api/teach", client.job(WORK))
        add_probe({"id": "R2a", "name": "schema_valid_answer_in_ask_text", "scope": "controlled faulty controller, actual HTTP and numeric check", "http_status": code, "text": value.get("response", {}).get("text"), "protection_satisfied": code != 200 or "14" not in value.get("response", {}).get("text", "")})
    finally:
        stop(instance, thread)

    class FalseCitationController(OfflineController):
        name = "controlled_citation_fault"
        def next(self, request, state, context, registry):
            course = find(state, "course_context")
            if course:
                return reply("教材已确认这个知识点属于第三十五章火星量子数学，而且其先修关系已由专家确认。你想先学什么？", "ask", [course["evidence"][0]["ref"]])
            return super().next(request, state, context, registry)
    instance, thread, _ = start("citation_fault", FixtureDeployment(lambda root: Agent(root, GRAPH, controller=FalseCitationController())))
    try:
        client = Client(instance.server_port)
        code, value = client.post("/api/teach", client.job({"question": "核对教材课程关联", "course_query": "13.1 三角形的概念", "subject": "数学"}))
        add_probe({"id": "R2b", "name": "valid_ref_false_claim", "scope": "controlled faulty controller, real graph and HTTP", "http_status": code, "text": value.get("response", {}).get("text"), "protection_satisfied": code != 200 or all(v not in value.get("response", {}).get("text", "") for v in ("火星量子数学", "专家确认"))})
    finally:
        stop(instance, thread)

    os.environ["QINGQI_REVIEW_FIXTURE_KEY"] = "local-protocol-fixture"
    for kind in ("unknown_controller", "known_worker_busy"):
        counter = {"requests": 0}
        class ModelHandler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass
            def do_POST(self):
                counter["requests"] += 1
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if counter["requests"] == 1 and kind == "unknown_controller":
                    self.close_connection = True
                    return
                if counter["requests"] == 1:
                    raw = b'{"error":"specialist_busy"}'
                    self.send_response(429)
                    self.send_header("Retry-After", "1")
                else:
                    payload = json.loads(body["messages"][1]["content"])["input"]
                    result = reply("请补充学习信息。", "clarify") if kind == "unknown_controller" else review(**payload)
                    raw = json.dumps({"choices": [{"message": {"content": json.dumps(result)}}]}).encode()
                    self.send_response(200)
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
        model_server = ThreadingHTTPServer(("127.0.0.1", 0), ModelHandler)
        model_thread = threading.Thread(target=model_server.serve_forever, daemon=True)
        model_thread.start()
        endpoint = Endpoint(name="fixture", base_url=f"http://127.0.0.1:{model_server.server_port}/v1", model="local-protocol-fixture", key_env="QINGQI_REVIEW_FIXTURE_KEY", enabled=True, allowed_hosts=("127.0.0.1",), timeout=3, json_mode=kind == "unknown_controller")
        if kind == "unknown_controller":
            factory = lambda root: Agent(root, GRAPH, controller=GLMController(JSONModel(endpoint)))
        else:
            factory = lambda root: Agent(root, GRAPH, workers=make_workers({"review27b": JSONModel(endpoint)}))
        instance, thread, root = start(kind, FixtureDeployment(factory))
        try:
            client = Client(instance.server_port)
            job = client.job(WORK)
            first, _ = client.post("/api/teach", job)
            second, _ = client.post("/api/teach", job)
            before_new_id = counter["requests"]
            with sqlite3.connect(root / "agent.sqlite") as db:
                ledger_rows = db.execute("SELECT COUNT(*) FROM calls").fetchone()[0]
            extra = {}
            if kind == "known_worker_busy":
                job["request"]["request_id"] = uuid.uuid4().hex
                third, _ = client.post("/api/teach", job)
                extra["new_id_status"] = third
            add_probe({"id": "R3" if kind == "unknown_controller" else "R4", "name": kind, "scope": "local HTTP model protocol fixture; no real billing", "first_status": first, "same_id_retry_status": second, "requests_before_new_id": before_new_id, "durable_tool_rows": ledger_rows, "protection_satisfied": before_new_id == 1 if kind == "unknown_controller" else first == 429 and second == 200, **extra})
        finally:
            stop(instance, thread)
            stop(model_server, model_thread)
    os.environ.pop("QINGQI_REVIEW_FIXTURE_KEY", None)

def offline_numeric():
    cases = [
        ("precedence_wrong", "2+3*4", ["2+3*4=20"], "incorrect", 0, "14", True),
        ("precedence_correct", "2+3*4", ["2+3*4=14"], "correct", -1, "14", True),
        ("whole_steps_correct", "2+3*4", ["2+3*4=2+12", "2+12=14"], "correct", -1, "14", True),
        ("second_step_wrong", "2+3*4", ["2+3*4=2+12", "2+12=15"], "incorrect", 1, "14", True),
        ("decimal", "0.1+0.2", ["0.1+0.2=0.3"], "correct", -1, "3/10", True),
        ("fraction", "1/2+1/3", ["1/2+1/3=5/6"], "correct", -1, "5/6", True),
        ("negative", "(-3)*(-2)", ["(-3)*(-2)=6"], "correct", -1, "6", True),
        ("parentheses", "(2+3)*4", ["(2+3)*4=14"], "incorrect", 0, "20", True),
        ("zero", "0*9", ["0*9=0"], "correct", -1, "0", True),
        ("unrelated_equality", "2+2", ["9=9"], "incorrect", 0, "4", True),
        ("chained_equality", "2+2", ["2+2=4=4"], "unsupported", -1, "4", False),
        ("natural_partial_steps", "2+3*4", ["3*4=12", "2+12=14"], "correct", -1, "14", False),
        ("algebra", "2*x+1", ["2*x+1=5"], "unsupported", -1, "", False),
        ("division_zero", "1/0", ["1/0=0"], "unsupported", -1, "", False),
        ("power", "2**3", ["2**3=8"], "correct", -1, "8", False),
    ]
    rows = []
    for name, expression, steps, status, first, answer, supported in cases:
        try:
            value = review(expression, [{"equation": step} for step in steps], "socratic")
            matches = value["status"] == status and value["first_error"] == first and (not answer or Fraction(value["answer"]) == Fraction(answer))
            row = {"id": name, "supported": supported, "gold": {"status": status, "first_error": first}, "observed": value, "matches_gold": matches}
        except Exception as error:
            row = {"id": name, "supported": supported, "error": type(error).__name__, "matches_gold": False}
        rows.append(row)
    RESULTS["numeric"] = {"scope": "local numeric tool, whole-value-preserving contract", "supported_correct": sum(row["matches_gold"] for row in rows if row["supported"]), "supported_total": sum(row["supported"] for row in rows), "cases": rows}
    emit({"numeric_supported": [RESULTS["numeric"]["supported_correct"], RESULTS["numeric"]["supported_total"]]})
    save()

def offline_routing():
    examples = [
        ("course_catalog", "请核对教材课程关联", {"course_query": "13.1 三角形的概念"}, ["course"]),
        ("course_where", "这个知识点对应教材哪章", {"course_query": "分数"}, ["course"]),
        ("course_prerequisite", "查询先修知识", {"course_query": "三角形"}, ["course"]),
        ("course_missing", "请核对教材关联", {}, ["course"]),
        ("review_work", "核对我的作答", {"expression": "2+2"}, ["review"]),
        ("review_hint", "给我一点提示", {"expression": "2+2"}, ["review", "tutor"]),
        ("review_explain", "请从头讲解", {"expression": "2+2"}, ["review"]),
        ("review_missing", "请核对我的答案", {}, ["review"]),
        ("diagnosis", "分析我的学情", {"history": [{"kind": "self_report", "text": "我总是先加后乘"}]}, ["diagnosis"]),
        ("diagnosis_paraphrase", "为什么总是算错", {}, ["diagnosis"]),
        ("concept_paraphrase", "我不理解分数的含义", {}, ["tutor"]),
        ("greeting", "你好", {}, ["chat"]),
        ("thanks", "谢谢", {}, ["chat"]),
        ("chat_tired", "今天有点累想聊聊", {}, ["chat"]),
        ("cancel_exact", "取消当前任务", {}, ["chat"]),
        ("cancel_not_command", "取消当前任务这个词是什么意思", {}, ["clarify"]),
        ("english_work", "Could you check my calculation?", {"expression": "2+2"}, ["review"]),
        ("english_next", "Which topic should I learn next?", {}, ["course"]),
        ("compound", "核对我的步骤并查询教材课程", {"expression": "2+2", "course_query": "分数"}, ["course", "review"]),
        ("unknown", "怎么办", {}, ["clarify"]),
    ]
    router = LayeredRouter()
    rows = []
    for name, question, fields, gold in examples:
        value = router.route(Request.parse({"request_id": uuid.uuid4().hex, "question": question, **fields}))
        rows.append({"id": name, "question": question, "gold_intents": gold, "observed_intents": list(value.intents), "clarify": value.clarify, "matches_gold": set(gold) == set(value.intents)})
    RESULTS["routing"] = {"scope": "hand-authored local router cases; GLM fallback disabled; not held-out semantic-model accuracy", "correct": sum(row["matches_gold"] for row in rows), "total": len(rows), "cases": rows}
    emit({"routing_local": [RESULTS["routing"]["correct"], len(rows)]})
    save()

def percentile(values, fraction):
    values = sorted(values)
    if not values:
        return None
    index = (len(values) - 1) * fraction
    low = int(index)
    high = min(low + 1, len(values) - 1)
    return round(values[low] + (values[high] - values[low]) * (index - low), 3)

def real_evaluation():
    settings = json.loads((EDUCATION / "server/connection.local.json").read_text(encoding="utf-8-sig"))
    if not os.environ.get("EDU_GLM_API_KEY"):
        raise RuntimeError("GLM credential was not supplied to the process")
    if not os.environ.get("EDU_WORKER_KEY"):
        os.environ["EDU_WORKER_KEY"] = subprocess.check_output(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "-p", str(settings["port"]), f'{settings["user"]}@{settings["host"]}', "cat", settings["token_file"]], stdin=subprocess.DEVNULL, timeout=20, text=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0).strip()
    deployment = Deployment(EDUCATION / "service/config/models.local.json")
    instance, thread, _ = start("real", deployment)
    rows = []
    RESULTS["real"] = {"executed": True, "case_source": "tools/system_review_cases.json", "cases": rows, "scope": "warm real GLM and specialists, sequential synthetic inputs, isolated HTTP owner"}
    try:
        client = Client(instance.server_port)
        corpus = json.loads((EDUCATION / "tools/system_review_cases.json").read_text(encoding="utf-8"))["real_cases"]
        for case in corpus:
            job = client.job(case["input"])
            started = time.perf_counter()
            code, value = client.post("/api/teach", job)
            row = {"id": case["id"], "kind": case["kind"], "supported": case["supported"], "http_status": code, "http_seconds": round(time.perf_counter() - started, 3), "gold": case["gold"], "success": False}
            if code == 200:
                result = value["response"]
                observations = value["session"]["messages"][-1]["trace"]["observations"]
                tools = [item["tool"] for item in observations]
                checked = next((item["result"] for item in observations if item["tool"] == "worker_review27b"), None)
                known_refs = {e["ref"] for item in observations for e in item["result"].get("evidence", [])}
                refs_valid = set(result["evidence_refs"]) <= known_refs
                action_match = result["teaching_action"] in case["gold"].get("actions", [result["teaching_action"]])
                if case["kind"] == "numeric":
                    gold = case["gold"]
                    answer_match = bool(checked) and Fraction(checked["answer"]) == Fraction(gold["answer"])
                    withheld = not gold.get("withhold_answer") or not re.search(r"(?<!\d)" + re.escape(gold["answer"]) + r"(?!\d)", result["text"])
                    row["success"] = bool(checked) and answer_match and checked["status"] == gold["status"] and checked["first_error"] == gold["first_error"] and action_match and refs_valid and withheld
                    row.update(review_status=checked["status"] if checked else None, first_error=checked["first_error"] if checked else None, answer_match=answer_match, answer_withheld=withheld)
                elif case["kind"] == "boundary":
                    row["success"] = result["teaching_action"] == case["gold"]["preferred_action"]
                    row["review_status"] = checked["status"] if checked else None
                else:
                    required = set(case["gold"]["required_tools"])
                    forbidden = set(case["gold"].get("forbidden_tools", []))
                    row["success"] = required <= set(tools) and not forbidden & set(tools) and refs_valid and action_match
                    if case["kind"] == "course":
                        row["success"] = row["success"] and bool(result["evidence_refs"])
                    elif case["kind"] == "difficulty":
                        row["success"] = row["success"] and bool(result["difficulty_candidates"])
                replay_started = time.perf_counter()
                replay_code, replay = client.post("/api/teach", job)
                row.update(action=result["teaching_action"], tools=tools, text=result["text"], evidence_refs=result["evidence_refs"], model_usage=result.get("model_usage", []), idempotent_replay=replay_code == 200 and replay["response"]["cache_hit"], replay_seconds=round(time.perf_counter() - replay_started, 3))
            else:
                row["error"] = value.get("error")
            rows.append(row)
            emit({key: row[key] for key in ("id", "http_status", "http_seconds", "success")})
            save()
    finally:
        stop(instance, thread)
    successes = [row for row in rows if row["http_status"] == 200]
    supported = [row for row in rows if row["supported"]]
    tokens = sum((entry.get("usage") or {}).get("total_tokens", 0) for row in successes for entry in row.get("model_usage", []))
    RESULTS["real"]["summary"] = {"completed": len(successes), "total": len(rows), "supported_success": sum(row["success"] for row in supported), "supported_total": len(supported), "all_case_success": sum(row["success"] for row in rows), "p50_seconds_all_attempts": percentile([row["http_seconds"] for row in rows], .5), "p95_seconds_all_attempts": percentile([row["http_seconds"] for row in rows], .95), "p50_seconds_completed": percentile([row["http_seconds"] for row in successes], .5), "idempotent_replays": sum(row.get("idempotent_replay", False) for row in rows), "reported_tokens_successful_turns_only": tokens, "token_caveat": "Failed turns may still incur model usage; their usage is not returned by the product API."}
    save()
    emit(RESULTS["real"]["summary"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--real", action="store_true")
    args = parser.parse_args()
    ROOT.mkdir(parents=True)
    offline_numeric()
    offline_routing()
    controlled_probes()
    if args.real:
        try:
            real_evaluation()
        except Exception as error:
            RESULTS["real"]["error"] = type(error).__name__
            emit({"real_evaluation_error": type(error).__name__})
    failures=[p["id"] for p in RESULTS["probes"] if not p.get("protection_satisfied",True)]
    if failures:raise AssertionError({"failed_protections":failures})
    RESULTS["execution_finished"] = True
    save()

if __name__ == "__main__":
    main()
