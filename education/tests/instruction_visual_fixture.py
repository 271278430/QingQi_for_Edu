"""Independent legacy number-line fixture for the reported redraw and answer request."""
import json,threading
from student_data_acceptance import fixture_root
from qingqi.product import server
from qingqi.storage import Store
from qingqi.web_store import WebStore
from qingqi.contracts import Request,Identity,canonical
from qingqi.visual_teaching import render_visuals

class Fixture:
    def __init__(self,stress=False):
        self.root=fixture_root();self.owner=Store(self.root);self.web=WebStore(self.root)
        self.entry=next(v for v in self.owner.catalogue.bank.values() if '2.061' in v['expression'] and '20610' in v['expression'])
        self.practice=self.web.start_practice('edu-math-student',{'item_id':self.entry['id'],'request_id':'legacy-decimal-practice'})
        self.session=self.practice['session']
        request=Request('legacy-decimal-chart','能画图给我展示吗')
        run,state,_=self.owner.begin(Identity('edu-math-student',self.session),request)
        visual=render_visuals(visuals=[{'kind':'number_line','title':'平方根的小数点移动规律（例子）','basis':'example',
            'points':[{'label':'√2.061≈1.436','x':1.436},{'label':'√20.61≈4.540','x':4.54},{'label':'√206.1≈14.36（例子）','x':14.36}],
            'moves':[{'start':1.436,'delta':12.924,'label':'被开方数移2位，根移1位：1.436→14.36'}]}])['visuals']
        if stress:
            visual=render_visuals(visuals=[{'kind':'number_line','title':'相邻点和长标签布局检验','basis':'example','points':[{'label':('这是需要完整保留的较长说明文字，不能挤在邻近点下面。'*3)+str(i+1),'x':1.436+i*.0001 if i<7 else 14.36} for i in range(8)],'moves':[]}])['visuals']
        state.update(phase='completed',practice_entry=self.entry,practice_assignment_id=self.practice['id'],route={'intents':['tutor'],'continuity':'continuation','teaching':{'mode':'heuristic','allow_final_answer':False,'label':'启发式提示'}})
        response={'run_id':run,'text':'原题数字为2.061和已知近似1.436，请保持题面条件。','teaching_action':'explain','evidence_refs':[],'step_refs':[],'visuals':visual,'route':state['route']}
        # 隔离夹具重建旧接受图，正式会话和画像不写入测试数据。
        with self.owner.db:self.owner.db.execute('UPDATE runs SET state=?,response=?,lease=NULL,expires=0 WHERE id=?',(canonical(state),canonical(response),run))
        self.instance=server(0,root=self.root);threading.Thread(target=self.instance.serve_forever,daemon=True).start()
        self.base=f'http://127.0.0.1:{self.instance.server_port}'
    def close(self):self.web.close();self.owner.close();self.instance.shutdown();self.instance.server_close()

if __name__=='__main__':
    import sys
    f=Fixture(stress='stress' in sys.argv);print(json.dumps({'base':f.base,'session':f.session,'answer':f.entry['key']['values'][0]}),flush=True)
    try:sys.stdin.buffer.read()
    finally:f.close()
