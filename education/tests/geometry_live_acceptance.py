"""Reported photograph through live Flash recognition and native geometry tools, isolated student."""
import base64
import http.cookiejar
import json
import threading
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import server,Deployment
from qingqi.storage import Store

def run():
    root=fixture_root();owner=Store(root)
    config=root/'geometry-live.local.json'
    original=json.loads(Path('education/service/config/models.local.json').read_text(encoding='utf-8-sig'))
    config.write_text(json.dumps({'turn_seconds':240,'lease_seconds':300,'models':{k:v for k,v in original['models'].items() if k in {'glm','vision'}}}),encoding='utf-8')
    instance=server(0,root=root,deployment=Deployment(config))
    threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(base+path,timeout=260) as response:return json.load(response)
    boot=get('/api/bootstrap');checks=[]
    def post(path,body):
        with opener.open(urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']}),timeout=260) as response:return json.load(response)
    def check(name,ok):
        assert ok,name
        checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
    try:
        image=Path('tmp/reported-image-ocr.local.jpg')
        picture=post('/api/tutor/images',{'request_id':'reported-picture','name':'geometry.jpg','data_url':'data:image/jpeg;base64,'+base64.b64encode(image.read_bytes()).decode()})['id']
        session=post('/api/sessions',{})['id']
        request={'request_id':'reported-full-answer-animation','question':'我想要你直接给我完整答案，并且附上合适的动画教学','images':[picture]}
        full=post('/api/teach',{'session':session,'request':request})['response']
        check('real_reported_picture_and_request_completed',full['controller']=='grounded_symbolic_geometry_v1' and full['teaching_action']=='give_answer' and full['repairs']==0)
        check('real_all_three_answers_and_domain_correct',all(s in full['text'] for s in ('（1）','（2）','（3）','45','8 - 2 x','\\le4')))
        check('real_two_animations_match_original_problem',{v['template'] for v in full['visuals']}=={'triangle_rotation','geometry_motion'} and next(v for v in full['visuals'] if v['template']=='geometry_motion')['params']['ratio']==.5)
        check('real_photo_has_verified_five_step_lessons',all(v['lesson']['mode']=='solution' and len(v['lesson']['steps'])==5 for v in full['visuals']))
        state=json.loads(owner.db.execute('select state from runs where id=?',(full['run_id'],)).fetchone()[0])
        internal=json.loads(owner.db.execute('select response from runs where id=?',(full['run_id'],)).fetchone()[0])
        report=next(o['result'] for o in state['observations'] if o['tool']=='solve_geometry')
        check('live_recognition_has_verified_symbolic_tool_evidence',all(report['proof_checks'].values()) and report['midpoint']['angles']['ECD']==45 and internal.get('model_usage'))
        replay=post('/api/teach',{'session':session,'request':request})['response']
        check('live_replay_does_not_repeat_recognition',replay['cache_hit'] and replay['text']==full['text'] and replay['visuals']==full['visuals'])
        corrected=post('/api/teach',{'session':session,'request':{'request_id':'correct-angle','question':'第（1）问的∠ECD为什么是90度？'}})['response']
        check('live_followup_corrects_previous_bad_angle','45' in corrected['text'] and 'ECD=90' not in corrected['text'])
        connected=post('/api/teach',{'session':session,'request':{'request_id':'connect-points','question':'请把图中的点全部连起来。'}})['response']
        check('live_followup_connects_all_six_points',len(connected['visuals'][0]['segments'])==15)
        check('live_teaching_and_animation_do_not_create_grades',get('/api/learning')['summary']['attempts']==0)
        Path('education/.local/reports/geometry-live-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'real_model':'configured_glm_vision','isolated_student':True,'reply':full['text'],'visuals':full['visuals'],'model_usage':internal.get('model_usage',[])},ensure_ascii=False,indent=2),encoding='utf-8')
    except Exception:
        row=owner.db.execute('select state from runs order by id desc limit 1').fetchone();state=json.loads(row[0]) if row else {}
        Path('education/.local/reports/geometry-live-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'failure':{'error':state.get('error'),'last_error':state.get('last_error'),'controller':state.get('controller'),'geometry_task':state.get('geometry_task'),'vision':state.get('vision'),'image_question':state.get('image_question'),'reply':locals().get('full',{}).get('text')}},ensure_ascii=False,indent=2),encoding='utf-8')
        raise
    finally:owner.close();instance.shutdown();instance.server_close()

if __name__=='__main__':run()
