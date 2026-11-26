"""Real HTTP regression: current operations must not become old-problem lessons."""
import http.cookiejar
import json
import re
import threading
import urllib.request
import urllib.error
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.product import server
from qingqi.storage import Store

root=fixture_root();instance=server(0,root=root)
threading.Thread(target=instance.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{instance.server_port}'
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
def get(path):
    with opener.open(base+path,timeout=70) as r:return json.load(r)
boot=get('/api/bootstrap')
def post(path,body):
    request=urllib.request.Request(base+path,data=json.dumps(body).encode(),headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
    try:
        with opener.open(request,timeout=90) as r:return json.load(r)
    except urllib.error.HTTPError as error:
        print('HTTP diagnostic',error.code,error.read().decode(),flush=True)
        raise
def teach(session,q,rid):return post('/api/teach',{'session':session,'request':{'question':q,'request_id':rid}})['response']
checks=[]
def check(name,value):
    assert value,name
    checks.append({'name':name,'passed':True});print(json.dumps(checks[-1]),flush=True)
owner=Store(root)
try:
    source=next(e for e in owner.catalogue.bank.values() if 'sqrt' in e['expression'] and 'b+2' in e['expression'].replace(' ','') and e.get('grade')==owner.catalogue.initial['grade'])
    assignment=post('/api/practice/start',{'item_id':source['id'],'request_id':'task-source'})
    teach(assignment['session'],'请用情景故事解释这道题，不给最终答案。','task-story')
    before=get('/api/learning')['summary']
    r=teach(assignment['session'],'给出推荐一个类似的题目','task-recommend-one')
    tasks=r.get('student_tasks',[])
    check('exact_reported_request_returns_one_real_question',len(tasks)==1 and tasks[0]['kind']=='recommend' and len(tasks[0]['items'])==1)
    check('recommendation_is_not_an_inherited_lesson',r['teaching_action']=='recommend' and not r.get('visuals') and '情景教学' not in r['text'] and '分别列出' not in r['text'])
    first=tasks[0]['items'][0]
    check('source_question_and_answer_are_not_returned',first['id']!=source['id'] and all(k not in first for k in ('key','answer','analysis')))
    check('recommendation_matches_knowledge_and_grade',bool(set(owner.catalogue.item(first['id']).get('topics',[first['topic']])) & set(source.get('topics',[source['topic']]))) and owner.catalogue.item(first['id'])['grade']==source['grade'])
    check('recommendation_does_not_claim_learning_progress',{k:v for k,v in get('/api/learning')['summary'].items() if k!='turns'}=={k:v for k,v in before.items() if k!='turns'})
    replay=teach(assignment['session'],'给出推荐一个类似的题目','task-recommend-one')
    check('same_request_replays_the_same_slate',replay['student_tasks']==tasks and replay['cache_hit'])
    more=teach(assignment['session'],'不要讲解，再推荐三道类似的题目。','task-recommend-three')
    items=more['student_tasks'][0]['items']
    check('three_means_three_distinct_question_cards',len(items)==3 and len({i['id'] for i in items})==3)
    check('repeat_recommendation_rotates_recent_exposure',first['id'] not in {i['id'] for i in items})
    profile=teach(assignment['session'],'帮我看看学情，暂时不讲这道题。','task-dashboard')
    check('dashboard_request_reads_real_evidence',profile['student_tasks'][0]['kind']=='learning_dashboard' and not profile.get('visuals') and profile['student_tasks'][0]['summary']['attempts']==before['attempts'])
    path=teach(assignment['session'],'给我看看现在的学习路径。','task-path')
    check('path_request_returns_current_learning_plan',path['student_tasks'][0]['kind']=='learning_path' and bool(path['student_tasks'][0]['path']['steps']) and not path.get('visuals'))
    back=teach(assignment['session'],'回到原题，给我一点提示。','task-back')
    check('read_only_tasks_do_not_replace_the_original_problem',back['teaching_action'] in ('ask','explain') and not back.get('student_tasks'))
    selected=teach(assignment['session'],'刚才推荐的第一题，给我一点提示。','task-select')
    state=json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(selected['run_id'],)).fetchone()[0])
    check('explicit_recommendation_reference_selects_the_correct_item',state['practice_entry']['id']==items[0]['id'])
    check('selection_keeps_the_same_conversation',owner.practice_assignment('edu-math-student',state['practice_assignment_id'])['session']==assignment['session'])
    check('selected_question_does_not_inherit_the_old_story',state.get('presentation',{}).get('kind')!='story')
    empty=post('/api/sessions',{})['id']
    clarify=teach(empty,'给我推荐一个类似的题目','task-missing-source')
    check('missing_reference_is_clarified_not_invented',clarify['teaching_action']=='clarify' and not clarify['student_tasks'][0]['items'] and not clarify.get('visuals'))
    no_supply=post('/api/teach',{'session':empty,'request':{'request_id':'task-no-supply','question':'给我推荐一道同类题目，不用讲解。','expression':'拓扑空间的同伦群'}})['response']
    check('unmatched_source_does_not_generate_unrelated_questions',no_supply['teaching_action']=='clarify' and no_supply['student_tasks'][0]['status']=='no_candidates' and not no_supply['student_tasks'][0]['items'] and not no_supply.get('visuals'))
    from qingqi.student_tasks import inspect_request
    from qingqi.contracts import Request
    for q in ['不用推荐题目，请解释这一步。','“推荐类似题”是什么意思？','已知老师推荐了三道题，求总用时。']:
        check('quoted_or_denied_recommendation_is_not_a_command_'+str(len(checks)),not inspect_request(Request('probe',q))['actions'])
    check('english_request_is_an_operation',inspect_request(Request('english','Recommend one similar exercise'))['actions'][0]['kind']=='recommend')
    check('english_denial_is_not_an_operation',not inspect_request(Request('english-deny',"Do not recommend any exercises; explain this step."))['actions'])
    for q in ['可以出一道同类型的练习吗？','再来一个差不多的题目','给我推荐三道同知识点的题']:
        check('natural_recommendation_variant_'+str(len(checks)),inspect_request(Request('variant',q))['only_queries'])
    check('explicit_new_task_remains_a_boundary',not inspect_request(Request('new-boundary','换一道新题'))['actions'])
    check('explicit_learning_evidence_still_uses_diagnosis',not inspect_request(Request('evidence','分析学情',history=[{'kind':'self_report','text':'经常漏步骤'}]))['actions'])
    indirect=teach(assignment['session'],'现在练什么比较合适','task-indirect')
    check('indirect_operation_uses_existing_router_and_returns_actual_questions',indirect['teaching_action']=='recommend' and bool(indirect['student_tasks'][0]['items']) and not indirect.get('visuals'))
    compound=teach(assignment['session'],'先讲一下这道题的思路，不给答案，然后推荐一个类似的题目。','task-compound')
    check('compound_request_contains_both_teaching_and_real_recommendation',len(compound['student_tasks'][0]['items'])==1 and compound['teaching_action'] not in ('recommend','learning_path','learning_dashboard') and len(compound['text'])>40)
    topic=owner.catalogue.topics[0]
    explicit=teach(assignment['session'],'给我推荐一道关于'+topic['title']+'的题目','task-explicit-topic')
    selected_topics=explicit['student_tasks'][0].get('items',[])
    check('explicit_topic_overrides_old_question_context',all(topic['id'] in owner.catalogue.item(i['id']).get('topics',[i['topic']]) for i in selected_topics))
    from qingqi.agent import Agent, InjectedInterruption
    from qingqi.contracts import Identity,Route
    class UnexpectedLesson:
        name='unexpected_lesson_fixture';uses_model=True
        def next(self,*args):raise AssertionError('a pure recommendation must not call the lesson model')
    class SemanticTaskRouter:
        def route(self,*args):return Route(('recommend',),('fixture_semantic_classifier',),method='schema_fixture')
    direct=Agent(root,Path(owner.catalogue.config['path']),controller=UnexpectedLesson(),router=SemanticTaskRouter())
    identity=Identity('edu-'+boot['profile'],assignment['session'])
    try:
        semantic=direct.run(identity,Request('task-semantic','现在练什么比较合适'))
        check('schema_classification_before_binding_can_route_indirect_requests',semantic['student_tasks'][0]['kind']=='recommend' and not semantic.get('visuals'))
        request=Request('task-interrupted','再推荐一个类似的题目')
        try:direct.run(identity,request,interrupt_after_tool='recommend_practice')
        except InjectedInterruption:pass
        else:raise AssertionError('failpoint was not reached')
        count=owner.db.execute("SELECT COUNT(*) FROM practice_events WHERE kind='chat_recommendations'").fetchone()[0]
        resumed=direct.run(identity,request)
        replayed=direct.run(identity,request)
        check('durable_result_resumes_without_lesson_or_duplicate_exposure',replayed['cache_hit'] and resumed['student_tasks']==replayed['student_tasks'] and owner.db.execute("SELECT COUNT(*) FROM practice_events WHERE kind='chat_recommendations'").fetchone()[0]==count+1)
        check('native_tool_and_skill_are_observed',resumed['tool_calls']==1 and 'student-recommendation' in json.loads(owner.db.execute('SELECT state FROM runs WHERE id=?',(resumed['run_id'],)).fetchone()[0])['skill_hashes'])
    finally:direct.close()
    teach(assignment['session'],'换一道新题','task-clear-boundary')
    cleared=teach(assignment['session'],'推荐一道类似的题目','task-after-boundary')
    check('explicit_new_task_does_not_resurrect_old_recommendation_sources',cleared['teaching_action']=='clarify' and cleared['student_tasks'][0]['status']=='needs_source')
finally:owner.close();instance.shutdown();instance.server_close()
Path('education/.local/reports/current-task-acceptance.local.json').write_text(json.dumps({'checks':checks,'passed':len(checks),'real_http':True},ensure_ascii=False,indent=2),encoding='utf-8')
