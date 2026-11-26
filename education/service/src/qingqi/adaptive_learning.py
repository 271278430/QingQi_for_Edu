"""Pure adaptive planning and three-item selection over the owner's snapshot."""
import hashlib
import re
from .contracts import fingerprint
from .catalogue import complete_item

# 难度供给纳入路线重点后，旧推荐快照必须失效，不能继续返回旧的进阶首题。
POLICY = 'curriculum_evidence_v9'


def recent_correct(profile):
    return profile.get('recent_independent_correct', profile['independent_correct'])


def checked(profile):
    # 一次独立诊断只允许继续探索目标，不把它改写成稳定掌握。
    return profile['state'] == 'steady' or (profile['state'] != 'needs_practice' and recent_correct(profile) >= 1 and (profile['accuracy'] or 0) >= 80)


def review_due(profile, now):
    # 复习、路径和看板读取同一事件投影，不能各自用最后作答时间另算到期。
    review = profile.get('review', {})
    return review.get('due_at') is not None and review['due_at'] <= now


def eligible_pool(bank, initial, events, active, now):
    used = {e['data']['item_id']: e for e in events if e['kind'] == 'answer'}
    active_id = active['item']['id'] if active else None
    return [e for e in bank.values() if complete_item(e) and (not initial or e.get('grade') == initial['grade'])
            and e['id'] not in (initial or {}).get('historical_items', []) and e['id'] != active_id
            and (e['id'] not in used or now - used[e['id']]['at'] >= (3 if used[e['id']]['data']['correct'] else 1) * 86400)]


def build_plan(goal, profiles, bank, initial, now, *, authored, available_topics):
    status = {p['id']: p for p in profiles}
    available = available_topics & set(status)
    route, visited = [], set()
    def visit(node, depth=0):
        if node in visited or node not in status or depth > 4 or len(route) >= 7:
            return
        visited.add(node)
        # 未经教研确认的候选关系不能强制学生重复前置内容。
        for previous in (status[node]['requires'][:3] if authored else []):
            visit(previous, depth + 1)
        if len(route) < 7:
            route.append(node)
    visit(goal['topic'])
    if goal['topic'] not in route and goal['topic'] in status:
        route = [*route[:6], goal['topic']]
    focus = next((node for node in route if node in available and not checked(status[node])), goal['topic'])
    goal_group = status.get(goal['topic'], {}).get('path', '').split('/')[0]
    def supporting_rank(node):
        p = status[node]
        need = 0 if p['attempts'] and p['state'] == 'needs_practice' else 1 if p['state'] == 'needs_practice' else 2 if review_due(p, now) else 3 if not checked(p) else 4
        return (p.get('path', '').split('/')[0] != goal_group, need, p.get('initial', {}).get('confidence', 0), node)
    supports = sorted(available - set(route), key=supporting_rank)
    if not authored:
        # 真实图谱只提供建议，目标稳定后才推进到同域的下一处需关注知识。
        if status[goal['topic']]['state'] == 'steady' and supports and not review_due(status[goal['topic']], now):
            focus = supports[0]
        route = list(dict.fromkeys([focus, *route, *supports[:2]]))[:3]
    if focus not in available:
        substitutes = sorted(available, key=supporting_rank)
        if substitutes:
            focus = substitutes[0]
            route = [focus, *[node for node in route if node != focus]][:7]
    steps = []
    for node in route:
        p = status[node]
        quick = checked(p) and p['state'] != 'steady'
        reason = '距离上次练习已有一段时间，安排新题复习确认。' if review_due(p, now) else '多道独立新题表现稳定，后续安排间隔复习。' if p['state'] == 'steady' else '新的独立诊断已确认起点，可以继续目标；仍需更多题型确认掌握。' if quick else '最近实际作答有误，先换一道较低难度变式定位问题。' if p['attempts'] and p['state'] == 'needs_practice' else '提示后完成仍需一题新的独立诊断，先巩固再推进。' if p['attempts'] and not recent_correct(p) else '参考历史画像选择诊断题，用新作答确认当前水平。' if p.get('initial') else '先用一道诊断题确认起点。'
        if node not in available:
            reason += '目前没有可用新题或原题尚在冷却期，保留目标并先练可用的相关知识。'
        steps.append({'topic': node, 'title': p['title'], 'objective': p['objective'], 'state': p['state'] if not authored or node == focus or checked(p) else 'waiting',
                      'role': '当前重点' if node == focus else '起点已确认' if quick else '目标推进' if node == goal['topic'] else '先修准备' if authored else '复习确认' if review_due(p, now) else '补强建议' if p['state'] == 'needs_practice' else '拓展诊断',
                      'reason': reason, 'has_practice': node in available})
    title = status.get(focus, {}).get('title', '当前目标')
    next_check = ('先修独立诊断答对后继续下一节点；提示后完成先换变式。目标节点继续用不同新题确认，多题表现稳定后逐步提升难度。' if authored
                  else '当前重点按独立作答继续巩固；提示后完成先换变式。目标多道新题表现稳定后，继续相关薄弱点并安排间隔复习。')
    return {'focus': focus, 'steps': steps, 'summary': f'本轮先练「{title}」，结合独立诊断、近期错误与复习间隔调整顺序。',
            'next_check': next_check,
            'dependency_source': 'authored_seed_dependencies' if authored else 'mounted_math_graph_unverified_candidates'}


def shape(entry):
    return re.sub(r'\s+', '', re.sub(r'\d+(?:\.\d+)?', '#', entry['expression'])).casefold()[:240]


def kind(entry):
    if entry.get('answer_kind') == 'choice':
        return '选择题'
    if entry.get('answer_count', 1) > 1:
        return '多空数值题'
    if entry.get('form'):
        return str(entry['form'])
    expression = entry['expression']
    if '(' in expression:
        return '括号计算' if not entry.get('grade') else '数值题'
    if entry['topic'] == 'fractions':
        return '分数计算'
    if entry['topic'] == 'signed':
        return '符号运算'
    return '数值题' if entry.get('grade') else '混合运算'


def target_level(profile):
    if profile['state'] == 'steady':
        return 3
    return 2 if recent_correct(profile) >= 2 and profile['state'] != 'needs_practice' else 1


def evidence_key(goal, events, active, version, now):
    return fingerprint({'goal': goal, 'work': [e for e in events if e['kind'] in {'answer', 'hint'}],
                        'active': active['id'] if active else None, 'version': version, 'policy': POLICY, 'day': int((now + 8 * 3600) // 86400)})


def recommend(goal, profiles, bank, initial, events, active, plan, now, version, serialize):
    status = {p['id']: p for p in profiles}
    key = evidence_key(goal, events, active, version, now)
    batches = [e['data'] for e in events if e['kind'] == 'recommendations']
    if batches and batches[-1]['evidence_key'] == key:
        saved = batches[-1]['result']
        return saved['items'], saved['info']
    used = {}
    for e in events:
        if e['kind'] == 'answer':
            used[e['data']['item_id']] = e
    pool = [e for e in eligible_pool(bank, initial, events, active, now) if e['topic'] in status]
    connected = [e for e in pool if e['topic'] in set(plan.get('related_topics', status))]
    # 知识点不足时通过题型与模板补齐；无关联题不能冒充目标练习。
    pool = connected
    seen = [item for batch in batches[-10:] for item in [*batch.get('previous', []), *[r['id'] for r in batch['result']['items']]]]
    recent = [e['data']['item_id'] for e in events if e['kind'] == 'answer'][-12:]
    def group(entry):
        return status[entry['topic']].get('path', '数学基础').split('/')[0]
    def priority(entry):
        p = status[entry['topic']]
        if p['attempts'] and p['state'] == 'needs_practice':
            return 0
        if review_due(p, now):
            return 1
        if p['state'] == 'needs_practice':
            return 2
        return 3 if p['state'] == 'diagnose' else 4 if p['state'] == 'practicing' else 5
    selected = []
    route_topics = {s['topic'] for s in plan['steps']}
    route_id = plan.get('selected_route', 'adaptive')
    for slot in range(min(3, len(pool))):
        candidates = [e for e in pool if e['id'] not in {r['id'] for r in selected}]
        if slot == 0:
            focused = [e for e in candidates if e['topic'] == plan['focus']]
            candidates = focused or candidates
        else:
            different = [e for e in candidates if e['topic'] not in {r['topic'] for r in selected}]
            candidates = different or candidates
            if slot == 1:
                in_route = [e for e in candidates if e['topic'] in route_topics]
                candidates = in_route or candidates
            else:
                # 第三题负责关联迁移；在可接受难度内轮换知识点，避免路线加权锁住三题。
                suitable = [e for e in candidates if abs(e['level'] - (1 if route_id == 'foundation' else target_level(status[e['topic']]))) <= 1]
                candidates = suitable or candidates
        def score(e):
            p = status[e['topic']]
            topic_seen = sum(bank[i]['topic'] == e['topic'] for i in seen if i in bank)
            type_seen = sum(kind(bank[i]) == kind(e) for i in seen[-12:] if i in bank)
            current_topic = sum(bank[i]['topic'] == e['topic'] for i in recent if i in bank)
            family_seen = sum(shape(bank[i]) == shape(e) for i in seen[-12:] if i in bank)
            overlap = sum(len(set(e.get('topics', [e['topic']])) & set(r.get('topics', [r['topic']]))) for r in selected)
            diversity = sum(22 * (group(e) == group(r)) + 15 * (kind(e) == kind(r)) + 25 * (shape(e) == shape(r)) for r in selected)
            # 不只随机换数字：知识点、题型、模板和近期曝光共同惩罚重复。
            level = 1 if route_id == 'foundation' else target_level(p)
            value = abs(e['level'] - level) * 22 + seen.count(e['id']) * 45 + family_seen * 8 + topic_seen * 5 + type_seen * 2 + current_topic * 4
            if e['topic'] not in route_topics and slot != 2:
                value += 70
            value += priority(e) * (12 if slot == 1 else 5) + diversity * (2 if slot == 2 else 1) + overlap * 12
            tie = hashlib.sha256((key + str(len(batches)) + e['id']).encode()).hexdigest()
            return (topic_seen if slot == 2 else 0), value, e['level'], tie
        selected.append(min(candidates, key=score))
    items = []
    for slot, e in enumerate(selected):
        p = status[e['topic']]
        due = e['id'] in used or review_due(p, now)
        purpose = '当前重点' if slot == 0 else '间隔复习' if due else '薄弱补强' if p['state'] == 'needs_practice' else '基础诊断' if slot == 1 else '多样练习'
        why = '近期作答有误，优先选择题库中较低难度的变式巩固。' if p['attempts'] and p['state'] == 'needs_practice' else '到达复习间隔，用新题检查保持情况。' if due else '提示后完成仍需新题确认独立表现。' if p['attempts'] and not recent_correct(p) else '依据历史画像，用同年级新题确认当前水平。' if p.get('initial') and not p['attempts'] else '用新题诊断未充分练习的知识点。' if p['state'] == 'diagnose' else '结合独立作答证据，逐步调整难度。'
        if slot == 2:
            why += '搭配不同知识点或题型，避免反复只练同一类。'
        if route_id != 'adaptive':
            why = f'按「{plan["route_title"]}」路线匹配。' + why
        if e['topic'] not in route_topics:
            why += '所选链路当前供给有限，补充与目标有教材或综合题关联的知识。'
        items.append({**serialize(e), 'purpose': purpose, 'kind': kind(e), 'group': group(e), 'reason': why})
    message = '本组兼顾目标、补弱复习与多样练习，每次作答后重新匹配学情。'
    if len(items) < 3:
        message = f'目标关联范围当前只有 {len(items)} 道同年级可核验且未处于冷却期的题目，可复习课堂材料或调整目标。'
    elif len({e['topic'] for e in selected}) < 3:
        message += '当前可用知识点有限，已尽量更换题型和题目模板。'
    return items, {'batch_id': 'auto:' + key[:16] + ':' + str(len(batches)), 'requested': 3, 'available': len(pool), 'message': message}
