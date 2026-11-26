"""Reported new-image plus animation/story request through isolated product HTTP."""
import base64
import http.cookiejar
import json
import urllib.error
import urllib.request
from pathlib import Path
from conversation_problem_fixture import Fixture,SOURCE
from multimodal_fixture import sample_image
from qingqi.storage import Store


def run():
    f=Fixture();f.start();owner=Store(f.root);checks=[]
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(f.base+path,timeout=100) as r:return json.load(r)
    boot=get('/api/bootstrap')
    def post(path,body):
        req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        try:
            with opener.open(req,timeout=100) as r:return json.load(r)
        except urllib.error.HTTPError as error:
            print(error.read().decode(),flush=True)
            row=owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone()
            if row:
                state=json.loads(row[0]);print(json.dumps({k:state.get(k) for k in ('last_error','presentation','teaching_plan')},ensure_ascii=False),flush=True)
            raise
    def teach(session,q,rid,images=None):return post('/api/teach',{'session':session,'request':{'request_id':rid,'question':q,**({'images':images} if images else {})}})['response']
    def check(name,value):
        assert value,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
    def state(response):return json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(response['run_id'],)).fetchone()[0])
    try:
        old=next(e for e in owner.catalogue.bank.values() if r'\sqrt{a-3}' in e['expression'] and '|b+2|' in e['expression'])
        a=post('/api/practice/start',{'item_id':old['id'],'request_id':'old-exercise'})
        image=post('/api/tutor/images',{'request_id':'new-function-image','name':'function.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})['id']
        response=teach(a['session'],'分别给出动画和情景教学','reported-combination',[image])
        check('reported_image_animation_and_story_request_succeeds',response['repairs']==0 and len(response.get('visuals',[]))==1 and sum(v['kind']=='animation_scene' for v in response['visuals'])==1 and response['visuals'][0]['template']=='function_reasoning')
        accepted=state(response)
        check('separately_is_not_a_negated_animation_or_story',accepted['teaching_plan']['visual']['prefer_animation'] and not accepted['teaching_plan']['visual']['forbid_animation'] and accepted['presentation']['kind']=='story')
        check('function_story_is_actually_explained','情景教学' in response['text'] and '相切' in response['text'])
        detail=get('/api/session?id='+a['session'])
        check('new_image_replaces_old_exercise_reference',detail['practice'] is None and accepted['image_question']['text']==SOURCE and 'a-3' not in response['text'])
        check('uploaded_image_is_attached_to_saved_user_message',detail['messages'][-1]['images'][0]['id']==image)
        count=len(f.calls);replay=teach(a['session'],'分别给出动画和情景教学','reported-combination',[image])
        check('combination_replays_without_ocr_or_tools',replay['cache_hit'] and replay['visuals']==response['visuals'] and len(f.calls)==count)
        emphasized=teach(a['session'],'特别想看这道题的动画和情景故事','especially')
        check('especially_is_not_a_negation',len(emphasized['visuals'])==1 and state(emphasized)['presentation']['kind']=='story')
        static=teach(a['session'],'请别给动画，用静态函数图和情景故事解释','static')
        check('explicit_no_animation_uses_approved_static_function_data',len(static['visuals'])==1 and static['visuals'][0]['kind']=='reasoning_diagram' and static['visuals'][0]['params']['k']==2 and static['visuals'][0]['params']['constant']==1 and static['visuals'][0]['params']['interval']==[-1,1] and '情景教学' in static['text'])
        text=teach(a['session'],'先别给动画，也别画图，只用文字情景解释','text-only')
        check('explicit_text_story_does_not_create_or_claim_a_drawing',not text.get('visuals') and '动画已生成' not in text['text'] and '情景教学' in text['text'])
        final=teach(a['session'],'分别给出完整答案、动画和情景故事','authorized')
        check('authorized_combination_keeps_exact_answer_and_original_graph',all(v['basis']=='problem' for v in final['visuals']) and '−3' in final['text'])
        check('continuing_image_does_not_repeat_ocr',len([p for p in f.calls if p.get('required_output_schema')])==1)
        from qingqi.visual_tasks import wants_animation,refuses_animation
        from qingqi.presentation import request_form
        for q in ['分别给出动画和情景教学','特别想看动画和故事','对比区别，分别给动画和情景图']:
            check('positive_word_scope_'+q,wants_animation(q) and not refuses_animation(q) and request_form(q)['kind']=='story')
        for q in ['别给动画','请别给动画','你先别给动画','不要动画','不用动画']:
            check('negative_command_scope_'+q,not wants_animation(q) and refuses_animation(q))
        fresh=post('/api/sessions',{})['id']
        nonnegative=teach(fresh,old['expression']+'。分别给出动画和情景教学，先不要答案','nonnegative-story')
        check('nonnegative_story_binds_expressions_instead_of_claiming_variables_nonnegative',r'\sqrt{a-3}' in nonnegative['text'] and '|b+2|' in nonnegative['text'] and '变量本身' in nonnegative['text'] and '手里有 $a$ 元' not in nonnegative['text'])
        check('nonnegative_story_has_a_real_original_problem_animation',nonnegative['visuals'][0]['template']=='nonnegative_reasoning' and nonnegative['visuals'][0]['basis']=='problem')
        nn_answer=teach(fresh,'请分别给出答案和情景解释，别给动画','nonnegative-answer')
        check('nonnegative_authorized_answer_keeps_negative_parameter_and_exact_sum','b=-2' in nn_answer['text'] and 'a+b=1' in nn_answer['text'] and len(nn_answer['visuals'])==1 and nn_answer['visuals'][0]['kind']=='reasoning_diagram')
        check('combined_presentations_do_not_become_grades',get('/api/learning')['summary']['attempts']==0)
    finally:owner.close();f.close()
    Path('education/.local/reports/combined-presentation-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'isolated':True,'checks':checks},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':run()
