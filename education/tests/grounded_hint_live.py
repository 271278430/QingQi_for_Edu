"""Small real GLM regression using isolated public catalogue tasks and actual hint API."""
import http.cookiejar
import json
import re
import threading
import sys
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
from qingqi.storage import Store

reused='--reuse-root' in sys.argv
root=Path(sys.argv[sys.argv.index('--reuse-root')+1]) if reused else fixture_root()
instance=server(0,root=root,deployment=Deployment(config=Path('education/service/config/vision.local.json')))
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
    for index,question in enumerate(['提示按钮','继续给我提示','我还没有算出m和n，再提示一步']):
        if index==0:
            result=post('/api/practice/hint',{'assignment_id':a['id'],'request_id':'live-hint','style':'heuristic'})
            text=result['text'];state=json.loads(owner.db.execute("SELECT state FROM runs WHERE json_extract(state,'$.practice_hint.payload.request_id')='live-hint'").fetchone()[0])
        else:
            result=post('/api/teach',{'session':a['session'],'request':{'request_id':f'live-turn-{index}','question':question}})
            assert result['response']['model_inference'];text=result['response']['text'];state=json.loads(owner.db.execute("SELECT state FROM runs WHERE json_extract(request,'$.request_id')=?",(f'live-turn-{index}',)).fetchone()[0])
        assert re.search(r'm|n|x',text) and not re.search(r'你(?:已经?|已).{0,14}(?:掌握|抓住|理解了|求出)',text)
        assert not re.search(r'(?:最终答案|结果|答案)(?:是|为|等于|：|:)\s*\$?9\b',text)
        assert state['practice_assessment']['status']=='unverified' and state['practice_assessment']['stage']==0 and not state['teaching_plan']['allow_final_answer']
        from qingqi.providers import _validate_tutoring_text
        _validate_tutoring_text(text,state['teaching_plan'],state,{'question':question})
        cases.append({'question':question,'reply':text,'controller':state['controller'],'repairs':state['repairs']});print(json.dumps({'case':index+1,'passed':True}),flush=True)
    previous=owner.db.execute("SELECT session FROM runs WHERE json_extract(request,'$.request_id')='variant' LIMIT 1").fetchone() if reused else None
    s=previous[0] if previous else post('/api/sessions',{})['id']
    result=post('/api/teach',{'session':s,'request':{'request_id':'variant','question':'已知mx+6=2x+n对任意x恒成立，请只给一个提示，不要答案。'}})
    assert result['response']['model_inference'] and not re.search(r'm\s*[-−]\s*5|n\s*\+\s*8',result['response']['text']) and re.search(r'2|6|恒成立|任意.*x|系数',result['response']['text'],re.S)
    cases.append({'question':'不同参数恒等式','reply':result['response']['text']});print(json.dumps({'case':4,'passed':True}),flush=True)
    assert get('/api/learning')['summary']['attempts']==0
    Path('education/.local/reports/grounded-hint-live.local.json').write_text(json.dumps({'passed':len(cases),'real_inference':True,'isolated':True,'cases':cases,'reused_accepted_results':reused,'scope':'四轮本轮实际GLM回归，非全面教学有效性评测'+('；复核已接受缓存，未重复调用' if reused else '')},ensure_ascii=False,indent=2),encoding='utf-8')
finally:owner.close();instance.shutdown();instance.server_close()
