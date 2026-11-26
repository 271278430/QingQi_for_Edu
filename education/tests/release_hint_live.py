"""One real hint-button probe in an isolated student root; reports no student content."""
import http.cookiejar
import json
import re
import threading
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
from qingqi.storage import Store

root=fixture_root()
instance=server(0,root=root,deployment=Deployment(Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
with opener.open(base+'/api/bootstrap',timeout=20) as r:boot=json.load(r)
def post(path,data):
    request=urllib.request.Request(base+path,data=json.dumps(data).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
    with opener.open(request,timeout=160) as r:return json.load(r)
owner=Store(root)
try:
    item=next(e for e in owner.catalogue.bank.values() if '和谐方程' in e['expression'] and '4x' in e['expression'])
    a=post('/api/practice/start',{'item_id':item['id'],'request_id':'live-release-start'})
    result=post('/api/practice/hint',{'assignment_id':a['id'],'style':'heuristic','request_id':'live-release-hint'})
    text=result['text'];row=owner.db.execute('SELECT state,response FROM runs ORDER BY id DESC LIMIT 1').fetchone()
    state,response=map(json.loads,row)
    assert not re.search(r'[?？]|告诉我|你能|请给出|看这张',text)
    assert state['teaching_plan']['interaction_style']=='hint_only' and not response.get('visuals')
    assert response['model_inference'] and owner.learning_overview('edu-math-student')['summary']['attempts']==0
    report={'passed':3,'real_inference':True,'isolated':True,'no_follow_up':True,'text_only':True,'model_calls':len(response.get('model_usage',[])),'duration_ms':response['duration_ms']}
    Path('education/.local/reports/release-hint-live.local.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report),flush=True)
finally:owner.close();instance.shutdown();instance.server_close()
