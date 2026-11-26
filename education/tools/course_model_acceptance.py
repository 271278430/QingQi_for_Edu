"""Real GLM course orchestration followed by graph verification."""
import http.cookiejar
import json
import urllib.request
import uuid
from pathlib import Path

base = "http://127.0.0.1:18772"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
boot = json.load(opener.open(base + "/api/bootstrap"))
def post(path, value):
    request = urllib.request.Request(base + path, data=json.dumps(value).encode(), headers={"Content-Type": "application/json", "Origin": base, "X-Qingqi-CSRF": boot["csrf"]})
    with opener.open(request, timeout=360) as response:
        return json.load(response)

session = post("/api/sessions", {"title": "课程模型与图谱核对"})["id"]
response = post("/api/teach", {"session": session, "request": {"request_id": uuid.uuid4().hex, "question": "请核对教材里的课程关联，帮我找到三角形概念的章节依据。", "course_query": "13.1 三角形的概念", "subject": "数学"}})
tools = [o["tool"] for o in response["session"]["messages"][-1]["trace"]["observations"]]
assert {"course_search", "worker_course8b", "course_context"} <= set(tools), tools
assert response["response"]["evidence_refs"]
report = {"passed": True, "tools": tools, "response": response["response"], "scope": "actual_GLM_course8b_graph_chain"}
Path(__file__).resolve().parents[1].joinpath(".local/reports/course-model-acceptance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"passed": True, "tools": tools}, ensure_ascii=False))
