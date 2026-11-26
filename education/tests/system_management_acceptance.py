"""Settings permissions, real effects, concurrency and source-backed architecture via HTTP."""
import http.cookiejar
import json
import threading
import urllib.error
import urllib.request
from pathlib import Path
from conversation_problem_fixture import Fixture
from qingqi.product import server,Deployment,password_hash

f=Fixture();f.start();checks=[];other=None
def client(base):
    o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with o.open(base+path,timeout=90) as r:return json.load(r)
    boot=get('/api/bootstrap')
    def post(path,data):
        with o.open(urllib.request.Request(base+path,data=json.dumps(data).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']}),timeout=90) as r:return json.load(r)
    return get,post,boot
get,post,boot=client(f.base)
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def status(action,expected):
    try:action()
    except urllib.error.HTTPError as e:return e.code==expected
    return False
try:
    check('local_owner_has_management_capability',boot['can_manage'] and boot['settings']['app_name']=='清启')
    overview=get('/api/settings');arch=get('/api/settings/architecture')
    check('real_source_modules_tools_and_skills_are_present',len(arch['modules'])==16 and {'loop','routing','tools','skills','memory','models','visuals','data','management','permissions'}<={m['id'] for m in arch['modules']} and len(arch['tools'])==10 and len(arch['skills'])==7 and {'recommend_practice','preview_learning_path','read_learning_dashboard'}<={t['name'] for t in arch['tools']})
    check('one_system_map_has_actual_source_and_owner',bool(arch['panorama']['nodes']) and not any(k in arch for k in ('request_flow','business_flow')) and all(m['files'] and m['owner'] and m['scope']['steps'] and m['reuse'] and m['limits'] for m in arch['modules']))
    check('admin_projection_contains_no_credentials_or_endpoint_urls',all(word not in json.dumps(overview) for word in ('password_hash','api_key','base_url','key_env')))
    body={'request_id':'setting-one',**overview['settings'],'app_name':'清启数学','notice':'按当前题目进行精确数学辅导','maintenance':True}
    saved=post('/api/settings',body)
    check('settings_are_persisted_and_visible_in_bootstrap',saved['version']==1 and get('/api/bootstrap')['settings']==saved)
    check('accepted_setting_command_is_idempotent',post('/api/settings',body)==saved)
    check('stale_version_is_rejected',status(lambda:post('/api/settings',{**body,'request_id':'stale'}),409))
    check('same_command_cannot_change_payload',status(lambda:post('/api/settings',{**body,'notice':'changed'}),409))
    before=get('/api/learning')['summary']
    session=post('/api/sessions',{})['id']
    check('maintenance_really_blocks_new_tutoring',status(lambda:post('/api/teach',{'session':session,'request':{'request_id':'paused','question':'直接算2+3'}}),423))
    check('maintenance_blocks_practice_and_keeps_reading_available',status(lambda:post('/api/practice/recommendations',{'request_id':'paused-batch'}),423) and get('/api/learning')['summary']==before and get('/api/settings/architecture')['version']==arch['version'])
    restored=post('/api/settings',{**saved,'request_id':'restore','app_name':'清启','notice':'','maintenance':False})
    check('operator_can_restore_service_without_restart',restored['version']==2 and not get('/api/bootstrap')['settings']['maintenance'])
    check('old_command_replay_projects_newer_settings_without_rollback',post('/api/settings',body)==restored and get('/api/bootstrap')['settings']==restored)
    check('html_setting_payload_is_rejected',status(lambda:post('/api/settings',{**restored,'request_id':'bad-html','notice':'<script>bad</script>'}),400))
    accounts=f.root/'accounts.fixture.json';accounts.write_text(json.dumps({'accounts':{'math-student':{'name':'普通学生','role':'student','password_hash':password_hash('local-fixture-pass'),'can_manage':False}}}),encoding='utf-8')
    other=server(0,root=f.root,deployment=Deployment(accounts=accounts));threading.Thread(target=other.serve_forever,daemon=True).start()
    g,p,b=client(f'http://127.0.0.1:{other.server_port}');login=p('/api/login',{'username':'math-student','password':'local-fixture-pass'});b.update(login)
    check('normal_student_cannot_read_or_write_admin_state',not login['can_manage'] and status(lambda:g('/api/settings'),403) and status(lambda:g('/api/settings/architecture'),403) and status(lambda:p('/api/settings',{**restored,'request_id':'unauthorized'}),403))
    Path('education/.local/reports/system-management.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
finally:
    f.close()
    if other:other.shutdown();other.server_close()
