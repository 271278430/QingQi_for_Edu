"""Bounded, directed learning routes from curriculum and student evidence."""
from itertools import combinations
from .adaptive_learning import POLICY, checked, review_due, recent_correct

ROUTES = ('adaptive', 'foundation', 'explore')


def branch_plan(base, goal, profiles, available, now, *, authored, bank=None, available_levels=None):
    status = {p['id']: p for p in profiles}
    target = goal['topic']
    available = set(available) & status.keys()
    basic_available = {n for n in available if available_levels is None or available_levels.get(n, 3) <= 1}
    limit = min(5, max(3, goal['minutes'] // 5))
    shared = {}
    for item in (bank or {}).values():
        for pair in combinations(sorted(set(item.get('topics', [item['topic']])) & status.keys()), 2):
            shared[pair] = shared.get(pair, 0) + 1

    def prior_chain(node):
        paths, queue = {}, [(node, [])]
        while queue:
            current, path = queue.pop(0)
            if len(path) >= 3:
                continue
            for previous in status[current]['requires']:
                if previous not in status or previous == node or previous in paths:
                    continue
                paths[previous] = [*path, previous]
                queue.append((previous, paths[previous]))
        return paths

    predecessors = {n: prior_chain(n) for n in status}

    def relation(a, b):
        if a == b:
            return {'kind': 'goal', 'cost': 0, 'label': '当前学习目标'}
        if a in predecessors[b] and b in predecessors[a]:
            # 互为先修意味着来源存在冲突，不能把循环画成学习进阶顺序。
            return None
        if a in predecessors[b] or b in predecessors[a]:
            forward = a in predecessors[b]
            chain = predecessors[b].get(a) if forward else predecessors[a][b]
            nodes = [*reversed(chain), b] if forward else [*reversed(chain), a]
            kind = 'confirmed_prerequisite' if authored else 'prerequisite_candidate'
            if len(chain) > 1:
                kind += '_chain'
            return {'kind': kind, 'cost': len(chain), 'label': '教材先修链：' + ' → '.join(status[n]['title'] for n in nodes) + ('（既有先修规则）' if authored else '（建议候选，尚未教研确认）')}
        count = shared.get(tuple(sorted((a, b))), 0)
        if count:
            return {'kind': 'shared_question', 'cost': 2, 'label': f'同年级题库有 {count} 道完整题同时关联这两个知识点'}
        foundations = sorted(set(predecessors[a]) & set(predecessors[b]), key=lambda n: (len(predecessors[a][n]) + len(predecessors[b][n]), n))
        common_base = next((n for n in foundations if len(predecessors[a][n]) + len(predecessors[b][n]) <= 3), None)
        if common_base:
            return {'kind': 'shared_foundation', 'cost': 3, 'label': '教材图谱指向共同基础「' + status[common_base]['title'] + '」'}
        left, right = status[a].get('path', '').split('/'), status[b].get('path', '').split('/')
        common = 0
        for p, q in zip(left, right):
            if not p or p != q:
                break
            common += 1
        # 仅“数与式”大类一致不能连接有理数加法与平方根。
        if common >= 2:
            return {'kind': 'same_unit', 'cost': max(3, 7 - common), 'label': '同属教材知识单元「' + '/'.join(left[:common]) + '」，安排同单元迁移诊断'}
        return None

    related = {n: link for n in status if (link := relation(target, n))}

    def need(node):
        p = status[node]
        rank = 0 if p['attempts'] and p['state'] == 'needs_practice' else 1 if review_due(p, now) else 2 if p['state'] == 'needs_practice' else 3 if not checked(p) else 4
        return rank, p.get('initial', {}).get('mastery', .5), p['title']

    nearby = sorted((available & related.keys()) - {target}, key=lambda n: (related[n]['cost'], need(n)))
    ancestors = sorted(predecessors[target], key=lambda n: (-len(predecessors[target][n]), need(n)))
    foundations = [n for n in ancestors if not checked(status[n]) or review_due(status[n], now)]
    support = [n for n in nearby if not checked(status[n]) or review_due(status[n], now)]
    initial_focus = base['focus'] if authored and base['focus'] in related else target
    if not authored and status[target]['state'] == 'steady' and not review_due(status[target], now) and support:
        initial_focus = min(support, key=lambda n: (need(n), related[n]['cost']))
    if initial_focus not in available:
        initial_focus = nearby[0] if nearby else target

    def append(chain, candidates):
        chain = list(dict.fromkeys(chain))
        for node in candidates:
            if len(chain) >= limit:
                break
            if node in chain or node not in related:
                continue
            # 先修方向不能倒置；每站须同时关联目标和上一站，禁止一路串到远处。
            if any(node in predecessors[p] for p in chain) or not relation(chain[-1], node):
                continue
            chain.append(node)
        return chain

    if authored:
        old_chain = [s['topic'] for s in base['steps'] if s['topic'] in related]
        steady = list(dict.fromkeys([*old_chain[:limit - 1], target]))
    else:
        steady = [initial_focus, target] if initial_focus in predecessors[target] else [target, initial_focus]
        steady = list(dict.fromkeys(steady))
    steady = append(steady, support + nearby)

    # 基础路线在目标前保留一条完整的、方向正确的准备链。
    prefix = foundations[-(limit - 1):]
    foundation = [*prefix, target]
    if not prefix:
        weak = next((n for n in support if target not in predecessors[n]), None)
        foundation = [weak, target] if weak else [target]
    applications = sorted((n for n in nearby if n not in predecessors[target]), key=lambda n: (0 if target in predecessors[n] else 1 if related[n]['kind'] == 'shared_question' else 2, related[n]['cost'], need(n)))
    foundation = append(foundation, applications)
    explore = append([target], applications)

    variants, signatures = [], set()
    old = {s['topic']: s for s in base['steps']}
    for route_id, title, chain in [('adaptive', '稳步推进', steady), ('foundation', '补弱优先', foundation), ('explore', '拓展应用', explore)]:
        if len(available & related.keys()) <= 1 and route_id != 'adaptive':
            continue
        chain = list(dict.fromkeys(chain))
        # 目标预先占位；不能截断后再插入目标而破坏已有连线。
        if target not in chain or len(chain) > limit or any(not relation(a, b) for a, b in zip(chain, chain[1:])):
            continue
        signature = frozenset(chain)
        if signature in signatures:
            continue
        signatures.add(signature)
        if not (set(chain) & available):
            if variants:
                continue
            chain = [target]
        if route_id == 'adaptive' and initial_focus in chain and initial_focus in available:
            focus = initial_focus
        elif route_id == 'foundation' and (basic := [n for n in chain if n in basic_available and (not checked(status[n]) or review_due(status[n], now))]):
            # 基础知识点可能仅映射进阶综合题，先诊断真正具有基础新题供给的站点。
            focus = target if target in basic and status[target]['attempts'] and status[target]['state'] == 'needs_practice' else basic[0]
        elif status[target]['attempts'] and status[target]['state'] == 'needs_practice' and target in available:
            focus = target
        else:
            focus = next((n for n in chain if n in available and (not checked(status[n]) or review_due(status[n], now))), next((n for n in chain if n in available), target))
        steps, edges = [], []
        for i, node in enumerate(chain):
            p = status[node]
            link = relation(chain[i - 1], node) if i else relation(target, node)
            if i:
                edges.append({'source': chain[i - 1], 'target': node, 'kind': link['kind'], 'label': link['label']})
            due = review_due(p, now)
            evidence = '近期作答有误，先用基础变式定位卡点。' if p['attempts'] and p['state'] == 'needs_practice' else '已到复习间隔，用新题确认保持情况。' if due else '提示后完成需再用新题确认独立表现。' if p['attempts'] and not recent_correct(p) else '历史画像提示需巩固，需用新作答确认。' if p.get('initial') and p['state'] == 'needs_practice' else '独立起点已确认，继续用不同题型检验。' if checked(p) else '缺少近期独立作答，先用诊断题确认。'
            checkpoint = '回顾错因后独立完成一道基础变式；仍出错就继续巩固，不直接跳到后继。' if p['attempts'] and p['state'] == 'needs_practice' else '独立完成一题间隔复习；答错就返回基础变式。' if due else '完成新的独立诊断，确认能够不用提示解答。' if p['attempts'] and not recent_correct(p) else '换题型或情境检验迁移，多道独立新题稳定后再进阶。' if checked(p) else '先完成一题独立诊断；提示后完成需换新题确认。'
            reason = link['label'] + '。' + evidence
            if node not in available:
                reason += '当前暂无完整可用的新题，保留教材节点，先练路线内可用站点。'
                checkpoint = '当前缺少可用新题，可先复习课堂材料或调整目标；不替换成无关联题目。'
            elif available_levels is not None and available_levels.get(node, 3) > 1 and not checked(p):
                reason += '该知识点当前仅有较难新题，先巩固可用的基础站点。'
                checkpoint = '先复习基础概念，其他基础站点诊断通过后再尝试这道较难题。'
            steps.append({'topic': node, 'title': p['title'], 'objective': p['objective'], 'state': old[node]['state'] if authored and route_id == 'adaptive' and node in old else p['state'], 'role': '当前重点' if node == focus else '目标推进' if node == target else '补强建议' if route_id == 'foundation' else '复习确认' if due else '拓展诊断', 'reason': reason, 'has_practice': node in available, 'checkpoint': checkpoint, 'review': p.get('review')})
        description = {'adaptive': '优先确认当前起点，再沿教材与题库关联逐步推进。', 'foundation': '沿目标所需的基础链补弱，再回到目标；已确认的基础不强制重做。', 'explore': '从目标转向后继或同年级综合题关联，检验迁移；难度跟随独立作答。'}[route_id]
        focus_title = status[focus]['title']
        explanation = f'本轮先练「{focus_title}」：' + next(s['reason'].split('。', 1)[-1] for s in steps if s['topic'] == focus)
        if not (available & related.keys()):
            description = '当前目标及关联范围暂缺可用新题，请复习课堂材料或调整目标。'
        variants.append({'id': route_id, 'title': title, 'description': description, 'focus': focus, 'steps': steps, 'edges': edges, 'reason': explanation})

    selected = next((r for r in variants if r['id'] == goal.get('route', 'adaptive')), variants[0])
    return {**base, 'routes': variants, 'selected_route': selected['id'], 'route_title': selected['title'], 'steps': selected['steps'], 'focus': selected['focus'], 'related_topics': sorted(related), 'planning_version': POLICY, 'summary': selected['description'], 'route_reason': selected['description'] + selected['reason']}
