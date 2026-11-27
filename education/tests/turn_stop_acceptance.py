"""Cancellation through real HTTP, real connection shutdown and the existing Store."""
import base64,http.cookiejar,json,threading,time,urllib.request,urllib.error
from pathlib import Path
from turn_stop_fixture import Fixture
from qingqi.storage import Store
from qingqi.contracts import Identity,Request
from qingqi.zcode_runtime import RuntimeFailure
from multimodal_fixture import sample_image

f=Fixture();owner=Store(f.root);checks=[]
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(f.base+path,timeout=20) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body,expected=200):
    req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'X-Qingqi-CSRF':boot['csrf'],'Content-Type':'application/json'})
    try:r=o.open(req,timeout=25)
    except urllib.error.HTTPError as error:r=error
    with r:
        value=json.load(r);assert r.status==expected,(r.status,value)
        return value
def check(name,ok):assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def running(session,request,stream=True):
    events=[];finished=threading.Event();visible=threading.Event()
    def read():
        req=urllib.request.Request(f.base+'/api/teach',data=json.dumps({'session':session,'request':request}).encode(),headers={'Origin':f.base,'X-Qingqi-CSRF':boot['csrf'],'Content-Type':'application/json',**({'Accept':'text/event-stream'} if stream else {})})
        try:
            try:r=o.open(req,timeout=25)
            except urllib.error.HTTPError as error:r=error
            with r:
                if stream:
                    for line in r:
                        if line.startswith(b'data: '):
                            event=json.loads(line[6:]);events.append(event)
                            if event['kind']=='delta':visible.set()
                else:events.append(json.load(r))
        finally:finished.set()
    thread=threading.Thread(target=read,daemon=True);thread.start();return events,finished,visible
try:
    session=post('/api/sessions',{},201)['id'];before=get('/api/learning')['summary']
    foreign=owner.upload_image('edu-other',{'request_id':'foreign-image','name':'private.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})['id']
    for resource in ({'images':[foreign]},{'visual_context':{'run_id':999999,'visual_index':0}}):
        request={'request_id':'foreign-resource-'+str(len(resource)), 'question':'解释这个图',**resource}
        for endpoint in ('/api/teach','/api/teach/stop'):post(endpoint,{'session':session,'request':request},403)
    check('foreign_resources_are_rejected_before_any_run_or_stop_record',not get('/api/session?id='+session)['messages'] and owner.db.execute('SELECT COUNT(*) FROM turn_stop_commands').fetchone()[0]==0 and not f.calls)
    identity=Identity('edu-local',session);request=Request.parse({'request_id':'stale-stop','question':'解释这个图'})
    try:owner.stop_turn(identity,request,expected_history_epoch=owner.history_status()['epoch']-1);raise AssertionError('stale epoch accepted')
    except RuntimeFailure as error:check('stale_admission_cannot_insert_stop_after_history_change',error.code=='history_changed')
    for n,stream in enumerate((True,False,True)):
        f.entered.clear();request={'request_id':f'stop-{n}','question':'二次函数的顶点是什么？'+('等待首字' if n==2 else '')}
        events,finished,visible=running(session,request,stream)
        assert f.entered.wait(8)
        if stream and n!=2:assert visible.wait(4)
        started=time.monotonic();reply=post('/api/teach/stop',{'session':session,'request':request})
        assert finished.wait(3),events
        last=events[-1];code=last.get('error')
        check(('stream' if stream else 'json')+'_stop_disconnects_provider_'+str(n),code=='turn_cancelled' and time.monotonic()-started<3 and f.closed>=n+1)
        detail=get('/api/session?id='+session);message=detail['messages'][-1]
        check('cancelled_turn_is_not_an_accepted_answer_'+str(n),message['response'] is None and message['trace']['error_code']=='turn_cancelled' and not message['trace']['running'])
        check('partial_text_is_retained_only_when_visible_'+str(n),bool(message.get('partial_response'))==(stream and n!=2))
        old=len(f.calls);replay=post('/api/teach',{'session':session,'request':request},409)
        check('stopped_request_does_not_call_provider_again_'+str(n),replay['error']=='turn_cancelled' and len(f.calls)==old)
        check('stop_command_is_idempotent_'+str(n),post('/api/teach/stop',{'session':session,'request':request})['status']=='stopped')
    early={'request_id':'early-stop','question':'二次函数的顶点是什么？'}
    post('/api/teach/stop',{'session':session,'request':early});old=len(f.calls)
    value=post('/api/teach',{'session':session,'request':early},409)
    check('stop_before_admission_prevents_model_call',value['error']=='turn_cancelled' and len(f.calls)==old)
    post('/api/teach/stop',{'session':session,'request':{**early,'question':'不同问题'}},400)
    other=post('/api/sessions',{},201)['id']
    post('/api/teach/stop',{'session':'not-owned','request':early},403)
    fast={'request_id':'after-stop','question':'快速解释二次函数的顶点，不用追问。'}
    value=post('/api/teach',{'session':session,'request':fast})
    check('new_turn_after_stop_completes_normally',bool(value['response']['text']))
    check('completed_result_wins_a_late_stop',post('/api/teach/stop',{'session':session,'request':fast})['status']=='completed')
    check('stop_does_not_change_learning_evidence',{k:v for k,v in get('/api/learning')['summary'].items() if k!='turns'}=={k:v for k,v in before.items() if k!='turns'})
    f.entered.clear();image=post('/api/tutor/images',{'request_id':'stop-image','name':'equation.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()},201)['id']
    request={'request_id':'stop-image-turn','question':'解释图片中的题目','images':[image]}
    events,finished,visible=running(other,request)
    assert f.entered.wait(8)
    post('/api/teach/stop',{'session':other,'request':request});assert finished.wait(3)
    check('cancelled_image_recognition_keeps_original_attachment',get('/api/session?id='+other)['messages'][-1]['images'][0]['id']==image)
    a=post('/api/practice/start',{'item_id':'order-1','request_id':'partial-help-practice'},201)
    f.entered.clear();request={'request_id':'partial-practice-hint','question':'这道题请给我一点提示。'}
    events,finished,visible=running(a['session'],request)
    assert f.entered.wait(8) and visible.wait(4)
    post('/api/teach/stop',{'session':a['session'],'request':request});assert finished.wait(3)
    result=post('/api/practice/answer',{'assignment_id':a['id'],'request_id':'answer-after-partial','answer':'14'})
    check('visible_partial_help_does_not_become_independent_success',result['correct'] and not result['independent'] and not result['unassisted'])
    check('cancellation_records_no_teacher_facts',owner.db.execute('SELECT COUNT(*) FROM facts').fetchone()[0]==0)
    from qingqi.management import overview
    from qingqi.product import Deployment
    check('user_stop_is_not_a_system_error',all(e['code']!='turn_cancelled' for e in overview(owner,Deployment(f.root/'stop.local.json'),'edu-'+boot['profile'])['recent_errors']))
    request=Request.parse({'request_id':'commit-race','question':'解释二次函数'});identity=Identity('edu-local',other)
    run,state,_=owner.begin(identity,request);counts=[owner.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0] for table in ('episodes','practice_events','facts')]
    owner.stop_turn(identity,request)
    try:owner.commit(run,identity,request,state,{'text':'不可提交'});raise AssertionError('commit after stop')
    except RuntimeFailure as error:
        check('accepted_stop_prevents_entire_commit_transaction',error.code=='turn_cancelled' and owner.db.execute('SELECT response FROM runs WHERE id=?',(run,)).fetchone()[0] is None and counts==[owner.db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0] for table in ('episodes','practice_events','facts')])
finally:owner.close();f.close()
f=Fixture(protocol='anthropic');o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));boot=get('/api/bootstrap')
try:
    session=post('/api/sessions',{},201)['id'];request={'request_id':'anthropic-stop','question':'二次函数的顶点是什么？'}
    events,finished,visible=running(session,request);assert f.entered.wait(8) and visible.wait(4)
    post('/api/teach/stop',{'session':session,'request':request});assert finished.wait(3)
    check('anthropic_stream_stop_disconnects_and_retains_partial',events[-1].get('error')=='turn_cancelled' and f.closed==1 and bool(get('/api/session?id='+session)['messages'][-1].get('partial_response')))
finally:f.close()
Path('education/.local/reports/turn-stop-acceptance.local.json').write_text(json.dumps({'checks':checks,'passed':len(checks),'real_http':True},ensure_ascii=False,indent=2),encoding='utf-8')
