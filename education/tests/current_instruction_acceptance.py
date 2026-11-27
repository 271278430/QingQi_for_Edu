"""CLI and real HTTP regressions for the reported answer request and source decimals."""
import json,http.cookiejar,urllib.request,threading
from pathlib import Path
from qingqi.contracts import Request,Route
from qingqi.teaching_policy import choose
from qingqi.math_display import compact_response
from qingqi.product import server
from qingqi.storage import Store
from student_data_acceptance import fixture_root

checks=[]
def check(name,value):
    assert value,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
route=Route(('tutor',),('owned_practice',),continuity='continuation')
cases=[('重新画过一张图给我，并且这次给我把这道题的答案全部给我',True),
       ('这次所有答案都告诉我',True),('答案给我，别再追问',True),
       ('先不要答案，但现在把完整答案给我',True),('把答案给我，不，先不要答案',False),
       ('先别给完整解答，请只提示',False),('讲解一下，不要最终答案',False),
       ('不给答案，先讲思路',False),('给答案，不，之后只要提示',False),
       ('我以前说“不要答案”，现在把全部答案给我',True),('解释“把答案给我”是什么意思',False),('答案先别给我',False),
       ('直接核对 2+3*4 的答案',True),('先解释这条辅助线，无需提供完整解题过程。',False),
       ('请解释“把答案给我”是什么意思',False),('请改为“把完整答案给我”',True)]
for i,(q,allowed) in enumerate(cases):
    decision=choose(Request('instruction-'+str(i),q),route,[],continuing_problem=True,prior_no_answer=True,prior_mode={'mode':'heuristic'})
    check('latest_current_answer_directive_'+str(i),decision['allow_final_answer']==allowed)
source='题干给定：√2.061≈1.436，√20.61≈4.54；精确小量0.0001。'
check('given_decimals_are_preserved_in_teacher_text',compact_response('√2.061≈1.436，0.0001；未知 x=0.333333333。',source=source)=='√2.061≈1.436，0.0001；未知 x≈0.33。')
from qingqi.math_display import model_history
history=[{'question':cases[0][0],'reply':'这题目标是自己完成，我不能直接报出结果。'},{'question':'你能解释平方根吗','reply':'先看√≈2.06。'},{'question':'保留原题的数字','reply':'已知√2.061≈1.436。'}]
filtered,omitted=model_history(history)
check('invalid_teacher_text_is_not_reused_as_memory_truth',omitted==[0,1] and not filtered[0]['reply'] and filtered[0]['question']==history[0]['question'] and filtered[2]['reply']==history[2]['reply'])
from qingqi.tutoring_scope import build
multi='(1) 求第一个量。(2) 求第二个量。(3) 求第三个量。'
scope=build(Request('all-parts','把这道题的答案全部给我，但第2问先不要给答案'),multi,None,route,[])
permissions={u['part']:u['allow_final_answer'] for u in scope['units']}
check('whole_answer_and_part_exception_resolve_before_execution',permissions=={1:True,2:False,3:True})
root=fixture_root();owner=Store(root);instance=server(0,root=root);threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=30) as response:return json.load(response)
boot=get('/api/bootstrap')
def post(path,body):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'X-Qingqi-CSRF':boot['csrf'],'Content-Type':'application/json'})
    with opener.open(req,timeout=45) as response:return json.load(response)
try:
    entry=next(v for v in owner.catalogue.bank.values() if '2.061' in v['expression'] and '20610' in v['expression'])
    practice=post('/api/practice/start',{'item_id':entry['id'],'request_id':'decimal-practice'})
    before=get('/api/learning')['summary']['attempts']
    hint=post('/api/teach',{'session':practice['session'],'request':{'request_id':'old-hint','question':'先给提示，不要答案。'}})['response']
    response=post('/api/teach',{'session':practice['session'],'request':{'request_id':'whole-answer','question':cases[0][0]}})['response']
    check('same_session_full_answer_overrides_previous_hint',response['route']['teaching']['allow_final_answer'] and response['teaching_action']=='give_answer')
    check('reference_answer_and_given_conditions_are_present',entry['key']['values'][0] in response['text'] and '2.061' in response['text'])
    check('answer_delivery_does_not_write_a_student_grade',get('/api/learning')['summary']['attempts']==before)
finally:owner.close();instance.shutdown();instance.server_close()
Path('education/.local/reports/current-instruction-acceptance.local.json').write_text(json.dumps({'checks':checks,'passed':len(checks)},indent=2),encoding='utf-8')
