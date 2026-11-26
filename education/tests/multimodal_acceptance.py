import base64
import http.cookiejar
import json
import threading
import urllib.request
import urllib.error
from pathlib import Path
from multimodal_fixture import fixture, sample_image, calls
from qingqi.web_store import WebStore

root, visual, instance = fixture()
threading.Thread(target=instance.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=45) as r: return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    req=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','Origin':base,'X-Qingqi-CSRF':boot['csrf']})
    with opener.open(req,timeout=45) as r: return json.load(r)
results=[]
def check(name,ok):
    assert ok,name
    results.append({'name':name,'passed':True}); print(json.dumps(results[-1]),flush=True)
def denied(run,status):
    try: run()
    except urllib.error.HTTPError as e: return e.code==status
    return False
def teach(s,q,images=None,rid=None):
    return post('/api/teach',{'session':s,'request':{'request_id':rid or __import__('uuid').uuid4().hex,'question':q,**({'images':images} if images else {})}})
try:
    payload={'request_id':'upload-1','name':'方程.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()}
    image=post('/api/tutor/images',payload)
    check('image_upload_normalized_and_idempotent',post('/api/tutor/images',payload)==image and image['width']==600)
    check('unsupported_svg_and_fake_image_rejected',denied(lambda:post('/api/tutor/images',{'request_id':'bad-1','name':'a.svg','data_url':'data:image/svg+xml;base64,PHN2Zy8+'}),400) and denied(lambda:post('/api/tutor/images',{'request_id':'bad-2','name':'fake.png','data_url':'data:image/png;base64,YmFk'}),400))
    check('image_upload_id_conflict_rejected',denied(lambda:post('/api/tutor/images',{**payload,'name':'other.png'}),403))
    with opener.open(base+image['url']) as r: check('owned_preview_is_actual_jpeg',r.headers['Content-Type']=='image/jpeg' and r.read(2)==b'\xff\xd8')
    session=post('/api/sessions',{})['id']
    result=teach(session,'请先引导我解方程，不要给答案。',[image['id']],'image-teach')
    check('vision_transcribes_real_image_protocol_then_guides',result['response']['teaching_action']=='ask' and result['session']['messages'][-1]['recognized_question']=='3x+2=14' and calls[0]['role']=='glm-5.3-flash')
    before=len(calls); teach(session,'请先引导我解方程，不要给答案。',[image['id']],'image-teach')
    check('completed_image_request_does_not_repeat_ocr',len(calls)==before)
    check('image_followup_linear_answer_checked_without_catalogue_grade',teach(session,'x=4')['response']['teaching_action']=='confirm' and get('/api/learning')['summary']['attempts']==0)
    multi_ids = [image['id']]
    for index in range(2):
        multi_ids.append(post('/api/tutor/images', {**payload, 'request_id': f'multi-upload-{index}', 'name': f'合成图片{index + 2}.png'})['id'])
    multi_session = post('/api/sessions', {})['id']
    call_start = len(calls)
    multi = teach(multi_session, '请分析这三张图片中的表格', multi_ids, 'three-image-teach')
    messages = multi['session']['messages'][-1]
    check('three_images_reach_both_recognition_and_natural_model_calls', len(calls) - call_start == 2 and all(c['images'] == 3 for c in calls[call_start:]))
    check('three_images_are_owned_and_ordered_in_the_same_message', [p['id'] for p in messages['images']] == multi_ids and messages['original_input']['images'] == multi_ids)
    before_multi = len(calls)
    teach(multi_session, '请分析这三张图片中的表格', multi_ids, 'three-image-teach')
    check('three_image_replay_preserves_history_without_new_model_calls', len(calls) == before_multi and len(get('/api/session?id=' + multi_session)['messages']) == 1)
    check('four_image_teaching_request_is_rejected', denied(lambda: teach(multi_session, '分析图片', multi_ids + [image['id']]), 400))
    check('image_question_can_be_corrected_in_conversation',teach(session,'图片识别错了，题目应改为 3x+2=17，请提示')['response']['teaching_action']=='ask' and teach(session,'x=5')['response']['teaching_action']=='confirm')
    geometric=post('/api/sessions',{})['id']
    guided=teach(geometric,'这是一道几何题，请追问引导我。',[image['id']])
    check('unverified_visual_problem_uses_flash_tutor_without_fake_confirmation',guided['response']['model_inference'] and guided['response']['teaching_action']=='ask' and '角' in guided['response']['text'] and len(calls)>before)
    descriptive=post('/api/sessions',{})['id']
    description=teach(descriptive,'分析一下这个图片中的表格表达了什么',[image['id']])
    check('image_description_accepts_natural_text_without_tool_json',description['response']['teaching_action']=='explain' and '统计表' in description['response']['text'] and calls[-1]['natural'])
    follow_description=teach(descriptive,'这张表中的数据应该怎样比较？')
    check('table_followup_keeps_same_owned_image_context',follow_description['response']['controller']=='glm_vision_text_controller' and follow_description['response']['teaching_action']=='explain' and calls[-1]['natural'])
    failed=post('/api/sessions',{})['id']
    try:
        teach(failed,'分析这个图片的表格，空回复',[image['id']],'empty-text')
        raise AssertionError('empty reply accepted')
    except urllib.error.HTTPError as error:
        check('invalid_model_reply_is_not_misreported_as_permission',error.code==502 and json.load(error)['error']=='model_protocol')
    count=len(calls)
    check('failed_text_request_is_not_automatically_regenerated',denied(lambda:teach(failed,'分析这个图片的表格，空回复',[image['id']],'empty-text'),502) and len(calls)==count)
    blur=post('/api/sessions',{})['id']
    check('unclear_image_asks_for_clearer_input',teach(blur,'这张图片很模糊',[image['id']])['response']['teaching_action']=='clarify')
    check('foreign_image_id_rejected',denied(lambda:teach(blur,'读取图片',['not-owned']),403))
    store=WebStore(root)
    try:
        from qingqi.contracts import Denied
        isolated=False
        try: store.owner.image('other-student',image['id'])
        except Denied: isolated=True
        check('image_read_is_student_isolated',isolated)
        item=next(e for e in store.owner.catalogue.bank.values() if e['grade']=='7' and e['answer_kind']=='numeric' and e['id'] not in store.owner.catalogue.initial['historical_items'] and e['id'] not in {v['item']['id'] for v in store.practice_history('edu-math-student')})
    finally: store.close()
    assignment=post('/api/practice/start',{'item_id':item['id'],'request_id':'history-start'})
    post('/api/practice/answer',{'assignment_id':assignment['id'],'request_id':'history-answer','answer':';'.join(item['key']['values'])})
    history=get('/api/practice/history')['items']
    check('history_contains_owned_actual_work_without_answers',any(h['session']==assignment['session'] and h['source']=='本产品作答' for h in history) and all('key' not in h['item'] and 'analysis' not in h['item'] for h in history))
finally:
    instance.shutdown(); instance.server_close(); visual.shutdown(); visual.server_close()
Path('education/.local/reports/multimodal-acceptance.json').write_text(json.dumps({'passed':len(results),'scenarios':results,'real_model':False},ensure_ascii=False,indent=2),encoding='utf-8')
