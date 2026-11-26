"""Original photograph and old accepted/clarify records, in an isolated live deployment."""
import base64
import http.cookiejar
import json
import sqlite3
import threading
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import server,Deployment
from qingqi.storage import Store
from qingqi.contracts import canonical

root=fixture_root();owner=Store(root);checks=[]
config=root/'problem-live.local.json';original=json.loads(Path('education/service/config/vision.local.json').read_text(encoding='utf-8-sig'))
config.write_text(json.dumps(original),encoding='utf-8')
instance=server(0,root=root,deployment=Deployment(config));threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(base+path,timeout=250) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    with o.open(urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']}),timeout=250) as r:return json.load(r)
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
try:
    prod=sqlite3.connect('file:education/service/runs/product/agent.sqlite?mode=ro',uri=True);prod.row_factory=sqlite3.Row
    rows=prod.execute('select * from runs where id in (59,60,61,62,63) order by id').fetchall();assert len(rows)==5
    old_image=json.loads(rows[0]['state'])['image_question']['images'][0]
    data=prod.execute('select data from tutor_images where id=? and student=?',(old_image,rows[0]['student'])).fetchone()[0];prod.close()
    image=post('/api/tutor/images',{'request_id':'real-cubic-image','name':'original-cubic.jpg','data_url':'data:image/jpeg;base64,'+base64.b64encode(data).decode()})['id']
    session=post('/api/sessions',{})['id']
    def teach(q,rid,images=None):return post('/api/teach',{'session':session,'request':{'request_id':rid,'question':q,**({'images':images} if images else {})}})['response']
    full=teach('直接给完整的答案','real-full',[image])
    check('real_original_picture_recognized_and_solved',full['controller']=='grounded_symbolic_function_v1' and '−3' in full['text'])
    animation=teach('给出关键可视化教学动画','real-animation')
    check('real_exact_short_followup_produces_original_cubic_animation',len(animation['visuals'])==2 and animation['visuals'][0]['plot']['a']==2 and animation['visuals'][0]['plot']['b']==-3 and '−3' in animation['text'])
    above=teach('就是上面那道题','real-above')
    check('real_exact_above_reference_keeps_same_problem','−3' in above['text'] and above['teaching_action']!='clarify')
    natural=teach('能换一种更直观的说法吗？说明为什么要比较端点和驻点就好。','real-natural-followup')
    natural_state=json.loads(owner.db.execute('select state from runs where id=?',(natural['run_id'],)).fetchone()[0])
    check('real_natural_followup_receives_original_question_and_prior_solution',natural['controller']=='glm_general_text_controller' and natural_state.get('problem_question',{}).get('text') and any('−3' in t['reply'] for t in natural_state.get('general_turns',[])) and natural['teaching_action']!='clarify' and not natural.get('visuals'))
    redraw=teach('重新给一个图解','real-after-natural')
    check('real_natural_followup_preserves_image_for_subsequent_redraw',len(redraw['visuals'])==2 and all(v['basis']=='problem' for v in redraw['visuals']))
    check('real_followups_never_repeat_ocr',owner.db.execute("select count(*) from model_invocations where invocation_id='vision:read'").fetchone()[0]==1)
    session=post('/api/sessions',{})['id']
    # 原来三条记录直接复制到隔离会话，生产库保持只读；保留旧控制器及失败路由。
    with owner.db:
        for row in rows:
            state=json.loads(row['state']);request=json.loads(row['request'])
            if state.get('image_question'):state['image_question']={**state['image_question'],'images':[image]}
            if request.get('images'):request['images']=[image]
            owner.db.execute('insert into runs(id,student,session,request_id,payload_hash,request,state,response) values(?,?,?,?,?,?,?,?)',(1000+row['id'],'edu-math-student',session,row['request_id'],row['payload_hash'],canonical(request),canonical(state),row['response']))
    recovered=teach('重新给一个图解，其中如果小数位太多就用分数或者其他形式表示，不要算干净','real-legacy')
    check('actual_old_run59_run60_run61_history_recovers_without_reupload',len(recovered['visuals'])==2 and '−3' in recovered['text'] and owner.db.execute("select count(*) from model_invocations where invocation_id='vision:read'").fetchone()[0]==1)
    check('reported_run62_run63_redraw_uses_original_not_hint_example',all(v['basis']=='problem' and v['plot'].get('display') for v in recovered['visuals']))
    check('live_tutoring_does_not_change_mastery_or_grades',get('/api/learning')['summary']['attempts']==0)
    Path('education/.local/reports/conversation-live.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'real_model':'glm-5.3-flash','production_database':'read_only','isolated_root':str(root),'reply':animation['text'],'visuals':animation['visuals']},ensure_ascii=False,indent=2),encoding='utf-8')
except Exception:
    row=owner.db.execute('select state from runs order by id desc limit 1').fetchone();state=json.loads(row[0]) if row else {}
    Path('education/.local/reports/conversation-live.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'failure':{k:state.get(k) for k in ('error','last_error','vision','image_question','function_task')}},ensure_ascii=False,indent=2),encoding='utf-8')
    raise
finally:owner.close();instance.shutdown();instance.server_close()
