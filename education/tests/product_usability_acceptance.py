"""Isolated product usability checks over real HTTP, catalogue, Agent and SQLite."""
import http.cookiejar
import json
import threading
import urllib.request
import uuid
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'service/src'))
from student_data_acceptance import fixture_root
from qingqi.storage import Store
from qingqi.product import server

root = fixture_root()
owner = Store(root)
entry = next(e for e in owner.catalogue.bank.values() if '和谐方程' in e['expression'] and '4x-2=x+10' in e['expression'].replace(' ', ''))
instance = server(0, root=root)
thread = threading.Thread(target=instance.serve_forever, daemon=True)
thread.start()
base = f'http://127.0.0.1:{instance.server_port}'
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

def get(path):
    with opener.open(base + path, timeout=45) as r:
        return json.load(r)

boot = get('/api/bootstrap')
def post(path, body):
    request = urllib.request.Request(base + path, data=json.dumps(body).encode(), headers={'Origin': base, 'Content-Type': 'application/json', 'X-Qingqi-CSRF': boot['csrf']})
    with opener.open(request, timeout=45) as r:
        return json.load(r)

results = []
def check(name, condition):
    assert condition, name
    results.append({'name': name, 'passed': True})
    print(json.dumps(results[-1]), flush=True)

def teach(session, question, request_id=None):
    return post('/api/teach', {'session': session, 'request': {'request_id': request_id or uuid.uuid4().hex, 'question': question, 'mode': 'auto'}})

try:
    first = post('/api/practice/start', {'item_id': entry['id'], 'request_id': 'begin-1'})
    second = post('/api/practice/start', {'item_id': entry['id'], 'request_id': 'begin-2'})
    check('same_unfinished_item_reuses_assignment_and_conversation', first['id'] == second['id'] and first['session'] == second['session'] and len(get('/api/sessions')['sessions']) == 1)
    check('start_alias_is_idempotent', post('/api/practice/start', {'item_id': entry['id'], 'request_id': 'begin-2'}) == second)
    view = get('/api/session?id=' + first['session'])
    check('bound_question_is_public_without_reference_answer', view['practice']['item']['id'] == entry['id'] and 'key' not in view['practice']['item'] and 'analysis' not in view['practice']['item'])
    ask = teach(first['session'], '这道题请用苏格拉底追问引导我，先不要给最终答案。')
    check('complete_algebra_question_is_guided_without_reasking_for_question', ask['response']['teaching_action'] == 'ask' and '请提供具体问题' not in ask['response']['text'] and '4x' in ask['response']['text'] and '22' not in ask['response']['text'])
    hint = teach(first['session'], '这道题请给我启发式提示，不要告诉我最终答案。')
    check('heuristic_is_specific_and_distinct', hint['response']['text'] != ask['response']['text'] and '移' in hint['response']['text'] and '22' not in hint['response']['text'])
    check('wrong_intermediate_work_is_not_confirmed', teach(first['session'], 'x=5')['response']['teaching_action'] == 'ask')
    correct = teach(first['session'], 'x=4')
    check('correct_intermediate_work_does_not_complete_exercise', correct['response']['teaching_action'] == 'confirm' and get('/api/learning')['summary']['attempts'] == 0)
    check('opposite_root_is_guided_and_checked', teach(first['session'], '另一个方程的解 x=-4')['response']['teaching_action'] == 'confirm')
    answer = teach(first['session'], '我的最终答案是 m=22', 'finish-answer')
    check('final_catalogue_work_updates_same_assisted_learning_evidence', answer['response']['teaching_action'] == 'confirm' and get('/api/learning')['summary']['attempts'] == 1 and get('/api/learning')['summary']['assisted_attempts'] == 1)
    teach(first['session'], '我的最终答案是 m=22', 'finish-answer')
    check('tutoring_replay_does_not_add_grade', get('/api/learning')['summary']['attempts'] == 1)
    check('completed_item_in_cooldown_does_not_create_fresh_conversation', post('/api/practice/start', {'item_id': entry['id'], 'request_id': 'begin-3'})['id'] == first['id'])
    free = post('/api/sessions', {})
    initial = teach(free['id'], '解方程 3x+2=14，请先给我一点提示，不要直接给答案。')
    check('natural_linear_question_gets_guidance', initial['response']['teaching_action'] == 'ask' and '请提供' not in initial['response']['text'])
    check('incorrect_transformation_keeps_original_equation', teach(free['id'], '3x=15')['response']['teaching_action'] != 'confirm')
    check('equivalent_intermediate_equation_is_checked_without_grade', teach(free['id'], '3x=12')['response']['teaching_action'] == 'confirm' and get('/api/learning')['summary']['attempts'] == 1)
    check('free_linear_answer_is_verified_but_not_a_catalogue_grade', teach(free['id'], 'x=4')['response']['teaching_action'] == 'confirm' and get('/api/learning')['summary']['attempts'] == 1)
    check('history_has_meaningful_question_titles', any('和谐' in s['title'] for s in get('/api/sessions')['sessions']))
    memory = owner.db.execute("SELECT text FROM episodes WHERE student='edu-math-student' AND session=? AND kind='student_work'", (first['session'],)).fetchall()
    check('final_work_is_in_memory_once_with_assisted_provenance', len(memory) == 1 and json.loads(memory[0]['text'])['answer'] == '22' and not json.loads(memory[0]['text'])['independent'])
    hint_again = post('/api/practice/hint', {'assignment_id': first['id'], 'style': 'heuristic', 'request_id': 'hint-again'})
    check('practice_hint_uses_actual_question', '4x' in hint_again['text'])
    cancelled = teach(first['session'], '取消')
    cancelled_state = json.loads(owner.db.execute('SELECT state FROM runs WHERE session=? ORDER BY id DESC LIMIT 1', (first['session'],)).fetchone()['state'])
    check('cancel_command_is_not_overwritten_by_question_scaffold', cancelled_state['route']['command'] == 'cancel' and cancelled['response']['teaching_action'] != 'confirm')
    teach(first['session'], '你能做什么')
    detached = teach(first['session'], 'x=4')
    check('cancel_persists_after_other_commands', detached['response']['teaching_action'] != 'confirm')
    back = teach(first['session'], '返回原练习，先给我提示')
    check('explicit_return_rebinds_original_question', '4x' in back['response']['text'])
    check('malformed_fraction_does_not_crash_or_confirm', teach(first['session'], 'x=1/0')['response']['teaching_action'] != 'confirm')
    teach(first['session'], 'x=4')
    with owner.db:
        owner.db.execute('UPDATE dialogue_state SET updated=0 WHERE session=?', (first['session'],))
    restarted = teach(first['session'], 'x=4')
    check('expired_stage_restarts_without_losing_owned_question', restarted['response']['teaching_action'] == 'confirm' and '相反数' in restarted['response']['text'])
    check('bare_numeric_reply_advances_current_question', teach(first['session'], '-4')['response']['teaching_action'] == 'confirm')
    isolated = post('/api/sessions', {})
    check('another_conversation_cannot_borrow_practice_context', teach(isolated['id'], 'x=4')['response']['teaching_action'] != 'confirm')
    for index, unsupported in enumerate(['解方程 x*x=4，请提示', '解方程 x+y=4，请提示', '解方程 x/0=4，请提示', '如果 x+2=4 且 x 是负数，求面积', '解方程 ' + '1+'*90 + 'x=4']):
        session = post('/api/sessions', {})
        check('unsupported_or_partial_equation_abstains_' + str(index), teach(session['id'], unsupported)['response']['teaching_action'] != 'confirm')
    choice = next(e for e in owner.catalogue.bank.values() if e['grade'] == '7' and e['answer_kind'] == 'choice' and e.get('options') and not e.get('missing_context'))
    assignment = post('/api/practice/start', {'item_id': choice['id'], 'request_id': 'choice-begin'})
    check('choice_question_is_guided_from_owned_stem', teach(assignment['session'], '请引导我完成这道题')['response']['teaching_action'] == 'ask')
    selected = teach(assignment['session'], choice['key']['values'][0])
    check('choice_answer_updates_learning_through_dialogue', selected['response']['teaching_action'] == 'confirm' and get('/api/learning')['summary']['attempts'] == 2)
finally:
    instance.shutdown()
    instance.server_close()
    thread.join(2)
    owner.close()

Path('education/.local/reports/product-usability-acceptance.json').write_text(json.dumps({'passed': len(results), 'scenarios': results, 'remote_inference': False}, ensure_ascii=False, indent=2), encoding='utf-8')
