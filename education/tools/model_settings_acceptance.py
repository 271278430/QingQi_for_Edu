"""Model selection, encrypted credentials and actual OpenAI/Anthropic HTTP regression."""
import base64,json,http.cookiejar,urllib.request,urllib.error
from pathlib import Path
from model_settings_fixture import Fixture,KEY
from multimodal_fixture import sample_image
from qingqi.storage import Store

f=Fixture();f.start();checks=[]
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(f.base+path) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body,expected=200,csrf=None,stream=False):
    req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'X-Qingqi-CSRF':csrf if csrf is not None else boot['csrf'],'Content-Type':'application/json',**({'Accept':'text/event-stream'} if stream else {})})
    try:response=o.open(req,timeout=100)
    except urllib.error.HTTPError as e:response=e
    with response as r:
        assert r.code==expected,(r.code,path,r.read().decode())
        if stream:return [json.loads(line[6:]) for line in r if line.startswith(b'data: ')]
        return json.load(r)
def check(name,ok):
    assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def provider(id,protocol='openai',image=True,model='vision-local'):
    return {'id':'custom-'+id,'display_name':id,'model':model,'base_url':f.model_base,'protocol':protocol,'supports_image':image,'supports_tools':True,'requires_key':True,'timeout':15,'max_tokens':1600,'json_mode':False,'api_key':KEY,'key_action':'replace'}
def save(p,rid=None):
    return post('/api/settings/model-providers',{'request_id':rid or 'save-'+p['id'],'version':get('/api/settings/models')['version'],'operation':'upsert','provider':p})
def select(mode,text,vision,rid):
    return post('/api/settings/model-selection',{'request_id':rid,'version':get('/api/settings/models')['version'],'mode':mode,'text_provider_id':text,'vision_provider_id':vision})
try:
    view=get('/api/settings/models');check('default_split_roles_and_no_keys_in_get',view['selection']['mode']=='split' and KEY not in json.dumps(view) and len(view['providers'])==2)
    save(provider('vision'));view=get('/api/settings/models');check('saved_key_is_encrypted_and_usable',KEY not in (f.root/'agent.sqlite').read_bytes().decode(errors='ignore') and next(p for p in view['providers'] if p['id']=='custom-vision')['credential_ready'])
    check('model_discovery_and_image_capability',post('/api/settings/models/discover',{'provider_id':'custom-vision'})['models'][1]['supports_image'] is True)
    check('text_and_synthetic_image_tests_use_formal_adapter',post('/api/settings/models/test',{'provider_id':'custom-vision','kind':'text'})['success'] and post('/api/settings/models/test',{'provider_id':'custom-vision','kind':'vision'})['success'] and f.calls[-1]['images'])
    select('shared','custom-vision','custom-vision','shared');check('one_multimodal_model_can_serve_both_roles',get('/api/settings/models')['selection']['mode']=='shared')
    session=post('/api/sessions',{},201)['id'];events=post('/api/teach',{'session':session,'request':{'request_id':'chosen-text','question':'二次函数的顶点是什么？'}},stream=True)
    check('selected_text_model_streams_real_provider_deltas',events[-1]['kind']=='done' and f.calls[-1]['model']=='vision-local' and any(e['kind']=='delta' for e in events))
    upload=post('/api/tutor/images',{'request_id':'image','name':'equation.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()},201)['id']
    events=post('/api/teach',{'session':session,'request':{'request_id':'chosen-image','question':'请教我这张图片里的题目','images':[upload]}},stream=True)
    check('chosen_visual_model_receives_owned_image',events[-1]['kind']=='done' and any(c['model']=='vision-local' and c['images'] for c in f.calls))
    save(provider('text',image=False,model='text-local'));version=get('/api/settings/models')['version']
    post('/api/settings/model-selection',{'request_id':'bad-vision','version':version,'mode':'shared','text_provider_id':'custom-text','vision_provider_id':'custom-text'},400)
    check('text_only_model_cannot_be_assigned_visual_role',get('/api/settings/models')['version']==version)
    select('split','custom-text','custom-vision','split');session=post('/api/sessions',{},201)['id'];events=post('/api/teach',{'session':session,'request':{'request_id':'separate-text','question':'二次函数的顶点是什么？'}},stream=True)
    check('split_roles_use_text_selection_not_vision_fallback',events[-1]['kind']=='done' and f.calls[-1]['model']=='text-local' and not f.calls[-1]['images'])
    post('/api/settings/model-providers',{'request_id':'delete-active','version':get('/api/settings/models')['version'],'operation':'delete','provider_id':'custom-text'},409)
    check('active_connection_delete_is_rejected',any(p['id']=='custom-text' for p in get('/api/settings/models')['providers']))
    post('/api/settings/model-selection',{'request_id':'csrf','version':get('/api/settings/models')['version'],'mode':'deployment'},403,csrf='bad')
    post('/api/settings/model-selection',{'request_id':'stale','version':0,'mode':'deployment'},409)
    check('csrf_and_version_conflict_have_no_configuration_effect',get('/api/settings/models')['selection']['text_provider_id']=='custom-text')
    p=provider('text',image=False,model='text-local');p.update(key_action='keep',api_key='');save(p,'keep-key');check('blank_key_retains_existing_encrypted_key',next(p for p in get('/api/settings/models')['providers'] if p['id']=='custom-text')['credential_ready'])
    save(provider('anthropic',protocol='anthropic'));select('shared','custom-anthropic','custom-anthropic','native');session=post('/api/sessions',{},201)['id'];events=post('/api/teach',{'session':session,'request':{'request_id':'native-stream','question':'二次函数的顶点是什么？'}},stream=True)
    check('anthropic_native_stream_uses_same_teaching_loop',events[-1]['kind']=='done' and f.calls[-1]['native'] and any(e['kind']=='delta' for e in events))
    check('anthropic_image_content_is_native',post('/api/settings/models/test',{'provider_id':'custom-anthropic','kind':'vision'})['success'] and f.calls[-1]['native'] and f.calls[-1]['images'])
    save(provider('failure',model='fail-model'));check('authentication_failure_is_not_reported_as_success',post('/api/settings/models/test',{'provider_id':'custom-failure','kind':'text'})['success'] is False)
    before=get('/api/settings/models');cmd={'request_id':'reset','version':before['version'],'mode':'deployment'};post('/api/settings/model-selection',cmd);post('/api/settings/model-selection',cmd)
    check('reset_and_same_id_replay_use_current_projection',get('/api/settings/models')['version']==before['version']+1 and get('/api/settings/models')['selection']['source']=='deployment')
    owner=Store(f.root)
    try:
        restored=f.deployment.model_settings(owner).view();check('saved_config_survives_new_owner_without_keys',len(restored['providers'])==6 and KEY not in json.dumps(restored))
    finally:owner.close()
    check('configuration_and_tutoring_do_not_create_student_grades',get('/api/learning')['summary']['attempts']==0)
    model_version=get('/api/settings/models')['version'];post('/api/settings/history/clear',{'request_id':'model-clear-history','scope':'project'})
    check('history_clear_preserves_model_configuration',get('/api/settings/models')['version']==model_version)
    f.deployment.manage_profiles.clear()
    req=urllib.request.Request(f.base+'/api/settings/models')
    try:o.open(req)
    except urllib.error.HTTPError as e:check('non_manager_cannot_read_model_configuration',e.code==403)
    else:raise AssertionError('manager permission missing')
    Path('education/.local/reports/model-settings-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True,'real_inference':False},ensure_ascii=False,indent=2),encoding='utf-8')
finally:f.close()
