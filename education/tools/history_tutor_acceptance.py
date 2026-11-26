"""User-reported history question through the real isolated HTTP owner."""
import http.cookiejar
import json
import threading
import urllib.request
import uuid
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import server
from qingqi.web_store import WebStore

root = fixture_root()
store = WebStore(root)
instance = server(0, root=root)
thread = threading.Thread(target=instance.serve_forever, daemon=True)
thread.start()
base = f'http://127.0.0.1:{instance.server_port}'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base + path, timeout=40) as response:
        return json.load(response)
boot = get('/api/bootstrap')
def post(path, payload):
    request = urllib.request.Request(base + path, data=json.dumps(payload).encode(), headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
    with opener.open(request, timeout=40) as response:
        return json.load(response)
def teach(session, question, rid=None):
    return post('/api/teach', {'session':session, 'request':{'request_id':rid or uuid.uuid4().hex,'question':question}})
results=[]
def check(name, passed):
    results.append({'name':name,'passed':bool(passed)})
    print(json.dumps(results[-1]), flush=True)
    assert passed, name
try:
    entry = next(e for e in store.owner.catalogue.bank.values() if '遮住' in e['expression'] and 'x=6' in e['expression'].replace(' ','') and '2x+y=16' in e['expression'].replace(' ',''))
    assignment = post('/api/practice/start', {'item_id':entry['id'],'request_id':'masked-start'})
    reply = teach(assignment['session'], '返回原练习，我想复习这道历史题，请先和我讨论解题思路。', 'masked-first')
    check('exact_reported_history_phrase_starts_the_owned_question', reply['response']['teaching_action']=='ask' and '你希望查询' not in reply['response']['text'] and '请提供' not in reply['response']['text'] and ('16' in reply['response']['text'] or '第二个方程' in reply['response']['text']))
    before = get('/api/learning')['summary']['attempts']
    checked = teach(assignment['session'], 'y=4')
    check('masked_system_intermediate_value_is_checked_without_grade', checked['response']['teaching_action']=='confirm' and get('/api/learning')['summary']['attempts']==before)
    check('masked_system_wrong_option_is_not_confirmed', teach(assignment['session'],'B')['response']['teaching_action']!='confirm')
    after_wrong = get('/api/learning')['summary']['attempts']
    final = teach(assignment['session'],'A','masked-final')
    check('final_choice_uses_same_catalogue_grade', final['response']['teaching_action']=='confirm' and get('/api/learning')['summary']['attempts']==after_wrong+1)
    teach(assignment['session'],'A','masked-final')
    check('final_replay_does_not_duplicate_grade',get('/api/learning')['summary']['attempts']==after_wrong+1)
    teach(assignment['session'],'取消')
    check('cancelled_binding_cannot_grade_a_bare_option',teach(assignment['session'],'A')['response']['teaching_action']!='confirm')
    check('explicit_history_return_restores_binding_after_cancel',teach(assignment['session'],'返回原练习，讨论解题思路')['response']['teaching_action']=='ask')
    isolated = post('/api/sessions',{})
    check('another_session_cannot_borrow_history_question',teach(isolated['id'],'y=4')['response']['teaching_action']!='confirm')
    from qingqi.catalogue import complete_item
    representatives = {}
    for e in store.owner.catalogue.bank.values():
        if e.get('grade')=='7' and complete_item(e):
            representatives.setdefault(e['topic'],e)
    for topic,e in representatives.items():
        a = post('/api/practice/start',{'item_id':e['id'],'request_id':uuid.uuid4().hex})
        result = teach(a['session'],'返回原练习，我想复习这道历史题，请先和我讨论解题思路。')
        check('owned_history_topic_'+topic,result['response']['teaching_action']=='ask' and '请提供' not in result['response']['text'] and '你希望查询' not in result['response']['text'])
        follow = teach(a['session'],'我有点疑惑，能解释一下刚才的关系吗？')
        check('contextual_followup_topic_'+topic,follow['response']['teaching_action'] in {'ask','explain'} and '你希望查询' not in follow['response']['text'])
finally:
    instance.shutdown(); instance.server_close(); thread.join(2); store.close()
Path('education/.local/reports/history-tutor-acceptance.json').write_text(json.dumps({'passed':len(results),'scenarios':results,'real_model':False},ensure_ascii=False,indent=2),encoding='utf-8')
