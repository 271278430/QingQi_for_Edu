"""Actual upload/teach HTTP regressions for recognition protocol and recovery."""
import base64
import http.cookiejar
import json
import threading
import urllib.error
import urllib.request
from pathlib import Path
from multimodal_fixture import fixture,sample_image,calls
from qingqi.storage import Store

root,model,instance=fixture()
threading.Thread(target=instance.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=60) as response:return json.load(response)
boot=get('/api/bootstrap')
def post(path,body):
    request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','Origin':base,'X-Qingqi-CSRF':boot['csrf']})
    with opener.open(request,timeout=60) as response:return json.load(response)
checks=[]
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
owner=Store(root)
try:
    from qingqi.tutor_images import describes_image
    check('negative_solving_clause_preserves_image_description',describes_image('请按图片顺序描述三张图，不解题。') and describes_image('描述图片，不求最终答案。') and not describes_image('描述图片，然后解题。'))
    image=post('/api/tutor/images',{'request_id':'schema-image','name':'equation.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})
    session=post('/api/sessions',{})['id']
    def teach(q,rid):return post('/api/teach',{'session':session,'request':{'request_id':rid,'question':q,'images':[image['id']]}})
    good=teach('解这道题','valid')
    check('recognition_schema_lives_in_system_and_native_json_mode',calls[0]['schema_in_system'] and calls[0]['json_mode']=={'type':'json_object'} and good['session']['messages'][-1]['recognized_question']=='3x+2=14')
    wrapped=teach('解这道题，测试识别包装字段','valid-extra')['response']
    wrapped_state=json.loads(owner.db.execute('select state from runs where id=?',(wrapped['run_id'],)).fetchone()[0])
    check('valid_recognition_ignores_known_provider_metadata',wrapped_state['vision']=={'text':'3x+2=14','unclear':False,'note':''})
    for index,q in enumerate(('测试识别回显','测试识别缺字段','测试识别错类型','测试识别未知字段')):
        rid='invalid-'+str(index)
        try:teach(q,rid)
        except urllib.error.HTTPError as error:
            body=json.load(error)
            check('model_format_failure_'+str(index),error.code==502 and body['error']=='model_protocol' and not body['recoverable'] and 'input' not in body['message'] and 'required_output_schema' not in body['message'])
        else:raise AssertionError('invalid recognition accepted')
        row=owner.db.execute('select id,state from runs where request_id=?',(rid,)).fetchone();state=json.loads(row['state'])
        check('diagnostic_and_failed_ledger_preserved_'+str(index),state['model_output_error'] and not state.get('vision') and owner.db.execute('select status from model_invocations where run_id=?',(row['id'],)).fetchone()[0]=='failed')
        before=len(calls)
        try:teach(q,rid)
        except urllib.error.HTTPError as error:check('same_request_does_not_repeat_failed_recognition_'+str(index),error.code==502 and len(calls)==before)
        else:raise AssertionError('failed request resumed')
    row=owner.db.execute("select id,state from runs where request_id='invalid-0'").fetchone();legacy=json.loads(row['state'])
    legacy.update(error_code=None,error_type='ContractError',error="$: unknown ['input', 'required_output_schema']")
    legacy.pop('model_output_error',None)
    with owner.db:owner.db.execute('update runs set state=? where id=?',(json.dumps(legacy),row['id']))
    history=next(m for m in get('/api/session?id='+session)['messages'] if m['request_id']=='invalid-0')
    check('legacy_failure_history_disables_same_request_resume',history['trace']['error_code']=='model_protocol')
    before=len(calls)
    try:teach('测试识别回显','invalid-0')
    except urllib.error.HTTPError as error:check('legacy_reported_failure_stops_before_changed_protocol',error.code==502 and json.load(error)['error']=='model_protocol' and len(calls)==before)
    else:raise AssertionError('legacy request resumed')
    fixed=teach('请重新引导我理解这道题','new-request')
    check('new_request_reuses_existing_uploaded_image',fixed['response']['teaching_action']=='ask' and fixed['session']['messages'][-1]['images'][0]['id']==image['id'] and owner.db.execute('select count(*) from tutor_images').fetchone()[0]==1)
    before=len(calls);replayed=teach('请重新引导我理解这道题','new-request')
    check('accepted_request_replay_does_not_repeat_ocr',replayed['response']['cache_hit'] and len(calls)==before)
    check('recognition_and_failures_do_not_create_grades',get('/api/learning')['summary']['attempts']==0)
    description=teach('请描述图片，不解题。','image-description')['response']
    state=json.loads(owner.db.execute('select state from runs where id=?',(description['run_id'],)).fetchone()[0])
    check('image_description_uses_direct_explanation_plan',state['teaching_plan']['mode']=='explain' and state['teaching_plan']['interaction_style']=='direct' and state['teaching_plan']['budget']['questions']==0 and not state['route']['teaching']['no_questions_requested'] and description['route']['teaching']['label']=='图片内容解读')
finally:
    owner.close();instance.shutdown();instance.server_close();model.shutdown();model.server_close()
Path('education/.local/reports/vision-schema-acceptance.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'real_model':False},ensure_ascii=False,indent=2),encoding='utf-8')
