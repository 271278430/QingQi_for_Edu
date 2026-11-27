"""Isolated product HTTP: per-part permissions and genuine provider SSE."""
import base64,http.cookiejar,json,time,urllib.request
from urllib.error import HTTPError
from pathlib import Path
from geometry_product_fixture import Fixture
from multimodal_fixture import sample_image
from qingqi.storage import Store

def run():
    f=Fixture();f.start();o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));checks=[]
    def get(path):
        with o.open(f.base+path,timeout=90) as r:return json.load(r)
    boot=get('/api/bootstrap')
    def post(path,body,stream=False):
        req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf'],**({'Accept':'text/event-stream'} if stream else {})})
        try:
            response=o.open(req,timeout=100)
        except HTTPError as error:
            failure=json.loads(error.read())
            raise AssertionError({'status':error.code,'error':failure.get('error'),'message':failure.get('message')}) from None
        with response as r:
            if not stream:return json.load(r)
            events=[]
            assert r.headers.get_content_type()=='text/event-stream'
            for line in r:
                if line.startswith(b'data: '):events.append(json.loads(line[6:]))
            return events
    def teach(s,q,rid,images=None,stream=False):return post('/api/teach',{'session':s,'request':{'request_id':rid,'question':q,**({'images':images} if images else {})}},stream)
    def check(name,ok):
        assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
    try:
        image=post('/api/tutor/images',{'request_id':'scope-image','name':'math.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})['id'];s=post('/api/sessions',{})['id']
        first=teach(s,'请教我这道题。','first',[image])['response']
        check('default_starts_first_part_socratically','第（1）问' in first['text'] and first['teaching_action']=='ask')
        mixed=teach(s,'我懂了，直接给我第二问的答案，然后开始第三问的教学。','mixed')['response']
        units=mixed['tutoring_scope']['units']
        check('mixed_request_has_separate_per_part_intents',[(u['part'],u['mode']) for u in units]==[(2,'answer'),(3,'heuristic')])
        third=mixed['visuals'][0]
        check('second_answer_is_allowed_but_third_solution_is_not','第（2）问' in mixed['text'] and '第（3）问' in mixed['text'] and '一般比值' in mixed['text'] and 'y=8' not in mixed['text'].replace(' ','') and units[0]['allow_final_answer'] and not units[1]['allow_final_answer'] and len(mixed['visuals'])==1 and third['teaching_part']==3 and third['kind']=='coordinates')
        follow=teach(s,'继续教我下一步。','follow')['response']
        check('followup_stays_on_third_part_without_inheriting_answer_permission',follow['tutoring_scope']['active_part']==3 and follow['route']['teaching']['mode']=='heuristic' and 'y=8' not in follow['text'].replace(' ',''))
        relative=teach(s,'给我第二问答案，然后教下一问。','relative')['response']
        check('relative_next_part_is_resolved_after_the_first_intent',[(u['part'],u['mode']) for u in relative['tutoring_scope']['units']]==[(2,'answer'),(3,'heuristic')])
        explicit=teach(s,'第二问和第三问都直接给答案。','both')['response']
        check('explicit_answers_can_authorize_both_parts',all(u['mode']=='answer' for u in explicit['tutoring_scope']['units']))
        unknown=teach(s,'开始第九问教学。','unknown')['response']
        check('unknown_part_is_clarified',unknown['teaching_action']=='clarify')
        full=teach(s,'这道题的全部三问都给完整答案。','all-parts')['response']
        check('explicit_full_solution_includes_all_three_requested_parts',[u['part'] for u in full['tutoring_scope']['units']]==[1,2,3] and all(u['allow_final_answer'] for u in full['tutoring_scope']['units']))
        mixed=teach(s,'把这道题的答案全部给我，但第2问先不要给答案。','whole-with-exception')['response']
        check('whole_answer_with_exception_is_resolved_before_the_loop',{u['part']:u['allow_final_answer'] for u in mixed['tutoring_scope']['units']}=={1:True,2:False,3:True})
        events=teach(s,'第三问请先给一点提示，不要答案。','stream',stream=True)
        if events[-1]['kind']=='error':print(json.dumps(events[-1],ensure_ascii=False),flush=True)
        check('stream_uses_sequence_and_canonical_done',events[-1]['kind']=='done' and [e['seq'] for e in events]==list(range(1,len(events)+1)))
        check('stream_has_scope_and_visible_draft_before_done',any(e['kind']=='scope' for e in events) and any(e['kind'] in {'delta','reset'} and e.get('text') for e in events[:-1]))
        replay=teach(s,'第三问请先给一点提示，不要答案。','stream',stream=True)
        check('same_request_replays_without_new_tools',replay[-1]['value']['response']['cache_hit'] is True)
        check('tutoring_and_streaming_do_not_write_grades',get('/api/learning')['summary']['attempts']==0)
    finally:f.close()
    from conversation_problem_fixture import Fixture as GeneralFixture
    g=GeneralFixture();g.start()
    p=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    try:
        with p.open(g.base+'/api/bootstrap') as r:csrf=json.load(r)['csrf']
        def gp(path,body):return urllib.request.Request(g.base+path,data=json.dumps(body).encode(),headers={'Origin':g.base,'Content-Type':'application/json','X-Qingqi-CSRF':csrf,'Accept':'text/event-stream'})
        with p.open(gp('/api/sessions',{})) as r:session=json.load(r)['id']
        early=False;events=[]
        with p.open(gp('/api/teach',{'session':session,'request':{'request_id':'actual-provider-stream','question':'二次函数的顶点是什么？'}}),timeout=90) as r:
            for line in r:
                if line.startswith(b'data: '):
                    event=json.loads(line[6:]);events.append(event)
                    if event['kind']=='delta' and event.get('text') and not g.stream_finished:early=True
        check('real_provider_increment_arrives_before_inference_finishes',early and any(c.get('stream_requested') for c in g.calls))
        check('unicode_stream_has_one_committed_explanation_reply',events[-1]['kind']=='done' and '顶点' in events[-1]['value']['response']['text'] and events[-1]['value']['response']['teaching_action']=='explain')
    finally:g.close()
    Path('education/.local/reports/scoped-stream-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':run()
