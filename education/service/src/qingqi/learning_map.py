"""Pure, source-labelled graph projection. No inferred mastery or fabricated edges."""

INITIAL_FIELDS = ('mastery', 'confidence', 'practice_count', 'accuracy', 'status', 'last_practiced_at')


def project_map(topics, initial, available):
    source = initial.get('topics', {})
    known = {t['id']: t for t in topics}
    nodes = []
    groups = {}
    for node_id in sorted(known.keys() | source.keys()):
        topic, snapshot = known.get(node_id), source.get(node_id)
        path = (snapshot or {}).get('path') or (topic or {}).get('path') or '数学基础'
        group = path.split('/')[0]
        if group == '五四制小学衔接' and '统计与概率' in path:
            group = '统计与概率'
        group_id = 'group:' + group
        groups.setdefault(group_id, {'id': group_id, 'title': group, 'count': 0})['count'] += 1
        nodes.append({'id': node_id, 'title': topic['title'] if topic else snapshot['name'],
                      'group': group_id, 'path': path, 'topic_id': node_id if topic else None,
                      'available': node_id in available,
                      **({'initial': {k: snapshot[k] for k in INITIAL_FIELDS}} if snapshot else {})})
    edges = [{'source': p, 'target': t['id'], 'kind': 'prerequisite_candidate'}
             for t in topics for p in t['requires'] if p in known and p != t['id']]
    return {'nodes': nodes, 'groups': list(groups.values()), 'edges': edges,
            'profile_topics': len(source), 'mapped_profile_topics': len(source.keys() & known.keys()),
            'relation_source': 'mounted_math_graph_unverified_candidates' if initial else 'authored_seed_dependencies'}
