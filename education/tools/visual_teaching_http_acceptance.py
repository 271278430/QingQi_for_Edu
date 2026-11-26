"""HTTP, native model protocol, persistence and original-question binding acceptance."""
import base64
import http.cookiejar
import json
import urllib.request
import urllib.error
import uuid

from visual_teaching_fixture import Fixture
from multimodal_fixture import sample_image
from qingqi.agent import PROJECT
from qingqi.storage import Store
from qingqi.visual_teaching import VERSION


def run():
    fixture=Fixture()
    fixture.start()
    checks=[]
    owner=Store(fixture.root)
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(fixture.base+path,timeout=50) as response:return json.load(response)
    boot=get('/api/bootstrap')
    def post(path,body):
        request=urllib.request.Request(fixture.base+path,data=json.dumps(body).encode(),headers={'Origin':fixture.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        with opener.open(request,timeout=50) as response:return json.load(response)
    def check(name,condition):
        assert condition,name
        checks.append({'name':name,'passed':True})
        print(json.dumps(checks[-1]),flush=True)
    try:
        session=post('/api/sessions',{})['id']
        image=post('/api/tutor/images',{'request_id':'image','name':'geometry.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()})
        def teach(question,images=None,request_id=None):
            return post('/api/teach',{'session':session,'request':{'request_id':request_id or uuid.uuid4().hex,'question':question,**({'images':images} if images else {})}})
        first=teach('请用数轴例子帮助理解，不要直接给答案。',[image['id']],'native-visual')
        check('uploaded_image_and_visual_in_same_dialogue',first['response']['visuals'][0]['kind']=='number_line' and first['session']['messages'][-1]['images'][0]['id']==image['id'])
        check('native_function_contract_and_second_text_call',len(fixture.calls)==3 and fixture.calls[1]['body']['tool_choice']=='auto' and fixture.calls[1]['body']['tools'][0]['function']['name']=='render_teaching_visual' and not fixture.calls[2]['body'].get('tools') and fixture.calls[2]['input']['visual_aids'][0]['kind']=='number_line')
        check('pinned_zcode_skill_drives_native_visual_selection','Use render_teaching_visual only when' in fixture.calls[1]['body']['messages'][0]['content'])
        before=len(fixture.calls)
        repeated=teach('请用数轴例子帮助理解，不要直接给答案。',[image['id']],'native-visual')
        check('http_same_request_replay_no_model_or_visual_redraw',repeated['response']['cache_hit'] and repeated['response']['visuals']==first['response']['visuals'] and len(fixture.calls)==before)
        for word,kind in [('坐标','coordinates'),('表格','table'),('柱状','bar_chart'),('情景','scene')]:
            before=len(fixture.calls)
            value=teach(f'请用{word}帮助理解当前题目。')
            check('native_'+kind,value['response']['visuals'][0]['kind']==kind and len(fixture.calls)==before+2)
        two=teach('请用两张数轴和表格帮助理解。')
        check('two_visuals_one_executor_call',len(two['response']['visuals'])==2 and two['response']['tool_calls']==1)
        plain=teach('普通对话：我今天有点累，先聊聊学习。')
        check('optional_plain_text_no_visual',not plain['response'].get('visuals'))
        detail=get('/api/session?id='+session)
        check('refreshed_projection_retains_identical_figures',detail['messages'][0]['response']['visuals']==first['response']['visuals'])
        state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(first['response']['run_id'],)).fetchone()[0])
        check('native_executor_trace_and_resume_signature',state['visual_version']==VERSION and sum(o['tool']=='render_teaching_visual' and o['runtime']['source']=='@zcode/core/ToolExecutor' for o in state['observations'])==1)
        check('visual_help_does_not_write_grades',get('/api/learning')['summary']['attempts']==0)
        inferred=teach('这道题请模拟缺少类型，使用情景图。')
        check('missing_discriminator_inferred_from_unique_complete_shape',inferred['response']['visuals'][0]['kind']=='scene' and inferred['response']['repairs']==0 and inferred['response']['tool_calls']==1)
        before=len(fixture.calls)
        repaired=teach('这道题请模拟缺失字段修复，使用情景图。')
        check('known_complete_selection_repairs_with_new_invocation_and_feedback',repaired['response']['visuals'][0]['kind']=='scene' and repaired['response']['repairs']==1 and len(fixture.calls)==before+3 and 'edges' in fixture.calls[before+1]['input']['protocol_error'] and repaired['response']['tool_calls']==1)
        before=len(fixture.calls)
        for _ in range(2):
            try:teach('这道题请模拟截断回复。',request_id='truncated-native')
            except urllib.error.HTTPError as error:
                check('truncated_native_stops_instead_of_executing_or_regenerating_'+str(_),error.code==502 and json.load(error)['error']=='model_protocol')
            else:raise AssertionError('truncated native tool was accepted')
        state=json.loads(owner.db.execute("SELECT state FROM runs WHERE request_id='truncated-native'").fetchone()[0])
        check('truncated_provider_metadata_saved_no_replay',len(fixture.calls)==before+1 and state['model_usage'][0]['finish_reason']=='length' and state['tool_calls']==0)
        entry=next(e for e in owner.catalogue.bank.values() if '遮住' in e['expression'] and 'x=6' in e['expression'].replace(' ','') and '2x+y=16' in e['expression'].replace(' ',''))
        assignment=post('/api/practice/start',{'item_id':entry['id'],'request_id':'owned-history'})
        session=assignment['session']
        history=teach('请用表格展示这道历史题的已知条件，不要答案。')
        check('history_question_same_native_visual_chain',history['response']['visuals'][0]['kind']=='table' and fixture.calls[-2]['input']['problem']['text']==entry['expression'] and fixture.calls[-1]['input']['teaching_constraint']['allow_final_answer'] is False)
    finally:
        owner.close()
        fixture.close()
    (PROJECT.parent/'.local/reports/visual-teaching-http-acceptance.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'actualZCodeRuntime':True,'realModel':False,'model_protocol_calls':len(fixture.calls)},ensure_ascii=False,indent=2),encoding='utf-8')


if __name__=='__main__':run()
