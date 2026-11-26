"""Isolated real configuration: screenshot continuity and one GLM text story."""
import http.cookiejar
import json
import threading
import time
import urllib.request
import urllib.error
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.contracts import Identity
from qingqi.product import Deployment,server
from qingqi.storage import Store

root=fixture_root();instance=server(0,root=root,deployment=Deployment(config=Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=150) as r:return json.load(r)
boot=get('/api/bootstrap');student='edu-'+boot['profile']
def post(path,body):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
    try:
        with opener.open(req,timeout=150) as r:return json.load(r)
    except urllib.error.HTTPError as error:
        print(error.read().decode(),flush=True)
        row=owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone()
        if row:
            state=json.loads(row[0]);print(json.dumps({k:state.get(k) for k in ('error','last_error','story_opening','phase','repairs')},ensure_ascii=False),flush=True)
        raise
def teach(session,question,rid):return post('/api/teach',{'session':session,'request':{'request_id':rid,'question':question}})['response']
owner=Store(root);cases=[]
try:
    entry=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and '个位' not in e['expression'])
    a=post('/api/practice/start',{'item_id':entry['id'],'request_id':'live-story-start'})
    teach(a['session'],'能给动画的教学方式吗','live-animation')
    with owner.db:owner.db.execute('UPDATE dialogue_state SET updated=? WHERE student=? AND session=?',(time.time()-4000,student,a['session']))
    for i,q in enumerate(['你不能创建情景故事来教学吗','题目就是上一个题目']):
        r=teach(a['session'],q,'live-story-'+str(i));assert r['teaching_action']!='clarify' and '积分' in r['text'] and not owner.dialogue(Identity(student,a['session']))['practice_detached']
        if i==0:assert r['visuals'][0]['params']['scenario']=='scorekeepers' and r['tool_calls']==1
        cases.append({'question':q,'text':r['text'],'model_inference':r['model_inference'],'tool_calls':r['tool_calls'],'repairs':r['repairs']});print(json.dumps({'case':len(cases),'passed':True}),flush=True)
    other=next(e for e in owner.catalogue.bank.values() if '遮住' in e['expression'] and 'x=6' in e['expression'].replace(' ','') and '2x+y=16' in e['expression'].replace(' ',''))
    b=post('/api/practice/start',{'item_id':other['id'],'request_id':'live-text-story-start'})
    q='请用一个简短的文字情景故事帮我理解这道题，说明故事里的量如何对应题目中的已知条件。不要动画，也不要直接给正确答案。'
    r=teach(b['session'],q,'live-glm-story');assert r['model_inference'] and r['teaching_action']!='clarify' and not r.get('visuals')
    state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(r['run_id'],)).fetchone()[0])
    assert state['practice_entry']['id']==other['id'] and state['teaching_plan']['presentation']['kind']=='story'
    assert '提供题目' not in r['text'] and '重新贴题' not in r['text']
    assert '蓝色积分计入 $2$ 份，紫色积分计入 $1$ 份' in r['text'] and '双份' not in r['text'] and '翻倍' not in r['text']
    assert state['story_opening']['math_source']=='owned_equation_coefficients'
    cases.append({'question':q,'text':r['text'],'model_inference':r['model_inference'],'tool_calls':r['tool_calls'],'repairs':r['repairs']});print(json.dumps({'case':len(cases),'passed':True}),flush=True)
    assert get('/api/learning')['summary']['attempts']==0
    Path('education/.local/reports/story-context-live.local.json').write_text(json.dumps({'passed':len(cases),'isolated':True,'cases':cases,'scope':'2个真实配置确定性故事续聊、1个真实GLM文字故事；不是所有题型或教学效果的全面评测'},ensure_ascii=False,indent=2),encoding='utf-8')
finally:owner.close();instance.shutdown();instance.server_close()
