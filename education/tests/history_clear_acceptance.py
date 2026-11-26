"""Project-wide history deletion through the authenticated API and original Store."""
import base64
import http.cookiejar
import json
import threading
import urllib.error
import urllib.request
from pathlib import Path
from conversation_problem_fixture import Fixture
from multimodal_fixture import sample_image
from qingqi.contracts import Identity, Request
from qingqi.product import server, Deployment, password_hash
from qingqi.storage import Store
from qingqi.web_store import WebStore
from qingqi.zcode_runtime import RuntimeFailure

f=Fixture();f.start();other=None;checks=[]
def client(base):
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(base+path,timeout=90) as r:return json.load(r)
    boot=get('/api/bootstrap')
    def post(path,body,csrf=True):
        headers={'Origin':base,'Content-Type':'application/json'}
        if csrf:headers['X-Qingqi-CSRF']=boot['csrf']
        with opener.open(urllib.request.Request(base+path,data=json.dumps(body).encode(),headers=headers),timeout=90) as r:return json.load(r)
    return get,post,boot
get,post,boot=client(f.base)
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def status(action,code):
    try:action()
    except urllib.error.HTTPError as error:return error.code==code
    return False
payload={'request_id':'clear-all','scope':'project'}
try:
    owner=Store(f.root)
    session=post('/api/sessions',{})['id']
    post('/api/teach',{'session':session,'request':{'request_id':'seed-reply','question':'2+3，直接给答案'}})
    post('/api/tutor/images',{'request_id':'seed-image','name':'test.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})
    item=get('/api/learning')['recommendations'][0]
    assignment=post('/api/practice/start',{'request_id':'seed-practice','item_id':item['id']})
    answer=owner.catalogue.item(item['id'])['key']['values'][0]
    post('/api/practice/answer',{'request_id':'seed-answer','assignment_id':assignment['id'],'answer':answer})
    owner.confirm_fact(Identity('edu-math-student',session),'fixture','synthetic-fact','synthetic-source',teacher_authorized=True)
    version=owner.catalogue.version;topics=len(owner.catalogue.initial['topics'])
    check('clear_without_csrf_is_rejected',status(lambda:post('/api/settings/history/clear',payload,False),403))
    locked,_,_=owner.begin(Identity('edu-math-student',session),Request.parse({'request_id':'active-run','question':'synthetic-pending'}))
    check('active_agent_lease_blocks_destructive_clear',status(lambda:post('/api/settings/history/clear',payload),409))
    owner.release(locked)
    admission=WebStore(f.root);old_epoch=admission.admit_teaching('edu-math-student',session);admission.close()
    result=post('/api/settings/history/clear',payload)
    check('authenticated_project_clear_removes_sessions',not get('/api/sessions')['sessions'] and result['deleted']['web_sessions']>=2)
    cleared=('runs','events','calls','model_invocations','episodes','facts','dialogue_state','tutor_images','practice_events','practice_starts','practice_assignments','learning_routes')
    check('all_related_history_and_memory_are_removed',all(owner.db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]==0 for t in cleared) and owner.current_problem(Identity('edu-math-student',session)) is None)
    check('imported_historical_questions_are_not_shown_again',get('/api/practice/history')['items']==[] and get('/api/learning')['initial']['history_count']==0)
    check('initial_profile_and_readonly_catalogue_are_retained',owner.catalogue.version==version and len(get('/api/learning')['topics'])==topics and get('/api/learning')['initial']['subject']=='数学' and get('/api/learning')['summary']['attempts']==0)
    try:owner.begin(Identity('edu-math-student',session),Request.parse({'request_id':'late-admitted','question':'late-request'}),expected_history_epoch=old_epoch)
    except RuntimeFailure as e:check('old_admission_cannot_resurrect_deleted_session',e.code=='history_changed')
    else:raise AssertionError('stale admission accepted')
    check('deleted_images_and_sessions_cannot_be_read',status(lambda:get('/api/session?id='+session),403))
    other=server(0,root=f.root,deployment=Deployment());threading.Thread(target=other.serve_forever,daemon=True).start()
    g,p,b=client(f'http://127.0.0.1:{other.server_port}')
    check('shared_second_entry_does_not_reimport_deleted_history',g('/api/sessions')['sessions']==[] and g('/api/practice/history')['items']==[] and g('/api/memory')['episodes']==[])
    imported=owner.catalogue.item(item['id'])
    # 在隔离Store模拟源快照仍持有历史题标记；清理后的新作答应以当前历史状态判断。
    owner.catalogue.initial={**owner.catalogue.initial,'historical_items':[imported['id']]}
    work=post('/api/practice/start',{'request_id':'fresh-imported-question','item_id':imported['id']})
    answer=owner.practice_action('edu-math-student','answer',{'request_id':'fresh-imported-answer','assignment_id':work['id'],'answer':imported['key']['values'][0]})
    check('cleared_imported_attempts_do_not_disqualify_new_independent_work',answer['correct'] and answer['independent_first'])
    fresh=post('/api/sessions',{})['id']
    post('/api/teach',{'session':fresh,'request':{'request_id':'after-clear','question':'2+3，直接给答案'}})
    replay=post('/api/settings/history/clear',payload)
    check('old_clear_replay_does_not_delete_new_history',replay['already_applied'] and get('/api/sessions')['sessions'][0]['id']==fresh and len(get('/api/session?id='+fresh)['messages'])==1)
    check('request_id_payload_conflict_is_rejected',status(lambda:post('/api/settings/history/clear',{**payload,'scope':'student'}),400))
    other.shutdown();other.server_close();other=None
    accounts=f.root/'history-accounts.local.json';accounts.write_text(json.dumps({'accounts':{'learner':{'name':'普通学生','role':'student','password_hash':password_hash('synthetic-pass'),'can_manage':False}}}),encoding='utf-8')
    other=server(0,root=f.root,deployment=Deployment(accounts=accounts));threading.Thread(target=other.serve_forever,daemon=True).start()
    g,p,b=client(f'http://127.0.0.1:{other.server_port}');b.update(p('/api/login',{'username':'learner','password':'synthetic-pass'}))
    check('ordinary_account_cannot_clear_any_history',status(lambda:p('/api/settings/history/clear',{'request_id':'unauthorized','scope':'project'}),403))
    check('clear_receipt_contains_only_counts_no_deleted_content',all(k not in json.dumps(result) for k in ('synthetic-fact','question','response','data_url','password')))
    owner.close()
    Path('education/.local/reports/history-clear.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
finally:
    f.close()
    if other:other.shutdown();other.server_close()
