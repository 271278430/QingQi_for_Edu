"""Isolated current-question history and a reasoning-only provider response."""
import json,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from student_data_acceptance import fixture_root
from qingqi.product import server,Deployment
from qingqi.storage import Store
from qingqi.web_store import WebStore
from qingqi.contracts import Identity,Request,canonical
from qingqi.visual_teaching import render_visuals

class Fixture:
    def __init__(self):
        self.root=fixture_root();self.calls=[];self.reply_valid=False;fixture=self
        class Model(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));fixture.calls.append(body)
                message={'content':''};finish='length'
                if fixture.reply_valid:
                    finish='stop';message={'content':'相反数在零的两侧，到原点的距离相等。例如 $2$ 和 $-2$ 满足这一关系，它们的和为零；这体现了关于原点对称。'}
                    if body.get('tools'):message={'content':None,'tool_calls':[{'id':'owned-valid-tool','type':'function','function':{'name':'render_teaching_visual','arguments':json.dumps({'visuals':[{'kind':'number_line','basis':'example','title':'相反数的对称位置','points':[{'label':'第一个解','x':2},{'label':'另一个解','x':-2}]}]})}}]}
                raw=json.dumps({'choices':[{'message':message,'finish_reason':finish}],'usage':{'completion_tokens':1600 if finish=='length' else 80,'completion_tokens_details':{'reasoning_tokens':1598 if finish=='length' else 0}}}).encode()
                self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        self.model=ThreadingHTTPServer(('127.0.0.1',0),Model);threading.Thread(target=self.model.serve_forever,daemon=True).start()
        config=self.root/'owned-visual.local.json'
        config.write_text(json.dumps({'turn_seconds':35,'lease_seconds':45,'models':{'glm':{'enabled':True,'base_url':f'http://127.0.0.1:{self.model.server_port}/v1','model':'reasoning-only','reasoning_effort':'max','max_tokens':1600,'timeout':20,'requires_key':False,'key_env':'','allowed_hosts':['127.0.0.1'],'supports_tools':True}}}),encoding='utf-8')
        self.owner=Store(self.root);self.archive=WebStore(self.root)
        self.entry=next(v for v in self.owner.catalogue.bank.values() if '和谐方程' in v['expression'] and '4x-2=x+10' in v['expression'].replace(' ',''))
        self.student='edu-math-student';self.session=self.archive.start_practice(self.student,{'item_id':self.entry['id'],'request_id':'owned-visual-start'})['session']
        visual=render_visuals(visuals=[{'kind':'number_line','title':'题干例子：两个解互为相反数','basis':'problem','points':[{'label':'第一个方程的解','x':2},{'label':'另一个方程的解','x':-2}]}])['visuals']
        self.seed(self.session,'请先解释相反数，不给最终答案。',visual,'两个示例方程的解在零的两侧，距离相等。')
        self.seed(self.session,'你是怎样选择教学方式的？',[],'会结合当前输入和已核验的学习证据决定，不把导师提示当作你的作答。')
        request=Request('old-truncated-animation','给我一个动画帮助理解');run,state,_=self.owner.begin(Identity(self.student,self.session),request)
        state.update(phase='blocked',error_code='model_truncated')
        with self.owner.db:self.owner.db.execute('UPDATE runs SET state=?,lease=NULL,expires=0 WHERE id=?',(canonical(state),run))
        self.instance=server(0,root=self.root,deployment=Deployment(config));threading.Thread(target=self.instance.serve_forever,daemon=True).start();self.base=f'http://127.0.0.1:{self.instance.server_port}'
    def seed(self,session,question,visuals,text):
        request=Request('seed-'+str(len(self.archive.detail(self.student,session)['messages'])),question)
        run,state,_=self.owner.begin(Identity(self.student,session),request)
        assignment=self.owner.db.execute('SELECT id FROM practice_assignments WHERE session=?',(session,)).fetchone()[0]
        state.update(phase='completed',practice_entry=self.entry,practice_assignment_id=assignment,route={'intents':['tutor'],'continuity':'continuation','teaching':{'mode':'heuristic','allow_final_answer':False,'label':'启发式提示'}})
        response={'run_id':run,'text':text,'teaching_action':'explain','evidence_refs':[],'step_refs':[],'visuals':visuals,'route':state['route']}
        # 只在独立夹具重建升级前已接受历史；正式学生记录不会被改写。
        with self.owner.db:self.owner.db.execute('UPDATE runs SET state=?,response=?,lease=NULL,expires=0 WHERE id=?',(canonical(state),canonical(response),run))
    def close(self):
        self.archive.close();self.owner.close();self.instance.shutdown();self.instance.server_close();self.model.shutdown();self.model.server_close()

if __name__=='__main__':
    import sys
    f=Fixture();print(json.dumps({'base':f.base,'session':f.session}),flush=True)
    try:sys.stdin.buffer.read()
    finally:f.close()
