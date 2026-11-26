"""Protocol and model-selection regressions against the observed production failure."""
import json,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from qingqi.model_stream import read,read_anthropic
from qingqi.providers import Endpoint,JSONModel
from qingqi.model_settings import ModelSettings
from qingqi.storage import Store
from qingqi.zcode_runtime import RuntimeFailure
from student_data_acceptance import fixture_root

checks=[]
def check(name,ok):
    assert ok,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def frame(value):return ('data: '+json.dumps(value,ensure_ascii=False)+'\n\n').encode()

def run():
    seen=[]
    def fragments():
        yield frame({'choices':[{'delta':{'content':'先看这条红线'}}]})
        check('text_delta_is_visible_before_punctuation_or_completion',seen==['先看这条红线'])
        yield frame({'choices':[{'delta':{'content':'与 $CD'}}]})
        check('unclosed_math_is_streamed_as_a_draft',seen[-1]=='与 $CD')
        yield frame({'choices':[{'delta':{'content':'$ 的关系。'},'finish_reason':'stop'}]})
        yield b'data: [DONE]\n\n'
    raw=json.loads(read(fragments(),lambda kind,text:seen.append(text) if kind=='delta' else None))
    check('completed_content_is_assembled_once',raw['choices'][0]['message']['content']==''.join(seen))
    wire=('data: {"choices":\r\ndata: [{"delta":{"content":"分数½与根号√"},"finish_reason":"stop"}]}\r\n\r\ndata: [DONE]\r\n\r\n').encode()
    pieces=[wire[i:i+1] for i in range(len(wire))];events=[]
    parsed=json.loads(read(pieces,lambda kind,text:events.append(text) if kind=='delta' else None))
    check('crlf_multiline_data_and_split_utf8_are_supported',parsed['choices'][0]['message']['content']=='分数½与根号√' and ''.join(events)=='分数½与根号√')
    values=[]
    read([frame({'choices':[{'delta':{'reasoning_content':'secret-chain-of-thought'}}]}),frame({'choices':[{'delta':{'content':'这是正文'},'finish_reason':'stop'}]}),b'data: [DONE]\n\n'],lambda kind,text:values.append((kind,text)))
    check('reasoning_only_emits_generic_progress_not_reasoning_text',any(k=='progress' for k,t in values) and all('secret-chain' not in t for k,t in values))
    tools=json.loads(read([frame({'choices':[{'delta':{'tool_calls':[{'index':0,'id':'tool1','function':{'name':'draw','arguments':'{"x":'}}]}}]}),frame({'choices':[{'delta':{'tool_calls':[{'index':0,'function':{'arguments':'1}'}}]},'finish_reason':'tool_calls'}]}),b'data: [DONE]\n\n'],lambda kind,text:values.append((kind,text))))['choices'][0]['message']['tool_calls']
    check('tool_arguments_assemble_without_becoming_visible_text',json.loads(tools[0]['function']['arguments'])=={'x':1} and tools[0]['function']['name']=='draw')
    from qingqi.teaching_policy import choose
    from qingqi.teaching_plan import validate_text
    from qingqi.contracts import Request,Route,ContractError
    plan=choose(Request.parse({'request_id':'concept','question':'顶点是什么'}),Route(('tutor',),()),[])['plan']
    validate_text('顶点',plan,partial=True)
    try:validate_text('顶点',plan)
    except ContractError:check('partial_concept_does_not_weaken_final_completeness_check',True)
    else:raise AssertionError('final concept explanation was not validated')
    try:read([b'data: {bad}\n\n'],lambda *args:None)
    except RuntimeFailure as e:check('malformed_provider_event_is_not_student_invalid_input',e.code=='model_protocol')
    else:raise AssertionError('bad provider event')
    try:read([frame({'choices':[{'delta':{'content':'未完成'}}]})],lambda *args:None)
    except EOFError:check('eof_without_terminal_event_is_not_completion',True)
    else:raise AssertionError('EOF accepted')
    root=fixture_root();store=Store(root)
    try:
        endpoint=Endpoint('vision','https://open.bigmodel.cn/api/paas/v4','glm-5.3-flash','',enabled=True,allowed_hosts=('open.bigmodel.cn',),requires_key=False,reasoning_effort='low',max_tokens=4096)
        settings=ModelSettings(store,'stream-check',{'vision':endpoint})
        settings.select({'request_id':'select-low','version':0,'mode':'split','text_provider_id':None,'vision_provider_id':'deployment-vision'})
        resolved=settings.resolve()['vision'].endpoint
        check('custom_role_selection_preserves_deployment_reasoning_effort',resolved.reasoning_effort=='low' and resolved.max_tokens==4096)
    finally:store.close()
    from qingqi.web_store import WebStore
    from qingqi.contracts import Identity
    web=WebStore(root)
    try:
        session=web.create('edu-math-student')['id'];owner=web.owner
        request=Request.parse({'request_id':'legacy-truncated','question':'讨论标注'})
        run_id,state,_=owner.begin(Identity('edu-math-student',session),request)
        state.update(phase='blocked',context={},annotation_source={'source':'accepted_visual_reference'},error_code='model_protocol',model_usage=[{'finish_reason':'length','tool_call_count':0}])
        owner.checkpoint(run_id,state,'turn_stopped');owner.release(run_id)
        projected=web.detail('edu-math-student',session)['messages'][-1]
        raw=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(run_id,)).fetchone()[0])
        check('legacy_annotation_truncation_projection_does_not_rewrite_history',projected['trace']['error_code']=='model_truncated' and projected['response'] is None and raw['error_code']=='model_protocol')
    finally:web.close()
    from unittest.mock import patch
    class Reply:
        def __init__(self,reason='stop',text='这是正常正文'):self.reason=reason;self.text=text
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def read(self,*args):return json.dumps({'choices':[{'message':{'content':self.text},'finish_reason':self.reason}],'usage':{'completion_tokens':4096,'completion_tokens_details':{'reasoning_tokens':4096}}}).encode()
    class Opener:
        def __init__(self,reply):self.reply=reply;self.bodies=[]
        def open(self,request,**kwargs):self.bodies.append(json.loads(request.data));return self.reply
    for effort in ('','high'):
        opener=Opener(Reply())
        with patch('urllib.request.build_opener',return_value=opener):
            JSONModel(Endpoint('vision',endpoint.base_url,endpoint.model,'',enabled=True,allowed_hosts=endpoint.allowed_hosts,requires_key=False,reasoning_effort=effort)).generate_text('教','输入')
        check('glm_default_high_and_explicit_high_'+(effort or 'default'),opener.bodies[0]['reasoning_effort']==(effort or 'high'))
    opener=Opener(Reply('length',''))
    with patch('urllib.request.build_opener',return_value=opener):
        try:JSONModel(endpoint).generate_text('教',{})
        except RuntimeFailure as e:check('reasoning_exhaustion_is_explicit_truncation_without_auto_replay',e.code=='model_truncated' and len(opener.bodies)==1)
        else:raise AssertionError('reasoning-only truncation accepted')
    Path('education/.local/reports/codex-stream-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2),encoding='utf-8')

if __name__=='__main__':run()
