"""Owned production HTTP paths; only provider SSE packets are synthetic."""
import json,os,threading,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from student_data_acceptance import fixture_root
from vision_protocol_fixture import request_envelope
from geometry_fixture_data import SOURCE
from multimodal_fixture import sample_image
from qingqi.product import server,Deployment
from qingqi.storage import Store

class Fixture:
    def __init__(self):
        self.root=fixture_root();self.calls=[];self.cut_remaining=1;fixture=self
        class Model(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):
                raw=json.dumps({'calls':len(fixture.calls),'reasoning_efforts':[b.get('reasoning_effort') for b in fixture.calls]}).encode()
                self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));env=request_envelope(body);fixture.calls.append(body)
                if env.get('required_output_schema'):
                    raw=json.dumps({'choices':[{'message':{'content':json.dumps({'text':SOURCE,'unclear':False,'note':''})},'finish_reason':'stop'}]}).encode()
                    self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw);return
                question=env.get('input',{}).get('question','');cut='模拟截断' in question and fixture.cut_remaining>0
                if cut:fixture.cut_remaining-=1
                self.send_response(200);self.send_header('Content-Type','text/event-stream');self.send_header('Connection','close');self.end_headers()
                def emit(value):self.wfile.write(('data: '+json.dumps(value,ensure_ascii=False)+'\r\n\r\n').encode());self.wfile.flush()
                emit({'choices':[{'delta':{'reasoning_content':'不要把这段内部推理显示给学生'}}]})
                emit({'choices':[{'delta':{'content':'先看红色辅助线'}}]})
                time.sleep(1.5)
                emit({'choices':[{'delta':{'content':'与 $CD'}}]})
                time.sleep(.15)
                if not cut:emit({'choices':[{'delta':{'content':'$ 的位置关系。'+'这条线是否有效，需要看它与本问条件的联系，而不能只凭图形外观判断。'*10+'它是否通过需要比较的两个端点？'}}]})
                emit({'choices':[{'delta':{},'finish_reason':'length' if cut else 'stop'}],'usage':{'completion_tokens':4096 if cut else 60,'completion_tokens_details':{'reasoning_tokens':4096 if cut else 0}}})
                self.wfile.write(b'data: [DONE]\r\n\r\n');self.wfile.flush()
        self.model=ThreadingHTTPServer(('127.0.0.1',0),Model);threading.Thread(target=self.model.serve_forever,daemon=True).start()
        os.environ['EDU_CODEX_STREAM_FIXTURE_KEY']='synthetic-local-only'
        config=self.root/'stream.local.json';config.write_text(json.dumps({'turn_seconds':35,'lease_seconds':40,'models':{'vision':{'enabled':True,'base_url':f'http://127.0.0.1:{self.model.server_port}/v1','model':'glm-5.3-flash','key_env':'EDU_CODEX_STREAM_FIXTURE_KEY','allowed_hosts':['127.0.0.1'],'timeout':20,'max_tokens':4096,'reasoning_effort':'low','json_mode':True}}}),encoding='utf-8')
        deployment=Deployment(config);self.instance=server(0,root=self.root,deployment=deployment)
        owner=Store(self.root)
        try:
            manager=deployment.model_settings(owner)
            manager.select({'request_id':'select-production-vision','version':manager.view()['version'],'mode':'split','text_provider_id':None,'vision_provider_id':'deployment-vision'})
        finally:owner.close()
        # 验证浏览器实际支持CRLF流，而不通过拦截后整段缓冲的假流来测试。
        handler=self.instance.RequestHandlerClass
        def stream_event(h,event):
            h.stream_seq+=1
            if getattr(h,'stream_disconnected',False):return
            try:h.wfile.write(('data: '+json.dumps({**event,'seq':h.stream_seq,'request_id':h.stream_request_id},ensure_ascii=False)+'\r\n\r\n').encode());h.wfile.flush()
            except OSError:h.stream_disconnected=True
        handler.stream_event=stream_event
        self.base=f'http://127.0.0.1:{self.instance.server_port}'
    def close(self):self.instance.server_close();self.model.shutdown();self.model.server_close()

if __name__=='__main__':
    f=Fixture();image=f.root/'question.png';image.write_bytes(sample_image());print(json.dumps({'base':f.base,'image':str(image),'stats':f'http://127.0.0.1:{f.model.server_port}/stats'}),flush=True)
    try:f.instance.serve_forever()
    finally:f.close()
