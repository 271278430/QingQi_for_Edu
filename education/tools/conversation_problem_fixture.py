"""Actual product HTTP and native tools; isolated OCR/general-model fixture."""
import json
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from student_data_acceptance import fixture_root
from vision_protocol_fixture import request_envelope
from qingqi.product import server, Deployment

SOURCE = '若函数 f(x) = 2x³ − ax² + 1 (a∈R) 在 (0,∞) 内有且仅有一个零点，则 f(x) 在 [−1,1] 上的最大值和最小值之和为多少？'

class Fixture:
    def __init__(self):
        self.root = fixture_root(); self.calls = []; calls = self.calls; self.ocr_result=None; self.text_result=None; self.stream_finished=True; fixture=self
        class Model(BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));env = request_envelope(body); env['stream_requested']=bool(body.get('stream')); calls.append(env)
                payload = env['input']
                content = json.dumps(fixture.ocr_result or {'text': SOURCE, 'unclear': False, 'note': ''}) if env.get('required_output_schema') else '关于当前题，先看导数的符号和端点，再比较区间内的函数值。'
                if not env.get('required_output_schema') and ('顶点' in payload.get('question','') or '顶点' in str(payload.get('problem',''))):
                    content='二次函数的顶点是抛物线转弯的那个点。开口向上时它表示最低位置，开口向下时表示最高位置；它也在对称轴上。例如 y=x² 的顶点是 (0,0)，观察顶点两侧会看到相同高度对应的横坐标互相对称。'
                elif not env.get('required_output_schema') and '平方根' in str(payload):
                    content='平方根是平方后等于给定数的数。例如 3 和 −3 的平方都是 9，所以 9 的平方根有两个。根号表示的是其中非负的算术平方根，因此 √9=3；这两个说法要区分清楚。'
                if not env.get('required_output_schema') and fixture.text_result is not None:content=fixture.text_result
                if body.get('stream') and not env.get('required_output_schema'):
                    fixture.stream_finished=False
                    self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
                    for i in range(0,len(content),7):
                        event={'choices':[{'index':0,'delta':{'content':content[i:i+7]}}]}
                        self.wfile.write(('data: '+json.dumps(event,ensure_ascii=False)+'\n\n').encode());self.wfile.flush();time.sleep(.12)
                    fixture.stream_finished=True
                    self.wfile.write(b'data: {"choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}\n\ndata: [DONE]\n\n');self.wfile.flush();return
                raw = json.dumps({'choices': [{'message': {'content': content}, 'finish_reason': 'stop'}]}).encode()
                self.send_response(200); self.send_header('Content-Length', str(len(raw))); self.end_headers(); self.wfile.write(raw)
        self.model = ThreadingHTTPServer(('127.0.0.1', 0), Model)
        threading.Thread(target=self.model.serve_forever, daemon=True).start()
        os.environ['EDU_PROBLEM_FIXTURE_KEY'] = 'synthetic-local-only'
        config = self.root / 'problem.local.json'
        config.write_text(json.dumps({'turn_seconds':90, 'lease_seconds':100, 'models': {'vision': {'enabled':True, 'base_url':f'http://127.0.0.1:{self.model.server_port}/v1', 'model':'glm-5.3-flash', 'key_env':'EDU_PROBLEM_FIXTURE_KEY', 'allowed_hosts':['127.0.0.1'], 'timeout':20}}}), encoding='utf-8')
        self.instance = server(0, root=self.root, deployment=Deployment(config)); self.base = f'http://127.0.0.1:{self.instance.server_port}'
    def start(self): threading.Thread(target=self.instance.serve_forever, daemon=True).start()
    def close(self):
        self.instance.shutdown(); self.instance.server_close(); self.model.shutdown(); self.model.server_close()

if __name__ == '__main__':
    f = Fixture()
    from multimodal_fixture import sample_image
    picture=f.root/'cubic.png';picture.write_bytes(sample_image())
    print(json.dumps({'base':f.base,'image':str(picture)}), flush=True)
    try: f.instance.serve_forever()
    finally: f.instance.server_close(); f.model.shutdown(); f.model.server_close()
