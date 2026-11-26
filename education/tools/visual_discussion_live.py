"""Authorized real Flash replay in an isolated root; never changes production history."""
import base64,http.cookiejar,json,sqlite3,threading,time,urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
from qingqi.storage import Store

production=Path('education/service/runs/product/agent.sqlite').resolve()
with sqlite3.connect(production.as_uri()+'?mode=ro',uri=True) as db:
    candidates=[json.loads(r[0]) for r in db.execute('SELECT request FROM runs ORDER BY id DESC LIMIT 50')]
    original=next(r for r in candidates if r.get('images') and not r.get('visual_context'))
    photo=db.execute('SELECT data FROM tutor_images WHERE id=?',(original['images'][0],)).fetchone()[0]
root=fixture_root();instance=server(0,root=root,deployment=Deployment(Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=30) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body,stream=False):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf'],**({'Accept':'text/event-stream'} if stream else {})})
    start=time.perf_counter();events=[];first_progress=None;first_text=None
    with opener.open(req,timeout=160) as response:
        if not stream:return json.load(response)
        for line in response:
            if not line.startswith(b'data: '):continue
            event=json.loads(line[6:]);events.append(event)
            if event['kind']=='progress' and first_progress is None:first_progress=round((time.perf_counter()-start)*1000,1)
            if event['kind'] in {'delta','reset'} and event.get('text') and first_text is None:first_text=round((time.perf_counter()-start)*1000,1)
    assert events[-1]['kind']=='done',events[-1]
    return events[-1]['value'],{'total_ms':round((time.perf_counter()-start)*1000,1),'first_progress_ms':first_progress,'first_visible_text_ms':first_text,'deltas':sum(v['kind']=='delta' for v in events)}
results=[]
try:
    image=post('/api/tutor/images',{'request_id':'live-original','name':'问题图片.jpg','data_url':'data:image/jpeg;base64,'+base64.b64encode(photo).decode()})['id']
    session=post('/api/sessions',{})['id']
    first,timing=post('/api/teach',{'session':session,'request':{'request_id':'live-reported-picture','question':original['question'],'images':[image]}},True)
    assert first['response']['teaching_action']=='ask' and first['response'].get('visuals')
    store=Store(root)
    state=json.loads(store.db.execute('SELECT state FROM runs WHERE id=?',(first['response']['run_id'],)).fetchone()[0])
    usage=json.loads(store.db.execute('SELECT response FROM runs WHERE id=?',(first['response']['run_id'],)).fetchone()[0]).get('model_usage',[])
    reasoning_values=[(u.get('usage') or {}).get('completion_tokens_details',{}).get('reasoning_tokens') for u in usage]
    reasoning=sum(v for v in reasoning_values if v is not None) if any(v is not None for v in reasoning_values) else None
    results.append({'name':'reported_picture_with_default_related_diagram','passed':True,**timing,'reasoning_tokens':reasoning,'tool_ms':[{'tool':v['tool'],'ms':v['duration_ms']} for v in state['observations']], 'teacher_text':first['response']['text']})
    print(json.dumps(results[-1]),flush=True)
    annotation=Path('education/.local/reports/annotation-returned.png').read_bytes()
    marked=post('/api/tutor/images',{'request_id':'live-marked','name':'我标注的教学图.png','data_url':'data:image/png;base64,'+base64.b64encode(annotation).decode()})['id']
    follow,timing=post('/api/teach',{'session':session,'request':{'request_id':'live-annotation','question':'我在图上画了红色辅助线。请结合原题第（1）问讨论这条线是否合适，先解释依据，不要给完整解答。','images':[marked],'visual_context':{'run_id':first['response']['run_id'],'visual_index':0}}},True)
    assert follow['response']['controller']=='glm_vision_text_controller' and follow['response']['teaching_action']=='ask'
    calls=[v[0] for v in store.db.execute('SELECT invocation_id FROM model_invocations WHERE run_id=?',(follow['response']['run_id'],))]
    # 标注不重复OCR；模型超出教学预算时，原质量机制允许一次聚焦改写。
    assert all(v.startswith('vision:tutor:') for v in calls) and len(calls) in {1,2}
    assert len(calls)==1 or sum(v.endswith(':focus') for v in calls)==1
    assert get('/api/learning')['summary']['attempts']==0
    results.append({'name':'real_annotation_discussion_without_retranscription_streamed','passed':True,**timing,'model_calls':len(calls),'quality_rewrite':any(v.endswith(':focus') for v in calls),'teacher_text':follow['response']['text']})
    print(json.dumps(results[-1]),flush=True)
    store.close()
    Path('education/.local/reports/visual-discussion-live.local.json').write_text(json.dumps({'passed':len(results),'cases':results,'isolated':True,'production_read_only':True},ensure_ascii=False,indent=2),encoding='utf-8')
finally:instance.shutdown();instance.server_close()
