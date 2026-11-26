"""Isolated catalogue fixture for current-task browser acceptance."""
import json
import sys
import threading
from student_data_acceptance import fixture_root
from qingqi.product import server
from qingqi.storage import Store
from qingqi.web_store import WebStore
from qingqi.contracts import Identity,Request,canonical

root=fixture_root();instance=server(0,root=root)
threading.Thread(target=instance.serve_forever,daemon=True).start()
owner=Store(root)
archive=WebStore(root)
legacy=archive.create('edu-math-student','旧版推荐记录')
request=Request('legacy-query','给我推荐一个类似的题目')
run_id,state,_=owner.begin(Identity('edu-math-student',legacy['id']),request)
state.update(phase='completed',effective_request=request.dump(),route={'intents':['tutor'],'teaching':{'label':'分步讲解','mode':'explain'}})
response={'run_id':run_id,'text':'情景教学：旧题讲解没有完成本轮推荐。','teaching_action':'explain','evidence_refs':[],'step_refs':[],'route':state['route']}
# 仅在隔离夹具重建旧版接受记录，测试升级后的只读提示与明确重新执行。
with owner.db:owner.db.execute('UPDATE runs SET state=?,response=?,lease=NULL,expires=0 WHERE id=?',(canonical(state),canonical(response),run_id))
archive.close()
entry=next(e for e in owner.catalogue.bank.values() if 'sqrt' in e['expression'] and 'b+2' in e['expression'].replace(' ','') and e.get('grade')==owner.catalogue.initial['grade'])
print(json.dumps({'base':f'http://127.0.0.1:{instance.server_port}','item':entry['id'],'legacy_session':legacy['id']}),flush=True)
try:sys.stdin.buffer.read()
finally:owner.close();instance.shutdown();instance.server_close()
