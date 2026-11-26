"""Actual authenticated specialist inference, records no credentials or paths."""
import json
import os
import sys
from pathlib import Path

EDUCATION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EDUCATION / "service/src"))
from qingqi.product import Deployment
from qingqi.providers import JSONModel
from qingqi.workers import make_workers

deployment = Deployment(EDUCATION / "service/config/models.local.json")
models = {name: JSONModel(endpoint) for name, endpoint in deployment.endpoints.items() if name != "glm"}
workers = make_workers(models)
cases = [
    ("worker_review27b", {"expression": "2+3*4", "steps": [{"equation": "2+3*4=20"}], "mode": "socratic"}),
    ("worker_review27b", {"expression": "2+2", "steps": [{"equation": "2+2=4"}], "mode": "explain"}),
    ("worker_difficulty8b", {"history": [{"kind": "self_report", "text": "我总是先从左往右计算，没有分清先乘除后加减。"}]}),
    ("worker_course8b", {"query": "七年级上册 · 角的比较", "candidates": [{"id": "probe-only", "title": "角的比较"}]}),
]
results = []
for tool, args in cases:
    try:
        value = workers[tool][1](**args)
        results.append({"tool": tool, "passed": True, "output": value})
    except Exception as error:
        results.append({"tool": tool, "passed": False, "error": type(error).__name__ + ": " + str(error)[:200]})
    print(json.dumps(results[-1], ensure_ascii=False), flush=True)
report = {"scope": "actual_specialist_inference", "cases": results, "usage": [u for model in models.values() for u in model.usage], "real_student_learning_measured": False}
(EDUCATION / ".local/reports/specialist-acceptance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
raise SystemExit(0 if all(r["passed"] for r in results) else 1)
