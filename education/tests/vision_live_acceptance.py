"""Explicit real GLM 5.3 Flash smoke check using a synthetic math image only."""
import base64
import http.cookiejar
import json
import threading
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from multimodal_fixture import sample_image
from qingqi.product import Deployment, server

root=fixture_root()
instance=server(0,root=root,deployment=Deployment(config=Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=150) as r: return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','Origin':base,'X-Qingqi-CSRF':boot['csrf']})
    with opener.open(req,timeout=150) as r: return json.load(r)
try:
    image=post('/api/tutor/images',{'request_id':'live-image','name':'synthetic-equation.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})
    session=post('/api/sessions',{})['id']
    result=post('/api/teach',{'session':session,'request':{'request_id':'live-teach','question':'请用中文引导我解这道方程，先不要直接给答案。','images':[image['id']]}})
    follow=post('/api/teach',{'session':session,'request':{'request_id':'live-follow','question':'x=4'}})
    report={'model':'glm-5.3-flash','real_inference':result['response']['model_inference'],'recognized':result['session']['messages'][-1]['recognized_question'],'reply':result['response']['text'],'action':result['response']['teaching_action'],
            'followup_action':follow['response']['teaching_action'],'catalogue_attempts':get('/api/learning')['summary']['attempts'],'synthetic_image':True}
    print(json.dumps(report,ensure_ascii=False),flush=True)
    assert report['real_inference'] and report['action']=='ask' and report['followup_action']=='confirm' and report['catalogue_attempts']==0
    Path('education/.local/reports/vision-live-acceptance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
finally:
    instance.shutdown();instance.server_close()
