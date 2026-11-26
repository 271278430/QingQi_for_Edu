"""Actual submitted image and GLM OCR; isolated teaching history only."""
import http.cookiejar
import json
import sqlite3
import threading
import urllib.error
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
from qingqi.storage import Store
from qingqi.tutor_images import data_uri

root=fixture_root();instance=server(0,root=root,deployment=Deployment(config=Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=180) as r:return json.load(r)
boot=get('/api/bootstrap');owner=Store(root)
def post(path,body):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
    try:
        with opener.open(req,timeout=180) as r:return json.load(r)
    except urllib.error.HTTPError as error:
        print(error.read().decode(),flush=True);raise
try:
    db=sqlite3.connect('file:education/service/runs/product/agent.sqlite?mode=ro',uri=True)
    request=json.loads(db.execute("SELECT request FROM runs WHERE json_extract(request,'$.question')=? AND json_array_length(json_extract(request,'$.images'))>0 ORDER BY id DESC LIMIT 1",('分别给出动画和情景教学',)).fetchone()[0])
    image=db.execute('SELECT data FROM tutor_images WHERE id=?',(request['images'][0],)).fetchone()[0];db.close()
    uploaded=post('/api/tutor/images',{'request_id':'actual-image','name':'submitted-function.jpg','data_url':data_uri(image)})['id']
    session=post('/api/sessions',{})['id']
    r=post('/api/teach',{'session':session,'request':{'request_id':'actual-combined-request','question':'分别给出动画和情景教学','images':[uploaded]}})['response']
    state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(r['run_id'],)).fetchone()[0])
    if not r.get('visuals'):
        print(json.dumps({'ocr':state.get('vision'),'image_question':state.get('image_question'),'text':r.get('text'),'teaching':state.get('route',{}).get('teaching'),'visual_task':state.get('visual_task')},ensure_ascii=False),flush=True)
    assert r['repairs']==0 and len(r['visuals'])==1 and r['visuals'][0]['template']=='function_reasoning' and r['visuals'][0]['reasoning_lesson']['given']['k']==2
    assert state['presentation']['kind']=='story' and state['teaching_plan']['visual']['prefer_animation'] and not state['teaching_plan']['visual']['forbid_animation']
    assert state['function_task']['arguments']['k']==2 and '情景教学' in r['text'] and '相切' in r['text']
    assert r['model_inference'] and get('/api/learning')['summary']['attempts']==0
    Path('education/.local/reports/combined-presentation-live.local.json').write_text(json.dumps({'passed':True,'isolated':True,'actual_submitted_image':True,'ocr':state['vision']['text'],'text':r['text'],'repairs':r['repairs'],'tool_calls':r['tool_calls'],'templates':[v['template'] for v in r['visuals']]},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'actual_image_glm_ocr_and_combined_teaching_passed':True,'repairs':r['repairs'],'tool_calls':r['tool_calls']}),flush=True)
finally:owner.close();instance.shutdown();instance.server_close()
