"""Repeatable HTTP route-quality audit over real mounted mathematics data."""
import http.cookiejar
import json
import re
import threading
import time
import urllib.request
from collections import Counter
from fractions import Fraction
from pathlib import Path
from student_data_acceptance import fixture_root
from qingqi.catalogue import Catalogue, complete_item
from qingqi.product import server


def run():
    root = fixture_root()
    catalogue = Catalogue(root)
    instance = server(0, root=root)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{instance.server_port}'
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    results, samples = [], []

    def get(path):
        with opener.open(base + path, timeout=40) as response:
            return json.load(response)

    boot = get('/api/bootstrap')

    def post(path, body):
        request = urllib.request.Request(base + path, data=json.dumps(body).encode(), headers={'Origin': base, 'Content-Type': 'application/json', 'X-Qingqi-CSRF': boot['csrf']})
        with opener.open(request, timeout=40) as response:
            return json.load(response)

    def check(name, condition):
        result = {'name': name, 'passed': bool(condition)}
        results.append(result)
        print(json.dumps(result), flush=True)

    try:
        initial = get('/api/learning')
        status = {p['id']: p for p in initial['topics']}
        available = {e['topic'] for e in catalogue.bank.values() if e.get('grade') == '7' and complete_item(e)}
        gap_titles = {'有理数的加法法则', '有理数的减法法则'}
        generated = [e for e in catalogue.bank.values() if e['id'].startswith('generated:')]
        check('empty_usable_addition_and_subtraction_supply_filled', Counter(e['title'] for e in generated) == Counter({title: 48 for title in gap_titles}))
        exact = True
        for e in generated:
            stem = e['expression']
            if e['form'] == '求缺项':
                match = re.search(r'(-?\d+)([+-])x=(-?\d+)', stem)
                a, total = Fraction(match[1]), Fraction(match[3])
                expected = total - a if match[2] == '+' else a - total
            elif e['form'] == '情境应用':
                a, b = [Fraction(n) for n in re.findall(r'\$(-?\d+)\$', stem)]
                expected = a + b if e['title'] == '有理数的加法法则' else a - b
            else:
                a, op, b = re.search(r'\((-?\d+)\)([+-])\((-?\d+)\)', stem).groups()
                expected = Fraction(a) + Fraction(b) if op == '+' else Fraction(a) - Fraction(b)
            actual = e['options'][ord(e['key']['values'][0]) - 65] if e['answer_kind'] == 'choice' else e['key']['values'][0]
            exact &= Fraction(actual) == expected and complete_item(e) and e['source'] == '系统基础变式（数值规则核验）'
        check('all_generated_answers_independently_checked_and_source_labelled', exact and len({e['id'] for e in generated}) == len(generated) and all(len({e['form'] for e in generated if e['title'] == title}) == 4 for title in gap_titles))

        def ordered(route):
            sequence = [s['topic'] for s in route['steps']]
            for i, node in enumerate(sequence):
                for predecessor in status[node]['requires']:
                    if predecessor in sequence and sequence.index(predecessor) > i:
                        return False
            return True

        goals = sorted(available)
        for goal in goals:
            lengths = []
            for minutes in (10, 25, 45):
                post('/api/learning/goal', {'topic': goal, 'minutes': minutes})
                view = get('/api/learning')
                plan = view['path']
                routes = plan['routes']
                cap = min(5, max(3, minutes // 5))
                check(f'{goal}_{minutes}_target_edges_order_and_budget', all(goal in [s['topic'] for s in r['steps']] and 1 <= len(r['steps']) <= cap and ordered(r) and len(r['edges']) == len(r['steps']) - 1 and all(e['label'] and e['source'] == r['steps'][i]['topic'] and e['target'] == r['steps'][i+1]['topic'] for i, e in enumerate(r['edges'])) for r in routes) and plan['today_minutes'] <= minutes)
                check(f'{goal}_{minutes}_routes_are_substantively_distinct', len({frozenset(s['topic'] for s in r['steps']) for r in routes}) == len(routes))
                # 单题/两题知识点真实存在，不用全库无关题填满；报告须明确供给限制。
                usable_count = sum(complete_item(e) and e.get('grade') == '7' and e['topic'] in plan['related_topics'] and e['id'] not in catalogue.initial['historical_items'] for e in catalogue.bank.values())
                expected = min(3, usable_count)
                check(f'{goal}_{minutes}_recommendations_stay_related', len(view['recommendations']) == expected and all(e['topic'] in plan['related_topics'] and catalogue.item(e['id'])['grade'] == '7' and 'key' not in e for e in view['recommendations']) and (not expected or view['recommendations'][0]['topic'] == plan['focus']) and (expected == 3 or '目标关联范围' in view['recommendation_info']['message']))
                lengths.append(max(len(r['steps']) for r in routes))
                if status[goal]['title'] in gap_titles:
                    check(f'{goal}_{minutes}_no_square_root_detour', all('平方根' not in s['title'] for r in routes for s in r['steps']))
                    samples.append({'goal': status[goal]['title'], 'minutes': minutes, 'routes': [{'title': r['title'], 'steps': [s['title'] for s in r['steps']]} for r in routes]})
            check(goal + '_longer_budget_keeps_or_expands_horizon', lengths == sorted(lengths))

        from qingqi.learning_branches import branch_plan
        far = next(n for n in available if '几何' in status[n].get('path', '') or '方程' in status[n].get('path', ''))
        target = next(n for n in status if status[n]['title'] == '有理数的加法法则')
        missing = branch_plan(initial['path'], {'topic': target, 'minutes': 15, 'route': 'adaptive'}, initial['topics'], {far}, time.time(), authored=False, bank={})
        check('no_related_supply_keeps_target_without_false_far_route', all([s['topic'] for s in r['steps']] == [target] for r in missing['routes']) and missing['focus'] == target)
        a = {**status[target], 'id': 'cycle-a', 'requires': ['cycle-b']}
        b = {**status[target], 'id': 'cycle-b', 'requires': ['cycle-a']}
        cycle = branch_plan({'focus': 'cycle-a', 'steps': [], 'next_check': 'diagnose'}, {'topic': 'cycle-a', 'minutes': 15}, [a, b], {'cycle-a', 'cycle-b'}, time.time(), authored=False)
        check('cyclic_source_dependency_does_not_become_a_learning_chain', len(cycle['routes']) == 1 and [s['topic'] for s in cycle['steps']] == ['cycle-a'] and cycle['routes'][0]['edges'] == [])

        post('/api/learning/goal', {'topic': target, 'minutes': 25})
        view = get('/api/learning')
        for route in view['path']['routes']:
            post('/api/learning/route', {'route': route['id'], 'request_id': 'audit-' + route['id']})
            chosen = get('/api/learning')
            check('route_' + route['id'] + '_controls_actual_batch', chosen['path']['selected_route'] == route['id'] and chosen['recommendations'][0]['topic'] == chosen['path']['focus'])
            if route['id'] == 'foundation':
                check('foundation_starts_with_available_basic_diagnostic', chosen['recommendations'][0]['level'] == 1 and chosen['path']['focus'] != next(n for n in status if status[n]['title'] == '相反数'))
        post('/api/learning/route', {'route': 'adaptive', 'request_id': 'audit-return'})
        current = get('/api/learning')
        first = current['recommendations'][0]
        assignment = post('/api/practice/start', {'item_id': first['id'], 'request_id': 'audit-start'})
        entry = catalogue.item(first['id'])
        incorrect = ('B' if entry['key']['values'][0] == 'A' else 'A') if entry['answer_kind'] == 'choice' else '999999'
        post('/api/practice/answer', {'assignment_id': assignment['id'], 'request_id': 'audit-wrong', 'answer': incorrect})
        wrong = get('/api/learning')
        focus_step = next(s for s in wrong['path']['steps'] if s['topic'] == wrong['path']['focus'])
        check('wrong_work_changes_checkpoint_and_next_basic_item', wrong['path']['focus'] == first['topic'] and wrong['recommendations'][0]['level'] == 1 and first['id'] != wrong['recommendations'][0]['id'] and '错' in focus_step['checkpoint'])
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join(2)
        catalogue.db.close()
    report = {'passed': sum(r['passed'] for r in results), 'failed': sum(not r['passed'] for r in results), 'goals': len(goals), 'real_model': False, 'scenarios': results, 'samples': samples}
    Path('education/.local/reports/route-quality-acceptance.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report['failed']


if __name__ == '__main__':
    raise SystemExit(bool(run()))
