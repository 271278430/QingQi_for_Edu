"""Real GLM visual description and math guidance, with synthetic images only."""
import base64
import http.cookiejar
import json
import threading
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from multimodal_fixture import sample_image, sample_table
from qingqi.product import Deployment, server

root=fixture_root()
instance=server(0,root=root,deployment=Deployment(config=Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=150) as response:return json.load(response)
boot=get('/api/bootstrap')
def post(path,body):
    request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','Origin':base,'X-Qingqi-CSRF':boot['csrf']})
    with opener.open(request,timeout=150) as response:return json.load(response)
results=[]
try:
    for name,image,question in [('table',sample_table(),'分析一下这个图片中的表格表达了什么'),('equation',sample_image(),'请引导我解这道方程，先不要直接给答案')]:
        attachment=post('/api/tutor/images',{'request_id':name+'-upload','name':name+'.png','data_url':'data:image/png;base64,'+base64.b64encode(image).decode()})
        session=post('/api/sessions',{})['id']
        result=post('/api/teach',{'session':session,'request':{'request_id':name+'-teach','question':question,'images':[attachment['id']]}})
        response=result['response']
        assert response['model_inference'] and response['controller']=='glm_vision_text_controller'
        assert response['teaching_action']==('explain' if name=='table' else 'ask')
        assert len(response['text'])>15 and not response['text'].lstrip().startswith('{')
        results.append({'case':name,'action':response['teaching_action'],'recognized':result['session']['messages'][-1]['recognized_question'],'reply':response['text'],'real_inference':True})
        if name=='table':
            follow=post('/api/teach',{'session':session,'request':{'request_id':'table-follow','question':'这张表中的数据应该怎样比较？'}})
            assert follow['response']['controller']=='glm_vision_text_controller' and follow['response']['model_inference']
            results.append({'case':'table-follow','action':follow['response']['teaching_action'],'reply':follow['response']['text'],'real_inference':True})
        else:
            follow=post('/api/teach',{'session':session,'request':{'request_id':'equation-follow','question':'x=4'}})
            assert follow['response']['teaching_action']=='confirm'
    attachments=[]
    for name, raw in [('equation-a',sample_image()),('practice-table',sample_table()),('equation-b',sample_image('2y + 1 = 7'))]:
        attachments.append(post('/api/tutor/images',{'request_id':'multi-'+name,'name':name+'.png','data_url':'data:image/png;base64,'+base64.b64encode(raw).decode()})['id'])
    session=post('/api/sessions',{})['id']
    multi=post('/api/teach',{'session':session,'request':{'request_id':'multi-live-teach','question':'请按顺序逐张描述这三张图片中的方程和表格，不求最终答案。','images':attachments}})
    assert multi['response']['model_inference'] and multi['response']['controller']=='glm_vision_text_controller'
    message=multi['session']['messages'][-1]
    assert [p['id'] for p in message['images']]==attachments
    recognized=message['recognized_question']
    import re
    assert re.search(r'3x\s*\+\s*2\s*=\s*14',recognized) and re.search(r'2y\s*\+\s*1\s*=\s*7',recognized),recognized
    assert any(word in recognized for word in ('Monday','周一','星期一')),recognized
    results.append({'case':'three-images','action':multi['response']['teaching_action'],'images':3,'recognized':recognized,'reply':multi['response']['text'],'real_inference':True})
    assert get('/api/learning')['summary']['attempts']==0
    report={'model':'glm-5.3-flash','passed':len(results),'synthetic_only':True,'catalogue_attempts':0,'cases':results}
    Path('education/.local/reports/image-repair-live-acceptance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'passed':len(results),'real_inference':True,'synthetic_only':True}),flush=True)
finally:
    instance.shutdown();instance.server_close()
