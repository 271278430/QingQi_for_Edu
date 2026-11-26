"""Local HTTP protocol fixture; verifies transport constraints, not model quality."""
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service/src"))
from qingqi.contracts import Request
from qingqi.providers import Endpoint, GLMController, JSONModel
from qingqi.layered_routing import make_dag

requests = []
class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        requests.append(body)
        payload = json.loads(body["messages"][1]["content"])["input"]
        refs = payload.get("observed_evidence_refs", [])
        action = {"kind": "respond", "reply": {"text": "请查看依据 e0。" if refs else "请继续思考。", "teaching_action": "ask", "evidence_refs": refs[:1], "step_refs": []}}
        raw = json.dumps({"choices": [{"message": {"content": json.dumps(action)}}]}).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

instance = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
thread = threading.Thread(target=instance.serve_forever, daemon=True)
thread.start()
previous_key = os.environ.get("QINGQI_PROTOCOL_FIXTURE_KEY")
os.environ["QINGQI_PROTOCOL_FIXTURE_KEY"] = "fixture-only"
tests = []
try:
    endpoint = Endpoint(name="fixture", base_url=f"http://127.0.0.1:{instance.server_port}/v1", model="fixture", key_env="QINGQI_PROTOCOL_FIXTURE_KEY", enabled=True, allowed_hosts=("127.0.0.1",), json_mode=True)
    state = {"route": {"intents": ["chat"], "task_dag": make_dag(("chat",)), "teaching": {"allow_final_answer": False}},
             "native_schedule": {"order": ["chat"]}, "cursor": 0, "observations": [], "allowed_tools": [], "diagnosis_history": [], "repairs": 0}
    class EmptyRegistry:
        specs = {}
        def model_contracts(self, names):
            assert names == []
            return []
    GLMController(JSONModel(endpoint)).next(Request.parse({"request_id": "fixture", "question": "课程查询", "mode": "socratic"}), state, {"content": {}}, EmptyRegistry())
    assert requests[-1]["response_format"] == {"type": "json_object"}
    tests.append({"name": "json_mode_sent_to_compatible_provider", "passed": True})
    schema = json.loads(requests[-1]["messages"][1]["content"])["required_output_schema"]
    actions = schema["properties"]["reply"]["properties"]["teaching_action"]["enum"]
    assert "ask" in actions and "explain" not in actions and "give_answer" not in actions and "confirm" not in actions
    tests.append({"name": "socratic_action_schema_respects_policy", "passed": True})
    plain = Endpoint(name="fixture", base_url=endpoint.base_url, model="fixture", key_env=endpoint.key_env, enabled=True, allowed_hosts=endpoint.allowed_hosts)
    JSONModel(plain).generate("fixture", {}, {"type": "object"})
    assert "response_format" not in requests[-1]
    tests.append({"name": "other_provider_format_unchanged", "passed": True})
    real_ref = "node:课标|urn:example:Section:l50"
    observed = {**state, "observations": [{"tool": "course_context", "result": {"evidence": [{"ref": real_ref, "text": "已查询章节", "source": "fixture"}]}}]}
    reply = GLMController(JSONModel(endpoint)).next(Request.parse({"request_id": "citation", "question": "已查询章节", "mode": "socratic"}), observed, {"content": {}}, EmptyRegistry())
    assert reply["reply"]["evidence_refs"] == [real_ref]
    assert reply["reply"]["text"] == "请查看依据 教材章节来源。"
    assert json.loads(requests[-1]["messages"][1]["content"])["input"]["state"]["observations"][0]["result"]["evidence"][0]["ref"] == "e0"
    tests.append({"name": "observed_alias_restores_exact_graph_reference", "passed": True})
finally:
    instance.shutdown()
    instance.server_close()
    thread.join(2)
    if previous_key is None:
        os.environ.pop("QINGQI_PROTOCOL_FIXTURE_KEY", None)
    else:
        os.environ["QINGQI_PROTOCOL_FIXTURE_KEY"] = previous_key

report = {"passed": len(tests) == 4, "tests": tests, "scope": "local actual HTTP protocol fixture, no remote inference"}
Path(__file__).resolve().parents[1].joinpath(".local/reports/provider-protocol-acceptance.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report))
