"""Protocol framing is bounded independently from visible teaching output."""
import json
from qingqi.model_stream import read,read_anthropic
from qingqi.zcode_runtime import RuntimeFailure
from pathlib import Path
checks=[]
def check(name,ok):assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]))
frames=[('data: '+json.dumps({'trace_metadata':'x'*1000,'choices':[{'index':0,'delta':{'reasoning_content':'思考'}}]})+'\n\n').encode() for _ in range(400)]
frames += [('data: '+json.dumps({'choices':[{'index':0,'delta':{'content':'零点表示函数值为零时的自变量取值。'}}]})+'\n\n').encode(),b'data: {"choices":[{"delta":{},"finish_reason":"stop"}]}\n\n',b'data: [DONE]\n\n']
values=[];data=json.loads(read(frames,lambda kind,text:values.append(text)))
check('large_metadata_frames_do_not_reject_short_valid_text','零点' in data['choices'][0]['message']['content'] and values)
try:read([b'data: '+json.dumps({'choices':[{'delta':{'content':'x'*130000}}]}).encode()+b'\n\n'],lambda *a:None)
except RuntimeFailure as e:check('actual_output_limit_remains_enforced',e.code=='model_protocol')
else:raise AssertionError('output budget')
try:read([b': '+b'x'*(8*1024*1024+1)],lambda *a:None)
except RuntimeFailure as e:check('frame_budget_is_unknown_and_not_protocol_auto_retry',e.code=='model_unknown')
else:raise AssertionError('frame budget')
native=[b'data: {"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}}\n\n',b'data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"OK"}}\n\n',b'data: {"type":"message_stop"}\n\n']
check('anthropic_stream_stays_compatible',json.loads(read_anthropic(native,lambda *a:None))['content'][0]['text']=='OK')
Path('education/.local/reports/model-stream-budget.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2),encoding='utf-8')
