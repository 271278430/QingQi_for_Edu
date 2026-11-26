"""Isolated HTTP / SQLite checks of recent diagnosis and retention scheduling."""
import http.cookiejar
import json
import threading
import time
import urllib.request
import uuid
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'service/src'))
from qingqi.agent import PROJECT
from qingqi.domain_tools import number
from qingqi.product import server
from qingqi.storage import Store


def run():
    root = PROJECT / 'runs/learning-evidence-acceptance' / uuid.uuid4().hex
    instance = server(0, root=root)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{instance.server_port}'
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def get(path):
        with opener.open(base + path, timeout=40) as response:
            return json.load(response)

    boot = get('/api/bootstrap')

    def post(path, body):
        req = urllib.request.Request(base + path, data=json.dumps(body).encode(), headers={'Origin': base, 'Content-Type': 'application/json', 'X-Qingqi-CSRF': boot['csrf']})
        with opener.open(req, timeout=40) as response:
            return json.load(response)

    owner = Store(root)
    student = 'demo-student-a'
    results = []
    t = time.time()

    def check(name, condition):
        results.append({'name': name, 'passed': bool(condition)})
        print(json.dumps(results[-1]), flush=True)

    def view(at=t):
        return owner._learning_snapshot(student, now=at)

    def profile(at=t):
        return next(p for p in view(at)['topics'] if p['id'] == 'order')

    def answer(item_id, value=None, at=t, hint=False):
        assignment = post('/api/practice/start', {'item_id': item_id, 'request_id': uuid.uuid4().hex})
        if hint:
            post('/api/practice/hint', {'assignment_id': assignment['id'], 'request_id': uuid.uuid4().hex, 'style': 'heuristic'})
        request_id = uuid.uuid4().hex
        entry = owner.catalogue.item(item_id)
        payload = {'assignment_id': assignment['id'], 'request_id': request_id, 'answer': str(number(entry['expression'])) if value is None else value}
        feedback = post('/api/practice/answer', payload)
        with owner.db:
            owner.db.execute('UPDATE practice_events SET at=? WHERE student=? AND request_id=?', (at, student, request_id))
        return feedback, payload

    try:
        # 上游演示身份的映射从 bootstrap 读取，不依赖 UI 自传 student 字段。
        student = 'edu-' + boot['profile']
        post('/api/learning/goal', {'topic': 'order', 'minutes': 20})
        answer('order-1', at=t - 20)
        one = profile()
        check('one_new_success_confirms_start_without_mastery', one['state'] == 'practicing')
        answer('order-2', at=t - 10)
        answer('order-4', at=t)
        stable = profile()
        check('three_different_recent_items_with_varied_level_are_steady', stable['state'] == 'steady')
        check('old_successes_expire_instead_of_claiming_current_mastery', profile(t + 31 * 86400)['state'] == 'diagnose')
        review = stable.get('review', {})
        check('stable_diagnostic_uses_three_day_review', review.get('interval_days') == 3 and review.get('status') == 'scheduled')
        check('review_becomes_due_without_new_score', profile(t + 4 * 86400).get('review', {}).get('status') == 'due' and view(t + 4 * 86400)['summary']['attempts'] == 3)
        answer('order-5', at=t + 3600)
        check('same_day_drilling_does_not_postpone_review', profile(t + 3600).get('review', {}).get('due_at') == review.get('due_at') and review.get('due_at') is not None)
        answer('order-6', at=t + 4 * 86400)
        spaced = profile(t + 4 * 86400).get('review', {})
        check('due_unassisted_correct_extends_to_seven_days', spaced.get('interval_days') == 7 and spaced.get('passed_checks') == 1)
        wrong, retry = answer('order-7', '999999', at=t + 5 * 86400)
        check('wrong_resets_mastery_and_retention_interval', profile(t + 5 * 86400)['state'] == 'needs_practice' and profile(t + 5 * 86400).get('review', {}).get('interval_days') == 1)
        # 同 assignment 错后改正不能利用旧成功恢复稳定或延长到期保持。
        correct = str(number(owner.catalogue.item('order-7')['expression']))
        fixed = post('/api/practice/answer', {**retry, 'request_id': 'retry-correct', 'answer': correct})
        with owner.db:
            owner.db.execute('UPDATE practice_events SET at=? WHERE student=? AND request_id=?', (t + 7 * 86400, student, 'retry-correct'))
        recovered = profile(t + 7 * 86400)
        check('retry_is_not_unassisted_or_a_first_success', fixed.get('unassisted') is False and not fixed['independent'])
        check('old_successes_cannot_restore_steady_after_assisted_correction', recovered['state'] == 'needs_practice')
        check('assisted_correction_does_not_postpone_overdue_review', recovered.get('review', {}).get('status') == 'due' and recovered.get('review', {}).get('passed_checks') == 0)
        check('original_request_replay_does_not_add_evidence', post('/api/practice/answer', {**retry, 'request_id': 'retry-correct', 'answer': correct}) == fixed and view(t + 7 * 86400)['summary']['attempts'] == 7)
        check('another_student_has_no_retention_or_grades', owner._learning_snapshot('isolated-student', now=t + 7 * 86400)['summary']['attempts'] == 0 and all(p.get('review', {}).get('due_at') is None for p in owner._learning_snapshot('isolated-student')['topics']))
        before = owner.db.total_changes
        get('/api/learning')
        get('/api/learning')
        check('overview_is_read_only', owner.db.total_changes == before)
        # 复做旧题可以检验保持，但不能增加“首次独立答对”统计。
        with owner.db:
            owner.db.execute('UPDATE practice_assignments SET created=? WHERE student=? AND item_id=?', (t - 4 * 86400, student, 'order-1'))
        first_count = view(t + 7 * 86400)['summary']['independent_correct']
        repeated, _ = answer('order-1', at=t + 10 * 86400)
        check('unassisted_repeat_verifies_retention_without_first_score', repeated.get('unassisted') is True and not repeated['independent'] and view(t + 10 * 86400)['summary']['independent_correct'] == first_count)
        for item_id, at, expected in [('order-8', t + 14 * 86400, 7), ('order-9', t + 22 * 86400, 14), ('order-3', t + 37 * 86400, 30)]:
            answer(item_id, at=at)
            check('spaced_check_interval_' + str(expected), profile(at)['review']['interval_days'] == expected)
    finally:
        owner.close()
        instance.shutdown()
        instance.server_close()
        thread.join(2)
    report = {'passed': sum(r['passed'] for r in results), 'failed': sum(not r['passed'] for r in results), 'scenarios': results, 'real_model': False}
    (PROJECT.parent / '.local/reports/learning-evidence-acceptance.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report['failed']


if __name__ == '__main__':
    raise SystemExit(bool(run()))
