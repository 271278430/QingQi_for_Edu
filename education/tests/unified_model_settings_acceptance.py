"""Real HTTP/Store scenarios for one editable directory and captured deployment options."""
import copy,json,os,http.cookiejar,urllib.request,urllib.error
from dataclasses import replace
from pathlib import Path
from model_settings_fixture import Fixture,KEY
from qingqi.storage import Store

f=Fixture();f.start();checks=[]
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(f.base+path,timeout=30) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body,status=200):
    req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
    try:r=o.open(req,timeout=40)
    except urllib.error.HTTPError as e:r=e
    with r:
        assert r.status==status,(path,r.status,r.read().decode())
        return json.load(r)
def check(name,ok):
    assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def use(role,id,status=200):
    return post('/api/settings/model-selection',{'request_id':'use-'+str(len(checks))+'-'+role,'version':get('/api/settings/models')['version'],'role':role,'provider_id':id},status)
def save(connection,model=None):
    p={k:connection[k] for k in ('id','display_name','base_url','protocol','requires_key','timeout','models')}
    if model:p['models'][0]['model']=model
    p.update(model='',supports_image=False,supports_tools=True,max_tokens=1600,json_mode=False,key_action='keep',api_key='')
    if connection.get('credential_ref'):p['credential_ref']=connection['credential_ref']
    if p['id']=='custom-preserved':p['credential_ref']='deployment-text'
    return post('/api/settings/model-providers',{'request_id':'edit-'+str(len(checks)),'version':get('/api/settings/models')['version'],'operation':'upsert','provider':p})
owner=Store(f.root)
try:
    view=get('/api/settings/models')
    check('deployment_models_are_editable_and_not_duplicated',len(view['connections'])==2 and all(not p['readonly'] and p['origin']=='deployment' for p in view['connections']))
    check('deployment_keys_never_enter_public_view_or_plain_sqlite',KEY not in json.dumps(view) and KEY.encode() not in (f.root/'agent.sqlite').read_bytes())
    manager=f.deployment.model_settings(owner);version=view['version']
    check('repeated_bootstrap_does_not_change_version_or_choice',not manager.sync_deployment() and get('/api/settings/models')['version']==version)
    custom=copy.deepcopy(view['connections'][0]);custom['id']='custom-preserved';custom['display_name']='已有供应商';save(custom)
    use('text','custom-preserved');before=get('/api/settings/models')
    f.deployment.endpoints.update({role:replace(f.deployment.endpoints['glm'],name=role,model=name,timeout=90,reasoning_effort='low',model_options={'temperature':.25},max_tokens=768,enabled=role!='difficulty8b') for role,name in [('course8b','course-local'),('difficulty8b','difficulty-local'),('review27b','review-local')]})
    manager=f.deployment.model_settings(owner)
    manager.sync_deployment();view=get('/api/settings/models')
    check('all_new_configured_specialists_are_imported',len(view['connections'])==6 and set(view['selection']['worker_provider_ids'])=={'course8b','difficulty8b','review27b'})
    check('adding_deployment_roles_preserves_saved_provider_and_text_choice',view['selection']['text_provider_id']=='custom-preserved' and any(p['id']=='custom-preserved' for p in view['connections']))
    disabled=next(p for p in view['providers'] if p['id']=='deployment-difficulty8b')
    check('disabled_deployment_stays_disabled_and_unassigned',not disabled['model_enabled'] and view['selection']['worker_provider_ids']['difficulty8b'] is None)
    models=f.deployment.current_models(f.root)
    check('specialist_budget_reasoning_and_options_reach_runtime',models['course8b'].endpoint.timeout==90 and models['course8b'].endpoint.max_tokens==768 and models['course8b'].endpoint.reasoning_effort=='low' and models['course8b'].endpoint.model_options=={'temperature':.25} and 'difficulty8b' not in models)
    models['course8b'].generate_text('只回复OK',{'task':'连接测试'})
    check('captured_specialist_is_really_called_with_its_options',f.calls[-1]['model']=='course-local' and f.calls[-1]['max_tokens']==768 and f.calls[-1]['reasoning_effort']=='low')
    connection=next(p for p in view['connections'] if p['id']=='deployment-text');save(copy.deepcopy(connection),'text-edited')
    check('editing_imported_model_changes_actual_runtime',f.deployment.current_models(f.root)['vision'].endpoint.model=='vision-local' and next(p for p in get('/api/settings/models')['providers'] if p['id']=='deployment-text')['model']=='text-edited')
    use('text','deployment-text');view=use('vision','deployment-vision')
    check('per_model_defaults_are_read_from_the_same_saved_directory',view['selection']['text_provider_id']=='deployment-text' and next(p for p in view['providers'] if p['id']=='deployment-text')['uses']==['text'] and f.deployment.current_models(f.root)['glm'].endpoint.model=='text-edited')
    v=view['version'];use('vision','deployment-text',400)
    check('text_only_model_cannot_become_vision_default',get('/api/settings/models')['version']==v)
    use('text','deployment-vision');view=get('/api/settings/models')
    check('one_multimodal_model_can_hold_both_defaults',view['selection']['mode']=='shared' and next(p for p in view['providers'] if p['id']=='deployment-vision')['uses']==['text','vision'])
    use('course8b',None)
    check('optional_specialist_can_be_unassigned_without_raw_fallback','course8b' not in f.deployment.current_models(f.root))
    alias=copy.deepcopy(next(p for p in get('/api/settings/models')['connections'] if p['id']=='deployment-course8b'))
    alias.update(id='custom-credential-alias',display_name='引用凭据的连接',credential_ref='deployment-course8b');save(alias)
    version=get('/api/settings/models')['version'];post('/api/settings/model-providers',{'request_id':'delete-imported','version':version,'operation':'delete','provider_id':'deployment-course8b'})
    manager.sync_deployment();check('removed_imported_connection_is_not_reinjected',not any(p['id']=='deployment-course8b' for p in get('/api/settings/models')['connections']))
    check('broken_reference_is_unavailable_without_blocking_settings_or_chat',not next(p for p in get('/api/settings/models')['connections'] if p['id']=='custom-credential-alias')['credential_ready'] and not next(p for p in get('/api/chat/models')['models'] if p['id']=='custom-credential-alias')['available'])
    f.deployment.endpoints['glm']=replace(f.deployment.endpoints['glm'],model='stale-file-model')
    manager.sync_deployment();check('deployment_file_does_not_overwrite_edited_model',next(p for p in get('/api/settings/models')['providers'] if p['id']=='deployment-text')['model']=='text-edited')
    value=os.environ.pop('EDU_MODEL_FIXTURE_KEY')
    try:check('imported_credential_remains_usable_without_original_environment',all(p['credential_ready'] for p in get('/api/settings/models')['connections'] if p['id']!='custom-credential-alias'))
    finally:os.environ['EDU_MODEL_FIXTURE_KEY']=value
    check('settings_and_uses_do_not_write_student_grades',get('/api/learning')['summary']['attempts']==0)
finally:owner.close();f.close()
Path('education/.local/reports/unified-model-settings.local.json').write_text(json.dumps({'checks':checks,'passed':len(checks),'isolated':True},ensure_ascii=False,indent=2),encoding='utf-8')
