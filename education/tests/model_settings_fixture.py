"""Real config/HTTP/Store/native protocol fixture; inference is deliberately synthetic."""
import base64,json,os,threading,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from student_data_acceptance import fixture_root
from multimodal_fixture import sample_image
from qingqi.product import Deployment,server
import qingqi.model_settings as model_settings

KEY='synthetic-model-adaptation-key'
class Fixture:
    def __init__(self):
        self.root=fixture_root();self.calls=[];fixture=self
        self.started=threading.Event();self.release=threading.Event()
        self.original_probe=model_settings.make_image_probe
        model_settings.make_image_probe=lambda:('31415','data:image/jpeg;base64,'+base64.b64encode(sample_image()).decode())
        class Model(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):
                raw=json.dumps({'data':[{'id':'text-local','supports_image':False},{'id':'vision-local','supports_image':True}]}).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));native=self.path.endswith('/messages')
                if body['model']=='fail-model':self.send_error(401);return
                authenticated=self.headers.get('Authorization')=='Bearer '+KEY or self.headers.get('x-api-key')==KEY
                if not authenticated and body['model']!='noauth-local':self.send_error(401);return
                content=body['messages'][-1]['content'];images=isinstance(content,list) and any(c['type'] in {'image','image_url'} for c in content)
                text=content if isinstance(content,str) else ''.join(c['text'] for c in content if c['type']=='text')
                payload=json.loads(text)['input'];system=body.get('system') or body['messages'][0]['content']
                fixture.calls.append({'model':body['model'],'images':images,'stream':bool(body.get('stream')),'native':native,'has_tools':bool(body.get('tools')),'authenticated':authenticated,'max_tokens':body['max_tokens'],'reasoning_effort':body.get('reasoning_effort'),'thinking':body.get('thinking')})
                if body['model']=='gated-model':
                    fixture.started.set()
                    if not fixture.release.wait(15):self.send_error(503);return
                if body['model']=='disconnect-model':
                    self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
                    self.wfile.write(b'data: {"choices":[{"index":0,"delta":{"content":"partial"}}]}\n\n');self.wfile.flush();self.close_connection=True;return
                answer='31415' if payload.get('task')=='读取图中整数' else 'OK' if payload.get('task')=='连接测试' else json.dumps({'text':'3x+5=17','unclear':False,'note':''}) if '只返回JSON结果' in system else '二次函数的顶点表示抛物线转弯的位置，开口向上时它是最低点。以y=x²为例，顶点在原点。你能用图像观察顶点两侧的对称关系吗？'
                if body.get('stream'):
                    self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
                    events=[]
                    if native:events=[{'type':'message_start','message':{'usage':{'input_tokens':12}}},{'type':'content_block_start','index':0,'content_block':{'type':'text','text':''}}]
                    events += [{'type':'content_block_delta','index':0,'delta':{'type':'text_delta','text':answer[i:i+9]}} if native else {'choices':[{'index':0,'delta':{'content':answer[i:i+9]}}]} for i in range(0,len(answer),9)]
                    events += [{'type':'message_delta','delta':{'stop_reason':'end_turn'},'usage':{'output_tokens':30}},{'type':'message_stop'}] if native else [{'choices':[{'index':0,'delta':{},'finish_reason':'stop'}]}]
                    for event in events:self.wfile.write(('data: '+json.dumps(event,ensure_ascii=False)+'\n\n').encode());self.wfile.flush();time.sleep(.02)
                    if not native:self.wfile.write(b'data: [DONE]\n\n');self.wfile.flush()
                    return
                result={'content':[{'type':'text','text':answer}],'stop_reason':'end_turn','usage':{'input_tokens':12,'output_tokens':30}} if native else {'choices':[{'message':{'content':answer},'finish_reason':'stop'}]}
                raw=json.dumps(result).encode();self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        self.model=ThreadingHTTPServer(('127.0.0.1',0),Model);threading.Thread(target=self.model.serve_forever,daemon=True).start()
        self.model_base=f'http://127.0.0.1:{self.model.server_port}/v1';os.environ['EDU_MODEL_FIXTURE_KEY']=KEY
        config=self.root/'model-fixture.local.json';config.write_text(json.dumps({'turn_seconds':90,'lease_seconds':100,'models':{role:{'enabled':True,'base_url':self.model_base,'model':name,'key_env':'EDU_MODEL_FIXTURE_KEY','allowed_hosts':['127.0.0.1'],'timeout':15,'supports_image':role=='vision'} for role,name in [('glm','text-local'),('vision','vision-local')]}}),encoding='utf-8')
        self.deployment=Deployment(config);self.instance=server(0,root=self.root,deployment=self.deployment);self.base=f'http://127.0.0.1:{self.instance.server_port}'
    def start(self):threading.Thread(target=self.instance.serve_forever,daemon=True).start()
    def close(self):self.instance.shutdown();self.instance.server_close();self.model.shutdown();self.model.server_close();model_settings.make_image_probe=self.original_probe

if __name__=='__main__':
    f=Fixture();image=f.root/'equation.png';image.write_bytes(sample_image());print(json.dumps({'base':f.base,'model_base':f.model_base,'key':KEY,'image':str(image)}),flush=True)
    try:f.instance.serve_forever()
    finally:f.instance.server_close();f.model.shutdown();model_settings.make_image_probe=f.original_probe
