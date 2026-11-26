"""Authorized real high/low inference, isolated from production histories and settings."""
import json,threading,time,http.cookiejar,urllib.request,base64
from pathlib import Path
from student_data_acceptance import fixture_root
from multimodal_fixture import sample_image
from qingqi.product import Deployment,server

root=fixture_root();instance=server(0,root=root,deployment=Deployment(Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
original=urllib.request.build_opener;calls=[]
class Spy:
    def __init__(self,opener):self.opener=opener
    def open(self,request,*args,**kwargs):
        if isinstance(request,urllib.request.Request) and request.full_url.endswith('/chat/completions'):
            body=json.loads(request.data);calls.append({'model':body['model'],'reasoning_effort':body.get('reasoning_effort'),'stream':bool(body.get('stream'))})
        return self.opener.open(request,*args,**kwargs)
urllib.request.build_opener=lambda *a,**kw:Spy(original(*a,**kw))
opener=original(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=30) as r:return json.load(r)
boot=get('/api/bootstrap');checks=[]
def post(path,body,stream=False):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'X-Qingqi-CSRF':boot['csrf'],'Content-Type':'application/json',**({'Accept':'text/event-stream'} if stream else {})})
    begin=time.perf_counter();first=None;events=[]
    with opener.open(req,timeout=200) as r:
        if not stream:return json.load(r)
        for line in r:
            if not line.startswith(b'data: '):continue
            event=json.loads(line[6:]);events.append(event)
            if event['kind']=='delta' and event.get('text') and first is None:first=round((time.perf_counter()-begin)*1000,1)
    assert events[-1]['kind']=='done',events[-1]
    return events[-1]['value'],{'first_delta_ms':first,'total_ms':round((time.perf_counter()-begin)*1000,1),'deltas':sum(e['kind']=='delta' for e in events)}
try:
    view=get('/api/chat/models');selection=view['selection'];assert all(x['reasoning_level']=='high' for x in selection.values())
    session=post('/api/sessions',{'model_selection':selection})['id']
    before=len(calls);result,timing=post('/api/teach',{'session':session,'request':{'request_id':'real-high','question':'二次函数的顶点是什么？请简短提示。','model_selection':selection}},True)
    if not (calls[before:] and timing['deltas']>0):print(json.dumps({'diagnosis':{'calls':calls[before:],'controller':result['response'].get('controller'),'text':result['response'].get('text'),'timing':timing}},ensure_ascii=False),flush=True)
    assert calls[before:] and all(c['reasoning_effort']=='high' for c in calls[before:]) and result['response']['text'] and timing['deltas']>0
    checks.append({'name':'real_high_text_sse','passed':True,'calls':len(calls)-before,**timing});print(json.dumps(checks[-1]),flush=True)
    selection={role:{**choice,'reasoning_level':'low'} for role,choice in selection.items()}
    view=get('/api/chat/models?session='+session)
    post('/api/chat/models',{'session':session,'version':view['version'],'request_id':'real-low','selection':selection})
    assert get('/api/chat/models?session='+session)['selection']==selection
    image=post('/api/tutor/images',{'request_id':'simple-equation','name':'equation.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})['id']
    before=len(calls);result,timing=post('/api/teach',{'session':session,'request':{'request_id':'real-low-image','question':'先引导我理解这道图片中的题目，不要给最终答案。','images':[image],'model_selection':selection}},True)
    assert calls[before:] and all(c['reasoning_effort']=='low' for c in calls[before:]) and result['session']['messages'][-1]['recognized_question']
    checks.append({'name':'real_low_visual_recognition_and_teaching','passed':True,'calls':len(calls)-before,**timing});print(json.dumps(checks[-1]),flush=True)
    assert get('/api/learning')['summary']['attempts']==0
    Path('education/.local/reports/composer-models-live.local.json').write_text(json.dumps({'checks':checks,'calls':calls,'isolated':True,'production_changed':False},indent=2),encoding='utf-8')
finally:urllib.request.build_opener=original;instance.shutdown();instance.server_close()
