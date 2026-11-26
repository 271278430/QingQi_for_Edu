"""Read-only diagnosis and retention projections over the single owner's events."""
from datetime import datetime

DAY = 86400
WINDOW_DAYS = 30
INTERVALS = (1, 3, 7, 14, 30)


def unassisted(event):
    # 旧记录没有复测辅助标记，不能把历史重做猜成无辅助证据。
    return event['data'].get('unassisted', event['data']['independent'])


def retention(history, bank, source, now):
    stage, passed, due_at, firsts, last_kind = 0, 0, None, set(), 'none'
    for e in history:
        d = e['data']
        if not d['correct'] or not unassisted(e):
            stage, passed, firsts = 0, 0, set()
            short = e['at'] + DAY
            # 辅助改正不推迟到期复测；答错则先补基础，安排短间隔重新确认。
            due_at = short if not d['correct'] else min(due_at or short, short)
            last_kind = 'wrong' if not d['correct'] else 'assisted'
            continue
        if d['independent']:
            firsts.add(d['item_id'])
        baseline = int(len(firsts) >= 3 and any(bank[i]['level'] >= 2 for i in firsts if i in bank))
        if due_at is None:
            stage = baseline
            due_at = e['at'] + INTERVALS[stage] * DAY
        elif e['at'] >= due_at:
            stage = min(max(stage + 1, baseline), len(INTERVALS) - 1)
            passed += 1
            due_at = e['at'] + INTERVALS[stage] * DAY
        elif baseline > stage:
            stage = baseline
            due_at = e['at'] + INTERVALS[stage] * DAY
        # 未到期的同日刷题不能不断把到期日往后移动。
        last_kind = 'unassisted'
    origin = 'recent_work' if history else 'none'
    if not history and source and source['status'] == '可进阶' and source.get('last_practiced_at'):
        try:
            due_at = datetime.fromisoformat(source['last_practiced_at'].replace('Z', '+00:00')).timestamp() + 3 * DAY
            stage, origin = 1, 'historical_suggestion'
        except (ValueError, TypeError, OverflowError):
            pass
    status = 'none' if due_at is None else 'due' if due_at <= now else 'scheduled'
    reason = ('历史画像仅用于提出复习建议，当前保持情况需新作答确认。' if origin == 'historical_suggestion' else
              '近期作答有误，先补基础，再独立确认。' if last_kind == 'wrong' else
              '辅助完成仍需无提示复测，已到期的计划不会因改正而延后。' if last_kind == 'assisted' else
              f'无辅助到期复测通过 {passed} 次，当前间隔 {INTERVALS[stage]} 天。' if passed else
              '多道变化难度的新题表现稳定，安排三天后的保持确认。' if stage == 1 else
              '一次正确只确认起点，安排次日独立确认。' if due_at is not None else
              '尚无可安排复测的实际作答证据。')
    return {'status': status, 'due_at': due_at, 'interval_days': INTERVALS[stage] if due_at is not None else None,
            'passed_checks': passed, 'source': origin, 'reason': reason}


def topic_evidence(topic, history, bank, source, now):
    history = sorted((e for e in history if e['at'] <= now), key=lambda e: e['at'])
    independent = [e for e in history if e['data']['independent']]
    recent_history = [e for e in history if e['at'] >= now - WINDOW_DAYS * DAY]
    recent = [e for e in recent_history if e['data']['independent']][-5:]
    rate = sum(e['data']['correct'] for e in recent) / len(recent) if recent else None
    # 掌握确认在最近一次错误/辅助完成后重新建立；旧答对不能盖过新的卡点。
    barrier = max((i for i, e in enumerate(recent_history) if not e['data']['correct'] or not unassisted(e)), default=-1)
    suffix = recent_history[barrier + 1:]
    eligible = {id(e) for e in recent}
    successes = {e['data']['item_id'] for e in suffix if id(e) in eligible and e['data']['correct']}
    varied = any(bank[i]['level'] >= 2 for i in successes if i in bank)
    if not history:
        state = 'needs_practice' if source and source['status'] == '待巩固' else 'diagnose'
    elif not recent_history:
        state = 'diagnose'
    elif not recent_history[-1]['data']['correct'] or not successes and any(not e['data']['correct'] for e in recent_history):
        state = 'needs_practice'
    elif len(successes) >= 3 and varied and rate is not None and rate >= .8:
        state = 'steady'
    else:
        state = 'practicing'
    return {**topic, 'attempts': len(history), 'independent_attempts': len(independent),
            'independent_correct': len({e['data']['item_id'] for e in independent if e['data']['correct']}),
            'recent_independent_attempts': len(recent), 'recent_independent_correct': len(successes), 'evidence_days': WINDOW_DAYS,
            'accuracy': round(rate * 100) if rate is not None else None, 'state': state,
            'last_at': history[-1]['at'] if history else None, 'review': retention(history, bank, source, now),
            **({'initial': {k: source[k] for k in ('mastery', 'confidence', 'practice_count', 'accuracy', 'status', 'last_practiced_at')}} if source else {})}


def review_overview(profiles):
    due = [p for p in profiles if p['review']['status'] == 'due']
    upcoming = [p['review']['due_at'] for p in profiles if p['review']['status'] == 'scheduled']
    return {'due_count': len(due), 'recent_due_count': sum(p['review']['source'] == 'recent_work' for p in due),
            'historical_due_count': sum(p['review']['source'] == 'historical_suggestion' for p in due),
            'next_at': min(upcoming) if upcoming else None}


def tutor_context(view, entry):
    from .teaching_goals import concepts
    matched = next((p for p in view['topics'] if entry and p['id'] == entry.get('topic')), None)
    names=concepts((entry or {}).get('expression','')+' '+(entry or {}).get('title',''))
    related=[p for p in view['topics'] if any(name in p['title'] for name in names)][:3]
    return {'source': 'readonly_learning_snapshot', 'matched_problem': matched is not None,
            'current_topic': {k: matched[k] for k in ('title', 'state', 'recent_independent_attempts', 'recent_independent_correct', 'accuracy', 'evidence_days', 'review')} if matched else None,
            'related_topics':[{k:p[k] for k in ('title','state','recent_independent_attempts','accuracy')} for p in related],
            'rule': '只按相关知识点的实际表现调整帮助。没有新证据时标为未知，概念问题仍可解释。历史估计与模型回复不是掌握事实。',
            'help_strategy': '先定位当前错因，给一小步提示；仍不理解时解释这一步或给相似小例子，再邀请独立尝试。' if matched and matched['state'] == 'needs_practice' else
                             '先让学生说明这一步的依据；即使历史正确率高，也不能跳过当前题核验。'}
