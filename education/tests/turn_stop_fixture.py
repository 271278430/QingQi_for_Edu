"""Owned HTTP product with a local provider that observes real peer disconnection."""
import json,socket,sys,threading,time,uuid
from pathlib import Path
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from demo import prepare
from qingqi.agent import PROJECT
from qingqi.product import server,Deployment
from vision_protocol_fixture import request_envelope

class Fixture:
    def __init__(self,protocol='openai'):
        self.root=prepare(PROJECT/'runs/turn-stop-acceptance'/uuid.uuid4().hex)
        self.calls=[];self.closed=0;self.release=threading.Event();self.entered=threading.Event();fixture=self
        class Model(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):
                raw=json.dumps({'calls':len(fixture.calls),'closed':fixture.closed}).encode()
                self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));fixture.calls.append(body)
                if protocol=='anthropic':
                    content=body['messages'][0]['content'];env=json.loads(content[0]['text'] if isinstance(content,list) else content)
                else:env=request_envelope(body)
                payload=env['input'];question=payload.get('question') or payload.get('request','')
                text='二次函数的顶点是抛物线转弯的位置。'
                if payload.get('problem',{}).get('text') and '二次函数' not in question:
                    text='先看 '+payload['problem']['text']+'，识别乘除部分，暂时保留加减。'
                schema=env.get('required_output_schema');value={'text':'3x+2=14','unclear':False,'note':''} if schema else text
                raw=json.dumps({'choices':[{'message':{'content':json.dumps(value) if schema else text},'finish_reason':'stop'}]}).encode()
                self.send_response(200)
                if body.get('stream'):self.send_header('Content-Type','text/event-stream')
                else:self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)))
                self.send_header('Connection','close');self.end_headers()
                def emit(value):self.wfile.write(('data: '+json.dumps(value,ensure_ascii=False)+'\n\n').encode());self.wfile.flush()
                if body.get('stream'):
                    if protocol=='anthropic':
                        emit({'type':'message_start','message':{'usage':{'input_tokens':1}}})
                        emit({'type':'content_block_start','index':0,'content_block':{'type':'text','text':''}})
                        if '首字' not in question:emit({'type':'content_block_delta','index':0,'delta':{'type':'text_delta','text':text}})
                    else:
                        emit({'choices':[{'delta':{'reasoning_content':'synthetic thinking'}}]})
                        if '首字' not in question:emit({'choices':[{'delta':{'content':text}}]})
                fixture.entered.set()
                if '快速' not in question:
                    self.connection.settimeout(.05)
                    deadline=time.monotonic()+10
                    while not fixture.release.is_set() and time.monotonic()<deadline:
                        try:
                            if self.connection.recv(1,socket.MSG_PEEK)==b'':fixture.closed+=1;return
                        except socket.timeout:continue
                        except OSError:fixture.closed+=1;return
                try:
                    if body.get('stream'):
                        if protocol=='anthropic':
                            if '首字' in question:emit({'type':'content_block_delta','index':0,'delta':{'type':'text_delta','text':text}})
                            emit({'type':'message_delta','delta':{'stop_reason':'end_turn'},'usage':{'output_tokens':30}});emit({'type':'message_stop'})
                        else:
                            if '首字' in question:emit({'choices':[{'delta':{'content':text}}]})
                            emit({'choices':[{'delta':{},'finish_reason':'stop'}],'usage':{'completion_tokens':30}})
                            self.wfile.write(b'data: [DONE]\n\n');self.wfile.flush()
                    else:self.wfile.write(raw)
                except OSError:fixture.closed+=1
        self.model=ThreadingHTTPServer(('127.0.0.1',0),Model)
        threading.Thread(target=self.model.serve_forever,daemon=True).start()
        config=self.root/'stop.local.json'
        config.write_text(json.dumps({'turn_seconds':30,'lease_seconds':40,'models':{'vision':{'enabled':True,'protocol':protocol,'base_url':f'http://127.0.0.1:{self.model.server_port}/v1','model':'stop-local','requires_key':False,'key_env':'','allowed_hosts':['127.0.0.1'],'supports_tools':False,'supports_image':True,'timeout':20}}}),encoding='utf-8')
        self.instance=server(0,root=self.root,deployment=Deployment(config));threading.Thread(target=self.instance.serve_forever,daemon=True).start()
        self.base=f'http://127.0.0.1:{self.instance.server_port}'
    def close(self):
        self.release.set();self.instance.shutdown();self.instance.server_close();self.model.shutdown();self.model.server_close()

if __name__=='__main__':
    f=Fixture();print(json.dumps({'base':f.base,'stats':f'http://127.0.0.1:{f.model.server_port}/stats'}),flush=True)
    try:sys.stdin.buffer.read()
    finally:f.close()
