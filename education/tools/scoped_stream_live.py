"""GLM API stream through the actual product, isolated student history."""
import http.cookiejar,json,threading,urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
root=fixture_root();instance=server(0,root=root,deployment=Deployment(Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
try:
    with o.open(base+'/api/bootstrap') as r:csrf=json.load(r)['csrf']
    def req(path,body,stream=False):return urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':csrf,**({'Accept':'text/event-stream'} if stream else {})})
    with o.open(req('/api/sessions',{})) as r:s=json.load(r)['id']
    events=[]
    with o.open(req('/api/teach',{'session':s,'request':{'request_id':'glm-real-stream','question':'函数的零点是什么？'}},True),timeout=180) as r:
        for line in r:
            if line.startswith(b'data: '):events.append(json.loads(line[6:]))
    assert events[-1]['kind']=='done',events[-1]
    reply=events[-1]['value']['response']
    assert reply['model_inference'] and reply['teaching_action']=='ask' and '？' in reply['text']
    assert any(e['kind']=='delta' and e.get('text') for e in events)
    report={'passed':True,'real_glm':True,'isolated':True,'events':[e['kind'] for e in events],'teaching_action':reply['teaching_action'],'text':reply['text'],'repairs':reply['repairs']}
    Path('education/.local/reports/scoped-stream-live.local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'real_glm_stream':True,'delta_events':sum(e['kind']=='delta' for e in events),'repairs':reply['repairs']}),flush=True)
finally:instance.shutdown();instance.server_close()
