"""Real image HTTP transport with a controlled OCR endpoint and isolated student."""
import base64,http.cookiejar,json,threading,urllib.request
from pathlib import Path
from multimodal_fixture import fixture,sample_image,calls
from qingqi.storage import Store

root,visual,instance=fixture()
threading.Thread(target=instance.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{instance.server_port}'
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(base+path,timeout=90) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'X-Qingqi-CSRF':boot['csrf'],'Content-Type':'application/json'})
    with o.open(request,timeout=90) as r:return json.load(r)
checks=[]
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
owner=Store(root)
try:
    session=post('/api/sessions',{})['id']
    images=[post('/api/tutor/images',{'request_id':f'task-photo-{i}','name':f'equation-{i}.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})['id'] for i in range(2)]
    result=post('/api/teach',{'session':session,'request':{'request_id':'photo-recommend','question':'给我推荐一道图片中这类题目，不用讲解。','images':images}})['response']
    check('multi_image_query_performs_one_ocr_and_no_lesson_generation',len(calls)==1 and calls[0]['images']==2 and 'unclear' in calls[0]['schema'])
    check('image_query_returns_a_real_matching_question',result['teaching_action']=='recommend' and len(result['student_tasks'][0]['items'])==1 and not result.get('visuals'))
    state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(result['run_id'],)).fetchone()[0])
    check('image_transcription_is_the_reference_not_the_teaching_task',state['task_plan']['source']['kind']=='image' and state['task_plan']['source']['question']=='3x+2=14')
    before=len(calls)
    repeat=post('/api/teach',{'session':session,'request':{'request_id':'photo-recommend-again','question':'再给我推荐一道类似的题'}})['response']
    check('same_session_repeat_keeps_query_image_reference',repeat['teaching_action']=='recommend' and len(calls)==before)
    follow=post('/api/teach',{'session':session,'request':{'request_id':'photo-teach','question':'图里这道题，给我一点提示。'}})['response']
    check('explicit_image_followup_recovers_latest_uploaded_equation',follow['teaching_action'] in ('ask','explain') and '3x' in follow['text'] and len(calls)==before+1)
    other=post('/api/sessions',{})['id']
    missing=post('/api/teach',{'session':other,'request':{'request_id':'other-reference','question':'推荐一道类似的题'}})['response']
    check('image_reference_does_not_cross_sessions',missing['teaching_action']=='clarify' and not missing['student_tasks'][0]['items'])
finally:owner.close();instance.shutdown();instance.server_close();visual.shutdown();visual.server_close()
Path('education/.local/reports/current-task-images.local.json').write_text(json.dumps({'checks':checks,'passed':len(checks),'controlled_vision':True},ensure_ascii=False,indent=2),encoding='utf-8')
