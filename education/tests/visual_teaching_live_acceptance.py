"""Small real GLM visual teaching check with a synthetic geometry image."""
import base64
import http.cookiejar
import io
import json
import threading
import urllib.request
import uuid
from pathlib import Path

from PIL import Image, ImageDraw
from student_data_acceptance import fixture_root
from qingqi.product import Deployment, server
from qingqi.storage import Store


def run():
    root=fixture_root()
    instance=server(0,root=root,deployment=Deployment(config=Path('education/service/config/vision.local.json')))
    threading.Thread(target=instance.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{instance.server_port}'
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    def get(path):
        with opener.open(base+path,timeout=150) as response:return json.load(response)
    boot=get('/api/bootstrap')
    def post(path,body):
        request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        with opener.open(request,timeout=150) as response:return json.load(response)
    checks=[]
    try:
        image=Image.new('RGB',(640,360),'white')
        draw=ImageDraw.Draw(image)
        draw.line([(300,40),(140,280),(460,280),(300,40)],fill='black',width=4)
        for label,point in [('A',(295,15)),('B',(120,288)),('C',(468,288))]:draw.text(point,label,fill='black',font_size=22)
        draw.text((470,85),'AB = AC',fill='black',font_size=26)
        stream=io.BytesIO()
        image.save(stream,format='PNG')
        uploaded=post('/api/tutor/images',{'request_id':'live-image','name':'isosceles.png','data_url':'data:image/png;base64,'+base64.b64encode(stream.getvalue()).decode()})
        session=post('/api/sessions',{})['id']
        cases=[
            ('table','这张图是等腰三角形。请用表格归纳已知条件和下一步思考方向，只给提示，不要最终结论。'),
            ('scene','请为这道题画一张关系图，帮助理解已知边与待讨论的角之间的联系，不要最终结论。'),
            ('number_line','为了理解负数，请用一个相似例子 -2+3，画数轴演示加法，并简短讲解。'),
            (None,'这道题我暂时理解了，普通对话聊聊如何集中学习注意力，不需要任何图示。'),
        ]
        for index,(kind,question) in enumerate(cases):
            value=post('/api/teach',{'session':session,'request':{'request_id':f'live-visual-{index}','question':question,**({'images':[uploaded['id']]} if index==0 else {})}})
            response=value['response']
            actual=[v['kind'] for v in response.get('visuals',[])]
            assert response['model_inference'] and len(response['text'])>10
            assert kind in actual if kind else not actual
            owner=Store(root)
            try:internal=json.loads(owner.db.execute('SELECT response FROM runs WHERE id=?',(response['run_id'],)).fetchone()[0])
            finally:owner.close()
            checks.append({'requested_kind':kind,'actual_kinds':actual,'question':question,'reply':response['text'],'visuals':response.get('visuals',[]),'duration_ms':response['duration_ms'],'model_usage':internal.get('model_usage',[]),'passed':True})
            print(json.dumps({'requested_kind':kind,'actual_kinds':actual,'passed':True}),flush=True)
        assert get('/api/learning')['summary']['attempts']==0
        report={'model':'glm-5.3-flash','passed':len(checks),'real_inference':True,'isolated_synthetic_image':True,'cases':checks,'scope':'四个真实API案例，验证按需选图与自然解释；不代表全题型教学效果。'}
        Path('education/.local/reports/visual-teaching-live-acceptance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    except Exception as error:
        owner=Store(root)
        try:
            row=owner.db.execute('SELECT state FROM runs ORDER BY id DESC LIMIT 1').fetchone()
            state=json.loads(row[0]) if row else {}
            failure={'passed':len(checks),'real_inference':True,'cases':checks,'failure':{'type':type(error).__name__,'error_code':state.get('error_code'),'error':state.get('error'),'protocol_error':state.get('last_error'),'model_usage':state.get('model_usage',[])},'scope':'已执行的真实合成题案例，失败保留，未完成案例不计通过。'}
            Path('education/.local/reports/visual-teaching-live-acceptance.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2),encoding='utf-8')
        finally:owner.close()
        raise
    finally:
        instance.shutdown()
        instance.server_close()


if __name__=='__main__':run()
