"""Reproduce the live definition wording through actual HTTP and streamed tutoring."""
import json,http.cookiejar,urllib.request
from pathlib import Path
from conversation_problem_fixture import Fixture
from qingqi.teaching_plan import validate_text
from qingqi.contracts import ContractError

f=Fixture();f.start();checks=[]
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(f.base+path) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body,stream=False):
    req=urllib.request.Request(f.base+path,data=json.dumps(body).encode(),headers={'Origin':f.base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf'],**({'Accept':'text/event-stream'} if stream else {})})
    with opener.open(req,timeout=90) as r:
        if not stream:return json.load(r)
        return [json.loads(line[6:]) for line in r if line.startswith(b'data: ')]
def check(name,ok):
    assert ok,name;checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
try:
    for i,text in enumerate([
        '**函数的零点**指的是：使函数值等于0的自变量的取值。例如f(x)=x−3，f(3)=0，所以3是它的零点。请你想一想：f(x)=x−2的零点是多少？',
        '零点是满足f(x)=0条件的自变量取值。它对应图象与横轴交点的横坐标。例如f(x)=x−1在x=1时值为0。你能找出f(x)=x−4的零点吗？',
        '零点对应图像与横轴交点的横坐标，而不是整个坐标点。比如y=x−2的图像在横坐标为2处与横轴相交。你能判断y=x−5的零点吗？',
        '二次函数y=ax²+bx+c的图象是抛物线，顶点就是它的最低点（a>0时）或最高点（a<0时）。顶点横坐标x=−b/(2a)，再代回求纵坐标。你能试算y=x²−2x−3的顶点横坐标吗？',
        '顶点就是整条曲线的最高点或最低点：a>0时开口向上、顶点最低，a<0时开口向下、顶点最高。抛物线关于过顶点的竖直线对称。你能说明y=x²的顶点位置吗？',
        '二次函数的顶点就是它升降方向的转折点：a>0时开口向上，顶点是最低点；a<0时开口向下，顶点是最高点。顶点横坐标x=−b/(2a)。你能先算出y=x²−2x−3的顶点横坐标吗？']):
        topic='零点' if i<3 else '顶点'
        f.text_result=text;session=post('/api/sessions',{})['id'];events=post('/api/teach',{'session':session,'request':{'request_id':'definition-'+str(i),'question':'函数的'+topic+'是什么？'}},True)
        check('definition_'+str(i)+'_is_committed_explanation_stream',events[-1]['kind']=='done' and events[-1]['value']['response']['teaching_action']=='explain' and events[-1]['value']['response']['route']['teaching']['mode']=='explain' and topic in events[-1]['value']['response']['text'])
    plan={'goal':'concept','budget':{'questions':1,'hard_questions':None}}
    for name,text in [('empty_encouragement','这个知识点很重要，我们一起好好思考。你有什么想法？'),('only_leading_question','零点表示函数值等于零，对吗？'),('empty_is_relation','函数就是必须掌握的重要知识。你有什么想法？'),('definition_only_in_question','这个知识很值得深入学习。顶点就是最高点或最低点，对吗？')]:
        try:validate_text(text,plan)
        except ContractError:check(name+'_remains_rejected',True)
        else:raise AssertionError(name)
    check('inspection_and_concept_dialogue_do_not_create_grades',get('/api/learning')['summary']['attempts']==0)
    Path('education/.local/reports/concept-definition.local.json').write_text(json.dumps({'passed':len(checks),'checks':checks,'isolated':True},ensure_ascii=False,indent=2),encoding='utf-8')
finally:f.close()
