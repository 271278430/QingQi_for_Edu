"""Real local web requests over the Agent; no remote model or browser fixture."""
import http.cookiejar
import json
import threading
import urllib.error
import urllib.request
import uuid

import pytest

from qingqi.agent import PROJECT
from qingqi.product import server


@pytest.fixture
def web():
    root = PROJECT / 'runs/web_tests' / uuid.uuid4().hex
    instance = server(0, root=root)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{instance.server_port}'
    jar = http.cookiejar.CookieJar()
    client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    def get(path):
        with client.open(base+path, timeout=40) as r:
            return json.load(r)
    bootstrap = get('/api/bootstrap')
    def post(path, body, csrf=True, origin=None):
        nonlocal bootstrap
        headers = {'Content-Type':'application/json','Origin': origin or base}
        if csrf:
            headers['X-Qingqi-CSRF'] = bootstrap['csrf']
        req = urllib.request.Request(base+path, data=json.dumps(body).encode(), headers=headers)
        with client.open(req, timeout=40) as r:
            value = json.load(r)
        if path in {'/api/profile', '/api/login'}:
            bootstrap = value
        return value
    yield base, client, get, post, root
    instance.shutdown()
    instance.server_close()
    thread.join(timeout=2)


def test_web_persists_real_teaching_trace_and_reload(web):
    _, _, get, post, _ = web
    session = post('/api/sessions', {})['id']
    out = post('/api/teach', {'session':session,'request':{'request_id':'r1','question':'给我个性化提示','expression':'2+3*4','steps':[{'equation':'2+3*4=20'}], 'history':[{'kind':'self_report','text':'我不理解运算顺序'}]}})
    assert out['response']['teaching_action']=='ask'
    assert out['response']['model_inference'] is False
    reloaded = get('/api/session?id='+session)
    assert len(reloaded['messages'])==1
    assert len(reloaded['messages'][0]['trace']['observations'])==2
    assert any(e['kind']=='committed' for e in reloaded['messages'][0]['trace']['events'])
    assert get('/api/sessions')['sessions'][0]['title']=='给我个性化提示'


def test_web_profile_switch_cannot_read_other_student_session_or_memory(web):
    _, _, get, post, _ = web
    a = post('/api/sessions', {})['id']
    post('/api/teach', {'session':a,'request':{'request_id':'private','question':'分析学情','history':[{'kind':'self_report','text':'学生A的独立学习记录'}]}})
    post('/api/profile', {'profile':'student-b'})
    assert get('/api/sessions')['sessions']==[]
    assert get('/api/memory')=={'episodes':[],'facts':[]}
    with pytest.raises(urllib.error.HTTPError) as err:
        get('/api/session?id='+a)
    assert err.value.code==403
    with pytest.raises(urllib.error.HTTPError) as err:
        post('/api/teach',{'session':a,'request':{'question':'你好'}})
    assert err.value.code==403
    post('/api/profile', {'profile':'student-a'})
    assert get('/api/sessions')['sessions'][0]['id']==a


def test_web_csrf_and_origin_and_unknown_profile_rejected(web):
    _, _, _, post, _ = web
    for kwargs in [{'csrf':False}, {'origin':'http://external.invalid'}]:
        with pytest.raises(urllib.error.HTTPError) as err:
            post('/api/sessions',{},**kwargs)
        assert err.value.code==403
    with pytest.raises(urllib.error.HTTPError) as err:
        post('/api/profile',{'profile':'arbitrary-user'})
    assert err.value.code==400


def test_web_ignores_no_identity_override_and_keeps_idempotence(web):
    _, _, get, post, _ = web
    s = post('/api/sessions',{})['id']
    request = {'request_id':'same','question':'检查作答','expression':'2+2','steps':[{'equation':'2+2=4'}]}
    assert post('/api/teach',{'session':s,'request':request})['response']['teaching_action']=='confirm'
    assert post('/api/teach',{'session':s,'request':request})['response']['cache_hit']
    assert len(get('/api/session?id='+s)['messages'])==1
    with pytest.raises(urllib.error.HTTPError) as err:
        post('/api/teach',{'session':s,'request':{**request,'student':'other'}})
    assert err.value.code==400


def test_web_static_assets_have_csp_and_no_file_traversal(web):
    base, client, _, _, _ = web
    import re
    with client.open(base+'/') as response:
        html = response.read().decode()
    assets = re.findall(r'(?:src|href)="(/assets/[^"]+)"', html)
    assert assets, 'current Vite build must expose actual assets'
    for path in ['/', *assets]:
        with client.open(base+path) as response:
            assert "script-src 'self'" in response.headers['Content-Security-Policy']
            assert response.read()
    with pytest.raises(urllib.error.HTTPError) as err:
        client.open(base+'/../../README.md')
    assert err.value.code in {403,404}
