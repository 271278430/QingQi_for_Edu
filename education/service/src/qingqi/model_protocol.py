"""Native protocol adapters share the same endpoint, authorization and teaching executor."""
import base64,json


def anthropic_body(model,system,user,max_tokens,images,tools):
    content=[{'type':'text','text':user}]
    content += [{'type':'image','source':{'type':'base64','media_type':'image/jpeg','data':image.split(',',1)[1]}} for image in images]
    body={'model':model,'system':system,'messages':[{'role':'user','content':content if images else user}],'max_tokens':max_tokens}
    if tools:body['tools']=[{'name':t['name'],'description':t['description'],'input_schema':t['inputSchema']} for t in tools]
    return body


def normalize_anthropic(data):
    text=''.join(c.get('text','') for c in data['content'] if c.get('type')=='text')
    calls=[{'id':c.get('id',''),'type':'function','function':{'name':c['name'],'arguments':json.dumps(c.get('input',{}))}} for c in data['content'] if c.get('type')=='tool_use']
    reason={'max_tokens':'length','tool_use':'tool_calls','end_turn':'stop','stop_sequence':'stop'}.get(data.get('stop_reason'),data.get('stop_reason'))
    return {'choices':[{'message':{'content':text,'tool_calls':calls},'finish_reason':reason}], 'usage':data.get('usage')}
