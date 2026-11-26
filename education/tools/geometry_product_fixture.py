"""Real owned HTTP/native tools; only image transcription is synthetic."""
import json
import os
import threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from student_data_acceptance import fixture_root
from vision_protocol_fixture import request_envelope
from geometry_fixture_data import SOURCE
from qingqi.product import server,Deployment

class Fixture:
    def __init__(self):
        self.root=fixture_root();self.calls=[];calls=self.calls
        class Model(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));env=request_envelope(body)
                calls.append(env)
                if not env.get('required_output_schema'):
                    if env.get('input',{}).get('annotation_discussion'):
                        content='我看到你在图上做了标注。先结合原题的垂直条件，检查你画的辅助线连接的是哪两个点；你能指出这条线要帮助比较哪一组角吗？'
                    elif '只描述这张图片' in env.get('input',{}).get('question',''):
                        content='图片展示一道等腰直角三角形题，包含三问和点 A、B、C、D、E、F。可见条件有 AC=BC、DF垂直DE；这里先描述题目，不展开证明。'
                    else:
                        self.send_error(500,'geometry proof must use the symbolic tool');return
                else:content=json.dumps({'text':SOURCE,'unclear':False,'note':''})
                raw=json.dumps({'choices':[{'message':{'content':content},'finish_reason':'stop'}]}).encode()
                self.send_response(200);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        self.model=ThreadingHTTPServer(('127.0.0.1',0),Model);threading.Thread(target=self.model.serve_forever,daemon=True).start()
        os.environ['EDU_GEOMETRY_FIXTURE_KEY']='synthetic-local-only'
        config=self.root/'geometry.local.json';config.write_text(json.dumps({'turn_seconds':90,'lease_seconds':100,'models':{'vision':{'enabled':True,'base_url':f'http://127.0.0.1:{self.model.server_port}/v1','model':'glm-5.3-flash','key_env':'EDU_GEOMETRY_FIXTURE_KEY','allowed_hosts':['127.0.0.1'],'timeout':20,'json_mode':True}}}),encoding='utf-8')
        self.instance=server(0,root=self.root,deployment=Deployment(config));self.base=f'http://127.0.0.1:{self.instance.server_port}'
    def start(self):threading.Thread(target=self.instance.serve_forever,daemon=True).start()
    def close(self):self.instance.shutdown();self.instance.server_close();self.model.shutdown();self.model.server_close()

if __name__=='__main__':
    from multimodal_fixture import sample_image
    f=Fixture();image=f.root/'geometry.png';image.write_bytes(sample_image())
    print(json.dumps({'base':f.base,'image':str(image)}),flush=True)
    try:f.instance.serve_forever()
    finally:f.instance.server_close();f.model.shutdown();f.model.server_close()
