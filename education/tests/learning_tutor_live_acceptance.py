"""Small real GLM evaluation of scaffold progression; isolated public math task."""
import http.cookiejar
import json
import re
import threading
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment, server
from qingqi.storage import Store

root = fixture_root()
instance = server(0, root=root, deployment=Deployment(config=Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{instance.server_port}'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def get(path):
    with opener.open(base + path, timeout=150) as response:
        return json.load(response)


boot = get('/api/bootstrap')


def post(path, body):
    request = urllib.request.Request(base + path, data=json.dumps(body).encode(), headers={'Origin': base, 'Content-Type': 'application/json', 'X-Qingqi-CSRF': boot['csrf']})
    with opener.open(request, timeout=150) as response:
        return json.load(response)


owner = Store(root)
try:
    entry = next(e for e in owner.catalogue.bank.values() if '遮住' in e['expression'] and 'x=6' in e['expression'].replace(' ', '') and '2x+y=16' in e['expression'].replace(' ', ''))
    assignment = post('/api/practice/start', {'item_id': entry['id'], 'request_id': 'live-start'})
    wrong = 'B' if entry['key']['values'][0] == 'A' else 'A'
    post('/api/practice/answer', {'assignment_id': assignment['id'], 'request_id': 'live-wrong', 'answer': wrong})
    cases = []
    for index, question in enumerate(('我想复习这道题，请给一个提示，不要答案。', '我还是不会，请解释把 x=6 代入第二个方程这一步。')):
        result = post('/api/teach', {'session': assignment['session'], 'request': {'request_id': f'live-scaffold-{index}', 'question': question}})
        response = result['response']
        assert response['model_inference'] and response['controller'] == 'glm_practice_text_controller'
        assert response['teaching_action'] == ('ask' if index == 0 else 'explain')
        assert len(response['text']) > 15 and not re.search(r'(?:最终答案|正确选项|答案是)\s*[:：]?\s*\$?[A-D]', response['text'])
        state = json.loads(owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone()[0])
        assert state['context']['content']['learner']['current_topic']['state'] == 'needs_practice'
        assert not state['route']['teaching']['allow_final_answer']
        cases.append({'question': question, 'reply': response['text'], 'action': response['teaching_action'], 'duration_ms': response['duration_ms'], 'real_inference': True})
    assert cases[0]['reply'] != cases[1]['reply'] and get('/api/learning')['summary']['attempts'] == 1
    report = {'model': 'glm-5.3-flash', 'passed': 2, 'real_inference': True, 'isolated_public_question': True,
              'cases': cases, 'scope': '两轮提示/卡点解释与学情读取；非大规模教学有效性评测'}
    Path('education/.local/reports/learning-tutor-live-acceptance.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False), flush=True)
finally:
    owner.close()
    instance.shutdown()
    instance.server_close()
