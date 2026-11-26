"""Current user operations are commands; the previous problem is a reference."""
import re
from .contracts import Request, Route, TEXT, SHORT, EVIDENCE, obj
from .planning import reply, find, next_tool_intent
from .request_controls import negated_before

VERSION='current_student_task_v1'
TOOLS={'recommend':'recommend_practice','learning_path':'preview_learning_path','learning_dashboard':'read_learning_dashboard'}
LABELS={'recommend':'相似练习','learning_path':'学习路径','learning_dashboard':'学情摘要','unsupported':'需求说明'}
NUMBERS={'一':1,'一个':1,'一道':1,'二':2,'两':2,'三':3,'1':1,'2':2,'3':3}
SOURCE_SCHEMA=obj({'kind':{'type':'string','enum':['catalogue','text','image','topic','none']},'item_id':TEXT,'question':{'type':'string','maxLength':6000}})
ARGUMENTS=obj({'source':SOURCE_SCHEMA,'query':TEXT,'count':{'type':'integer','minimum':1,'maximum':3},'difficulty':{'type':'string','enum':['adaptive','easy','challenge']},'minutes':{'type':'integer','minimum':0,'maximum':180}})
ITEM=obj({'id':SHORT,'topic':SHORT,'title':TEXT,'expression':{'type':'string','maxLength':6000},'level':{'type':'integer','minimum':1,'maximum':10},'version':SHORT,
          'options':{'type':'array','items':TEXT,'maxItems':20},'answer_kind':TEXT,'answer_count':{'type':'integer','minimum':1,'maximum':30},'source':TEXT,'usable':{'type':'boolean'},'quality_note':TEXT,
          'reason':TEXT,'purpose':TEXT,'kind':TEXT,'group':TEXT},['id','topic','title','expression','level','version','usable','reason'])
OUTPUT=obj({'kind':{'type':'string','enum':list(TOOLS)},'status':{'type':'string','enum':['ok','needs_source','no_candidates','limited_supply','unknown_topic']},
            'text':TEXT,'items':{'type':'array','items':ITEM,'maxItems':3},'summary':{'type':'object'},'topics':{'type':'array','items':{'type':'object'},'maxItems':3},'path':{'type':'object'},
            'evidence':{'type':'array','items':EVIDENCE,'maxItems':12}},['kind','status','text','evidence'])


def _clauses(text):
    # 引用的题干/术语是资料，不能因为其中含“推荐”就发起一个操作。
    text=re.sub(r'[“「"]([^”」"]*)[”」"]', '', text)
    return [p.strip() for p in re.split(r'[，,。；;\n]',text) if p.strip()]


def _negated(clause,start):
    return negated_before(clause,start) or bool(re.search(r"(?:don't|do not|not|never|no need to)\s+(?:please\s+)?$",clause[max(0,start-32):start],re.I))


def inspect_request(request):
    actions=[];teaching=False;unsupported=[]
    for clause in _clauses(request.question):
        # 明确结束旧任务仍是会话边界；“推荐/换一组题”才生成候选而保留资料。
        if re.fullmatch(r'(?:请|我要|我想|现在|先)?(?:开始新题|开始新问题|换(?:一|个|道|一个|一道)?新(?:题|问题|任务))[！!？?]?',clause):continue
        if re.match(r'已知|题目(?:是|说)|若[有是]|设[有是]',clause):continue
        if re.search(r'(?:是什么意思|是什么含义|如何理解|什么是).{0,8}(?:推荐|推题)|(?:推荐|推题).{0,8}(?:是什么意思|是什么含义)',clause):continue
        # “推荐的第一题”是候选引用，不是让系统再推荐一次。
        recommend=re.search(r'(?:推荐|推题|出题).{0,24}(?:题|练习|problem|exercise)|(?:再来|再出|再给|换|出一|来一|给一).{0,16}(?:题|练习)|(?:同类|同类型|类似|差不多|同知识点|一样知识点).{0,12}(?:题|练习)|(?:recommend|give me|another).{0,30}(?:problem|exercise)',clause,re.I)
        if recommend and not re.search(r'推荐(?:的|过的).{0,12}(?:第|这)',clause) and not _negated(clause,recommend.start()):
            actions.append({'kind':'recommend','clause':clause})
        path=re.search(r'(?:规划|安排|制定|查看|看看|看下|给我看|显示|调整).{0,16}(?:学习路径|学习路线|学习计划)|(?:学习路径|学习路线).{0,12}(?:怎么安排|怎么看|怎样规划)',clause)
        if path and not negated_before(clause,path.start()):actions.append({'kind':'learning_path','clause':clause})
        dashboard=re.search(r'(?:查看|看看|看下|总结|分析|显示|查一下).{0,14}(?:学情|掌握情况|学习情况|薄弱点)|(?:我的学情|我掌握得).{0,8}(?:怎样|如何|怎么样)',clause)
        # 明确提交学习记录做困难诊断仍走专项任务；查看已有学情才是只读查询。
        if dashboard and not request.history and not negated_before(clause,dashboard.start()):actions.append({'kind':'learning_dashboard','clause':clause})
        for m in re.finditer(r'讲解|讲一下|讲讲|解释|辅导|提示|引导|追问|解答|求解|核对|画图|动画|演示|explain|teach|hint',clause,re.I):
            if not _negated(clause,m.start()):teaching=True
        if re.search(r'导出|发送给|发到|删除文件|推荐.{0,8}(?:书|电影|商品|餐厅)',clause):unsupported.append(clause)
    unique=[]
    for action in actions:
        if action['kind'] not in {a['kind'] for a in unique}:unique.append(action)
    count=3;difficulty='adaptive'
    for action in unique:
        if action['kind']!='recommend':continue
        clause=action['clause']
        matches=list(re.finditer(r'([一二两三123])\s*(?:道|个|题|exercise|problem)',clause,re.I))
        if not matches:matches=list(re.finditer(r'\b(one|two|three)\b',clause,re.I))
        for m in matches:
            if not negated_before(clause,m.start()):count=NUMBERS.get(m[1],{'one':1,'two':2,'three':3}.get(m[1].lower(),3))
        difficulty='easy' if re.search(r'简单|基础|容易|easy',clause,re.I) else 'challenge' if re.search(r'更难|难一点|挑战|进阶|hard',clause,re.I) else 'adaptive'
    return {'version':VERSION,'actions':unique,'only_queries':bool(unique or unsupported) and not teaching,'teaching':teaching,'unsupported':unsupported,'count':count,'difficulty':difficulty}


def task_candidate(request):
    if request.history:return False
    for clause in _clauses(request.question):
        if re.match(r'已知|题目(?:是|说)|设[有是]',clause):continue
        cue=re.search(r'练(?:什么|哪些)|(?:什么|哪些|哪种).{0,12}(?:题|练习)|(?:题|练习).{0,12}(?:适合|推荐)|学习路径|学习路线|学情',clause)
        if cue and not _negated(clause,cue.start()):return True
    return False


def from_route(plan,route,request):
    kinds=[kind for kind in route.intents if kind in TOOLS]
    if not kinds:
        if route.intents==('clarify',) and not plan['teaching']:
            return {**plan,'only_queries':True,'unsupported':[request.question]}
        return plan
    return {**plan,'actions':[{'kind':kind,'clause':request.question} for kind in kinds],
            'only_queries':not plan['teaching'],'classification_source':route.method}


def source_reference(store,identity,problem,request,vision=None,selection=None):
    if selection:return {'kind':'catalogue','item_id':selection['entry']['id'],'question':selection['entry']['expression']}
    if request.images and vision:return {'kind':'image','item_id':'','question':vision.get('text','')}
    if request.expression:return _text_reference(store,request.expression)
    if not re.search(r'原(?:题|练习)',request.question) and (not problem or inspect_request(request)['only_queries']):
        latest=store.latest_student_recommendation(identity)
        if latest and latest.get('source') and latest['run_id']>=((problem or {}).get('source_run_id') or 0):return latest['source']
    if problem and problem.get('assignment_id'):
        item=store.practice_assignment(identity.student,problem['assignment_id'])['item']
        return {'kind':'catalogue','item_id':item['id'],'question':item['expression']}
    if problem:
        entry=problem.get('linear_entry');text=(problem.get('problem_question') or problem.get('image_question') or {}).get('text') or problem.get('expression')
        if entry:text=entry['expression']
        if text:return _text_reference(store,text,'image' if problem.get('image_question') else 'text')
    from .teaching_goals import concepts
    return {'kind':'topic' if concepts(request.question) else 'none','item_id':'','question':request.question if concepts(request.question) else ''}


def _text_reference(store,text,kind='text'):
    from .catalogue import normalized
    stem=normalized(text)
    match=next((item for item in store.catalogue.bank.values() if normalized(item['expression'])==stem),None)
    return {'kind':'catalogue' if match else kind,'item_id':match['id'] if match else '', 'question':text}


def is_query_turn(state,question=''):
    if state.get('task_plan'):return state['task_plan']['only_queries']
    original=question or state.get('effective_request',{}).get('question','')
    return inspect_request(Request('history-inspection',original))['only_queries'] if original else False


def bind_plan(plan,source,request,topics=()):
    from .teaching_goals import concepts
    actions=[]
    for action in plan['actions']:
        clause=action['clause']
        titles=[t['title'] for t in topics if t['title'] in clause and not _negated(clause,clause.index(t['title']))]
        query=max(titles,key=len) if titles else ' '.join(concepts(clause))
        minutes=re.search(r'(\d{1,3})\s*分钟',action['clause'])
        args={'source':source,'query':query,'count':plan['count'],'difficulty':plan['difficulty'],'minutes':min(180,int(minutes[1])) if minutes else 0}
        actions.append({**action,'tool':TOOLS[action['kind']],'arguments':args})
    return {**plan,'actions':actions,'source':source,'original_question':request.question}


def decision(plan):
    kind=plan['actions'][0]['kind'] if plan['actions'] else 'unsupported'
    budget={'target_min':0,'target_max':260,'hard_max':1800,'questions':0,'hard_questions':0,'review_questions':0,'unit':'unicode_characters'}
    return {'mode':'chat','requested_mode':'auto','display_mode':kind,'label':LABELS[kind],'reason':'按当前消息执行学生任务；原题只提供参考。',
            'allow_final_answer':False,'no_final_requested':False,'no_questions':True,'no_questions_requested':False,'goal':kind,'source':'current_task',
            'plan':{'version':VERSION,'goal':kind,'mode':'chat','content_style':'task_result','interaction_style':'direct','allow_final_answer':False,'budget':budget,
                    'visual':{'delivery':'text','max_outputs':0}},'budget':budget}


def next_action(state):
    current=next_tool_intent(state)
    for action in state.get('task_plan',{}).get('actions',[]):
        if current==action['kind'] and find(state,action['tool']) is None:return {'kind':'call','tool':action['tool'],'arguments':action['arguments']}
    return None


def outputs(state):
    return [find(state,a['tool']) for a in state.get('task_plan',{}).get('actions',[]) if find(state,a['tool']) is not None]


def validate_outcome(state,result):
    from .contracts import ContractError
    values=outputs(state)
    if len(values)!=len(state['task_plan']['actions']):raise ContractError('current student task did not produce its required results')
    if state['task_plan']['only_queries'] and result['text']!=render_text(state):raise ContractError('query reply must describe the executed task results')
    for value,action in zip(values,state['task_plan']['actions']):
        if value['kind']!=action['kind']:raise ContractError('tool outcome differs from the requested student operation')
        if value['kind']=='recommend' and len(value.get('items',[]))>action['arguments']['count']:raise ContractError('recommendation count exceeds the requested quantity')


def render_text(state):
    values=outputs(state)
    return '\n\n'.join(v['text'] for v in values) if values else '当前支持数学辅导、学习路径、学情查看和个性化练习。这个请求没有对应的可执行工具，请说明希望完成的学生学习任务。'


class StudentTaskController:
    name='controlled_student_task_v1';uses_model=False
    def next(self,request,state,context,registry):
        action=next_action(state)
        if action:return action
        values=outputs(state);kind=state['task_plan']['actions'][0]['kind'] if values else 'clarify'
        if any(v['status'] in {'needs_source','no_candidates','unknown_topic'} for v in values):kind='clarify'
        refs=[e['ref'] for v in values for e in v.get('evidence',[])]
        return reply(render_text(state),kind,refs)
