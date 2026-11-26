"""Real GLM natural tutoring of public catalogue questions in an isolated student."""
import http.cookiejar
import json
import re
import threading
import urllib.request
import uuid
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.catalogue import Catalogue, complete_item
from qingqi.product import Deployment, server

root = fixture_root()
c = Catalogue(root)
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


def teach(session, question, request_id=None):
    return post('/api/teach', {'session': session, 'request': {'request_id': request_id or uuid.uuid4().hex, 'question': question}})


results = []
try:
    masked = next(e for e in c.bank.values() if '遮住' in e['expression'] and 'x=6' in e['expression'].replace(' ', '') and '2x+y=16' in e['expression'].replace(' ', ''))
    entries = [masked]
    for keyword in ('坐标', '不等式', '角', '实际问题与一元一次方程'):
        entry = next(e for e in c.bank.values() if keyword in e['title'] and e.get('grade') == '7' and complete_item(e))
        entries.append(entry)
    for entry in entries:
        a = post('/api/practice/start', {'item_id': entry['id'], 'request_id': uuid.uuid4().hex})
        q = '返回原练习，我想复习这道历史题，请先和我讨论解题思路。先不要给最终答案。'
        before = get('/api/learning')['summary']['attempts']
        first = teach(a['session'], q)
        reply = first['response']
        assert reply['model_inference'] and reply['controller'] == 'glm_practice_text_controller'
        assert reply['teaching_action'] == 'ask' and len(reply['text']) > 25 and not re.search(r'你希望查询课程|请提供完整题目|正确选项[是为][:：]?\s*[ABCD]', reply['text'])
        follow = teach(a['session'], '我有点疑惑，能具体解释刚才这个条件怎么用吗？还是先不要给最终答案。')
        assert follow['response']['model_inference'] and follow['response']['controller'] == 'glm_practice_text_controller'
        assert get('/api/learning')['summary']['attempts'] == before
        results.append({'topic': entry['title'], 'problem': entry['expression'], 'first': reply['text'], 'followup': follow['response']['text'], 'real_inference': True})
        print(json.dumps({'topic': entry['title'], 'passed': True}), flush=True)
        if entry is masked:
            assert not re.search(r'y\s*=\s*4|[■★]\s*[=＝]\s*(4|10)', reply['text'])
            checked = teach(a['session'], 'y=4')
            assert checked['response']['teaching_action'] == 'confirm' and get('/api/learning')['summary']['attempts'] == before
            final = teach(a['session'], 'A', 'live-final-fixed')
            assert final['response']['teaching_action'] == 'confirm'
            teach(a['session'], 'A', 'live-final-fixed')
            assert get('/api/learning')['summary']['attempts'] == before + 1
    Path('education/.local/reports/history-tutor-live-acceptance.json').write_text(json.dumps({'model': 'glm-5.3-flash', 'passed': len(results), 'real_model': True, 'isolated_student': True, 'cases': results}, ensure_ascii=False, indent=2), encoding='utf-8')
finally:
    instance.shutdown()
    instance.server_close()
    c.db.close()
