"""HTTP/Store regression for frozen session choices and original ZCode option mapping."""
import json,http.cookiejar,urllib.request,urllib.error,base64
from pathlib import Path
from model_settings_fixture import Fixture,KEY
from qingqi.provider_models import model_config
from qingqi.model_options import patches
from qingqi.contracts import ContractError,Request
from multimodal_fixture import sample_image

f=Fixture();f.start();checks=[]
o=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with o.open(f.base+path) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body,expected=200,stream=False):
    req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'X-Qingqi-CSRF':boot['csrf'],'Content-Type':'application/json',**({'Accept':'text/event-stream'} if stream else {})})
    try:r=o.open(req,timeout=100)
    except urllib.error.HTTPError as e:r=e
    with r:
        assert r.code==expected,(r.code,path,r.read().decode())
        return [json.loads(l[6:]) for l in r if l.startswith(b'data: ')] if stream else json.load(r)
def check(name,ok):assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
def view(session=''):return get('/api/chat/models?session='+session)
def save(v,selection,rid):return post('/api/chat/models',{'session':v['session'],'selection':selection,'version':v['version'],'request_id':rid})
try:
    p={'id':'custom-reason','display_name':'可调推理','model':'','base_url':f.model_base,'protocol':'openai','supports_image':True,'supports_tools':False,'requires_key':True,'timeout':15,'max_tokens':1600,'json_mode':False,'api_key':KEY,'key_action':'replace'}
    c=model_config(p);c['optionSpecs']['reasoningLevel']={'values':['low','high','max'],'map':'{"reasoning_effort": reasoningLevel}'}
    p['models']=[{'key':'text','model':'text-local','config':c},{'key':'vision','model':'vision-local','config':c}]
    config=post('/api/settings/model-providers',{'version':get('/api/settings/models')['version'],'request_id':'provider','operation':'upsert','provider':p})
    post('/api/settings/model-selection',{'version':config['version'],'request_id':'defaults','mode':'split','text_provider_id':'custom-reason~text','vision_provider_id':'custom-reason~vision'})
    v=view();check('default_high_in_both_roles_and_safe_student_catalogue',all(x['reasoning_level']=='high' for x in v['selection'].values()) and all('base_url' not in m and 'map' not in m for m in v['models']) and KEY not in json.dumps(v))
    selection={**v['selection'],'text':{**v['selection']['text'],'reasoning_level':'low'}}
    body={'session':'','version':v['version'],'selection':selection,'request_id':'low-draft'};saved=post('/api/chat/models',body);replayed=post('/api/chat/models',body)
    check('low_is_persisted_and_duplicate_save_is_idempotent',view()['selection']['text']['reasoning_level']=='low' and saved['version']==replayed['version'])
    session=post('/api/sessions',{'model_selection':selection},201)['id']
    check('implicit_session_retains_draft_low',view(session)['selection']==selection)
    new=post('/api/sessions',{},201)['id'];check('explicit_new_session_defaults_high',view(new)['selection']['text']['reasoning_level']=='high')
    events=post('/api/teach',{'session':session,'request':{'request_id':'frozen-low','question':'二次函数的顶点是什么？','model_selection':selection}},stream=True)
    check('selected_low_reaches_actual_http_and_stream',events[-1]['kind']=='done' and f.calls[-1]['reasoning_effort']=='low' and any(e['kind']=='delta' for e in events))
    v=view(session);high={**v['selection'],'text':{**v['selection']['text'],'reasoning_level':'high'}};save(v,high,'high')
    before=len(f.calls);events=post('/api/teach',{'session':session,'request':{'request_id':'frozen-low','question':'二次函数的顶点是什么？','model_selection':selection}},stream=True)
    check('same_request_replay_keeps_snapshot_without_model_call',events[-1]['kind']=='done' and len(f.calls)==before)
    events=post('/api/teach',{'session':session,'request':{'request_id':'new-high','question':'抛物线的顶点在哪里？','model_selection':high}},stream=True)
    check('next_turn_high_reaches_http',events[-1]['kind']=='done' and f.calls[-1]['reasoning_effort']=='high')
    image=post('/api/tutor/images',{'request_id':'img','name':'题目.png','data_url':'data:image/png;base64,'+base64.b64encode(sample_image()).decode()},201)['id']
    start=len(f.calls);events=post('/api/teach',{'session':new,'request':{'request_id':'image-high','question':'教我图片中的题目','images':[image],'model_selection':high}},stream=True)
    check('recognition_and_teaching_keep_visual_high',events[-1]['kind']=='done' and all(c['reasoning_effort']=='high' for c in f.calls[start:] if c['images']))
    before=len(f.calls)
    for name,bad in [('unknown_model',{**high,'text':{**high['text'],'model_id':'missing'}}),('unknown_level',{**high,'text':{**high['text'],'reasoning_level':'bogus'}}),('stale_model',{**high,'text':{**high['text'],'model_version':999}})]:
        post('/api/teach',{'session':session,'request':{'request_id':name,'question':'顶点在哪里','model_selection':bad}},409)
    check('invalid_or_stale_snapshot_rejected_before_http',len(f.calls)==before)
    post('/api/chat/models',{'session':session,'version':0,'request_id':'stale-choice','selection':high},409)
    post('/api/chat/models',{'session':new,'version':view(new)['version'],'request_id':'no-owner','selection':high,'api_key':'not-allowed'},400)
    check('version_and_command_fields_are_strict',view(session)['selection']['text']['reasoning_level']=='high')
    try:patches('{"messages": []}',['low'])
    except ContractError:check('option_map_cannot_change_messages_or_auth',True)
    else:raise AssertionError('unrestricted map')
    check('original_cel_evaluates_custom_level_map',patches('{"reasoning_effort": reasoningLevel == "quick" ? "low" : "high"}',['quick','deep'])['quick']['reasoning_effort']=='low')
    check('legacy_request_dump_stays_compatible','model_selection' not in Request.parse({'request_id':'old','question':'题目'}).dump())
    f.deployment.endpoints.pop('glm')
    post('/api/settings/model-selection',{'version':get('/api/settings/models')['version'],'request_id':'flash-defaults','mode':'deployment'})
    flash=post('/api/sessions',{},201)['id'];before=len(f.calls)
    events=post('/api/teach',{'session':flash,'request':{'request_id':'flash-low','question':'二次函数的顶点是什么？','model_selection':selection}},stream=True)
    check('flash_text_model_selection_keeps_original_fast_routing',events[-1]['kind']=='done' and len(f.calls)==before+1 and f.calls[-1]['model']=='text-local' and f.calls[-1]['reasoning_effort']=='low')
    before=len(f.calls);events=post('/api/teach',{'session':flash,'request':{'request_id':'flash-cancel','question':'取消当前任务','model_selection':selection}},stream=True)
    check('model_choice_does_not_send_cancel_to_model',events[-1]['kind']=='done' and len(f.calls)==before)
    post('/api/settings/model-providers',{'version':get('/api/settings/models')['version'],'request_id':'remove-chat-models','operation':'delete','provider_id':'custom-reason'})
    broken=view(session);check('deleted_chat_choices_are_explicitly_unavailable',len(broken['issues'])==2)
    replacement=next(m for m in broken['models'] if m['id']=='deployment-vision')
    choice={'model_id':replacement['id'],'model_version':replacement['version'],'reasoning_level':replacement['default_level']}
    half=save(broken,{'text':choice},'repair-text');fixed=save(half,{'vision':choice},'repair-vision')
    check('both_invalid_roles_can_be_repaired_one_at_a_time',len(half['issues'])==1 and not fixed['issues'] and fixed['selection']=={'text':choice,'vision':choice})
    f.deployment.manage_profiles.clear();check('student_can_choose_without_management_permission',not view(session)['issues'])
    Path('education/.local/reports/composer-models.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True,'live_inference':False},indent=2),encoding='utf-8')
finally:f.close()
