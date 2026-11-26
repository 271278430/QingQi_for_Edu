"""Public demo startup and real HTTP actions, with no private catalogue or model key."""
import http.cookiejar
import json
import threading
import urllib.request
import uuid
import subprocess
import sys
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from demo import prepare
from qingqi.agent import PROJECT
from qingqi.catalogue import Catalogue
from qingqi.product import server

root=prepare(PROJECT/'runs/demo-acceptance'/uuid.uuid4().hex)
instance=server(0,root=root)
threading.Thread(target=instance.serve_forever,daemon=True).start()
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
base=f'http://127.0.0.1:{instance.server_port}'
checks=[]
calls=[]
class Model(BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_POST(self):
        body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));calls.append(body)
        payload=json.loads(body['messages'][-1]['content'])['input']
        expression=payload.get('problem',{}).get('text','')
        text=f'先看原题 {expression}，按括号、乘除、加减的顺序整理，只处理当前一步，保留最后结果。'
        raw=json.dumps({'choices':[{'message':{'content':text}}]}).encode()
        self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
model=ThreadingHTTPServer(('127.0.0.1',0),Model)
threading.Thread(target=model.serve_forever,daemon=True).start()
def get(path):
    with opener.open(base+path,timeout=40) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
    with opener.open(request,timeout=40) as r:return json.load(r)
def check(name,value):
    assert value,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
try:
    cli=subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/'tools/import_student_data.py')],capture_output=True,text=True)
    check('public_import_requires_explicit_source_paths',cli.returncode==2 and all('--'+name in cli.stderr for name in ('books','questions','profiles','conversations')))
    check('demo_boots_without_private_data_or_key',boot['demo'] and boot['profile']=='demo-student' and not any(m['enabled'] for m in boot['models']))
    c=Catalogue(root)
    try:check('authored_demo_has_45_items_and_5_topics',len(c.bank)==45 and len(c.topics)==5 and c.initial['source']=='项目自编合成演示')
    finally:c.close()
    view=get('/api/learning');check('demo_shows_map_and_three_questions',len(view['recommendations'])==3 and bool(view['knowledge_map']['nodes']))
    a=post('/api/practice/start',{'item_id':'order-1','request_id':'demo-start'})
    h=post('/api/practice/hint',{'assignment_id':a['id'],'request_id':'demo-hint','style':'heuristic'})
    check('demo_hint_is_a_line_not_a_follow_up',bool(h['text']) and not any(t in h['text'] for t in ('？','?','告诉我','你能')))
    result=post('/api/practice/answer',{'assignment_id':a['id'],'request_id':'demo-answer','answer':'14'})
    check('demo_grading_updates_learning_evidence',result['correct'] and get('/api/learning')['summary']['attempts']==1)
    batch=post('/api/practice/recommendations',{'request_id':'demo-batch'})
    check('demo_can_renew_three_diverse_questions',len({i['id'] for i in batch['items']})==3)
    arch=get('/api/settings/architecture');check('demo_exposes_current_single_architecture',arch['version']=='source_architecture_v11' and len(arch['modules'])==16 and 'request_flow' not in arch)
    check('reopening_demo_keeps_the_same_student_state',prepare(root)==root and get('/api/learning')['summary']['attempts']==1)
    view=get('/api/settings/models')
    saved=post('/api/settings/model-providers',{'request_id':'demo-model','version':view['version'],'operation':'upsert','provider':{
        'id':'custom-demo','display_name':'演示本地连接','model':'demo-hint','base_url':f'http://127.0.0.1:{model.server_port}/v1','protocol':'openai',
        'supports_image':True,'supports_tools':False,'requires_key':False,'timeout':15,'max_tokens':1200,'json_mode':False,'key_action':'keep','api_key':''}})
    provider_id=next(p['id'] for p in saved['providers'] if p.get('model')=='demo-hint')
    post('/api/settings/model-selection',{'request_id':'demo-select','version':saved['version'],'mode':'shared','text_provider_id':provider_id,'vision_provider_id':provider_id})
    a=post('/api/practice/start',{'item_id':'order-2','request_id':'configured-start'})
    body={'assignment_id':a['id'],'request_id':'configured-hint','style':'heuristic'}
    hint=post('/api/practice/hint',body)
    check('gui_model_is_used_for_hints_without_cli_configuration',len(calls)==1 and calls[0]['model']=='demo-hint' and bool(hint['text']))
    check('gui_text_alias_does_not_add_a_model_router_call','只返回JSON' not in calls[0]['messages'][0]['content'])
    check('configured_hint_replay_is_still_idempotent',post('/api/practice/hint',body)==hint and len(calls)==1)
    recommended=post('/api/teach',{'session':a['session'],'request':{'request_id':'demo-chat-recommend','question':'给我推荐一道类似的题目，不用讲解。','expression':a['item']['expression']}})['response']
    items=recommended['student_tasks'][0]['items']
    check('public_chat_recommends_a_real_authored_question',recommended['teaching_action']=='recommend' and len(items)==1 and items[0]['id']!=a['item']['id'] and items[0]['topic']==a['item']['topic'] and all(k not in items[0] for k in ('key','answer','analysis')))
    check('public_recommendation_skips_the_lesson_model_and_keeps_grades',len(calls)==1 and not recommended.get('model_inference') and not recommended.get('visuals') and get('/api/learning')['summary']['attempts']==1)
finally:instance.shutdown();instance.server_close();model.shutdown();model.server_close()
Path('education/.local/reports/demo-acceptance.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks},indent=2),encoding='utf-8')
