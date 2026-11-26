"""Full real-provider HTTP teaching chain, separate from offline acceptance."""
import http.cookiejar
import json
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

base = "http://127.0.0.1:18772"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base + path, timeout=360) as response:
        return json.load(response)
boot = get("/api/bootstrap")
def post(path, body):
    request = urllib.request.Request(base + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "Origin": base, "X-Qingqi-CSRF": boot["csrf"]})
    with opener.open(request, timeout=360) as response:
        return json.load(response)

cases = [
    ("incorrect_socratic", {"question": "请检查我实际写的步骤，给我一项提示，先不要告诉我答案。", "expression": "2+3*4", "steps": [{"equation": "2+3*4=20"}], "mode": "socratic"}, "worker_review27b"),
    ("correct_work_protected", {"question": "请核对我的作答是否正确。", "expression": "2+2", "steps": [{"equation": "2+2=4"}], "mode": "explain"}, "worker_review27b"),
    ("actual_history_difficulty", {"question": "根据我的实际学习记录分析学习困难，先给我针对性的追问。", "history": [{"kind": "self_report", "text": "我总是先从左往右计算，没有分清先乘除后加减。"}], "mode": "socratic"}, "worker_difficulty8b"),
]
rows = []
for name, payload, required in cases:
    session = post("/api/sessions", {"title": "真实模型验收 · " + name})["id"]
    job = {"session": session, "request": {"request_id": uuid.uuid4().hex, **payload}}
    try:
        value = post("/api/teach", job)
        result = value["response"]
        detail = value["session"]
        tools = [o["tool"] for o in detail["messages"][-1]["trace"]["observations"]]
        assert result["model_inference"] and result["controller"] == "glm_json_controller" and required in tools, tools
        if name == "incorrect_socratic":
            assert result["teaching_action"] == "ask" and result["step_refs"] == [0] and "14" not in result["text"]
        if name == "correct_work_protected":
            assert result["teaching_action"] == "confirm"
        if name == "actual_history_difficulty":
            assert result["difficulty_candidates"] and result["teaching_action"] == "ask"
        cached = post("/api/teach", job)["response"]
        assert cached["cache_hit"]
        rows.append({"name": name, "passed": True, "tools": tools, "response": result, "idempotent_replay": True})
    except urllib.error.HTTPError as error:
        rows.append({"name": name, "passed": False, "status": error.code, "body": json.load(error)})
    except Exception as error:
        rows.append({"name": name, "passed": False, "error": type(error).__name__ + ": " + str(error)[:200]})
    print(json.dumps({k: v for k, v in rows[-1].items() if k != "response"}, ensure_ascii=False), flush=True)
target = Path(__file__).resolve().parents[1] / ".local/reports/model-acceptance.json"
target.write_text(json.dumps({"scope": "GLM-5.3 + actual specialists + HTTP + persistence", "cases": rows, "real_student_learning_measured": False}, ensure_ascii=False, indent=2), encoding="utf-8")
raise SystemExit(0 if all(r["passed"] for r in rows) else 1)
