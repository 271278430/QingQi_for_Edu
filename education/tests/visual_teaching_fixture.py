"""Local function-call fixture on the real teaching HTTP/SQLite/ZCode chain."""
import base64
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from student_data_acceptance import fixture_root
from multimodal_fixture import sample_image
from qingqi.product import Deployment, server
from vision_protocol_fixture import request_envelope


def figures(question):
    base={'title':'帮助理解当前这一步','basis':'example'}
    if '坐标' in question:
        return [{**base,'kind':'coordinates','points':[{'label':'A','x':2,'y':-3},{'label':'B','x':-1,'y':2}]}]
    if '表格' in question:
        return [{**base,'kind':'table','basis':'problem','columns':['已知条件','理解方向'],'rows':[['两边相等','关注对应角'],['等式两边','做同样的运算']]}]
    if '柱状' in question:
        return [{**base,'kind':'bar_chart','bars':[{'label':'甲','value':3},{'label':'乙','value':5}]}]
    if '情景' in question:
        return [{**base,'kind':'scene','nodes':['家','学校','图书馆'],'edges':[{'source':0,'target':1,'label':'步行'},{'source':1,'target':2,'label':'继续行走'}]}]
    return [{**base,'kind':'number_line','points':[{'label':'起点','x':-2}], 'moves':[{'start':-2,'delta':3,'label':'向右移动'}]}]


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
                payload=request_envelope(body)
                calls.append({'body':body,'input':payload['input']})
                data=payload['input']
                question=data.get('question','')
                if 'required_output_schema' in payload:
                    message={'content':json.dumps({'text':'已知三角形 ABC，AB=AC，请理解两个底角的关系。','unclear':False,'note':''})}
                elif body.get('tools') and '普通对话' not in question:
                    visuals=figures(question)
                    if '两张' in question:visuals+=figures('表格')
                    if '缺失字段修复' in question and not data.get('protocol_error'):visuals[0].pop('edges',None)
                    if '缺少类型' in question:visuals[0].pop('kind',None)
                    message={'content':None,'tool_calls':[{'id':'call_visual','type':'function','function':{'name':'render_teaching_visual','arguments':json.dumps({'visuals':visuals},ensure_ascii=False)}}]}
                else:
                    message={'content':'数轴上的位置表示有方向的数，向右是增加、向左是减少。附图是相似例子，帮助观察变化，再回到原题讨论。你能说明两者有什么联系吗？' if data.get('visual_aids') else '我们从你卡住的一步开始。你能告诉我目前理解到哪里了吗？'}
                if '截断回复' in question:
                    message={'content':None,'tool_calls':[{'id':'call_partial','type':'function','function':{'name':'render_teaching_visual','arguments':'{"visuals":['}}]}
                raw=json.dumps({'choices':[{'message':message,'finish_reason':'length' if '截断回复' in question else 'tool_calls' if message.get('tool_calls') else 'stop'}],'usage':{'total_tokens':60}}).encode()
                self.send_response(200)
                self.send_header('Content-Type','application/json')
                self.send_header('Content-Length',str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

        self.model=ThreadingHTTPServer(('127.0.0.1',0),Model)
        threading.Thread(target=self.model.serve_forever,daemon=True).start()
        os.environ['EDU_VISUAL_FIXTURE_KEY']='local-protocol-fixture'
        config=self.root/'visual-model.fixture.json'
        config.write_text(json.dumps({'turn_seconds':60,'lease_seconds':80,'models':{'vision':{'enabled':True,'base_url':f'http://127.0.0.1:{self.model.server_port}/v1','model':'glm-5.3-flash','key_env':'EDU_VISUAL_FIXTURE_KEY','allowed_hosts':['127.0.0.1'],'timeout':20}}}),encoding='utf-8')
        self.instance=server(0,root=self.root,deployment=Deployment(config=config))
        self.base=f'http://127.0.0.1:{self.instance.server_port}'

    def start(self):threading.Thread(target=self.instance.serve_forever,daemon=True).start()

    def close(self):
        self.instance.shutdown()
        self.instance.server_close()
        self.model.shutdown()
        self.model.server_close()


if __name__=='__main__':
    fixture=Fixture()
    print(json.dumps({'base':fixture.base,'image':base64.b64encode(sample_image()).decode()}),flush=True)
    try:fixture.instance.serve_forever()
    finally:
        fixture.instance.server_close()
        fixture.model.shutdown()
        fixture.model.server_close()
