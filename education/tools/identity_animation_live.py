"""Real deployment configuration and GLM visual selection, using isolated public problems."""
import http.cookiejar
import json
import threading
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
from qingqi.storage import Store

root=fixture_root();instance=server(0,root=root,deployment=Deployment(config=Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=150) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
    with opener.open(req,timeout=150) as r:return json.load(r)
owner=Store(root);cases=[]
try:
    entry=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and '个位' not in e['expression'])
    a=post('/api/practice/start',{'item_id':entry['id'],'request_id':'live-start'})
    for index,q in enumerate(['能给动画的教学方式吗','还是不懂，继续给我提示']):
        r=post('/api/teach',{'session':a['session'],'request':{'request_id':f'live-identity-{index}','question':q}})['response']
        if index==0:assert r['visuals'][0]['template']=='identity_probe' and r['repairs']==0 and r['tool_calls']==1 and not r['model_inference']
        else:assert 'm=5' in r['text'] and '5 应该' not in r['text'] and r['repairs']==0
        cases.append({'question':q,'text':r['text'],'template':r.get('visuals',[{}])[0].get('template') if r.get('visuals') else None,'model_inference':r['model_inference'],'tool_calls':r['tool_calls'],'repairs':r['repairs']});print(json.dumps({'case':index+1,'passed':True}),flush=True)
    s=post('/api/sessions',{})['id']
    q='请用一个简单的一次函数动画帮助我理解斜率的含义，举一个清楚标注的例子。'
    r=post('/api/teach',{'session':s,'request':{'request_id':'live-function-animation','question':q}})['response']
    assert r['model_inference'] and r['tool_calls']==1 and all(v['template']=='function_trace' for v in r['visuals'])
    cases.append({'question':q,'text':r['text'],'templates':[v['template'] for v in r['visuals']],'model_inference':True,'tool_calls':r['tool_calls'],'repairs':r['repairs']});print(json.dumps({'case':3,'passed':True}),flush=True)
    assert get('/api/learning')['summary']['attempts']==0
    Path('education/.local/reports/identity-animation-live.local.json').write_text(json.dumps({'passed':len(cases),'isolated':True,'cases':cases,'scope':'真实配置下2个确定性数学场景、1个真实GLM动画选择与解释场景；不是全面教学有效性评测'},ensure_ascii=False,indent=2),encoding='utf-8')
finally:owner.close();instance.shutdown();instance.server_close()
