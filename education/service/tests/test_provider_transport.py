"""Local HTTP contract fixtures: real transport, no actual model inference."""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from qingqi.contracts import ContractError, obj
from qingqi.providers import Endpoint, JSONModel


@pytest.mark.parametrize("protocol", ["openai", "anthropic"])
def test_model_client_transports_json_and_records_provider_usage(protocol, monkeypatch):
    calls = []
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            calls.append((self.path, json.loads(self.rfile.read(int(self.headers["Content-Length"])))) )
            if protocol == "openai":
                body = {"choices": [{"message": {"content": '{"ok":true}'}}], "usage": {"prompt_tokens": 11, "completion_tokens": 4}}
            else:
                body = {"content": [{"type": "text", "text": '{"ok":true}'}], "usage": {"input_tokens": 11, "output_tokens": 4}}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())
    instance = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    monkeypatch.setenv("QINGQI_LOCAL_FIXTURE_KEY", "synthetic-contract-fixture-no-real-secret")
    client = JSONModel(Endpoint("fixture", f"http://127.0.0.1:{instance.server_port}/v1", "fixture-not-llm", "QINGQI_LOCAL_FIXTURE_KEY", protocol=protocol, enabled=True, allowed_hosts=("127.0.0.1",)))
    try:
        assert client.generate("Return JSON", {"question": "hello"}, obj({"ok": {"type": "boolean"}})) == {"ok": True}
        assert len(client.usage) == 1
        assert calls[0][0].endswith("/messages" if protocol == "anthropic" else "/chat/completions")
        assert "synthetic-contract-fixture" not in json.dumps(calls)
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join(timeout=2)


def test_model_json_error_is_contract_error_for_bounded_loop_repair(monkeypatch):
    class Response:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def read(self, *args):
            return b'{"choices":[{"message":{"content":"not-json"}}]}'
    class Opener:
        def open(self, *args, **kwargs):
            return Response()
    monkeypatch.setenv("QINGQI_LOCAL_FIXTURE_KEY", "fixture-only")
    monkeypatch.setattr("urllib.request.build_opener", lambda *args: Opener())
    client = JSONModel(Endpoint("fixture", "http://127.0.0.1:1/v1", "fixture", "QINGQI_LOCAL_FIXTURE_KEY", enabled=True, allowed_hosts=("127.0.0.1",)))
    with pytest.raises(ContractError, match="JSON"):
        client.generate("system", {}, {})
