"""Isolated HTTP acceptance for evidence-driven paths and diverse three-item batches."""
import http.cookiejar
import json
import sys
import threading
import urllib.request
import uuid
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'service/src'))
from qingqi.agent import PROJECT
from qingqi.product import server
from qingqi.storage import Store
from qingqi.domain_tools import number
from student_data_acceptance import fixture_root

results = []


def check(name, condition):
    assert condition, name
    results.append({'name': name, 'passed': True})
    print(json.dumps(results[-1]), flush=True)


class Client:
    def __init__(self, root):
        self.root = root
        self.instance = server(0, root=root)
        self.thread = threading.Thread(target=self.instance.serve_forever, daemon=True)
        self.thread.start()
        self.base = f'http://127.0.0.1:{self.instance.server_port}'
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.boot = self.get('/api/bootstrap')

    def get(self, path):
        with self.opener.open(self.base + path, timeout=40) as response:
            return json.load(response)

    def post(self, path, body):
        request = urllib.request.Request(self.base + path, data=json.dumps(body).encode(), headers={'Origin': self.base, 'Content-Type': 'application/json', 'X-Qingqi-CSRF': self.boot['csrf']})
        with self.opener.open(request, timeout=40) as response:
            return json.load(response)

    def answer(self, item, answer, hint=False):
        assignment = self.post('/api/practice/start', {'item_id': item['id'], 'request_id': uuid.uuid4().hex})
        if hint:
            self.post('/api/practice/hint', {'assignment_id': assignment['id'], 'request_id': uuid.uuid4().hex, 'style': 'heuristic'})
        return self.post('/api/practice/answer', {'assignment_id': assignment['id'], 'request_id': uuid.uuid4().hex, 'answer': answer})

    def close(self):
        self.instance.shutdown()
        self.instance.server_close()
        self.thread.join(2)


client = Client(PROJECT / 'runs/adaptive-seed' / uuid.uuid4().hex)
try:
    client.post('/api/learning/goal', {'topic': 'fractions', 'minutes': 10})
    view = client.get('/api/learning')
    routes = view['path']['routes']
    check('branch_map_has_distinct_available_chains', len(routes) >= 2 and len({tuple(s['topic'] for s in r['steps']) for r in routes}) == len(routes))
    alternative = next(r for r in routes if r['id'] != 'adaptive')
    choice = {'route': alternative['id'], 'request_id': 'choose-route-fixed'}
    accepted = client.post('/api/learning/route', choice)
    chosen = client.get('/api/learning')
    check('route_choice_changes_actual_three_item_match', chosen['path']['selected_route'] == alternative['id'] and chosen['recommendations'][0]['topic'] == chosen['path']['focus'] and chosen['recommendations'] != view['recommendations'] and len(chosen['recommendations']) == 3)
    check('route_choice_is_idempotent_persistent_and_not_a_grade', accepted == client.post('/api/learning/route', choice) and client.get('/api/learning')['goal']['route'] == alternative['id'] and client.get('/api/learning')['summary']['attempts'] == 0)
    try:
        client.post('/api/learning/route', {**choice, 'route': 'adaptive'})
        raise AssertionError('route conflict accepted')
    except __import__('urllib.error', fromlist=['HTTPError']).HTTPError as error:
        check('route_request_id_conflict_rejected', error.code == 403)
    client.post('/api/learning/route', {'route': 'adaptive', 'request_id': 'restore-adaptive'})
    client.post('/api/learning/route', choice)
    check('old_route_replay_cannot_overwrite_newer_choice', client.get('/api/learning')['path']['selected_route'] == 'adaptive')
    isolated = Store(client.root)
    try:
        check('route_choice_is_student_isolated', isolated._learning_snapshot('another-student')['goal']['route'] == 'adaptive')
    finally:
        isolated.close()
    view = client.get('/api/learning')
    check('three_items_with_distinct_topics_and_explanations', len(view['recommendations']) == 3 and len({i['topic'] for i in view['recommendations']}) == 3 and all(i['reason'] and i['purpose'] and i['kind'] for i in view['recommendations']))
    check('confirmed_prerequisite_and_budget_respected', view['path']['focus'] == 'order' and view['path']['today_minutes'] <= 10 and view['path']['next_check'])
    first = view['recommendations'][0]
    client.answer(first, str(number(first['expression'])))
    advanced = client.get('/api/learning')
    check('one_independent_diagnostic_advances_without_claiming_mastery', advanced['path']['focus'] == 'brackets' and next(t for t in advanced['topics'] if t['id'] == 'order')['state'] != 'steady')
    first = advanced['recommendations'][0]
    client.answer(first, str(number(first['expression'])), hint=True)
    held = client.get('/api/learning')
    check('hinted_success_does_not_skip_prerequisite', held['path']['focus'] == 'brackets' and held['recommendations'][0]['level'] == 1)
    first = held['recommendations'][0]
    client.answer(first, '999999')
    wrong = client.get('/api/learning')
    check('wrong_work_changes_next_foundation_practice', wrong['recommendations'][0]['topic'] == first['topic'] and wrong['recommendations'][0]['level'] == 1 and first['id'] not in {r['id'] for r in wrong['recommendations']})
    before = wrong['summary']['attempts']
    batch_request = {'request_id': 'renew-fixed'}
    batch = client.post('/api/practice/recommendations', batch_request)
    check('new_batch_is_idempotent_and_not_a_grade', batch == client.post('/api/practice/recommendations', batch_request) and client.get('/api/learning')['summary']['attempts'] == before)
    check('get_learning_keeps_current_batch_stable', [r['id'] for r in client.get('/api/learning')['recommendations']] == [r['id'] for r in batch['items']])
    read_ids = {r['id'] for r in batch['items']}
    check('renew_limits_recent_repetition', read_ids != {r['id'] for r in wrong['recommendations']})
finally:
    client.close()

root = fixture_root()
client = Client(root)
catalogue = Store(root)
try:
    initial = client.get('/api/learning')
    batch = initial['recommendations']
    check('real_catalogue_three_topics_same_grade_and_no_keys', len(batch) == 3 and len({i['topic'] for i in batch}) == 3 and all(catalogue.catalogue.item(i['id'])['grade'] == '7' and 'key' not in i and 'analysis' not in i for i in batch))
    check('imported_candidates_do_not_block_goal', initial['path']['focus'] == initial['goal']['topic'] and all(s['state'] != 'waiting' for s in initial['path']['steps']))
    check('real_path_includes_nonblocking_supporting_suggestions', len(initial['path']['steps']) >= 2 and any(s['role'] in {'补强建议', '复习确认', '拓展诊断'} for s in initial['path']['steps']))
    option = next(r for r in initial['path']['routes'] if r['id'] != 'adaptive')
    client.post('/api/learning/route', {'route': option['id'], 'request_id': 'real-route'})
    branch = client.get('/api/learning')
    check('real_data_route_choice_changes_recommendations_without_grade', branch['recommendations'] != initial['recommendations'] and branch['summary']['attempts'] == 0 and branch['recommendations'][0]['topic'] == branch['path']['focus'])
    client.post('/api/learning/goal', {'topic': branch['goal']['topic'], 'minutes': 25})
    check('goal_budget_change_preserves_route_preference', client.get('/api/learning')['goal']['route'] == option['id'])
    from qingqi.learning_branches import branch_plan
    limited = branch_plan(initial['path'], initial['goal'], initial['topics'], {initial['path']['focus']}, time.time(), authored=False)
    check('single_topic_supply_does_not_fabricate_multiple_branches', len(limited['routes']) == 1)
    client.post('/api/learning/route', {'route': 'adaptive', 'request_id': 'real-restore'})
    kinds, topics, ids = set(), set(), set()
    for index in range(5):
        next_batch = client.post('/api/practice/recommendations', {'request_id': f'real-batch-{index}'})['items']
        check(f'real_batch_{index}_has_three_distinct_knowledge_points', len(next_batch) == 3 and len({i['topic'] for i in next_batch}) == 3)
        check(f'real_batch_{index}_mixes_available_question_types', len({i['kind'] for i in next_batch}) >= 2)
        kinds.update(i['kind'] for i in next_batch)
        topics.update(i['topic'] for i in next_batch)
        ids.update(i['id'] for i in next_batch)
    check('several_batches_expand_topics_types_and_items', len(topics) >= 5 and len(kinds) >= 2 and len(ids) >= 9)
    check('recommendation_exposure_keeps_initial_and_new_scores_separate', client.get('/api/learning')['summary']['attempts'] == 0 and client.get('/api/learning')['initial']['n_attempts'] == 89)
    first = client.get('/api/learning')['recommendations'][0]
    entry = catalogue.catalogue.item(first['id'])
    client.answer(first, ';'.join(entry['key']['values']))
    supplied = client.get('/api/learning')
    check('path_focus_matches_recommendation_when_goal_has_no_fresh_supply', supplied['path']['focus'] == supplied['recommendations'][0]['topic'] and any(s['topic'] == supplied['goal']['topic'] for s in supplied['path']['steps']))
    from qingqi.adaptive_learning import eligible_pool
    candidates = eligible_pool(catalogue.catalogue.bank, catalogue.catalogue.initial, [], supplied['active'], time.time())
    counts = {i['topic']: sum(e['topic'] == i['topic'] for e in candidates) for i in candidates}
    fresh_topics = [n for n in counts if not next(p for p in supplied['topics'] if p['id']==n)['attempts'] and counts[n]>=4]
    target = max(fresh_topics or counts, key=counts.get)
    assert counts[target] >= 4
    client.post('/api/learning/goal', {'topic': target, 'minutes': 15})
    for step in range(3):
        live = client.get('/api/learning')
        first = live['recommendations'][0]
        assert first['topic'] == target, {'step': step, 'target': target, 'first': first['topic'], 'path': live['path']}
        entry = catalogue.catalogue.item(first['id'])
        client.answer(first, ';'.join(entry['key']['values']))
    learned = client.get('/api/learning')
    check('stable_real_goal_continues_to_another_learning_need', next(p for p in learned['topics'] if p['id'] == target)['state'] == 'steady' and learned['path']['focus'] != target)
    from qingqi.learning import learning_projection
    events = [{'kind': r['kind'], 'data': json.loads(r['data']), 'at': r['at']} for r in catalogue.db.execute('SELECT kind,data,at FROM practice_events WHERE student=? ORDER BY id', ('edu-math-student',))]
    future = learning_projection(learned['goal'], events, learned['active'], 0, catalogue=catalogue.catalogue, initial=catalogue.catalogue.initial, now=time.time() + 4 * 86400)
    check('time_progression_replans_due_review_instead_of_reusing_stale_batch', future['path']['focus'] == target and '复习' in future['path']['steps'][0]['reason'])
finally:
    catalogue.close()
    client.close()

(PROJECT.parent / '.local/reports/adaptive-learning-acceptance.json').write_text(json.dumps({'passed': len(results), 'scenarios': results, 'remote_inference': False}, ensure_ascii=False, indent=2), encoding='utf-8')
