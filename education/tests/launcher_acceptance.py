"""Launcher readiness regression using real local HTTP and synthetic credentials."""
import importlib.util
import json
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace


def run():
    spec = importlib.util.spec_from_file_location('run_models', Path(__file__).resolve().parents[1] / 'tools/run_models.py')
    launcher = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(launcher)
    visits = []
    key = 'synthetic-specialist-credential'

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            role = self.path.split('/')[1]
            visits.append(role)
            status = 200 if self.headers.get('Authorization') == 'Bearer ' + key and role not in {'glm', 'vision'} else 401
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'data': [{'id': role + '-model'}]}).encode())

    instance = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    results = []
    try:
        with tempfile.TemporaryDirectory() as root:
            launcher.configuration = Path(root) / 'models.json'
            for name, disabled, mismatch, credential, expected_error in [
                ('cloud_roles_excluded', None, False, key, None),
                ('disabled_specialist_skipped', 'difficulty8b', False, key, None),
                ('wrong_model_rejected', None, True, key, 'ValueError'),
                ('wrong_credential_rejected', None, False, 'wrong-synthetic-key', 'HTTP 401'),
            ]:
                visits.clear()
                models = {role: {'enabled': role != disabled, 'model': role + '-model', 'base_url': f'http://127.0.0.1:{instance.server_port}/{role}/v1'} for role in ('glm', 'vision', 'course8b', 'difficulty8b', 'review27b')}
                if mismatch:
                    models['course8b']['model'] = 'wrong-deployment'
                launcher.configuration.write_text(json.dumps({'models': models}), encoding='utf-8')
                clock = [0.0]
                launcher.time = SimpleNamespace(monotonic=lambda: clock[0], sleep=lambda _: clock.__setitem__(0, 26.0))
                error = None
                try:
                    launcher.wait_for_workers(SimpleNamespace(poll=lambda: None), credential)
                except SystemExit as caught:
                    error = str(caught)
                passed = (error is None if expected_error is None else error is not None and expected_error in error)
                passed = passed and not {'glm', 'vision'}.intersection(visits) and (disabled is None or disabled not in visits)
                if expected_error is None:
                    passed = passed and set(visits) == {'course8b', 'difficulty8b', 'review27b'} - {disabled}
                results.append({'name': name, 'passed': bool(passed), 'roles_requested': list(visits), 'error': error})
                print(json.dumps(results[-1]), flush=True)
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join()
    report = {'scope': 'real_local_http_launcher_readiness', 'cases': results, 'passed': sum(r['passed'] for r in results)}
    (Path(__file__).resolve().parents[1] / '.local/reports/launcher-acceptance.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    raise SystemExit(0 if all(r['passed'] for r in results) else 1)


if __name__ == '__main__':
    run()
