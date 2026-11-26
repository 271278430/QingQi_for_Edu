"""Actual HTTP model configuration races, frozen turns and unknown-outcome recovery."""
import concurrent.futures,json,http.cookiejar,urllib.request,urllib.error
from pathlib import Path
from model_settings_fixture import Fixture,KEY

f=Fixture();f.start();checks=[]
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(f.base+path) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body,expected=200,stream=False):
    req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'X-Qingqi-CSRF':boot['csrf'],'Content-Type':'application/json',**({'Accept':'text/event-stream'} if stream else {})})
    try:r=o.open(req,timeout=90)
    except urllib.error.HTTPError as e:r=e
    with r:
        assert r.code==expected,(path,r.code,r.read().decode())
        return [json.loads(line[6:]) for line in r if line.startswith(b'data: ')] if stream else json.load(r)
def check(name,ok):
    assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def provider(model='vision-local',image=True,tools=True,key=True):
    return {'id':'custom-race','display_name':'race','model':model,'base_url':f.model_base,'protocol':'openai','supports_image':image,'supports_tools':tools,'requires_key':key,'timeout':15,'max_tokens':1600,'json_mode':False,'api_key':KEY if key else '', 'key_action':'replace' if key else 'clear'}
counter=0
def save(p,expected=200):
    global counter
    counter+=1
    return post('/api/settings/model-providers',{'request_id':'save-'+str(counter),'version':get('/api/settings/models')['version'],'operation':'upsert','provider':p},expected)
def select():
    global counter
    counter+=1
    return post('/api/settings/model-selection',{'request_id':'select-'+str(counter),'version':get('/api/settings/models')['version'],'mode':'shared','text_provider_id':'custom-race','vision_provider_id':'custom-race'})
def teach(session,rid):return post('/api/teach',{'session':session,'request':{'request_id':rid,'question':'二次函数的顶点是什么？'}},stream=True)
try:
    save(provider());select();version=get('/api/settings/models')['version']
    save(provider(image=False),400)
    check('editing_active_visual_connection_cannot_disable_images',get('/api/settings/models')['version']==version)
    save(provider(model='noauth-local',key=False,tools=False));session=post('/api/sessions',{},201)['id'];events=teach(session,'noauth')
    check('local_no_auth_model_and_no_native_tools_are_supported',events[-1]['kind']=='done' and not f.calls[-1]['authenticated'] and not f.calls[-1]['has_tools'])
    save(provider(model='gated-model'));session=post('/api/sessions',{},201)['id']
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        f.started.clear();f.release.clear();future=pool.submit(teach,session,'frozen-turn')
        assert f.started.wait(15),'model did not start'
        save(provider(model='updated-model'));f.release.set();events=future.result()
    check('in_flight_turn_keeps_frozen_model_when_settings_change',events[-1]['kind']=='done' and f.calls[-1]['model']=='gated-model')
    count=len(f.calls);events=teach(session,'frozen-turn')
    check('completed_turn_replays_after_model_change_without_inference',events[-1]['kind']=='done' and len(f.calls)==count)
    next_session=post('/api/sessions',{},201)['id'];events=teach(next_session,'new-selection')
    check('new_turn_uses_new_configuration',events[-1]['kind']=='done' and f.calls[-1]['model']=='updated-model')
    save(provider(model='gated-model'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        f.started.clear();f.release.clear();future=pool.submit(post,'/api/settings/models/test',{'provider_id':'custom-race','kind':'text'})
        assert f.started.wait(15),'probe did not start'
        save(provider(model='updated-model'));f.release.set();result=future.result()
    view=get('/api/settings/models')
    check('probe_for_old_provider_version_is_not_committed',result.get('stale') and not next(p for p in view['providers'] if p['id']=='custom-race')['tests'])
    save(provider(model='disconnect-model'));session=post('/api/sessions',{},201)['id'];count=len(f.calls);events=teach(session,'unknown-turn')
    check('incomplete_stream_records_unknown_without_auto_retry',events[-1]['kind']=='error' and events[-1]['error']=='model_unknown' and len(f.calls)==count+1)
    save(provider(model='updated-model'));count=len(f.calls);events=teach(session,'unknown-turn')
    check('changed_model_rejects_unfinished_old_request_without_inference',events[-1]['kind']=='error' and events[-1]['error']=='model_changed' and len(f.calls)==count)
    version=get('/api/settings/models')['version']
    for field,value in [('base_url',123),('base_url','http://127.0.0.1:bad'),('protocol',[]),('credential_ref',[]),('key_action',[])]:
        p=provider();p[field]=value;save(p,400)
    post('/api/settings/model-selection',{'request_id':'wrong-role','version':version,'mode':'split','text_provider_id':[],'vision_provider_id':'custom-race'},400)
    post('/api/settings/models/test',{'provider_id':'custom-race','kind':[]},400)
    check('malformed_model_fields_return_validation_without_state_change',get('/api/settings/models')['version']==version and len(f.calls)==count)
    p=provider();p['model']=' vision-local ';p['base_url']=' '+f.model_base+' ';view=save(p)
    saved=next(p for p in view['providers'] if p['id']=='custom-race')
    check('copied_model_and_url_whitespace_is_normalized',saved['model']=='vision-local' and saved['base_url']==f.model_base)
    check('configuration_races_do_not_create_grades',get('/api/learning')['summary']['attempts']==0)
    Path('education/.local/reports/model-settings-edge.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True,'real_inference':False},ensure_ascii=False,indent=2),encoding='utf-8')
finally:
    f.release.set();f.close()
