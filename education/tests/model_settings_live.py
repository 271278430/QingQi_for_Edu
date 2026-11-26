"""Real GLM/Flash through saved ModelSelection; all writes use an isolated student root."""
import json,http.cookiejar,threading,urllib.request,urllib.error
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server

root=fixture_root();deployment=Deployment(Path('education/service/config/vision.local.json'));instance=server(0,root=root,deployment=deployment)
threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(base+path,timeout=30) as r:return json.load(r)
boot=get('/api/bootstrap');checks=[]
def post(path,body,stream=False):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf'],**({'Accept':'text/event-stream'} if stream else {})})
    try:response=o.open(req,timeout=180)
    except urllib.error.HTTPError as error:raise AssertionError(json.loads(error.read())) from None
    with response as r:
        if stream:return [json.loads(line[6:]) for line in r if line.startswith(b'data: ')]
        return json.load(r)
try:
    data=get('/api/settings/models');default=next(p for p in data['providers'] if p['id']=='deployment-vision')
    provider={k:default[k] for k in ('model','base_url','protocol','supports_image','supports_tools','requires_key','timeout','max_tokens','json_mode')}
    provider.update(id='custom-live-adaptation',display_name='真实适配验收',credential_ref='deployment-vision',key_action='keep',api_key='')
    provider['timeout']=min(60,provider['timeout'])
    from qingqi.provider_models import model_config
    provider['models']=[{'key':'main','model':provider['model'],'config':model_config(provider)}]
    data=post('/api/settings/model-providers',{'request_id':'save-live','version':data['version'],'operation':'upsert','provider':provider})
    for kind in ('text','vision'):
        result=post('/api/settings/models/test',{'provider_id':'custom-live-adaptation','kind':kind})
        checks.append({'name':kind+'_through_saved_real_adapter','passed':result['success'],'message':result['message']})
        print(json.dumps(checks[-1],ensure_ascii=False),flush=True)
        assert result['success'],result
    post('/api/settings/model-selection',{'request_id':'select-live','version':data['version'],'mode':'shared','text_provider_id':'custom-live-adaptation','vision_provider_id':'custom-live-adaptation'})
    session=post('/api/sessions',{})['id'];events=post('/api/teach',{'session':session,'request':{'request_id':'saved-selection-live','question':'二次函数的顶点是什么？请用苏格拉底式教学，先给必要解释再追问。','mode':'socratic'}},True)
    assert events[-1]['kind']=='done',events[-1]
    response=events[-1]['value']['response'];assert response['model_inference'] and response['teaching_action']=='ask'
    checks.append({'name':'shared_real_selection_streams_socratic_tutoring','passed':True,'deltas':sum(e['kind']=='delta' for e in events),'repairs':response['repairs']});print(json.dumps(checks[-1]),flush=True)
    assert get('/api/learning')['summary']['attempts']==0
    Path('education/.local/reports/model-settings-live.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True,'real_inference':True,'production_student_unchanged':True},ensure_ascii=False,indent=2),encoding='utf-8')
finally:instance.shutdown();instance.server_close()
