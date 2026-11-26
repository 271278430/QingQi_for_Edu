"""Synthetic teaching protocol, actual product HTTP and owned learning data."""
import json
from vision_protocol_fixture import request_envelope
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from student_data_acceptance import fixture_root
from qingqi.product import Deployment, server


def animation(template):
    params={'absolute_distance':{'values':[-4,-2,0,4]},'square_root':{'areas':[0,4,9,16]},'nonnegative_sum':{'pairs':[[4,2],[2,4],[0,0]]},'number_line_motion':{'start':-2,'delta':4},'travel_motion':{'start_a':0,'speed_a':1,'start_b':40,'speed_b':-1,'until':8}}[template]
    return {'kind':'animation_scene','title':'用变化理解这个概念','basis':'example','template':template,'params':params,'duration':12}


class Fixture:
    def __init__(self):
        self.root=fixture_root()
        self.calls=[]
        calls=self.calls
        class Model(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                content=body['messages'][1]['content']
                envelope=request_envelope(body)
                payload=envelope['input']; calls.append({'body':body,'input':payload})
                q=payload.get('question',''); plan=payload.get('teaching_plan',{})
                if envelope.get('required_output_schema'):
                    message={'content':json.dumps({'text':'已知实数 a、b 满足 sqrt(a-3)+|b+2|=0，求 a+b。','unclear':False,'note':''})}
                elif '测试持续空回复' in q:
                    message={'content':''}
                elif '测试过长回复' in q and not payload.get('protocol_error'):
                    message={'content':'先看已知条件。'*120}
                elif '测试持续过长' in q:
                    message={'content':'先看已知条件。'*120}
                elif body.get('tools') and '动画' in q and not payload.get('visual_aids'):
                    template=next((t for name,t in [('距离','absolute_distance'),('开方','square_root'),('非负','nonnegative_sum'),('加减','number_line_motion'),('路程','travel_motion')] if name in q),'absolute_distance')
                    message={'content':None,'tool_calls':[{'id':'call_animation','type':'function','function':{'name':'render_teaching_visual','arguments':json.dumps({'visuals':[animation(template)]})}}]}
                elif '√9' in q:
                    message={'content':'算术平方根取非负值，√9 = 3。'}
                elif plan.get('goal')=='concept' or '根号' in q or '绝对值' in q:
                    text=r'根号表示非负的算术平方根，比如 $\sqrt{9}=3$。绝对值表示到零的距离，所以 $|-2|=2$。'
                    if payload.get('problem'):text+='题里的两项都非负，相加为零时必须分别为零；这帮助我们把原来的条件拆成两个简单等式。'
                    if plan.get('budget',{}).get('questions',1):text+='你能先把这两个等式写出来吗？'
                    message={'content':text}
                else:
                    message={'content':'我们先处理当前这一步：用已经给出的条件代入关系，保持等式两边一致，再回到原题核对符号。' + ('你愿意先写出代入后的式子吗？' if plan.get('budget',{}).get('questions',1) else '')}
                raw=json.dumps({'choices':[{'message':message,'finish_reason':'tool_calls' if message.get('tool_calls') else 'stop'}],'usage':{'total_tokens':80}}).encode()
                self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        self.model=ThreadingHTTPServer(('127.0.0.1',0),Model)
        threading.Thread(target=self.model.serve_forever,daemon=True).start()
        os.environ['EDU_EVOLUTION_FIXTURE_KEY']='synthetic-local-fixture'
        path=self.root/'evolution-model.fixture.json'
        path.write_text(json.dumps({'turn_seconds':80,'lease_seconds':100,'models':{'vision':{'enabled':True,'base_url':f'http://127.0.0.1:{self.model.server_port}/v1','model':'glm-5.3-flash','key_env':'EDU_EVOLUTION_FIXTURE_KEY','allowed_hosts':['127.0.0.1'],'timeout':20}}}),encoding='utf-8')
        self.instance=server(0,root=self.root,deployment=Deployment(config=path));self.base=f'http://127.0.0.1:{self.instance.server_port}'
    def start(self):threading.Thread(target=self.instance.serve_forever,daemon=True).start()
    def close(self):
        self.instance.shutdown();self.instance.server_close();self.model.shutdown();self.model.server_close()


if __name__=='__main__':
    fixture=Fixture()
    print(json.dumps({'base':fixture.base}),flush=True)
    try:fixture.instance.serve_forever()
    finally:fixture.instance.server_close();fixture.model.shutdown();fixture.model.server_close()
