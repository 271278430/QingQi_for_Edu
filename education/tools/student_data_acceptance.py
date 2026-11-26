"""Real catalogue/HTTP acceptance; no model calls or source-file mutations."""
import http.cookiejar
import json
import shutil
import sys
import threading
import urllib.error
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'service/src'))
from qingqi.agent import PROJECT
from qingqi.tools import Registry
from qingqi.catalogue import Catalogue, answer_key, complete_item, incomplete_formula, missing_context, stem_key, text
from qingqi.contracts import ContractError, Identity
from qingqi.product import server
from qingqi.storage import Store
from qingqi.graph import Graph


def fixture_root():
    root = PROJECT / 'runs/student-data-acceptance' / uuid.uuid4().hex
    root.mkdir(parents=True)
    shutil.copyfile(PROJECT / 'runs/product/catalogue.local.json', root / 'catalogue.local.json')
    return root


def verify():
    root = fixture_root()
    c = Catalogue(root)
    instance = server(0, root=root)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{instance.server_port}'
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    results = []
    def get(path):
        with opener.open(base+path, timeout=30) as response:
            return json.load(response)
    boot = get('/api/bootstrap')
    def post(path, body):
        request = urllib.request.Request(base+path, data=json.dumps(body).encode(), headers={'Origin':base,'Content-Type':'application/json','X-Qingqi-CSRF':boot['csrf']})
        with opener.open(request, timeout=30) as response:
            return json.load(response)
    def check(name, condition):
        assert condition, name
        results.append({'name':name,'passed':True})
        print(json.dumps(results[-1]), flush=True)
    def denied(action, status):
        try:
            action()
        except urllib.error.HTTPError as error:
            return error.code == status
        return False
    try:
        report = json.loads(c.db.execute("SELECT value FROM metadata WHERE key='import_report'").fetchone()[0])
        check('math_graph_and_source_aliases_loaded', report['math_books'] == 29 and report['source_questions'] == 6683 and c.db.execute('SELECT COUNT(*) FROM aliases').fetchone()[0] == 6683)
        check('duplicates_conflicts_low_confidence_quarantined', report['duplicates_merged'] > 0 and c.db.execute("SELECT COUNT(*) FROM items i JOIN aliases a ON a.item_id=i.id WHERE a.reason IN ('answer_conflict','low_confidence','grade_conflict') AND i.eligible=1").fetchone()[0] == 0)
        check('only_one_student_identity', boot['profile'] == 'math-student' and boot['role'] == 'student' and len(boot['profiles']) == 1 and denied(lambda:post('/api/profile',{'profile':'teacher-demo'}),403))
        v = get('/api/learning')
        mapping = v['knowledge_map']
        mapped_ids = {n['id'] for n in mapping['nodes']}
        check('learning_map_preserves_all_initial_topics_and_real_edges', sum('initial' in n for n in mapping['nodes']) == 71 and sum(n['topic_id'] is None for n in mapping['nodes']) == 18 and all(e['source'] in mapped_ids and e['target'] in mapped_ids and e['kind'] == 'prerequisite_candidate' for e in mapping['edges']))
        check('map_does_not_leak_answers_or_create_new_work', 'key' not in mapping and all('answer' not in n and 'questions' not in n and 'student_id' not in n for n in mapping['nodes']) and v['summary']['attempts']==0)
        check('source_initialization_separate_from_new_scores', v['initial']['n_attempts'] == 89 and v['initial']['identity_link'] == 'unlinked_example' and v['summary']['attempts'] == 0 and v['summary']['turns'] == 0)
        check('same_grade_recommendations_no_answer_leak', bool(v['recommendations']) and all(c.item(e['id'])['grade']=='7' for e in v['recommendations']) and all('key' not in e and 'analysis' not in e and 'source_qids' not in e for e in v['recommendations']))
        owner = Store(root)
        check('initial_profile_is_low_trust_memory', owner.retrieve(Identity('edu-math-student','s'),'数学')['episodes'][0]['kind'] == 'imported_profile')
        owner.close()
        graph = Graph(Path(c.config['path']))
        check('graph_ids_and_prerequisite_policy', all(graph.db.execute('SELECT 1 FROM nodes WHERE id=?',(t['id'],)).fetchone() for t in v['topics']) and graph.db.execute("SELECT COUNT(*) FROM prerequisites p JOIN edges e ON e.id=p.id WHERE e.relation='co_occurs_with'").fetchone()[0] == 0)
        graph.close()
        registry = Registry(Path(c.config['path']), root=root)
        try:
            result = registry.call('course_context', {'node_id':v['goal']['topic']}, {'course_context'})['result']
            check('actual_zcode_mcp_reads_imported_math_graph', result['node_id'] == v['goal']['topic'] and result['evidence'] and registry.runtime.process is not None)
        finally:
            registry.close()
        # 历史题现在明确按复习计分；首次独立场景必须选未出现在导入作答中的新题。
        historical_ids = set(c.initial.get('historical_items', []))
        e = next(e for e in c.bank.values() if complete_item(e) and e['grade']=='7' and e['answer_kind']=='choice' and e['id'] not in historical_ids)
        a = post('/api/practice/start',{'item_id':e['id'],'request_id':'start-choice'})
        check('choice_options_without_standard_answer', a['item']['options'] and 'key' not in a['item'] and denied(lambda:post('/api/practice/hint',{'assignment_id':a['id'],'request_id':'early-solution','style':'explain'}),403))
        submitted = {'assignment_id':a['id'],'request_id':'choice-answer','answer':e['key']['values'][0]}
        result = post('/api/practice/answer',submitted)
        check('choice_real_answer_updates_only_new_scores', result['correct'] and result['independent_first'] and get('/api/learning')['summary']['attempts']==1 and get('/api/learning')['initial']['n_attempts']==89)
        check('replay_is_idempotent', post('/api/practice/answer',submitted)==result and get('/api/learning')['summary']['attempts']==1)
        check('unsupported_and_cross_grade_items_rejected', denied(lambda:post('/api/practice/start',{'item_id':next(r[0] for r in c.db.execute('SELECT id FROM items WHERE eligible=0')),'request_id':'unsupported'}),400) and denied(lambda:post('/api/practice/start',{'item_id':next(e['id'] for e in c.bank.values() if e['grade']=='8'),'request_id':'cross-grade'}),403))
        incomplete = next(e for e in c.bank.values() if not complete_item(e) and e['grade']=='7')
        check('missing_diagrams_and_tables_block_new_practice_and_recommendations', denied(lambda:post('/api/practice/start',{'item_id':incomplete['id'],'request_id':'missing-context'}),400) and all(complete_item(c.item(i['id'])) for i in get('/api/learning')['recommendations']) and missing_context('图1中有九个数') and missing_context('根据下表统计'))
        broken = next(e for e in c.bank.values() if incomplete_formula(e['expression']) and e['grade']=='7')
        check('truncated_math_blocks_new_practice_but_answer_blanks_remain_valid', denied(lambda:post('/api/practice/start',{'item_id':broken['id'],'request_id':'broken-formula'}),400) and incomplete_formula('$4x-$') and not incomplete_formula('求 $m=$'))
        n = next(e for e in c.bank.values() if complete_item(e) and e['grade']=='7' and e['answer_kind']=='numeric')
        a2 = post('/api/practice/start',{'item_id':n['id'],'request_id':'start-numeric'})
        f = post('/api/practice/answer',{'assignment_id':a2['id'],'request_id':'numeric-answer','answer':';'.join(n['key']['values'])})
        check('numeric_answers_verified_exactly', f['correct'])
        historical = next(e for e in c.bank.values() if complete_item(e) and e['grade']=='7' and e['answer_kind']=='choice' and e['id'] in historical_ids)
        review = post('/api/practice/start',{'item_id':historical['id'],'request_id':'start-historical-review'})
        reviewed = post('/api/practice/answer',{'assignment_id':review['id'],'request_id':'historical-review-answer','answer':historical['key']['values'][0]})
        check('historical_review_is_not_new_independent_diagnosis', reviewed['correct'] and not reviewed['independent'] and not reviewed['independent_first'] and get('/api/learning')['initial']['n_attempts']==89)
        owner = Store(root)
        count = owner.db.execute("SELECT COUNT(*) FROM episodes WHERE kind LIKE 'imported_%'").fetchone()[0]
        check('initialization_idempotent_and_student_isolated', count == c.initial['history_count']+1 and not owner.retrieve(Identity('edu-other','s'),'数学')['episodes'] and not owner.db.execute('SELECT 1 FROM facts').fetchone())
        owner.close()
        check('safe_text_and_option_equivalence', '<script>' not in text('<script>bad()</script><p>题干</p>') and 'bad' not in text('<script>bad()</script>') and answer_key('A',['正确','错误'])==answer_key(['正确'],['正确','错误']))
        check('question_number_and_blank_punctuation_deduplicated', stem_key('3. 求下列结果（ ）') == stem_key('求下列结果') and stem_key('求0.5的倒数') != stem_key('求05的倒数'))
        path = PROJECT.parent / '.local/reports/student-data-verification.json'
        path.write_text(json.dumps({'passed':len(results),'scenarios':results},ensure_ascii=False,indent=2),encoding='utf-8')
    finally:
        instance.shutdown()
        instance.server_close()
        c.close()


if __name__ == '__main__':
    verify()
