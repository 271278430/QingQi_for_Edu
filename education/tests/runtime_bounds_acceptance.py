"""Protocol probes: callbacks cannot replay a handler or renew the operation deadline."""
import json,time,uuid
from pathlib import Path
from qingqi.agent import PROJECT
from qingqi.zcode_runtime import ZCodeRuntime,RuntimeFailure
from qingqi.domain_tools import SPECS,difficulty

root=PROJECT/'runs/runtime-bounds-acceptance'/uuid.uuid4().hex;checks=[]
def check(name,ok):assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def fixture(delay=0):
    calls=[]
    def handler(**args):calls.append(args);time.sleep(delay);return difficulty(**args)
    runtime=ZCodeRuntime(PROJECT/'data/curriculum.sqlite',SPECS,{'difficulty_candidates':handler},root)
    runtime._write=lambda frame:None
    return runtime,calls
args={'name':'difficulty_candidates','arguments':{'history':[]},'timeout_ms':1000}
callback=lambda n:{'callback':n,'name':args['name'],'arguments':args['arguments']}
r,calls=fixture();r.messages.put(callback(1));r.messages.put(callback(1))
try:r.rpc('call',args,timeout=.2,start=False)
except RuntimeFailure as e:check('duplicate_callback_is_rejected_before_second_execution',e.code=='runtime_protocol' and len(calls)==1)
else:raise AssertionError('duplicate accepted')
r,calls=fixture(.04)
for i in (1,2,3):r.messages.put(callback(i))
r.messages.put({'id':1,'result':{'unexpected':'late result'}})
try:r.rpc('call',args,timeout=.065,start=False)
except RuntimeFailure as e:check('callbacks_do_not_renew_rpc_deadline',e.code=='runtime_timeout' and len(calls)<=2)
else:raise AssertionError('deadline extended')
r,calls=fixture(.02);r.deadline=time.perf_counter()+.005;r.messages.put(callback(1));r.messages.put({'id':1,'result':{}})
try:r.rpc('call',args,timeout=1,start=False)
except RuntimeFailure as e:check('turn_deadline_caps_individual_operation',e.code=='runtime_timeout')
else:raise AssertionError('turn deadline ignored')
r,calls=fixture();r.deadline=time.perf_counter()-1;r.messages.put({'id':1,'result':{'closed':True}})
check('cleanup_remains_bounded_and_allowed_after_turn_deadline',r.rpc('close',{},timeout=.1,start=False)['closed'])
Path('education/.local/reports/runtime-bounds-acceptance.local.json').write_text(json.dumps({'checks':checks,'passed':len(checks)},indent=2),encoding='utf-8')
