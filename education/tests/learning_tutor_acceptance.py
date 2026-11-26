"""Real product / local model-protocol acceptance; no real inference claims."""
import base64
import http.cookiejar
import json
import os
import threading
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from student_data_acceptance import fixture_root
from multimodal_fixture import sample_image
from qingqi.product import Deployment, server
from qingqi.storage import Store


def run():
    root = fixture_root()
    calls, checks = [], []

    class Model(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            content = body['messages'][1]['content']
            payload = json.loads(content[0]['text'] if isinstance(content, list) else content)
            calls.append(payload['input'])
            schema = payload.get('required_output_schema')
            if schema or 'request' in payload['input']:
                text = json.dumps({'text': '已知三角形 ABC，AB=AC，讨论两个底角的关系。', 'unclear': False, 'note': ''})
            elif payload['input'].get('teaching_mode') == 'explain':
                text = '我们把当前卡点拆小：等式两边做相同的运算，等式仍成立。比如 $z+3=8$，可以先在两边减去3。再回到原题，你愿意只写这一步吗？'
            else:
                text = '先看题中的已知条件，再确定当前要代入哪一个关系。你能先写出代入后的等式吗？'
            raw = json.dumps({'choices': [{'message': {'content': text}}], 'usage': {'total_tokens': 60}}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

    model = ThreadingHTTPServer(('127.0.0.1', 0), Model)
    threading.Thread(target=model.serve_forever, daemon=True).start()
    os.environ['EDU_LEARNING_FIXTURE_KEY'] = 'local-protocol-fixture'
    config = root / 'learning-model.fixture.json'
    config.write_text(json.dumps({'turn_seconds': 60, 'lease_seconds': 80, 'models': {'vision': {'enabled': True, 'base_url': f'http://127.0.0.1:{model.server_port}/v1', 'model': 'glm-5.3-flash', 'key_env': 'EDU_LEARNING_FIXTURE_KEY', 'allowed_hosts': ['127.0.0.1'], 'timeout': 20}}}), encoding='utf-8')
    instance = server(0, root=root, deployment=Deployment(config=config))
    threading.Thread(target=instance.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{instance.server_port}'
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def get(path):
        with opener.open(base + path, timeout=50) as response:
            return json.load(response)

    boot = get('/api/bootstrap')

    def post(path, body):
        req = urllib.request.Request(base + path, data=json.dumps(body).encode(), headers={'Origin': base, 'Content-Type': 'application/json', 'X-Qingqi-CSRF': boot['csrf']})
        with opener.open(req, timeout=50) as response:
            return json.load(response)

    def teach(session, question, images=None, request_id=None):
        return post('/api/teach', {'session': session, 'request': {'request_id': request_id or uuid.uuid4().hex, 'question': question, **({'images': images} if images else {})}})

    def check(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})
        print(json.dumps(checks[-1]), flush=True)

    owner = Store(root)
    try:
        entry = next(e for e in owner.catalogue.bank.values() if '遮住' in e['expression'] and 'x=6' in e['expression'].replace(' ', '') and '2x+y=16' in e['expression'].replace(' ', ''))
        a = post('/api/practice/start', {'item_id': entry['id'], 'request_id': 'start-bound'})
        post('/api/practice/answer', {'assignment_id': a['id'], 'request_id': 'wrong', 'answer': 'B' if entry['key']['values'][0] == 'A' else 'A'})
        teach(a['session'], '我想复习这道题，请先给我一点提示，不要答案。')
        learner = calls[-1].get('learner_context', {})
        check('owned_problem_receives_actual_weak_topic_evidence', learner.get('matched_problem') and learner.get('current_topic', {}).get('state') == 'needs_practice')
        second = teach(a['session'], '还是不会，能解释这一步吗？')
        check('struggle_escalates_to_explanation_without_final_answer', second['response']['teaching_action'] == 'explain' and calls[-1]['teaching_mode'] == 'explain' and calls[-1].get('teaching_constraint', {}).get('allow_final_answer') is False)
        for _ in range(5):
            teach(a['session'], '这一步为什么可以这样做？')
        teach(a['session'], '请详细讲解。')
        check('explicit_no_answer_survives_more_than_five_turns', calls[-1].get('teaching_constraint', {}).get('allow_final_answer') is False)
        state = json.loads(owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone()[0])
        check('learner_context_is_in_checkpoint_and_byte_budget', state['context']['content'].get('learner') == calls[-1].get('learner_context') and state['context']['metrics']['selected_bytes'] <= state['context']['metrics']['budget'])
        teach(a['session'], '开始新题，解方程 4x+1=13，请直接给答案。')
        check('new_problem_does_not_inherit_no_answer_constraint', json.loads(owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone()[0])['route']['teaching']['allow_final_answer'])
        new_session = post('/api/sessions', {})['id']
        image = post('/api/tutor/images', {'request_id': 'image', 'name': 'geometry.png', 'data_url': 'data:image/png;base64,' + base64.b64encode(sample_image()).decode()})
        teach(new_session, '请给一点提示，不要答案。', [image['id']])
        check('image_tutor_receives_context_without_guessing_topic', calls[-1].get('learner_context', {}).get('matched_problem') is False and calls[-1].get('learner_context', {}).get('current_topic') is None)
        third = teach(new_session, '还是不会，能解释这一步吗？')
        check('image_struggle_uses_step_help_without_final_answer', third['response']['teaching_action'] == 'explain' and calls[-1].get('teaching_constraint', {}).get('allow_final_answer') is False)
        check('help_and_unmatched_image_do_not_create_grades', get('/api/learning')['summary']['attempts'] == 1)
        check('other_student_context_does_not_inherit_weak_topic', owner.tutor_learning_context(__import__('qingqi.contracts', fromlist=['Identity']).Identity('another-student', 's'), entry)['current_topic']['recent_independent_attempts'] == 0)
    finally:
        owner.close()
        instance.shutdown()
        instance.server_close()
        model.shutdown()
        model.server_close()
    from qingqi.agent import PROJECT
    report = {'passed': sum(c['passed'] for c in checks), 'failed': sum(not c['passed'] for c in checks), 'scenarios': checks, 'model_calls': len(calls), 'real_model': False}
    (PROJECT.parent / '.local/reports/learning-tutor-acceptance.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report['failed']


if __name__ == '__main__':
    raise SystemExit(bool(run()))
