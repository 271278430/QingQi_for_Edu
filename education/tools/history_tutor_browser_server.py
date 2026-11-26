"""Actual reported question with controlled plain model text, no real inference."""
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from student_data_acceptance import fixture_root
from qingqi.product import Deployment, server
from qingqi.web_store import WebStore

root = fixture_root()
store = WebStore(root)
entry = next(e for e in store.owner.catalogue.bank.values() if '遮住' in e['expression'] and 'x=6' in e['expression'].replace(' ', '') and '2x+y=16' in e['expression'].replace(' ', ''))
a = store.start_practice('edu-math-student', {'item_id': entry['id'], 'request_id': 'browser-history-start'})
store.owner.practice_action('edu-math-student', 'answer', {'assignment_id': a['id'], 'request_id': 'browser-history-answer', 'answer': 'B'})
addition = next(t['id'] for t in store.owner.catalogue.topics if t['title'] == '有理数的加法法则')
store.owner.set_learning_goal('edu-math-student', addition, 25)
store.close()
class TextFixture(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        payload = json.loads(request['messages'][1]['content'])['input']
        assert '2x+y=16' in payload['problem']['text'].replace(' ', '')
        reply = '先看第二个方程 $2x+y=16$，代入 $x=6$ 得到含 $■$ 的式子。这个条件里没有 $★$，你准备怎样写出代入后的等式？'
        raw = json.dumps({'choices': [{'message': {'content': reply}}], 'usage': {'total_tokens': 60}}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


model = ThreadingHTTPServer(('127.0.0.1', 0), TextFixture)
threading.Thread(target=model.serve_forever, daemon=True).start()
os.environ['EDU_HISTORY_FIXTURE_KEY'] = 'local-protocol-fixture'
config = root / 'history-model.fixture.json'
config.write_text(json.dumps({'models': {'vision': {'enabled': True, 'base_url': f'http://127.0.0.1:{model.server_port}/v1', 'model': 'glm-5.3-flash', 'key_env': 'EDU_HISTORY_FIXTURE_KEY', 'allowed_hosts': ['127.0.0.1'], 'timeout': 20}}}), encoding='utf-8')
instance = server(0, root=root, deployment=Deployment(config=config))
print(json.dumps({'base': f'http://127.0.0.1:{instance.server_port}', 'title': entry['title']}), flush=True)
try:
    instance.serve_forever()
finally:
    instance.server_close()
    model.shutdown()
    model.server_close()
