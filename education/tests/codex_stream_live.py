"""Read-only copy of the reported failure; real provider writes only to an isolated root."""
import base64,http.cookiejar,json,re,sqlite3,threading,time,urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
from qingqi.storage import Store

production=Path('education/service/runs/product/agent.sqlite').resolve()
with sqlite3.connect(production.as_uri()+'?mode=ro',uri=True) as db:
    rows=db.execute('SELECT request,state FROM runs ORDER BY id DESC LIMIT 50').fetchall()
    failed=next((json.loads(req),json.loads(state)) for req,state in rows if json.loads(req).get('visual_context') and json.loads(state).get('error_code')=='model_protocol')
    original=json.loads(next(req for req,state in rows if json.loads(req).get('images') and not json.loads(req).get('visual_context')))
    photo=db.execute('SELECT data FROM tutor_images WHERE id=?',(original['images'][0],)).fetchone()[0]
    marked=db.execute('SELECT data FROM tutor_images WHERE id=?',(failed[0]['images'][0],)).fetchone()[0]
root=fixture_root();deployment=Deployment(Path('education/service/config/vision.local.json'))
instance=server(0,root=root,deployment=deployment)
owner=Store(root)
try:deployment.model_settings(owner).select({'request_id':'same-visual-adapter-path','version':0,'mode':'split','text_provider_id':None,'vision_provider_id':'deployment-vision'})
finally:owner.close()
threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=30) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body,stream=False):
    request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf'],**({'Accept':'text/event-stream'} if stream else {})})
    start=time.perf_counter();events=[];first=None
    with opener.open(request,timeout=150) as r:
        if not stream:return json.load(r)
        for line in r:
            if not line.startswith(b'data: '):continue
            event=json.loads(line[6:]);events.append(event)
            if event['kind']=='delta' and event.get('text') and first is None:first=round((time.perf_counter()-start)*1000,1)
    assert events[-1]['kind']=='done',events[-1]
    return events[-1]['value'],{'total_ms':round((time.perf_counter()-start)*1000,1),'first_delta_ms':first,'deltas':sum(e['kind']=='delta' for e in events)}
try:
    def upload(data,id):return post('/api/tutor/images',{'request_id':id,'name':'问题图片.jpg','data_url':'data:image/jpeg;base64,'+base64.b64encode(data).decode()})['id']
    image=upload(photo,'original-source');session=post('/api/sessions',{})['id']
    source=post('/api/teach',{'session':session,'request':{'request_id':'source-question','question':original['question'],'images':[image]}})
    annotation=upload(marked,'exact-reported-annotation')
    result,timing=post('/api/teach',{'session':session,'request':{'request_id':'exact-reported-question','question':failed[0]['question'],'images':[annotation],'visual_context':{'run_id':source['response']['run_id'],'visual_index':0}}},True)
    response=result['response'];assert response['teaching_action']=='ask' and response['controller']=='glm_vision_text_controller'
    assert re.search(r'\bEF\b|E\s*(?:—|-|到|和|、|与)\s*F|E点.{0,6}F点|点\s*E.{0,6}点\s*F',response['text']), '本题新增红线连接E、F，不能拿原有CD替代它。'
    assert '分别在两个直角三角形' not in response['text'], '图中ADE/CDF不能凭外观称为直角三角形。'
    owner=Store(root)
    try:
        ids=[v[0] for v in owner.db.execute('SELECT invocation_id FROM model_invocations WHERE run_id=?',(response['run_id'],))]
        raw=json.loads(owner.db.execute('SELECT response FROM runs WHERE id=?',(response['run_id'],)).fetchone()[0])
        assert ids and all(v.startswith('vision:tutor:') for v in ids)
        assert len(ids)==1,'这条短标注讨论不需要再次整轮润色。'
        assert all(u['finish_reason']=='stop' for u in raw.get('model_usage',[]))
    finally:owner.close()
    assert get('/api/learning')['summary']['attempts']==0
    report={'passed':True,'question':failed[0]['question'],**timing,'model_calls':len(ids),'teacher_text':response['text'],'model_usage':raw.get('model_usage'),'isolated':True,'production_read_only':True}
    Path('education/.local/reports/codex-stream-live.local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False),flush=True)
finally:instance.shutdown();instance.server_close()
