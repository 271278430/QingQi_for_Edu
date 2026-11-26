"""Bounded OpenAI SSE adapter; tool deltas are assembled before authorization."""
import json,re,time
from .contracts import ContractError
from .zcode_runtime import RuntimeFailure

MAX_FRAME_BYTES=8*1024*1024
MAX_OUTPUT_BYTES=128000

def _events(response,deadline):
    pending=b'';lines=[];size=0
    for chunk in response:
        size+=len(chunk)
        if deadline and time.monotonic()>deadline:raise TimeoutError('model stream deadline exceeded')
        if size>MAX_FRAME_BYTES:raise RuntimeFailure('model_unknown','回复流超过传输预算，结果未确认；已阻止静默重发。')
        pending+=chunk
        while b'\n' in pending:
            line,pending=pending.split(b'\n',1);line=line.rstrip(b'\r')
            if not line:
                if lines:yield b'\n'.join(lines);lines=[]
            elif line.startswith(b'data:'):lines.append(line[5:].lstrip(b' '))
    if pending.startswith(b'data:'):lines.append(pending[5:].lstrip(b' '))
    if lines:yield b'\n'.join(lines)

def _decode(value):
    try:event=json.loads(value)
    except (ValueError,UnicodeError) as error:raise RuntimeFailure('model_protocol','模型回复流格式异常，原输入已保留。') from error
    if not isinstance(event,dict):raise RuntimeFailure('model_protocol','模型回复流格式异常，原输入已保留。')
    if event.get('error'):raise RuntimeFailure('model_failed','模型服务报告失败，原输入和已生成文字已保留。')
    choices=event.get('choices',[])
    if not isinstance(choices,list) or any(not isinstance(choice,dict) or choice.get('delta') is not None and not isinstance(choice.get('delta'),dict) for choice in choices):
        raise RuntimeFailure('model_protocol','模型增量数据格式异常，原输入已保留。')
    return event

def _visible(content,visible,observer,validator):
    if content==visible:return visible
    try:
        if validator:validator(content)
    except ContractError:return visible
    # 对照Codex OutputTextDelta，正文不能等待句号或公式闭合；最终接受另由Store校验和提交。
    observer('delta',content[len(visible):]);return content

def _thinking(observer,last):
    now=time.monotonic()
    if last is None or now-last>=5:
        observer('progress','教师正在分析题意，正文生成后会逐段显示。')
        return now
    return last

def read(response,observer,validator=None,deadline=None):
    content='';visible='';tools={};finish=None;usage=None;done=False;thinking=None
    for value in _events(response,deadline):
        if value==b'[DONE]':done=True;break
        event=_decode(value)
        if event.get('usage'):usage=event['usage']
        for choice in event.get('choices',[]):
            if choice.get('index',0)!=0:continue
            delta=choice.get('delta') or {}
            if choice.get('finish_reason'):finish=choice['finish_reason']
            if delta.get('reasoning_content'):thinking=_thinking(observer,thinking)
            if delta.get('content'):
                if not isinstance(delta['content'],str):raise RuntimeFailure('model_protocol','模型文字增量格式异常，原输入已保留。')
                content+=delta['content']
                if len(content.encode())>MAX_OUTPUT_BYTES:raise RuntimeFailure('model_protocol','模型实际输出超出预算，已停止此请求。')
                visible=_visible(content,visible,observer,validator)
            for tool in delta.get('tool_calls',[]):
                index=tool.get('index',0);entry=tools.setdefault(index,{'id':'','type':'function','function':{'name':'','arguments':''}})
                if tool.get('id'):entry['id']=tool['id']
                for field in ('name','arguments'):entry['function'][field]+=tool.get('function',{}).get(field,'')
        if len(content.encode())+sum(len(t['function']['arguments'].encode()) for t in tools.values())>MAX_OUTPUT_BYTES:raise RuntimeFailure('model_protocol','模型实际输出超出预算，已停止此请求。')
    if not done and not finish:raise EOFError('model stream ended before completion')
    _visible(content,visible,observer,validator)
    return json.dumps({'choices':[{'message':{'content':content,'tool_calls':[tools[k] for k in sorted(tools)]},'finish_reason':finish or 'stop'}],'usage':usage}).encode()


def read_anthropic(response,observer,validator=None,deadline=None):
    blocks={};text='';visible='';reason=None;usage={};done=False;thinking=None
    for value in _events(response,deadline):
        event=_decode(value);kind=event.get('type')
        if kind=='error':raise RuntimeFailure('model_failed','模型服务报告失败，原输入和已生成文字已保留。')
        if kind=='message_start':usage.update(event.get('message',{}).get('usage',{}))
        if kind=='content_block_start':
            blocks[event['index']]=dict(event['content_block'])
            if event['content_block'].get('type')=='text':text+=event['content_block'].get('text','');visible=_visible(text,visible,observer,validator)
        if kind=='content_block_delta':
            delta=event.get('delta',{});block=blocks.setdefault(event.get('index',0),{'type':'text','text':''})
            if delta.get('type')=='text_delta':
                block['text']=block.get('text','')+delta.get('text','');text+=delta.get('text','')
                if len(text.encode())>MAX_OUTPUT_BYTES:raise RuntimeFailure('model_protocol','模型实际输出超出预算，已停止此请求。')
                visible=_visible(text,visible,observer,validator)
            if delta.get('type')=='thinking_delta':thinking=_thinking(observer,thinking)
            if delta.get('type')=='input_json_delta':block['partial']=block.get('partial','')+delta.get('partial_json','')
        if kind=='message_delta':reason=event.get('delta',{}).get('stop_reason');usage.update(event.get('usage',{}))
        if kind=='message_stop':done=True;break
        if len(text.encode())+sum(len(b.get('partial','').encode()) for b in blocks.values())>MAX_OUTPUT_BYTES:raise RuntimeFailure('model_protocol','模型实际输出超出预算，已停止此请求。')
    if not done:raise EOFError('model stream ended before completion')
    for block in blocks.values():
        if 'partial' in block:block['input']=json.loads(block.pop('partial'))
    _visible(text,visible,observer,validator)
    return json.dumps({'content':[blocks[k] for k in sorted(blocks)],'stop_reason':reason or 'end_turn','usage':usage}).encode()
