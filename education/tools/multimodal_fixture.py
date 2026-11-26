"""Local OpenAI vision protocol fixture, not a real model evaluation."""
import io
import json
import os
import base64
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image, ImageDraw
from student_data_acceptance import fixture_root
from qingqi.product import Deployment, server
from qingqi.contracts import canonical
from vision_protocol_fixture import request_envelope

calls = []
class VisionHandler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def do_POST(self):
        body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        content=body['messages'][1]['content']
        assert body['model']=='glm-5.3-flash' and isinstance(content,list)
        photos=[x['image_url']['url'] for x in content if x['type']=='image_url']
        assert photos and all(x.startswith('data:image/jpeg;base64,') for x in photos)
        for photo in photos:
            Image.open(io.BytesIO(base64.b64decode(photo.split(',',1)[1]))).verify()
        payload=request_envelope(body)
        schema = payload.get('required_output_schema', {})
        calls.append({'role':body['model'],'images':len(photos),'schema':list(schema.get('properties', {})), 'natural':not schema,'schema_in_system':schema and 'required_output_schema' not in json.loads(content[0]['text']),'json_mode':body.get('response_format')})
        if 'unclear' in schema.get('properties', {}):
            q=payload['input'].get('request','')
            value={'text':'学习记录统计表：Monday 6题、答对4题；Tuesday 8题、答对6题；Wednesday 10题、答对8题。' if '表格' in q else '已知三角形 ABC，请解释角之间的关系。' if '几何' in q else '3x+2=14', 'unclear':'模糊' in q, 'note':'图片模糊，请补一张清晰图片。' if '模糊' in q else ''}
            if '测试识别回显' in q:value={'input':payload['input'],'required_output_schema':schema}
            elif '测试识别包装字段' in q:value={**value,'input':payload['input'],'required_output_schema':schema}
            elif '测试识别未知字段' in q:value={**value,'other_field':'untrusted-extra'}
            elif '测试识别缺字段' in q:value={'note':'只有说明，没有题目'}
            elif '测试识别错类型' in q:value={'text':'3x+2=14','unclear':'false','note':''}
        elif not schema:
            assert 'response_format' not in body
            q = payload['input'].get('question', '')
            value = '' if '空回复' in q else '这是一张统计表，列出了各项记录，可以比较各行数值；看不清的单元格需要补一张清晰截图。' if '表格' in q else '图片中的可见条件和关系已列出，可以按题号整理各部分内容。' if '直接说明图片表达的信息' in body['messages'][0]['content'] else '先观察题中已经标出的角。你准备先用哪条角的性质？' if '三角形' in str(payload) else '先看 3x+2=14，把常数项移到等号另一边。你准备怎样做？'
        else:
            question=payload['input'].get('context',{}).get('practice',{}).get('question','')
            prompt='先看 3x+2=14，把常数项移到等号另一边。你准备怎样做？' if '3x' in question else '先观察题中已经标出的角。你准备先用哪条角的性质？'
            value={'kind':'respond','reply':{'text':prompt,'teaching_action':'ask','evidence_refs':[],'step_refs':[]}}
        raw=canonical({'choices':[{'message':{'content':value if isinstance(value,str) else canonical(value)}}],'usage':{'total_tokens':42}}).encode()
        self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)

def fixture():
    root=fixture_root()
    visual=ThreadingHTTPServer(('127.0.0.1',0),VisionHandler)
    threading.Thread(target=visual.serve_forever,daemon=True).start()
    os.environ['EDU_VISION_FIXTURE_KEY']='local-protocol-fixture'
    config=root/'vision.fixture.json'
    config.write_text(json.dumps({'turn_seconds':60,'lease_seconds':80,'models':{'vision':{'base_url':f'http://127.0.0.1:{visual.server_port}/v1','model':'glm-5.3-flash','key_env':'EDU_VISION_FIXTURE_KEY','enabled':True,'allowed_hosts':['127.0.0.1'],'timeout':20,'json_mode':True}}}),encoding='utf-8')
    product=server(0,root=root,deployment=Deployment(config=config))
    return root, visual, product

def sample_image(text='3x + 2 = 14'):
    image=Image.new('RGB',(600,160),'white')
    ImageDraw.Draw(image).text((20,55),text,fill='black',font_size=40)
    output=io.BytesIO(); image.save(output,'PNG')
    return output.getvalue()

def sample_table():
    image=Image.new('RGB',(720,320),'white')
    draw=ImageDraw.Draw(image)
    draw.text((25,15),'Weekly Practice (Synthetic Example)',fill='black',font_size=25)
    for row, values in enumerate([('Day','Attempts','Correct'),('Monday','6','4'),('Tuesday','8','6'),('Wednesday','10','8')]):
        y=65+row*55
        draw.line((20,y,700,y),fill='black',width=1)
        for x,value in zip([30,330,540],values): draw.text((x,y+10),value,fill='black',font_size=23)
    output=io.BytesIO();image.save(output,'PNG');return output.getvalue()
