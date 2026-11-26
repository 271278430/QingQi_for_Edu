"""Real primary GLM and Flash visual tasks on an isolated student, never production grades."""
import http.cookiejar
import json
import re
import threading
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import server,Deployment
from qingqi.storage import Store


def run():
    root=fixture_root();owner=Store(root);original=json.loads(Path('education/service/config/models.local.json').read_text(encoding='utf-8-sig'))
    config=root/'visual-v3-real.local.json'
    config.write_text(json.dumps({'turn_seconds':240,'lease_seconds':300,'models':{k:v for k,v in original['models'].items() if k in {'glm','vision'}}}),encoding='utf-8')
    instance=server(0,root=root,deployment=Deployment(config));threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(p):
        with opener.open(base+p,timeout=260) as response:return json.load(response)
    boot=get('/api/bootstrap');cases=[]
    def post(p,b):
        with opener.open(urllib.request.Request(base+p,data=json.dumps(b).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']}),timeout=260) as response:return json.load(response)
    try:
        entry=next(e for e in owner.catalogue.bank.values() if '正方形' in e['expression'] and '-2' in e['expression'] and '三个顶点' in e['expression'])
        assignment=post('/api/practice/start',{'item_id':entry['id'],'request_id':'real-square'})
        tasks=[('given_points','请把这三个已知点画在坐标系里。'),('reported_connect','你可以把这个坐标系的图片中的点都给我划线连起来吗'),('reported_socratic','能一步步苏格拉底式的讲解吗'),('animated_connect','请用动画逐条连接图中的三个已知点。')]
        for i,(name,q) in enumerate(tasks):
            response=post('/api/teach',{'session':assignment['session'],'request':{'request_id':f'live-visual-{i}','question':q}})['response']
            assert response['model_inference'] or name in {'reported_connect','animated_connect'};state=json.loads(owner.db.execute('select state from runs where id=?',(response['run_id'],)).fetchone()[0]);visuals=response.get('visuals',[])
            if name=='given_points':assert any(v['kind']=='coordinates' and len(v['points'])==3 for v in visuals)
            if name=='reported_connect':assert len(visuals[0]['segments'])==3 and len(visuals[0]['points'])==3
            if name=='reported_socratic':
                assert state['teaching_plan']['content_style']=='stepwise' and state['teaching_plan']['interaction_style']=='guided_question'
                question_count=len(re.findall(r'[?？]',re.sub(r'\$[^$]*\$','',response['text'])))
                assert question_count<=state['teaching_plan']['budget']['review_questions'] or state.get('soft_quality_flags')
            if name=='animated_connect':assert visuals[0]['template']=='coordinate_drawing' and visuals[0]['frames'][-1]['values']['visible_segments']==3
            assert not re.search(r'\(\s*-2\s*[,，]\s*-2\s*\)',response['text'])
            cases.append({'name':name,'passed':True,'reply':response['text'],'plan':state['teaching_plan'],'visuals':visuals,'model_usage':state.get('model_usage',[]),'actual_model':response['model_inference'],'reply_source':state.get('reply_source'),'quality_rewrite':state.get('quality_rewrite'),'quality_flags':state.get('soft_quality_flags',[])})
            print(json.dumps({'name':name,'passed':True,'chars':len(response['text']),'repairs':response['repairs']}),flush=True)
        general=post('/api/sessions',{})['id']
        for i,(name,q,kind) in enumerate([('function','请画一次函数 y=2x+1 的图像，并简短解释。','function_plot'),('fraction','请画一个 3/4 的分数面积图，帮助理解。','area_model'),('pythagorean','请用 3、4、5 直角三角形的勾股面积动画帮助理解。','animation_scene')]):
            response=post('/api/teach',{'session':general,'request':{'request_id':f'live-new-{i}','question':q}})['response']
            assert any(v['kind']==kind for v in response.get('visuals',[]))
            if name=='function':assert response['visuals'][0]['a']==2 and response['visuals'][0]['b']==1
            if name=='fraction':assert response['visuals'][0]['numerator']==3 and response['visuals'][0]['denominator']==4
            cases.append({'name':name,'passed':True,'reply':response['text'],'visuals':response.get('visuals',[]),'actual_model':response['model_inference']})
            print(json.dumps({'name':name,'passed':True}),flush=True)
        assert get('/api/learning')['summary']['attempts']==0
        Path('education/.local/reports/visual-tasks-v3-live.json').write_text(json.dumps({'passed':len(cases),'real_model_turns':sum(c['actual_model'] for c in cases),'tool_only_turns':sum(not c['actual_model'] for c in cases),'isolated_student':True,'cases':cases},ensure_ascii=False,indent=2),encoding='utf-8')
    except Exception as error:
        row=owner.db.execute('select state from runs order by id desc limit 1').fetchone();state=json.loads(row[0]) if row else {}
        Path('education/.local/reports/visual-tasks-v3-live.json').write_text(json.dumps({'passed':len(cases),'cases':cases,'failure':{'type':type(error).__name__,'error':state.get('error'),'last_error':state.get('last_error'),'usage':state.get('model_usage',[])}},ensure_ascii=False,indent=2),encoding='utf-8')
        raise
    finally:owner.close();instance.shutdown();instance.server_close()


if __name__=='__main__':run()
