"""End-to-end routing behavior with independent expectations and real tools."""
import json
import time
import uuid

import pytest

from qingqi.agent import Agent, PROJECT, InjectedInterruption
from qingqi.contracts import ContractError, Identity, Request
from qingqi.layered_routing import AhoCorasick, LayeredRouter, validate_dag


@pytest.fixture
def agent():
    a=Agent(PROJECT/'runs/routing_tests'/uuid.uuid4().hex,PROJECT/'data/curriculum.sqlite')
    yield a
    a.close()


def run(agent, question, *, student='a', session='s', **fields):
    return agent.run(Identity(student,session),Request.parse({'request_id':uuid.uuid4().hex,'question':question,**fields}))


@pytest.mark.parametrize('question,action,mode',[
    ('请直接告诉我 2+3*4 的答案','give_answer','answer'),
    ('2+3*4 怎么做？请从头讲解','explain','explain'),
    ('请算 2+3*4，先不要直接给答案，只给一个提示','ask','socratic'),
    ('别再追问了，直接核对 2+3*4 的结果','give_answer','answer'),
])
def test_automatic_mode_and_inline_numeric_question(agent,question,action,mode):
    r=run(agent,question)
    assert r['teaching_action']==action
    assert r['teaching_decision']['mode']==mode
    assert r['teaching_decision']['requested_mode']=='auto'
    if mode=='socratic':
        assert '14' not in r['text']
    else:
        assert '14' in r['text']
    assert len(r['route']['layers'])==6


def test_correct_work_preempts_unnecessary_correction(agent):
    r=run(agent,'检查这题并从头讲解',expression='2+3*4',steps=[{'equation':'2+3*4=14'}])
    assert r['teaching_action']=='confirm'
    assert r['teaching_decision']['display_mode']=='confirm'


def test_repeated_struggle_uses_verified_work_and_changes_help(agent):
    first=run(agent,'检查作答，给一个提示',expression='2+3*4',steps=[{'equation':'2+3*4=20'}])
    second=run(agent,'我还是不会')
    assert first['teaching_action']=='ask'
    assert second['teaching_action']=='explain'
    # 自动升级讲解只解释卡点，不能把“还是不会”当作授权公布最终答案。
    assert second['step_refs']==[0] and '14' not in second['text']
    assert second['teaching_decision']['automatic_scaffold']
    assert not second['teaching_decision']['allow_final_answer']
    assert second['teaching_decision']['evidence'][0]['run_id']==first['run_id']
    assert second['route']['continuity']=='continuation'
    assert '3 × 4 = 12' in second['text'] and '最后一步先留给你来算' in second['text']


@pytest.mark.parametrize('student,session',[('b','s'),('a','other')])
def test_reference_does_not_bind_other_student_or_session(agent,student,session):
    run(agent,'提示我',expression='2+3*4',steps=[{'equation':'2+3*4=20'}])
    r=run(agent,'我还是不会',student=student,session=session)
    assert r['teaching_action']=='clarify' and r['tool_calls']==0


def test_expired_task_is_not_reused(agent):
    run(agent,'提示我',expression='2+3*4',steps=[{'equation':'2+3*4=20'}])
    with agent.store.db:
        agent.store.db.execute('UPDATE dialogue_state SET updated=?',(time.time()-1900,))
    r=run(agent,'我还是不会')
    assert r['teaching_action']=='clarify' and r['tool_calls']==0
    assert r['route']['layers'][2]['expired']


def test_pending_course_name_reply_is_verified_in_graph(agent):
    initial=run(agent,'帮我查询教材章节')
    assert initial['teaching_action']=='clarify'
    reply=run(agent,'一氧化碳')
    assert reply['tool_calls']==2 and '碳的氧化物' in reply['text']
    assert reply['route']['continuity']=='continuation'
    assert agent.store.dialogue(Identity('a','s'))['verified_work']['node_id']


def test_pending_numeric_question_accepts_slot_then_starts_review(agent):
    assert run(agent,'请检查我的作答')['teaching_action']=='clarify'
    r=run(agent,'2+3*4')
    assert r['tool_calls']==1 and r['teaching_action']=='ask'


def test_graph_pronoun_binds_only_verified_same_session_node(agent):
    initial=run(agent,'查询教材章节',course_query='一氧化碳',subject='化学')
    follow=run(agent,'那个知识点有哪些先修关系？')
    assert follow['route']['continuity']=='continuation'
    assert '一氧化碳' in follow['text'] and follow['tool_calls']==2
    binding=follow['route']['layers'][2]['bindings'][0]
    assert binding['source']=='verified_same_session_graph_reference'
    assert binding['run_id']==initial['run_id'] and binding['node_id']


def test_new_task_does_not_reuse_previous_problem(agent):
    run(agent,'提示我',expression='2+3*4',steps=[{'equation':'2+3*4=20'}])
    r=run(agent,'换一道题，请从头讲解')
    assert r['teaching_action']=='clarify' and r['tool_calls']==0


def test_cancellation_is_exact_whitelist_and_clears_state(agent):
    run(agent,'提示我',expression='2+3*4',steps=[{'equation':'2+3*4=20'}])
    r=run(agent,'取消当前任务')
    assert r['route']['command']=='cancel' and r['tool_calls']==0
    assert agent.store.dialogue(Identity('a','s'))['verified_work'] is None
    assert run(agent,'取消当前任务这个词是什么意思')['route']['command']==''


def test_chat_does_not_call_old_coursework_tools(agent):
    run(agent,'提示我',expression='2+3*4',steps=[{'equation':'2+3*4=20'}])
    r=run(agent,'今天有点累，想聊聊天')
    assert r['teaching_action']=='chat' and r['tool_calls']==0
    assert r['teaching_decision']['display_mode']=='chat'


def test_manual_preference_remains_optional_but_no_answer_request_is_honored(agent):
    r=run(agent,'不要给答案，请只提示',expression='2+3*4',mode='answer')
    assert r['teaching_action']=='ask' and '14' not in r['text']
    r=run(agent,'请检查作答',expression='2+3*4',mode='explain')
    assert r['teaching_action']=='explain'


def test_stepwise_explanation_can_keep_final_answer_hidden(agent):
    r=run(agent,'分步讲解这道题，但不要给答案',expression='2+3*4')
    assert r['teaching_action']=='explain'
    assert '12' in r['text'] and '14' not in r['text']


def test_routing_decision_and_reused_input_are_durable(agent):
    q=Request.parse({'request_id':'resume-auto','question':'直接核对 2+3*4 的答案'})
    with pytest.raises(InjectedInterruption):
        agent.run(Identity('a','s'),q,interrupt_after_tool=True)
    r=agent.run(Identity('a','s'),q)
    assert r['teaching_action']=='give_answer'
    assert agent.store.db.execute('SELECT attempts FROM calls').fetchone()[0]==1
    assert agent.run(Identity('a','s'),q)['cache_hit']


def test_whitelisted_task_and_unsupported_export_are_not_confused(agent):
    r=run(agent,'查询教材章节；把结果导出到邮箱',course_query='一氧化碳',subject='化学')
    assert r['tool_calls']==2 and '碳的氧化物' in r['text']
    assert '没有执行' in r['text'] and r['route']['unresolved_clauses']


@pytest.mark.parametrize('nodes',[
    [{'id':'a','intent':'review','depends_on':['b'],'requires_confirmation':False},{'id':'b','intent':'diagnosis','depends_on':['a'],'requires_confirmation':False}],
    [{'id':'a','intent':'review','depends_on':['missing'],'requires_confirmation':False}],
    [{'id':'a','intent':'export','depends_on':[],'requires_confirmation':False}],
    [{'id':'a','intent':'review','depends_on':[],'requires_confirmation':True}],
])
def test_invalid_or_unregistered_dag_rejected(nodes):
    with pytest.raises(ContractError):
        validate_dag({'nodes':nodes})


def test_ac_matches_signals_but_whitelist_requires_whole_command():
    matcher=AhoCorasick(['课标','教材','取消'])
    assert matcher.matches('查看教材课标')==['教材','课标']
    route=LayeredRouter().route(Request.parse({'request_id':'x','question':'不要取消我的任务'}))
    assert not route.command


class FallbackFixture:
    def __init__(self, intent='chat'):
        self.calls=[]
        self.intent=intent
    def generate(self, system, payload, schema):
        self.calls.append(payload)
        return {'nodes':[{'id':'fallback','intent':self.intent,'depends_on':[],'requires_confirmation':False}]}


def test_partial_fallback_receives_only_unknown_clause():
    fixture=FallbackFixture()
    q=Request.parse({'request_id':'partial','question':'查询教材章节；帮我和一只火星猫交谈','course_query':'一氧化碳'})
    route=LayeredRouter(fallback=fixture).route(q)
    assert fixture.calls[0]['clauses']==['帮我和一只火星猫交谈']
    assert set(route.intents)=={'course','chat'}
    assert route.layers[-1]['model_called']


def test_fallback_cannot_invent_problem_or_execute_export():
    fixture=FallbackFixture('review')
    route=LayeredRouter(fallback=fixture).route(Request.parse({'request_id':'x','question':'火星猫宇宙泡泡'}))
    assert route.intents==('clarify',) and route.clarify
    fixture=FallbackFixture()
    route=LayeredRouter(fallback=fixture).route(Request.parse({'request_id':'x','question':'查询教材；导出到邮箱','course_query':'一氧化碳'}))
    assert fixture.calls==[] and route.unresolved_clauses
