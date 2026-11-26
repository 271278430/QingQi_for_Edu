"""Synthetic visual planner over the real owned product and native ZCode tools."""
import json
import os
import threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from student_data_acceptance import fixture_root
from qingqi.product import server,Deployment
from vision_protocol_fixture import request_envelope


class Fixture:
    @staticmethod
    def examples():
        base={'basis':'example','title':'变化帮助理解'}
        points=[{'label':'A(-2,1)','x':-2,'y':1},{'label':'B(1,1)','x':1,'y':1},{'label':'C(1,-2)','x':1,'y':-2}]
        segments=[{'source':0,'target':1,'style':'solid','role':'edge'},{'source':1,'target':2,'style':'solid','role':'edge'},{'source':0,'target':2,'style':'dashed','role':'diagonal'}]
        animation=lambda template,params:{**base,'kind':'animation_scene','template':template,'params':params,'duration':12}
        return {'geometry':{**base,'kind':'coordinates','points':points,'segments':segments,'polygons':[{'vertices':[0,1,2]}],'circles':[{'center':1,'radius':1}]},
                'linear':{**base,'kind':'function_plot','function':'linear','a':2,'b':1,'domain':[-3,3]},
                'quadratic':{**base,'kind':'function_plot','function':'quadratic','a':1,'b':0,'c':0,'domain':[-3,3]},
                'fraction_area':{**base,'kind':'area_model','numerator':3,'denominator':4,'shape':'circle'},
                'drawing_animation':animation('coordinate_drawing',{'points':points,'segments':segments}),
                'fraction_animation':animation('fraction_fill',{'numerator':3,'denominator':4}),
                'pythagorean':animation('pythagorean',{'a':3,'b':4})}

    def __init__(self):
        self.root=fixture_root();self.calls=[];calls=self.calls;examples=self.examples()
        class Model(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                content=body['messages'][1]['content'];envelope=request_envelope(body)
                data=envelope['input'];calls.append(data);q=data.get('question','');plan=data.get('teaching_plan',{})
                if envelope.get('required_output_schema'):message={'content':json.dumps({'text':'两个可见点 A(-2,1)、B(1,1)，第三个点不清楚。' if '模糊' in data.get('request','') else '三个点 A(-2,1)、B(1,1)、C(1,-2)。','unclear':'模糊' in data.get('request',''),'note':'坐标图不完整，请提供清晰图片。' if '模糊' in data.get('request','') else ''})}
                elif data.get('quality_rewrite') and '测试聚焦失败' in q:
                    self.send_error(503);return
                elif data.get('quality_rewrite') and '测试聚焦泄露' in q:message={'content':'答案是 D，第四个顶点是 (-2,-2)。'}
                elif data.get('quality_rewrite'):message={'content':'先看 A 与 B：纵坐标相同，表示两点在同一高度。已知点 $C(1,-2)$$。你觉得 $AB$ 是水平还是竖直的？'}
                elif '苏格拉底' in q and not data.get('protocol_error') and not data.get('visual_aids'):
                    # 同题自然追问走文本API；质量模拟也须覆盖这一真实通路。
                    message={'content':'我们先比较 A 与 B 的纵坐标。它们相同吗？线段是水平的吗？长度是多少？'}
                elif body.get('tools'):
                    name=next((k for word,k in [('一次函数','linear'),('二次函数','quadratic'),('分数动画','fraction_animation'),('分数','fraction_area'),('勾股','pythagorean'),('连点动画','drawing_animation'),('几何','geometry')] if word in q),None)
                    if name:message={'content':None,'tool_calls':[{'id':'visual','type':'function','function':{'name':'render_teaching_visual','arguments':json.dumps({'visuals':[examples[name]]})}}]}
                    elif '虚假完成' in q and not data.get('protocol_error'):message={'content':'已经画好了三条连线。'}
                    elif '苏格拉底' in q and not data.get('protocol_error'):message={'content':'我们先比较 A 与 B 的纵坐标。它们相同吗？线段是水平的吗？长度是多少？'}
                    else:message={'content':'我们先比较 A 与 B 的纵坐标。纵坐标相同表示两个点同高，先判断这个位置关系。你觉得 $AB$ 是水平还是竖直的？'}
                elif data.get('visual_aids'):
                    v=data['visual_aids'][0]
                    message={'content':'已经连接三个已知点，实线与虚线展示不同方向；没有补出所求顶点。' if v.get('segments') or v.get('template')=='coordinate_drawing' else '这幅图表示数值之间的关系；观察图中的变化，可以理解当前概念。'}
                else:message={'content':'先比较点的坐标，纵坐标相同表示两个点同高。你觉得 AB 是什么方向？'}
                raw=json.dumps({'choices':[{'message':message,'finish_reason':'tool_calls' if message.get('tool_calls') else 'stop'}],'usage':{'total_tokens':90}}).encode()
                self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        self.model=ThreadingHTTPServer(('127.0.0.1',0),Model);threading.Thread(target=self.model.serve_forever,daemon=True).start()
        os.environ['EDU_VISUAL_V3_FIXTURE_KEY']='synthetic-local-protocol'
        config=self.root/'visual-v3.fixture.json'
        config.write_text(json.dumps({'turn_seconds':80,'lease_seconds':100,'models':{'vision':{'enabled':True,'base_url':f'http://127.0.0.1:{self.model.server_port}/v1','model':'glm-5.3-flash','key_env':'EDU_VISUAL_V3_FIXTURE_KEY','allowed_hosts':['127.0.0.1'],'timeout':20}}}),encoding='utf-8')
        self.instance=server(0,root=self.root,deployment=Deployment(config));self.base=f'http://127.0.0.1:{self.instance.server_port}'
        from qingqi.web_store import WebStore
        store=WebStore(self.root)
        try:
            entry=next(e for e in store.owner.catalogue.bank.values() if '正方形' in e['expression'] and '-2' in e['expression'] and '三个顶点' in e['expression'])
            self.assignment=store.start_practice(store.owner.catalogue.config['student'],{'item_id':entry['id'],'request_id':'browser-square'})
        finally:store.close()
    def start(self):threading.Thread(target=self.instance.serve_forever,daemon=True).start()
    def close(self):self.instance.shutdown();self.instance.server_close();self.model.shutdown();self.model.server_close()


if __name__=='__main__':
    fixture=Fixture();print(json.dumps({'base':fixture.base}),flush=True)
    try:fixture.instance.serve_forever()
    finally:fixture.instance.server_close();fixture.model.shutdown();fixture.model.server_close()
