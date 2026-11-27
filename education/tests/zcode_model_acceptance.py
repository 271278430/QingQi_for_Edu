"""Normal HTTP provider/model lifecycle and concrete inference configuration."""
import json,base64,http.cookiejar,urllib.request,urllib.error
from pathlib import Path
from model_settings_fixture import Fixture,KEY
from multimodal_fixture import sample_image
from qingqi.provider_models import model_config

f=Fixture();f.start();checks=[]
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(f.base+path) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body,expected=200,stream=False):
    req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf'],**({'Accept':'text/event-stream'} if stream else {})})
    try:r=o.open(req,timeout=90)
    except urllib.error.HTTPError as error:r=error
    with r:
        assert r.code==expected,(r.code,r.read().decode())
        return [json.loads(line[6:]) for line in r if line.startswith(b'data: ')] if stream else json.load(r)
def check(name,ok):
    assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def save(provider,expected=200):
    return post('/api/settings/model-providers',{'request_id':'save-'+str(get('/api/settings/models')['version'])+str(expected),'version':get('/api/settings/models')['version'],'operation':'upsert','provider':provider},expected)
try:
    initial=get('/api/settings/models');check('deployment_connections_import_once_as_editable_main_models',len(initial['connections'])==2 and all(p['models'][0]['key']=='main' and not p['readonly'] for p in initial['connections']) and initial['version']==1)
    p={'id':'custom-multiple','display_name':'multiple','base_url':f.model_base,'protocol':'openai','requires_key':True,'timeout':15,'model':'','supports_image':False,'supports_tools':True,'max_tokens':1600,'json_mode':False,'key_action':'replace','api_key':KEY}
    text=model_config(p);text['properties']['contextWindow']=65536;text['optionSpecs']['maxOutputTokens']['max']=768
    vision=model_config({**p,'supports_image':True});p['models']=[{'key':'text','model':'text-local','config':text},{'key':'vision','model':'vision-local','config':vision}]
    view=save(p);check('two_models_share_one_encrypted_connection',len(view['connections'])==3 and len(view['providers'])==4 and KEY not in json.dumps(view))
    post('/api/settings/model-selection',{'request_id':'split-models','version':view['version'],'mode':'split','text_provider_id':'custom-multiple~text','vision_provider_id':'custom-multiple~vision'})
    session=post('/api/sessions',{},201)['id'];events=post('/api/teach',{'session':session,'request':{'request_id':'text-model','question':'二次函数的顶点是什么？'}},stream=True)
    check('text_role_uses_selected_model_and_output_budget',events[-1]['kind']=='done' and f.calls[-1]['model']=='text-local' and f.calls[-1]['max_tokens']==768)
    models=f.deployment.current_models(f.root);check('model_context_budget_reaches_frozen_endpoint',models['glm'].endpoint.context_window==65536)
    image=post('/api/tutor/images',{'request_id':'image','name':'example.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()},201)['id']
    events=post('/api/teach',{'session':session,'request':{'request_id':'vision-model','question':'教我图片中的题目','images':[image]}},stream=True)
    check('visual_role_receives_owned_image_using_its_model',events[-1]['kind']=='done' and any(c['model']=='vision-local' and c['images'] for c in f.calls))
    old=get('/api/settings/models')['version'];p['models'][1]['config']['enabled']=False;save(p,400)
    check('active_model_cannot_be_disabled',get('/api/settings/models')['version']==old)
    p['models'][1]['config']['enabled']=True;p['models'][1]['config']['properties']['inputFormat']['supportsImage']=False;save(p,400)
    check('active_visual_capability_cannot_be_removed',get('/api/settings/models')['version']==old)
    check('discovery_belongs_to_connection_not_model_id',len(post('/api/settings/models/discover',{'provider_id':'custom-multiple'})['models'])==2)
    check('model_configuration_does_not_create_grades',get('/api/learning')['summary']['attempts']==0)
    Path('education/.local/reports/zcode-model-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True},indent=2),encoding='utf-8')
finally:f.close()
