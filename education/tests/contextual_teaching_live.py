"""Authorized actual model, isolated learner, contextual explanation with paired visuals."""
import http.cookiejar,json,threading,time,urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
from qingqi.storage import Store

root=fixture_root();owner=Store(root)
instance=server(0,root=root,deployment=Deployment(Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=30) as r:return json.load(r)
boot=get('/api/bootstrap');checks=[]
def post(path,body,stream=False):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf'],**({'Accept':'text/event-stream'} if stream else {})})
    start=time.perf_counter();events=[];first=None
    with opener.open(req,timeout=200) as r:
        if not stream:return json.load(r)
        for line in r:
            if line.startswith(b'data: '):
                event=json.loads(line[6:]);events.append(event)
                if event['kind']=='delta' and event.get('text') and first is None:first=round((time.perf_counter()-start)*1000)
    assert events[-1]['kind']=='done',{'terminal':events[-1]['kind'],'error':events[-1].get('error')}
    return events[-1]['value']['response'],{'first_delta_ms':first,'total_ms':round((time.perf_counter()-start)*1000),'deltas':sum(e['kind']=='delta' for e in events)}
try:
    entry=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and '个位' not in e['expression'])
    assignment=post('/api/practice/start',{'item_id':entry['id'],'request_id':'start'})
    for i,q in enumerate(['这道题为什么要比较系数？解释当前一步，先不要最终答案。','继续解释这一步，先不要最终答案。']):
        response,timing=post('/api/teach',{'session':assignment['session'],'request':{'request_id':'contextual-live-'+str(i),'question':q}},True)
        assert response['route']['teaching']['mode']=='explain'
        if i==0:assert response['model_inference']
        visuals=response.get('visuals',[])
        assert len(visuals)==1 and visuals[0]['kind']=='reasoning_diagram'
        assert visuals[0]['algebra_lesson']['equation']=='mx-8=5x+n' and visuals[0]['algebra_lesson']['mode']=='hint'
        assert '(-3)^{2026}' not in response['text'] and '抓住' not in response['text']
        usage=json.loads(owner.db.execute('SELECT response FROM runs WHERE id=?',(response['run_id'],)).fetchone()[0]).get('model_usage',[])
        checks.append({'name':'actual_contextual_explanation_'+str(i),'passed':True,'mode':'explain','visual_count':1,'model_inference':response['model_inference'],'usage':usage,**timing})
        print(json.dumps(checks[-1]),flush=True)
    assert get('/api/learning')['summary']['attempts']==0
    Path('education/.local/reports/single-teaching-visual-live.local.json').write_text(json.dumps({'checks':checks,'isolated':True,'production_changed':False},indent=2),encoding='utf-8')
finally:owner.close();instance.shutdown();instance.server_close()
