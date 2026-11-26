"""Real GLM evaluation with isolated questions and natural teaching requests."""
import http.cookiejar
import json
import re
import threading
import urllib.request
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
from qingqi.storage import Store


def run():
    root=fixture_root();owner=Store(root);cases=[]
    instance=server(0,root=root,deployment=Deployment(config=Path('education/service/config/vision.local.json')))
    threading.Thread(target=instance.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{instance.server_port}'
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(base+path,timeout=180) as response:return json.load(response)
    boot=get('/api/bootstrap')
    def post(path,body):
        request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        with opener.open(request,timeout=180) as response:return json.load(response)
    try:
        entry=next(e for e in owner.catalogue.bank.values() if 'a-3' in e['expression'].replace(' ','') and 'b+2' in e['expression'].replace(' ','') and '绝对值' in e['title'])
        assignment=post('/api/practice/start',{'item_id':entry['id'],'request_id':'live-root'})
        questions=[
            ('reported_concept','我不太能理解这个根号计算和绝对值运算，能告诉我怎么更好的理解这个吗'),
            ('short_no_questions','不要反问我，简短解释为什么这两项要分别等于零，不要答案。'),
            ('animated_nonnegative','请用一个相似例子的非负量动画帮助理解，不要直接给原题答案。'),
            ('answer','现在直接给正确答案。'),
        ]
        for i,(name,q) in enumerate(questions):
            value=post('/api/teach',{'session':assignment['session'],'request':{'request_id':'live-evolution-'+str(i),'question':q}})
            result=value['response'];internal=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(result['run_id'],)).fetchone()[0]);plan=internal['teaching_plan']
            assert result['model_inference'] or name=='answer'
            assert '你希望查询' not in result['text'] and len(result['text'])<=plan['budget']['hard_max']
            if name=='reported_concept':assert result['teaching_action']=='explain' and ('绝对值' in result['text']) and ('根号' in result['text'] or '平方根' in result['text'])
            if name=='short_no_questions':assert '？' not in result['text'] and '?' not in result['text']
            if name=='animated_nonnegative':assert any(v.get('kind')=='animation_scene' and v['template']=='nonnegative_sum' for v in result.get('visuals',[]))
            if name!='answer':assert not re.search(r'(?:答案|应选|选择|选)[是为：:\s$]*D(?![A-Za-z])',result['text'])
            else:assert result['teaching_action']=='give_answer' and 'D' in result['text'] and '1' in result['text']
            cases.append({'name':name,'passed':True,'question':q,'reply':result['text'],'mode':plan['mode'],'plan':plan,'visuals':result.get('visuals',[]),'duration_ms':result['duration_ms'],'actual_model':result['model_inference']})
            print(json.dumps({'name':name,'passed':True,'chars':len(result['text']),'visuals':[v['kind'] for v in result.get('visuals',[])]}),flush=True)
        general=post('/api/sessions',{})['id']
        value=post('/api/teach',{'session':general,'request':{'request_id':'live-unbound','question':'什么是绝对值？请用距离动画和一个简单例子解释。'}})
        assert '绝对值' in value['response']['text'] and any(v.get('template')=='absolute_distance' for v in value['response'].get('visuals',[]))
        cases.append({'name':'unbound_concept_animation','passed':True,'reply':value['response']['text'],'visuals':value['response'].get('visuals',[]),'actual_model':True})
        follow=post('/api/teach',{'session':general,'request':{'request_id':'live-general-followup','question':'那负数呢？请简短解释，不要反问。'}})['response']
        assert follow['teaching_action']=='explain' and '绝对值' in follow['text'] and '负' in follow['text'] and '？' not in follow['text'] and '?' not in follow['text']
        cases.append({'name':'unbound_concept_continuation','passed':True,'reply':follow['text'],'actual_model':follow['model_inference']})
        assert get('/api/learning')['summary']['attempts']==0
        Path('education/.local/reports/tutoring-evolution-live-acceptance.json').write_text(json.dumps({'passed':len(cases),'real_inference':True,'isolated_student':True,'cases':cases,'scope':'真实辅导相关性、长度、模式与动画案例；非所有题型效果认证。'},ensure_ascii=False,indent=2),encoding='utf-8')
    except Exception as error:
        row=owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone();state=json.loads(row[0]) if row else {}
        Path('education/.local/reports/tutoring-evolution-live-acceptance.json').write_text(json.dumps({'passed':len(cases),'cases':cases,'real_inference':True,'failure':{'type':type(error).__name__,'error':state.get('error'),'protocol_error':state.get('last_error'),'usage':state.get('model_usage',[])}},ensure_ascii=False,indent=2),encoding='utf-8')
        raise
    finally:owner.close();instance.shutdown();instance.server_close()


if __name__=='__main__':run()
