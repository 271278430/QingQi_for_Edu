"""Real Flash test of the reported owned photo, using an isolated student."""
import base64
import http.cookiejar
import json
import threading
import urllib.request
from pathlib import Path
from multimodal_fixture import sample_image,sample_table
from student_data_acceptance import fixture_root
from qingqi.product import Deployment,server
from qingqi.storage import Store

root=fixture_root();owner=Store(root)
instance=server(0,root=root,deployment=Deployment(config=Path('education/service/config/vision.local.json')))
threading.Thread(target=instance.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=220) as response:return json.load(response)
boot=get('/api/bootstrap')
def post(path,body):
    request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
    with opener.open(request,timeout=220) as response:return json.load(response)
def upload(name,raw):
    return post('/api/tutor/images',{'request_id':'upload-'+name,'name':name+'.jpg','data_url':'data:image/jpeg;base64,'+base64.b64encode(raw).decode()})['id']
cases=[]
try:
    photo=upload('reported-geometry',Path('tmp/reported-image-ocr.local.jpg').read_bytes())
    session=post('/api/sessions',{})['id']
    body={'session':session,'request':{'request_id':'reported-photo-teach','question':'解这道题','images':[photo]}}
    first=post('/api/teach',body)
    recognized=first['session']['messages'][-1]['recognized_question']
    assert 'ABC' in recognized and 'AC' in recognized and 'DF' in recognized
    assert first['response']['model_inference'] and first['response']['teaching_action'] in {'ask','explain','clarify'}
    state=json.loads(owner.db.execute('select state from runs where id=?',(first['response']['run_id'],)).fetchone()[0])
    assert state['vision']['text']==recognized and isinstance(state['vision']['unclear'],bool)
    usage=[json.loads(row[0]).get('usage') for row in owner.db.execute('select result from model_invocations where run_id=? and status=?',(first['response']['run_id'],'done'))]
    cases.append({'name':'reported_photo_exact_question','reply':first['response']['text'],'recognized':recognized,'unclear':state['vision']['unclear'],'model_usage':usage})
    print(json.dumps({'name':cases[-1]['name'],'passed':True}),flush=True)
    assert post('/api/teach',body)['response']['cache_hit']
    cases.append({'name':'accepted_photo_replay','passed':True})
    follow=post('/api/teach',{'session':session,'request':{'request_id':'reported-photo-follow','question':'这张图中第（1）问怎么入手？先给我一个提示。'}})
    assert follow['response']['controller']=='glm_vision_text_controller'
    cases.append({'name':'same_photo_followup','reply':follow['response']['text']})
    print(json.dumps({'name':cases[-1]['name'],'passed':True}),flush=True)
    import io
    from PIL import Image
    def jpeg(raw):
        out=io.BytesIO();Image.open(io.BytesIO(raw)).convert('RGB').save(out,format='JPEG');return out.getvalue()
    ids=[photo,upload('equation',jpeg(sample_image())),upload('table',jpeg(sample_table()))]
    other=post('/api/sessions',{})['id']
    multi=post('/api/teach',{'session':other,'request':{'request_id':'three-photo-read','question':'请按图片顺序描述三张图中的几何题、方程、学习记录表，不解题。','images':ids}})
    text=multi['session']['messages'][-1]['recognized_question']
    assert 'ABC' in text and '14' in text and any(v in text for v in ('Monday','周一','星期一'))
    assert len(multi['session']['messages'][-1]['images'])==3
    cases.append({'name':'reported_photo_and_two_synthetic_images','recognized':text,'reply':multi['response']['text']})
    print(json.dumps({'name':cases[-1]['name'],'passed':True}),flush=True)
    assert get('/api/learning')['summary']['attempts']==0
    report={'passed':len(cases),'model':'glm-5.3-flash','scope':'recognition, transport and dialogue continuity; geometric proof correctness is not verified','isolated_student':True,'actual_reported_photo':True,'fixture_root':str(root),'cases':cases}
    Path('education/.local/reports/vision-schema-live.local.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
except Exception:
    row=owner.db.execute('select state from runs order by id desc limit 1').fetchone();state=json.loads(row[0]) if row else {}
    Path('education/.local/reports/vision-schema-live.local.json').write_text(json.dumps({'passed':len(cases),'fixture_root':str(root),'cases':cases,'error':state.get('error'),'model_output_error':state.get('model_output_error'),'last_error':state.get('last_error'),'teaching_plan':state.get('teaching_plan'),'usage':state.get('model_usage')},ensure_ascii=False,indent=2),encoding='utf-8')
    raise
finally:
    owner.close();instance.shutdown();instance.server_close()
