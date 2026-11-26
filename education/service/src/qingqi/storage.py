from __future__ import annotations

import json
import sqlite3
import time
import uuid
from pathlib import Path

from .contracts import ContractError, Denied, Identity, Request, canonical, fingerprint


class Busy(RuntimeError):
    pass


class Store:
    def __init__(self, root: Path, *, lease_seconds=30):
        self.lease_seconds = lease_seconds
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "agent.sqlite"
        self.db = sqlite3.connect(self.path, timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS runs (
          id INTEGER PRIMARY KEY, student TEXT, session TEXT, request_id TEXT, payload_hash TEXT,
          request TEXT, state TEXT, response TEXT, lease TEXT, expires REAL DEFAULT 0,
          UNIQUE(student,session,request_id));
        CREATE TABLE IF NOT EXISTS events (
          id INTEGER PRIMARY KEY, run_id INTEGER REFERENCES runs(id), kind TEXT, data TEXT, at REAL);
        CREATE TABLE IF NOT EXISTS calls (
          run_id INTEGER REFERENCES runs(id), call_id TEXT, payload_hash TEXT,
          status TEXT, result TEXT, attempts INTEGER DEFAULT 0, PRIMARY KEY(run_id,call_id));
        CREATE TABLE IF NOT EXISTS model_invocations (
          run_id INTEGER REFERENCES runs(id), invocation_id TEXT, payload_hash TEXT,
          status TEXT, result TEXT, PRIMARY KEY(run_id,invocation_id));
        CREATE INDEX IF NOT EXISTS runs_session_lease ON runs(student,session,expires);
        CREATE INDEX IF NOT EXISTS events_run ON events(run_id,id);
        CREATE TABLE IF NOT EXISTS episodes (
          id INTEGER PRIMARY KEY, student TEXT, session TEXT, run_id INTEGER REFERENCES runs(id),
          kind TEXT, text TEXT, provenance TEXT, at REAL, UNIQUE(run_id,kind,text));
        CREATE TABLE IF NOT EXISTS facts (
          id INTEGER PRIMARY KEY, student TEXT, fact_key TEXT, value TEXT, source TEXT,
          trust TEXT, version INTEGER, at REAL, UNIQUE(student,fact_key,version));
        CREATE TABLE IF NOT EXISTS dialogue_state (
          student TEXT, session TEXT, data TEXT, updated REAL,
          PRIMARY KEY(student,session));
        CREATE INDEX IF NOT EXISTS episodes_student ON episodes(student,id);
        CREATE TABLE IF NOT EXISTS learning_goals(student TEXT PRIMARY KEY,topic TEXT,minutes INTEGER);
        CREATE TABLE IF NOT EXISTS learning_routes(student TEXT PRIMARY KEY,route TEXT);
        CREATE TABLE IF NOT EXISTS practice_assignments(
          id TEXT PRIMARY KEY,student TEXT,session TEXT,item_id TEXT,version TEXT,
          request_id TEXT,payload_hash TEXT,created REAL,UNIQUE(student,request_id));
        CREATE TABLE IF NOT EXISTS practice_events(
          id INTEGER PRIMARY KEY,student TEXT,assignment TEXT REFERENCES practice_assignments(id),
          request_id TEXT,payload_hash TEXT,kind TEXT,data TEXT,at REAL,UNIQUE(student,request_id));
        CREATE INDEX IF NOT EXISTS practice_student ON practice_events(student,id);
        CREATE TABLE IF NOT EXISTS practice_starts(student TEXT,request_id TEXT,payload_hash TEXT,assignment TEXT REFERENCES practice_assignments(id),PRIMARY KEY(student,request_id));
        CREATE TABLE IF NOT EXISTS tutor_images(id TEXT PRIMARY KEY,student TEXT,request_id TEXT,payload_hash TEXT,name TEXT,width INTEGER,height INTEGER,data BLOB,at REAL,UNIQUE(student,request_id));
        CREATE TABLE IF NOT EXISTS student_initial(student TEXT PRIMARY KEY,version TEXT,data TEXT);
        CREATE TABLE IF NOT EXISTS system_settings(id INTEGER PRIMARY KEY CHECK(id=1),data TEXT);
        CREATE TABLE IF NOT EXISTS system_setting_events(principal TEXT,request_id TEXT,payload_hash TEXT,data TEXT,at REAL,PRIMARY KEY(principal,request_id));
        CREATE TABLE IF NOT EXISTS history_control(id INTEGER PRIMARY KEY CHECK(id=1),epoch INTEGER,suppress_imported INTEGER,updated REAL);
        INSERT OR IGNORE INTO history_control VALUES(1,0,0,0);
        CREATE TABLE IF NOT EXISTS history_clear_events(principal TEXT,request_id TEXT,payload_hash TEXT,epoch INTEGER,counts TEXT,at REAL,PRIMARY KEY(principal,request_id));
        """)
        self.owner = uuid.uuid4().hex
        from .catalogue import Catalogue
        self.catalogue = Catalogue(self.root)
        self._initialize_student()

    def _initialize_student(self):
        c = self.catalogue
        if not c.config:
            return
        student = c.config['student']
        with self.db:
            row = self.db.execute('SELECT version FROM student_initial WHERE student=?', (student,)).fetchone()
            if row:
                if row['version'] != c.version:
                    if self.db.execute('SELECT 1 FROM practice_assignments WHERE student=? UNION ALL SELECT 1 FROM runs WHERE student=? LIMIT 1', (student, student)).fetchone():
                        raise Denied('initialized student catalogue version changed')
                    # 初始化修订只替换无新学习记录的导入快照，不覆盖真实作答。
                    self.db.execute('DELETE FROM episodes WHERE student=? AND provenance=? AND kind IN (?,?)', (student, row['version'], 'imported_profile', 'imported_history'))
                    self.db.execute('DELETE FROM student_initial WHERE student=?', (student,))
                    self.db.execute('DELETE FROM learning_goals WHERE student=?', (student,))
                else:
                    return
            initial=dict(c.initial)
            if self.history_status()['suppress_imported']:
                initial.update(history_count=0,historical_items=[])
            self.db.execute('INSERT INTO student_initial VALUES(?,?,?)', (student, c.version, canonical(initial)))
            weak = sorted(c.initial['topics'].items(), key=lambda pair: pair[1]['mastery'])
            from .catalogue import complete_item
            available = {e['topic'] for e in c.bank.values() if complete_item(e) and e['grade'] == c.initial['grade']}
            focus = next((key for key,_ in weak if key in available), next((t['id'] for t in c.topics if t['id'] in available)))
            self.db.execute('INSERT OR IGNORE INTO learning_goals VALUES(?,?,?)', (student, focus, 20))
            summary = {'grade': c.initial['grade'], 'source': c.initial['source'], 'trust': 'imported_model_estimate_not_verified_mastery', 'as_of': c.initial['as_of'], 'weak_topics': [{'name':p['name'],'mastery_estimate':p['mastery'],'confidence':p['confidence']} for _,p in weak[:8]]}
            if not self.history_status()['suppress_imported']:
                self.db.execute('INSERT INTO episodes(student,session,kind,text,provenance,at) VALUES(?,?,?,?,?,?)', (student, 'imported-initial', 'imported_profile', canonical(summary), c.version, 0))
            for row in [] if self.history_status()['suppress_imported'] else c.history:
                content = canonical({'student_prompt': row['prompt'], 'historical_assistant_response': row['response'][:2400], 'trust': 'imported_history_not_student_work'})
                self.db.execute('INSERT INTO episodes(student,session,kind,text,provenance,at) VALUES(?,?,?,?,?,?)', (student, 'imported-history', 'imported_history', content, c.version, 0))

    def close(self):
        self.catalogue.close()
        self.db.close()

    def history_status(self):
        row=self.db.execute('SELECT epoch,suppress_imported,updated FROM history_control WHERE id=1').fetchone()
        return {'epoch':row['epoch'],'suppress_imported':bool(row['suppress_imported']),'updated':row['updated']}

    def clear_history(self,principal,payload):
        from .contracts import validate,obj,SHORT
        from .zcode_runtime import RuntimeFailure
        validate(payload,obj({'request_id':SHORT,'scope':{'type':'string','enum':['project']}}))
        digest=fingerprint(payload)
        self.db.execute('PRAGMA secure_delete=ON')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            previous=self.db.execute('SELECT payload_hash,epoch,counts FROM history_clear_events WHERE principal=? AND request_id=?',(principal,payload['request_id'])).fetchone()
            if previous:
                if previous['payload_hash']!=digest:raise RuntimeFailure('settings_conflict','该清理编号已用于不同操作。')
                result={'epoch':self.history_status()['epoch'],'deleted':json.loads(previous['counts']),'already_applied':True}
                self.db.commit();return result
            if self.db.execute('SELECT 1 FROM runs WHERE lease IS NOT NULL AND expires>? LIMIT 1',(time.time(),)).fetchone():
                raise RuntimeFailure('history_busy','有辅导任务正在执行，请等待结束后再清空历史。',recoverable=True)
            # 原Store按外键顺序清除所有相关记录；只留无正文的幂等回执，不能用旧编号再次删除新对话。
            tables=('practice_events','practice_starts','practice_assignments','calls','model_invocations','events','episodes','facts','dialogue_state','runs','tutor_images','web_sessions','learning_routes')
            existing={r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            deleted={table:self.db.execute(f'DELETE FROM {table}').rowcount for table in tables if table in existing}
            # 会话选模是历史附属状态；清空历史时一并删除，但供应商和凭据配置仍保留。
            for table in ('model_settings','model_setting_events'):
                if table in existing:deleted['chat_'+table]=self.db.execute(f"DELETE FROM {table} WHERE instr(scope,':chat:')>0").rowcount
            for row in self.db.execute('SELECT student,data FROM student_initial').fetchall():
                data=json.loads(row['data']);data.update(history_count=0,historical_items=[])
                self.db.execute('UPDATE student_initial SET data=? WHERE student=?',(canonical(data),row['student']))
            epoch=self.history_status()['epoch']+1;now=time.time()
            self.db.execute('UPDATE history_control SET epoch=?,suppress_imported=1,updated=? WHERE id=1',(epoch,now))
            self.db.execute('INSERT INTO history_clear_events VALUES(?,?,?,?,?,?)',(principal,payload['request_id'],digest,epoch,canonical(deleted),now))
            self.db.commit()
            return {'epoch':epoch,'deleted':deleted,'already_applied':False}
        except BaseException:
            self.db.rollback();raise

    def upload_image(self, student, payload):
        from .tutor_images import normalize
        digest = fingerprint(payload)
        raw, width, height = normalize(payload['data_url'])
        self.db.execute('BEGIN IMMEDIATE')
        try:
            existing = self.db.execute('SELECT id,payload_hash FROM tutor_images WHERE student=? AND request_id=?', (student, payload['request_id'])).fetchone()
            if existing:
                if existing['payload_hash'] != digest:
                    raise Denied('image upload request conflict')
                result = self.image(student, existing['id'])['public']
            else:
                size = self.db.execute('SELECT coalesce(sum(length(data)),0) FROM tutor_images WHERE student=?', (student,)).fetchone()[0]
                if size + len(raw) > 24 * 1024 * 1024:
                    raise ContractError('图片空间已满，请联系产品维护者整理学习图片。')
                image_id = uuid.uuid4().hex
                self.db.execute('INSERT INTO tutor_images VALUES(?,?,?,?,?,?,?,?,?)', (image_id, student, payload['request_id'], digest, payload['name'][:80], width, height, raw, time.time()))
                result = self.image(student, image_id)['public']
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise

    def image(self, student, image_id):
        row = self.db.execute('SELECT * FROM tutor_images WHERE student=? AND id=?', (student, image_id)).fetchone()
        if not row:
            raise Denied('image not owned by student')
        return {'data': row['data'], 'public': {'id': row['id'], 'name': row['name'], 'width': row['width'], 'height': row['height'], 'url': '/api/tutor/image?id=' + row['id']}}

    def set_learning_goal(self, student, topic, minutes):
        with self.db:
            self.db.execute("INSERT INTO learning_goals VALUES(?,?,?) ON CONFLICT(student) DO UPDATE SET topic=excluded.topic,minutes=excluded.minutes", (student, topic, minutes))

    def practice_assignment(self, student, assignment_id):
        from .learning import public_item
        from .practice_tutoring import hint_projection
        row = self.db.execute("SELECT * FROM practice_assignments WHERE id=? AND student=?", (assignment_id, student)).fetchone()
        if not row:
            raise Denied("practice not owned by current student")
        if row["version"] != self.catalogue.version:
            raise Denied("practice bank version changed")
        events = self.db.execute("SELECT kind,data FROM practice_events WHERE student=? AND assignment=? ORDER BY id", (student, assignment_id)).fetchall()
        feedback = next((json.loads(e["data"]) for e in reversed(events) if e["kind"] == "answer"), None)
        entry=self.catalogue.item(row['item_id'])
        guidance = next((hint_projection(entry,json.loads(e["data"]))["text"] for e in reversed(events) if e["kind"] == "hint"), "")
        return {"id": row["id"], "session": row["session"], "item": public_item(self.catalogue.item(row["item_id"])), "feedback": feedback, "guidance": guidance,
                "hint_count": sum(e["kind"] == "hint" for e in events)}

    def practice_entry(self, identity):
        from .catalogue import complete_item
        row = self.db.execute('SELECT id,item_id,version FROM practice_assignments WHERE student=? AND session=? ORDER BY created DESC LIMIT 1', (identity.student, identity.session)).fetchone()
        if not row:
            return None
        if row['version'] != self.catalogue.version:
            raise Denied('practice bank version changed')
        entry = self.catalogue.item(row['item_id'])
        if not complete_item(entry):
            raise ContractError('原题不完整，请返回个性化练习选择一题完整的新题。')
        return {'assignment_id': row['id'], 'entry': entry}

    def _practice_feedback(self, student, assignment, submitted, *, exclude_run=None):
        entry = self.catalogue.item(assignment['item']['id'])
        correct = self.catalogue.grade(entry, submitted)
        prior = self.db.execute("SELECT 1 FROM practice_events e JOIN practice_assignments a ON a.id=e.assignment WHERE e.student=? AND a.item_id=? AND e.kind IN ('answer','hint') LIMIT 1", (student, entry['id'])).fetchone()
        # 闲聊、澄清和未返回的请求没有提供教学帮助，不能降低独立作答证据。
        helped = self.db.execute("SELECT 1 FROM runs r JOIN practice_assignments a ON a.session=r.session AND a.student=r.student WHERE r.student=? AND a.item_id=? AND r.response IS NOT NULL AND json_extract(r.response,'$.teaching_action') IN ('ask','explain','give_answer','confirm') AND (json_extract(r.state,'$.practice_assignment_id')=a.id OR replace(replace(replace(json_extract(r.state,'$.effective_request.expression'),' ',''),'×','*'),'÷','/')=?) AND (? IS NULL OR r.id<>?) LIMIT 1", (student,entry['id'],entry['expression'].replace(' ','').replace('×','*').replace('÷','/'),exclude_run,exclude_run)).fetchone()
        # 清空后的源快照仍可含旧题标记；历史已停用时不能据此扣除新作答的独立性。
        historical=[] if self.history_status()['suppress_imported'] else self.catalogue.initial.get('historical_items', [])
        independent = not prior and not helped and entry['id'] not in historical
        current_work = self.db.execute("SELECT 1 FROM practice_events WHERE student=? AND assignment=? AND kind IN ('answer','hint') LIMIT 1", (student, assignment['id'])).fetchone()
        # 数学符号的等值表示不能成为绕过辅助记录、伪装独立作答的路径。
        current_help = self.db.execute("SELECT 1 FROM runs WHERE student=? AND session=? AND response IS NOT NULL AND json_extract(response,'$.teaching_action') IN ('ask','explain','give_answer','confirm') AND (json_extract(state,'$.practice_assignment_id')=? OR replace(replace(replace(json_extract(state,'$.effective_request.expression'),' ',''),'×','*'),'÷','/')=?) AND (? IS NULL OR id<>?) LIMIT 1", (student,assignment['session'],assignment['id'],entry['expression'].replace(' ','').replace('×','*').replace('÷','/'),exclude_run,exclude_run)).fetchone()
        # 复做可验证保持，但当前题被提示或重试后完成不能当作无辅助复测。
        unassisted = not current_work and not current_help
        from .practice_tutoring import identity_answer
        exact=identity_answer(entry)
        return {'correct': correct, 'independent': independent, 'unassisted': unassisted, 'independent_first': correct and independent, 'item_id': entry['id'], 'topic': entry['topic'], 'topics': entry.get('topics', [entry['topic']]), 'submitted': submitted.strip(),
                'text': ('已通过恒等关系的精确核验。' if exact else '与题库参考答案一致。请解释关键步骤。' if self.catalogue.config else '答案正确。请用自己的话解释关键步骤。') if correct else '答案还不一致。' + self.catalogue.hint(entry, 'heuristic', assignment['hint_count'])}

    def learning_overview(self, student):
        # 看板、路径和推题均从同一快照派生，不能读到半次作答提交。
        self.db.execute("BEGIN")
        try:
            value = self._learning_snapshot(student)
            self.db.commit()
            return value
        except Exception:
            self.db.rollback()
            raise

    def _learning_snapshot(self, student, *, now=None):
        from .learning import learning_projection
        row = self.db.execute("SELECT topic,minutes FROM learning_goals WHERE student=?", (student,)).fetchone()
        # 挂载教材没有种子知识点 order；新学生必须用本题库目标，不能读别人的目标。
        goal = dict(row) if row else {"topic": self.catalogue.topics[0]['id'], "minutes": 20}
        route = self.db.execute('SELECT route FROM learning_routes WHERE student=?', (student,)).fetchone()
        goal['route'] = route['route'] if route else 'adaptive'
        events = [{"kind": r["kind"], "data": json.loads(r["data"]), "at": r["at"]} for r in self.db.execute("SELECT kind,data,at FROM practice_events WHERE student=? ORDER BY id", (student,))]
        latest = self.db.execute("SELECT id FROM practice_assignments WHERE student=? ORDER BY created DESC,id DESC LIMIT 1", (student,)).fetchone()
        active = self.practice_assignment(student, latest["id"]) if latest else None
        turns = self.db.execute("SELECT COUNT(*) FROM runs WHERE student=? AND response IS NOT NULL", (student,)).fetchone()[0]
        initial = self.db.execute('SELECT data FROM student_initial WHERE student=?', (student,)).fetchone()
        return learning_projection(goal, events, active, turns, now=now, catalogue=self.catalogue, initial=json.loads(initial['data']) if initial else None)

    def select_learning_route(self, student, payload):
        digest = fingerprint({'kind': 'learning_route', **payload})
        self.db.execute('BEGIN IMMEDIATE')
        try:
            previous = self.db.execute('SELECT kind,payload_hash,data FROM practice_events WHERE student=? AND request_id=?', (student, payload['request_id'])).fetchone()
            if previous:
                if previous['kind'] != 'learning_route' or previous['payload_hash'] != digest:
                    raise Denied('route request_id payload conflict')
                self.db.commit()
                # 已接受的旧编号只重放回执，不能把后来选择的路线改回去。
                return json.loads(previous['data'])
            routes = self._learning_snapshot(student)['path']['routes']
            if not any(r['id'] == payload['route'] and any(s['has_practice'] for s in r['steps']) for r in routes):
                raise ContractError('这条路线当前没有可用题目，请选择地图中的其他路线。')
            result = {'selected_route': payload['route']}
            self.db.execute('INSERT INTO learning_routes VALUES(?,?) ON CONFLICT(student) DO UPDATE SET route=excluded.route', (student, payload['route']))
            self.db.execute('INSERT INTO practice_events(student,assignment,request_id,payload_hash,kind,data,at) VALUES(?,NULL,?,?,?,?,?)', (student, payload['request_id'], digest, 'learning_route', canonical(result), time.time()))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise

    def tutor_learning_context(self, identity, entry):
        from .learning_evidence import tutor_context
        return tutor_context(self._learning_snapshot(identity.student), entry)

    def renew_recommendations(self, student, payload):
        from .adaptive_learning import evidence_key
        digest = fingerprint({'kind': 'recommendations', **payload})
        self.db.execute('BEGIN IMMEDIATE')
        try:
            previous = self.db.execute('SELECT kind,payload_hash,data FROM practice_events WHERE student=? AND request_id=?', (student, payload['request_id'])).fetchone()
            if previous:
                if previous['kind'] != 'recommendations' or previous['payload_hash'] != digest:
                    raise Denied('recommendation request_id payload conflict')
                self.db.commit()
                return json.loads(previous['data'])['result']
            # 同一换组事务使用同一时刻，跨日时也不会写入与结果不符的指纹。
            snapshot_at = time.time()
            old = self._learning_snapshot(student, now=snapshot_at)
            draft = {'evidence_key': '', 'previous': [i['id'] for i in old['recommendations']], 'result': {'items': [], 'info': {}}}
            row = self.db.execute('INSERT INTO practice_events(student,assignment,request_id,payload_hash,kind,data,at) VALUES(?,NULL,?,?,?,?,?)', (student, payload['request_id'], digest, 'recommendations', canonical(draft), time.time()))
            value = self._learning_snapshot(student, now=snapshot_at)
            events = [{'kind': r['kind'], 'data': json.loads(r['data']), 'at': r['at']} for r in self.db.execute('SELECT kind,data,at FROM practice_events WHERE student=? ORDER BY id', (student,))]
            draft['evidence_key'] = evidence_key(value['goal'], events, value['active'], self.catalogue.version, snapshot_at)
            draft['result'] = {'items': value['recommendations'], 'info': {**value['recommendation_info'], 'batch_id': payload['request_id']}}
            self.db.execute('UPDATE practice_events SET data=? WHERE id=?', (canonical(draft), row.lastrowid))
            self.db.commit()
            return draft['result']
        except Exception:
            self.db.rollback()
            raise

    def prepare_model_hint(self,student,payload):
        """Read command identity and exact owned resource; Agent/commit owns all writes."""
        digest=fingerprint({'kind':'hint',**payload})
        previous=self.db.execute('SELECT payload_hash,data FROM practice_events WHERE student=? AND request_id=?',(student,payload['request_id'])).fetchone()
        if previous:
            if previous['payload_hash']!=digest:raise Denied('practice request_id payload conflict')
            from .practice_tutoring import hint_projection
            assignment=self.practice_assignment(student,payload['assignment_id'])
            return {'result':hint_projection(self.catalogue.item(assignment['item']['id']),json.loads(previous['data']))}
        assignment=self.practice_assignment(student,payload['assignment_id'])
        from .catalogue import complete_item
        if not complete_item(self.catalogue.item(assignment['item']['id'])):raise ContractError('原题不完整，请选择完整的新练习。')
        if assignment['feedback'] and assignment['feedback']['correct']:raise Denied('completed practice does not need another hint')
        return {'payload':payload,'payload_hash':digest,'assignment_id':assignment['id'],'session':assignment['session'],
                'item_id':assignment['item']['id'],'count':assignment['hint_count'],'hints':self.practice_hint_history(student,assignment['id'])}

    def practice_hint_history(self,student,assignment_id):
        from .practice_tutoring import hint_projection
        assignment=self.practice_assignment(student,assignment_id)
        entry=self.catalogue.item(assignment['item']['id'])
        rows=self.db.execute("SELECT data FROM practice_events WHERE student=? AND assignment=? AND kind='hint' ORDER BY id DESC LIMIT 3",(student,assignment_id)).fetchall()
        return [hint_projection(entry,json.loads(row['data']))['text'][:1800] for row in reversed(rows)]

    def _commit_model_hint(self,identity,state,response):
        marker=state.get('practice_hint')
        if not marker:return
        assignment=self.practice_assignment(identity.student,marker['assignment_id'])
        if assignment['session']!=identity.session or assignment['item']['id']!=marker['item_id']:raise Denied('hint resource changed')
        payload=marker['payload']
        previous=self.db.execute('SELECT payload_hash FROM practice_events WHERE student=? AND request_id=?',(identity.student,payload['request_id'])).fetchone()
        if previous:raise Denied('hint command already committed or conflicts with another practice')
        result={'text':response['text'],'style':payload['style'],'hint_count':assignment['hint_count']+1}
        # 与辅导回复共用当前事务；恢复只重放同一结果，不能另存一份提示或推断成绩。
        self.db.execute('INSERT INTO practice_events(student,assignment,request_id,payload_hash,kind,data,at) VALUES(?,?,?,?,?,?,?)',
                        (identity.student,assignment['id'],payload['request_id'],marker['payload_hash'],'hint',canonical(result),time.time()))

    def practice_action(self, student, kind, payload):
        digest = fingerprint({"kind": kind, **payload})
        self.db.execute("BEGIN IMMEDIATE")
        try:
            previous = self.db.execute("SELECT payload_hash,data FROM practice_events WHERE student=? AND request_id=?", (student, payload["request_id"])).fetchone()
            if previous:
                if previous["payload_hash"] != digest:
                    raise Denied("practice request_id payload conflict")
                self.db.commit()
                result=json.loads(previous['data'])
                if kind=='hint':
                    from .practice_tutoring import hint_projection
                    assignment=self.practice_assignment(student,payload['assignment_id'])
                    result=hint_projection(self.catalogue.item(assignment['item']['id']),result)
                return result
            assignment = self.practice_assignment(student, payload["assignment_id"])
            entry = self.catalogue.item(assignment["item"]["id"])
            from .catalogue import complete_item
            if not complete_item(entry):
                raise ContractError('原题不完整，历史记录已保留，请选择一题完整的新练习。')
            active = self.db.execute("SELECT 1 FROM runs WHERE student=? AND session=? AND lease IS NOT NULL AND expires>?", (student, assignment["session"], time.time())).fetchone()
            if active:
                raise Busy("tutoring still running for this practice")
            if kind == "hint":
                if payload['style'] == 'explain' and not assignment['feedback']:
                    raise Denied('submit an answer before requesting solution')
                stage = (self.dialogue(Identity(student, assignment['session'])).get('pending') or {}).get('stage', 0)
                result = {"text": self.catalogue.hint(entry, payload["style"], assignment["hint_count"], stage), "style": payload["style"], "hint_count": assignment["hint_count"] + 1}
            else:
                if assignment["feedback"] and assignment["feedback"]["correct"]:
                    raise Denied("completed practice cannot be graded again")
                result = self._practice_feedback(student, assignment, payload['answer'])
                self._record_practice_work(student, assignment, entry, result)
            self.db.execute("INSERT INTO practice_events(student,assignment,request_id,payload_hash,kind,data,at) VALUES(?,?,?,?,?,?,?)", (student, assignment["id"], payload["request_id"], digest, kind, canonical(result), time.time()))
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise

    def _record_practice_work(self, student, assignment, entry, result):
        # 两种作答入口记录同一份真实证据，参考答案和模型推断不成为掌握事实。
        self.db.execute('INSERT INTO episodes(student,session,kind,text,provenance,at) VALUES(?,?,?,?,?,?)', (student, assignment['session'], 'student_work', canonical({'expression': entry['expression'], 'topic': entry['title'], 'answer': result['submitted'], 'verified_correct': result['correct'], 'independent': result['independent']}), 'verified_practice@' + entry['version'], time.time()))

    def begin(self, identity: Identity, request: Request, *, expected_history_epoch=None) -> tuple[int, dict, dict | None]:
        payload = request.dump()
        digest = fingerprint(payload)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            if expected_history_epoch is not None and expected_history_epoch!=self.history_status()['epoch']:
                # 会话鉴权与Agent准入之间可能发生全量清理；旧请求不能重新写回已删除的历史。
                from .zcode_runtime import RuntimeFailure
                raise RuntimeFailure('history_changed','历史已清空，此请求不再执行。请刷新后新建学习对话。')
            row = self.db.execute("SELECT * FROM runs WHERE student=? AND session=? AND request_id=?",
                                  (identity.student, identity.session, request.request_id)).fetchone()
            if row and row["payload_hash"] != digest:
                raise Denied("request_id reused with different payload")
            if row and row["response"]:
                self.db.commit()
                return row["id"], json.loads(row["state"]), json.loads(row["response"])
            # 请求租约只锁一条 request，多个标签页仍可覆盖同一会话；准入时同时检查会话。
            active = self.db.execute("SELECT id FROM runs WHERE student=? AND session=? AND lease IS NOT NULL AND expires>? AND id<>?",
                                     (identity.student, identity.session, time.time(), row["id"] if row else -1)).fetchone()
            if active:
                raise Busy("another request owns this learning session")
            if row and row["lease"] and row["lease"] != self.owner and row["expires"] > time.time():
                raise Busy("request already executing; retry after lease expiry")
            state = json.loads(row["state"]) if row else {"phase": "new", "observations": [], "cursor": 0, "tool_calls": 0, "repairs": 0}
            if row:
                run_id = row["id"]
                self.db.execute("UPDATE runs SET lease=?,expires=? WHERE id=?", (self.owner, time.time() + self.lease_seconds, run_id))
            else:
                run_id = self.db.execute("INSERT INTO runs(student,session,request_id,payload_hash,request,state,lease,expires) VALUES(?,?,?,?,?,?,?,?)",
                                        (identity.student, identity.session, request.request_id, digest, canonical(payload), canonical(state), self.owner, time.time() + self.lease_seconds)).lastrowid
            self.db.commit()
            return run_id, state, None
        except BaseException:
            self.db.rollback()
            raise

    def checkpoint(self, run_id: int, state: dict, event: str):
        with self.db:
            updated = self.db.execute("UPDATE runs SET state=?,expires=? WHERE id=? AND lease=?",
                                     (canonical(state), time.time() + self.lease_seconds, run_id, self.owner)).rowcount
            if updated != 1:
                raise Busy("lost execution lease")
            self.db.execute("INSERT INTO events(run_id,kind,data,at) VALUES(?,?,?,?)", (run_id, event, canonical(state), time.time()))

    def release(self, run_id: int):
        with self.db:
            self.db.execute("UPDATE runs SET lease=NULL,expires=0 WHERE id=? AND lease=?", (run_id, self.owner))

    def prepare_call(self, run_id: int, call_id: str, payload: dict) -> dict | None:
        digest = fingerprint(payload)
        with self.db:
            row = self.db.execute("SELECT * FROM calls WHERE run_id=? AND call_id=?", (run_id, call_id)).fetchone()
            if row and row["payload_hash"] != digest:
                raise Denied("call_id collision")
            if row and row["status"] == "done":
                return json.loads(row["result"])
            if not row:
                self.db.execute("INSERT INTO calls(run_id,call_id,payload_hash,status) VALUES(?,?,?,?)", (run_id, call_id, digest, "pending"))
        return None

    def attempt(self, run_id: int, call_id: str) -> int:
        with self.db:
            self.db.execute("UPDATE calls SET attempts=attempts+1 WHERE run_id=? AND call_id=?", (run_id, call_id))
        return self.db.execute("SELECT attempts FROM calls WHERE run_id=? AND call_id=?", (run_id, call_id)).fetchone()[0]

    def finish_call(self, run_id: int, call_id: str, result: dict):
        with self.db:
            self.db.execute("UPDATE calls SET status='done',result=? WHERE run_id=? AND call_id=?", (canonical(result), run_id, call_id))

    def defer_call(self, run_id, call_id):
        with self.db:
            self.db.execute("UPDATE calls SET attempts=MAX(0,attempts-1) WHERE run_id=? AND call_id=? AND status='pending'", (run_id, call_id))

    def begin_invocation(self, run_id, invocation_id, payload):
        from .zcode_runtime import RuntimeFailure
        digest = fingerprint(payload)
        with self.db:
            row = self.db.execute("SELECT * FROM model_invocations WHERE run_id=? AND invocation_id=?", (run_id, invocation_id)).fetchone()
            if row and row["payload_hash"] != digest:
                raise Denied("model invocation input changed")
            if row and row["status"] == "done":
                return json.loads(row["result"])
            if row and row["status"] in {"sending", "unknown"}:
                # 已发出却没有已知结果的主控请求不能在用户重试时再次外发。
                raise RuntimeFailure("model_unknown", "上次模型请求结果尚不确定，已阻止同编号重新生成。")
            if row and row["status"] == "failed":
                raise RuntimeFailure("model_failed", "该模型调用已失败；同编号不能静默重新生成。")
            if row:
                self.db.execute("UPDATE model_invocations SET status='sending' WHERE run_id=? AND invocation_id=?", (run_id, invocation_id))
            else:
                self.db.execute("INSERT INTO model_invocations VALUES(?,?,?,?,NULL)", (run_id, invocation_id, digest, "sending"))
        return None

    def finish_invocation(self, run_id, invocation_id, status, result=None):
        with self.db:
            self.db.execute("UPDATE model_invocations SET status=?,result=? WHERE run_id=? AND invocation_id=?",
                            (status, canonical(result) if result is not None else None, run_id, invocation_id))

    def retrieve(self, identity: Identity, query: str, limit: int = 6) -> dict:
        # Separate student filtering precedes relevance ranking. No global vector index leaks.
        rows = self.db.execute("SELECT id,kind,text,provenance,at FROM episodes WHERE student=? ORDER BY CASE WHEN kind='imported_profile' THEN 0 ELSE 1 END,id DESC LIMIT 100", (identity.student,)).fetchall()
        words = {query[i:i + 2] for i in range(max(0, len(query) - 1))}
        scored = sorted(rows, key=lambda r: (r['kind'] == 'imported_profile', sum(w in r["text"] for w in words), r["id"]), reverse=True)
        facts = self.db.execute("SELECT fact_key,value,source,trust,version FROM facts WHERE student=? AND id IN (SELECT MAX(id) FROM facts WHERE student=? GROUP BY fact_key) ORDER BY id DESC LIMIT 10", (identity.student, identity.student)).fetchall()
        return {"episodes": [dict(r) for r in scored[:limit]], "facts": [dict(r) for r in facts]}

    def confirm_fact(self, identity: Identity, key: str, value: str, source: str, *, teacher_authorized: bool = False):
        if not teacher_authorized:
            raise Denied("only trusted teacher workflow may confirm mastery facts")
        with self.db:
            version = self.db.execute("SELECT COALESCE(MAX(version),0)+1 FROM facts WHERE student=? AND fact_key=?", (identity.student, key)).fetchone()[0]
            self.db.execute("INSERT INTO facts(student,fact_key,value,source,trust,version,at) VALUES(?,?,?,?,?,?,?)", (identity.student, key, value, source, "teacher_confirmed", version, time.time()))

    def recent_turns(self, identity: Identity, limit: int = 6) -> list[dict]:
        """Only completed turns from this authenticated student's SAME session."""
        rows = self.db.execute("SELECT id,request,state,response FROM runs WHERE student=? AND session=? AND response IS NOT NULL ORDER BY id DESC LIMIT ?",
                               (identity.student, identity.session, limit)).fetchall()
        return [{"run_id": r["id"], "request": json.loads(r["state"]).get("effective_request", json.loads(r["request"])),
                 "response": json.loads(r["response"]), "student_question": json.loads(r["request"])["question"],
                 "geometry_task": json.loads(r["state"]).get("geometry_task"),
                 "command": json.loads(r["state"]).get("route",{}).get("command"),
                 "presentation": json.loads(r["state"]).get("presentation"),
                 "practice_item_id":json.loads(r['state']).get('practice_entry',{}).get('id')} for r in rows]

    def referenced_image(self,identity,ttl=1800):
        """Read a recent accepted image only for an explicit same-session reference."""
        rows=self.db.execute('SELECT r.state,(SELECT MAX(at) FROM events WHERE run_id=r.id) AS updated FROM runs r WHERE r.student=? AND r.session=? AND r.response IS NOT NULL ORDER BY r.id DESC LIMIT 10',(identity.student,identity.session)).fetchall()
        for row in rows:
            if not row['updated'] or time.time()-row['updated']>ttl:return None
            state=json.loads(row['state'])
            # 取消/新题是上下文边界，不能用旧图片恢复已结束的教学任务。
            if state.get('route',{}).get('command') in {'cancel','new_task'}:return None
            if state.get('image_question'):return state['image_question']
        return None

    def current_problem(self,identity):
        """Recover a static binding from accepted turns, within this identity only."""
        work=(self.dialogue(identity).get('verified_work') or {})
        if work:return self._with_image_disclosure(identity,work)
        rows=self.db.execute('SELECT id,state,request,response FROM runs WHERE student=? AND session=? AND response IS NOT NULL ORDER BY id DESC LIMIT 50',(identity.student,identity.session)).fetchall()
        for row in rows:
            state=json.loads(row['state']);route=state.get('route',{});response=json.loads(row['response'])
            if route.get('command') in {'cancel','new_task'}:return None
            from .conversation import starts_new_problem
            if response.get('teaching_action')=='clarify' and starts_new_problem(json.loads(row['request'])['question']):return None
            # 旧版澄清覆盖了题目；澄清本身不是学生提供了一道新题。
            if response.get('teaching_action')=='clarify' or route.get('intents')==['chat']:continue
            binding={'source_run_id':row['id'],'answer_disclosed':bool(route.get('teaching',{}).get('allow_final_answer'))}
            if state.get('contextual_followup') and route.get('continuity')=='continuation' and state.get('current_problem'):
                return self._with_image_disclosure(identity,dict(state['current_problem']))
            if state.get('image_question'):return self._with_image_disclosure(identity,{**binding,'source':'unverified_image_transcription','image_question':state['image_question']})
            if state.get('practice_entry') and state.get('practice_assignment_id'):
                # TTL或旧澄清只结束临时步骤；从当前身份的有效练习恢复持久原题。
                assignment=self.practice_assignment(identity.student,state['practice_assignment_id'])
                if assignment['session']==identity.session:
                    return {**binding,'source':'owned_catalogue_question','assignment_id':assignment['id']}
            if state.get('practice_entry') and not state.get('practice_assignment_id'):return {**binding,'source':'student_linear_equation','linear_entry':state['practice_entry']}
            if state.get('problem_question') or state.get('controller')=='glm_general_text_controller':
                return {**binding,'source':'unverified_text_question','problem_question':state.get('problem_question') or {'text':json.loads(row['request'])['question']}}
            if route.get('continuity')=='new_task':return None
        return None

    def _with_image_disclosure(self,identity,work):
        if work.get('tutoring_scope'):return work
        if work.get('image_question') and not work.get('answer_disclosed'):
            rows=self.db.execute('SELECT state,response FROM runs WHERE student=? AND session=? AND response IS NOT NULL ORDER BY id DESC LIMIT 50',(identity.student,identity.session)).fetchall()
            for row in rows:
                state=json.loads(row['state']);route=state.get('route',{})
                if route.get('command') in {'cancel','new_task'}:break
                # 披露是同一题资源的历史属性；旧版一次误判new_task不能抹掉已公开解法。
                if self._same_image_problem(state.get('image_question'),work['image_question']) and route.get('teaching',{}).get('allow_final_answer') and json.loads(row['response']).get('teaching_action')!='clarify':return {**work,'answer_disclosed':True}
        return work

    @staticmethod
    def _same_image_problem(left,right):
        if not left or not right or left.get('unclear') or right.get('unclear'):return False
        import re
        import unicodedata
        normalize=lambda q:re.sub(r'\s+|\\(?:left|right)','',unicodedata.normalize('NFKC',q).replace('−','-'))
        # 同题重传会生成新附件ID，OCR备注也会变化；同身份下比较完整题干，不用备注作题目身份。
        return bool(left.get('text') and normalize(left['text'])==normalize(right.get('text','')))

    def problem_turns(self,identity,problem,limit=8):
        """Same-session accepted explanations of the bound resource, in chronological order."""
        source=(problem or {}).get('image_question') or (problem or {}).get('problem_question')
        if not source:return []
        rows=self.db.execute('SELECT state,request,response FROM runs WHERE student=? AND session=? AND response IS NOT NULL ORDER BY id DESC LIMIT 50',(identity.student,identity.session)).fetchall()
        turns=[]
        for row in rows:
            state=json.loads(row['state']);route=state.get('route',{});request=json.loads(row['request']);response=json.loads(row['response'])
            from .conversation import starts_new_problem
            if route.get('command') in {'cancel','new_task'} or starts_new_problem(request['question']):break
            if response.get('teaching_action')=='clarify' or route.get('intents')==['chat']:continue
            reference=state.get('image_question') or state.get('problem_question')
            if state.get('contextual_followup') and route.get('continuity')=='continuation':
                previous=state.get('current_problem') or {}
                reference=previous.get('image_question') or previous.get('problem_question') or reference
            # 历史解释属于题目资源而不是某个控制器；成功的新题是边界，不能串入另一道题。
            if not self._same_image_problem(reference,source):break
            turns.append({'question':request['question'][:2000],'reply':response['text'][:3500]})
            if len(turns)>=limit:break
        return list(reversed(turns))

    def prior_visual(self,identity,entry=None,image=None,part=None):
        """Only an accepted plot from this exact owned problem or image."""
        rows=self.db.execute('SELECT state,response FROM runs WHERE student=? AND session=? AND response IS NOT NULL ORDER BY id DESC LIMIT 12',(identity.student,identity.session)).fetchall()
        reference=(self.current_problem(identity) or {}).get('visual_reference')
        if reference:
            referenced=self.db.execute('SELECT state,response FROM runs WHERE id=? AND student=? AND session=? AND response IS NOT NULL',(reference['run_id'],identity.student,identity.session)).fetchone()
            if referenced:rows.insert(0,referenced)
        for row in rows:
            state=json.loads(row['state'])
            same=bool(entry and state.get('practice_entry',{}).get('id')==entry['id']) or bool(image and self._same_image_problem(state.get('image_question'),image))
            if not same:continue
            from .projection import project_response
            for visual in reversed(project_response(json.loads(row['response']),state).get('visuals',[])):
                import re
                named=re.search(r'第\s*[（(]?\s*([1-9])\s*[）)]?\s*问',visual.get('title','')+' '+state.get('geometry_question',''))
                visual_part=visual.get('teaching_part') or (int(named[1]) if named else state.get('tutoring_scope',{}).get('active_part'))
                if part and visual_part and part!=visual_part:continue
                if visual['kind']=='coordinates' or visual.get('template')=='coordinate_drawing':return visual
        return None

    def visual_source(self,identity,reference):
        row=self.db.execute('SELECT request,state,response FROM runs WHERE id=? AND student=? AND session=? AND response IS NOT NULL',(reference['run_id'],identity.student,identity.session)).fetchone()
        if not row:raise Denied('只能讨论同一学习会话中已完成的教学图。')
        state=json.loads(row['state']);response=json.loads(row['response']);index=reference['visual_index']
        if index>=len(response.get('visuals',[])):raise Denied('该教学图不存在或尚未完成。')
        question=(state.get('image_question') or state.get('problem_question') or {}).get('text') or state.get('practice_entry',{}).get('expression') or json.loads(row['request'])['question']
        visual=response['visuals'][index]
        scope=dict(response.get('tutoring_scope') or state.get('tutoring_scope') or {})
        import re
        part=re.search(r'第\s*[（(]?\s*([1-9])\s*[）)]?\s*问',visual.get('title',''))
        selected=visual.get('teaching_part') or (int(part[1]) if part else {'ratio':2,'function':3}.get(visual.get('params',{}).get('lesson_goal')))
        if selected in scope.get('available_parts',[]):scope['active_part']=selected
        work={'source':'accepted_visual_reference','source_run_id':reference['run_id'],'problem_question':{'text':question},'tutoring_scope':scope}
        if state.get('practice_assignment_id'):work.update(source='owned_catalogue_question',assignment_id=state['practice_assignment_id'])
        if state.get('image_question'):work['image_question']=state['image_question']
        geometry=visual.get('geometry') or visual
        points=geometry.get('points',[]);segments=geometry.get('segments',[])
        known={'points':[p['label'] for p in points],
               'segments':[{'from':points[s['source']]['label'],'to':points[s['target']]['label'],'style':s.get('style','solid'),'role':s.get('role','edge')} for s in segments if 0<=s['source']<len(points) and 0<=s['target']<len(points)]}
        solved=next((o['result'] for o in state.get('observations',[]) if o['tool']=='solve_geometry'),None)
        verified={'source_part':1,'angles':solved['midpoint']['angles']} if selected==1 and solved and solved.get('status')=='verified' and 'midpoint' in solved.get('parts',[]) else None
        # 原有CD不能被误说成学生新画的红色EF；只传点名/拓扑，不重复大段坐标或泄露解答。
        return {'question':question,'problem':work,'visual':{**{k:v for k,v in visual.items() if k in {'title','kind','basis','caption'}},'existing_elements':known,**({'verified_geometry':verified} if verified else {})}}

    def dialogue(self, identity: Identity, ttl=1800) -> dict:
        row = self.db.execute('SELECT data,updated FROM dialogue_state WHERE student=? AND session=?',
                              (identity.student, identity.session)).fetchone()
        if not row:
            return {'pending': None, 'active_task': None, 'verified_work': None, 'expired': False}
        if time.time()-row['updated'] > ttl:
            old=json.loads(row['data']);work=old.get('verified_work') or {}
            # 原题是会话资源，TTL仅清除临时教学步骤；不得把原图片/文本题一起抹掉。
            durable=bool(work.get('image_question') or work.get('problem_question') or work.get('linear_entry') or work.get('assignment_id'))
            assignment_preference=bool(work.get('assignment_id'))
            return {'pending':None,'active_task':None,'verified_work':work if durable else None,'expired':True,'practice_detached':old.get('practice_detached',False),'no_final_requested':old.get('no_final_requested',False) if assignment_preference else False,'no_questions':old.get('no_questions',False) if assignment_preference else False,'presentation':old.get('presentation') if durable else None,'teaching_mode':old.get('teaching_mode') if durable else None}
        return {**json.loads(row['data']), 'expired': False}

    def commit(self, run_id: int, identity: Identity, request: Request, state: dict, response: dict):
        # Response, episodic memory and final state commit in ONE transaction.
        # 恢复成功后当前投影不能继续带旧超时；原失败事件仍留在不可变事件记录中。
        for key in ('error','error_code','error_type'):state.pop(key,None)
        with self.db:
            row = self.db.execute("SELECT student,session,response,lease FROM runs WHERE id=?", (run_id,)).fetchone()
            if (row["student"], row["session"]) != (identity.student, identity.session) or row["lease"] != self.owner:
                raise Denied("commit identity/lease mismatch")
            for h in request.history:
                self.db.execute("INSERT OR IGNORE INTO episodes(student,session,run_id,kind,text,provenance,at) VALUES(?,?,?,?,?,?,?)",
                                (identity.student, identity.session, run_id, h["kind"], h["text"], "request_history_unverified", time.time()))
            if request.steps:
                self.db.execute("INSERT OR IGNORE INTO episodes(student,session,run_id,kind,text,provenance,at) VALUES(?,?,?,?,?,?,?)",
                                (identity.student, identity.session, run_id, "student_work", canonical({"expression": request.expression, "steps": request.steps}), "current_student_work", time.time()))
            for kind, text, source in [("question", request.question, "student_request"), ("agent_reply", response["text"], "agent_inference_not_mastery")]:
                self.db.execute("INSERT OR IGNORE INTO episodes(student,session,run_id,kind,text,provenance,at) VALUES(?,?,?,?,?,?,?)",
                                (identity.student, identity.session, run_id, kind, text, source, time.time()))
            self._commit_dialogue(identity, request, state, response, run_id)
            self._commit_model_hint(identity,state,response)
            self._commit_practice_work(identity, request, state, run_id)
            self.db.execute("UPDATE runs SET state=?,response=?,lease=NULL,expires=0 WHERE id=?", (canonical(state), canonical(response), run_id))
            self.db.execute("INSERT INTO events(run_id,kind,data,at) VALUES(?,?,?,?)", (run_id, "committed", canonical(response), time.time()))

    def _commit_dialogue(self, identity, request, state, response, run_id):
        command = state['route'].get('command')
        if command in {'cancel', 'new_task'}:
            data = {'pending': None, 'active_task': None, 'verified_work': None, 'practice_detached': True}
        elif state.get('practice_entry'):
            assessed = state['practice_assessment']
            work = {'source': 'owned_catalogue_question', 'source_run_id': run_id, 'assignment_id': state.get('practice_assignment_id')}
            if not state.get('practice_assignment_id'):
                work = {'source': 'student_linear_equation', 'source_run_id': run_id, 'linear_entry': state['practice_entry']}
            data = {'pending': None if assessed['complete'] and assessed['status'] == 'correct' else {'kind': 'student_response', 'slot': 'catalogue_work', 'stage': assessed['stage'], 'prompt_count': state['practice_prompt_count'], 'run_id': run_id},
                    'active_task': {'run_id': run_id, 'intents': ['tutor']}, 'verified_work': work}
            if state.get('image_question'):
                data['verified_work']['image_question'] = state['image_question']
        elif state.get('image_question'):
            data = {'pending': {'kind': 'student_response', 'slot': 'image_work', 'run_id': run_id}, 'active_task': {'run_id': run_id, 'intents': ['tutor']},
                    'verified_work': {'source': 'unverified_image_transcription', 'source_run_id': run_id, 'image_question': state['image_question']}}
        elif state['route']['intents'] == ('chat',) or state['route']['intents'] == ['chat']:
            # Chat must not extend the lifetime of stale coursework bindings.
            return
        else:
            observations = {o['tool']: o['result'] for o in state['observations']}
            checked = observations.get('review_arithmetic') or observations.get('worker_review27b')
            course = observations.get('course_context')
            old = self.dialogue(identity)
            work = None
            if checked and checked['status'] != 'unsupported':
                work = {'expression': request.expression, 'steps': request.steps, 'subject': request.subject,
                        'source_run_id': run_id, 'source': 'actual_work_with_completed_review'}
            elif course:
                work = {'course_query': request.course_query, 'subject': request.subject,
                        'node_id': course['node_id'], 'source_run_id': run_id, 'source': 'verified_graph_node'}
            elif state.get('contextual_followup') and state['route'].get('continuity')=='continuation' and state.get('current_problem'):
                # 主导师改述原题时保持图片和原题的所有权，不能以操作文字重建题目资源。
                work=dict(state['current_problem'])
            elif state.get('problem_question') and response['teaching_action']!='clarify':
                work={'source':'unverified_text_question','source_run_id':run_id,'problem_question':state['problem_question']}
            elif not state.get('explicit_problem_boundary') and (response['teaching_action']=='clarify' or state['route'].get('continuity') == 'continuation'):
                # 缺少当前步骤可澄清，但不能覆盖已经接受的静态原题。
                work = old.get('verified_work') or self.current_problem(identity)
            pending = None
            if response['teaching_action'] == 'clarify':
                intents = state['route']['intents']
                slot = 'expression' if 'review' in intents and not request.expression else 'course_query' if 'course' in intents and not request.course_query else 'history' if 'diagnosis' in intents and not request.history and not request.steps else 'task_description'
                pending = {'kind': 'required_slot', 'slot': slot, 'run_id': run_id, 'prompt': response['text']}
            elif checked and (response['teaching_action'] == 'ask' or response['teaching_action'] == 'confirm' and not self._numeric_work_complete(request)):
                pending = {'kind': 'student_response', 'slot': 'work_or_explanation', 'run_id': run_id, 'prompt': response['text']}
            data = {'pending': pending, 'active_task': {'run_id': run_id, 'intents': state['route']['intents'],
                      'status': 'awaiting_student' if pending else 'completed'}, 'verified_work': work}
        work=data.get('verified_work')
        if work and state.get('annotation_source',{}).get('problem',{}).get('assignment_id'):
            work.update(source='owned_catalogue_question',assignment_id=state['annotation_source']['problem']['assignment_id'])
            state['practice_detached']=False
            data['practice_detached']=False
        if work and command not in {'cancel','new_task'}:
            prior=state.get('current_problem') or {}
            same=state['route'].get('continuity')=='continuation' or bool(not state.get('explicit_problem_boundary') and self._same_image_problem(work.get('image_question'),prior.get('image_question')))
            if state.get('annotation_source'):work['visual_reference']=request.visual_context
            elif same and prior.get('visual_reference'):work['visual_reference']=prior['visual_reference']
            work['answer_disclosed']=bool(response['teaching_action']!='clarify' and state['route']['teaching']['allow_final_answer'] or same and prior.get('answer_disclosed'))
            if state.get('tutoring_scope') and response['teaching_action']!='clarify':
                from .tutoring_scope import public
                scope=public(state['tutoring_scope'])
                # 已公开答案只登记到对应小问，当前小问是本次最后的教学任务。
                old=(prior.get('tutoring_scope') or {}) if same else {}
                scope['answer_parts']=sorted(set(old.get('answer_parts',[]))|{u['part'] for u in scope['units'] if u['allow_final_answer']})
                work['tutoring_scope']=scope;work['answer_disclosed']=scope['active_part'] in scope['answer_parts']
        data['practice_detached'] = state.get('practice_detached', False)
        data['no_final_requested'] = bool(state['route']['teaching'].get('no_final_requested')) if command not in {'cancel', 'new_task'} else False
        data['no_questions'] = bool(state['route']['teaching'].get('no_questions_requested',state['route']['teaching'].get('no_questions'))) if command not in {'cancel','new_task'} else False
        if response['teaching_action']=='clarify' and not state.get('explicit_problem_boundary') and work:
            # 未识别教学请求不等于换题；澄清须保留同题限制，不用默认策略覆盖旧偏好。
            old=self.dialogue(identity)
            data['no_final_requested']=old.get('no_final_requested',False)
            data['no_questions']=old.get('no_questions',False)
            if work.get('source')=='owned_catalogue_question':data['practice_detached']=False
        if work and command not in {'cancel','new_task'}:
            data['presentation']=state.get('presentation') or (self.dialogue(identity).get('presentation') if not state.get('explicit_problem_boundary') else None)
            decision=state['route']['teaching']
            mode={'version':'contextual_mode_v1','mode':decision['mode'],'label':decision['label'],'reason':decision['reason'],'source':decision.get('source','adaptive_context'),
                  'part':state.get('tutoring_scope',{}).get('active_part'),'source_run_id':run_id}
            if response['teaching_action']=='clarify':mode=self.dialogue(identity).get('teaching_mode')
            if state.get('practice_hint'):
                # 单次提示卡片不等于学生改了对话教法，也不把禁追问规则带到导师对话。
                previous=self.dialogue(identity)
                mode=previous.get('teaching_mode');data['no_questions']=previous.get('no_questions',False)
            data['teaching_mode']=mode
            if mode:work['teaching_mode']=mode
            work['no_final_requested']=data['no_final_requested']
        self.db.execute('INSERT INTO dialogue_state(student,session,data,updated) VALUES(?,?,?,?) ON CONFLICT(student,session) DO UPDATE SET data=excluded.data,updated=excluded.updated',
                        (identity.student, identity.session, canonical(data), time.time()))

    @staticmethod
    def _numeric_work_complete(request):
        from .teaching_responses import completed_numeric_work
        return completed_numeric_work(request.expression, request.steps)

    def _commit_practice_work(self, identity, request, state, run_id):
        from .learning import numeric_answer
        assessed = state.get('practice_assessment')
        if state.get('practice_assignment_id') and assessed and assessed['complete']:
            assignment = self.practice_assignment(identity.student, state['practice_assignment_id'])
            if assignment['feedback'] and assignment['feedback']['correct']:
                return
            # 对话最终作答复用同一反馈判据，在回复事务内写入；部分步骤不进入成绩。
            result = self._practice_feedback(identity.student, assignment, assessed['submitted'], exclude_run=run_id)
            result['source'] = 'verified_tutoring_work'
            self._record_practice_work(identity.student, assignment, self.catalogue.item(assignment['item']['id']), result)
            self.db.execute('INSERT INTO practice_events(student,assignment,request_id,payload_hash,kind,data,at) VALUES(?,?,?,?,?,?,?)', (identity.student, assignment['id'], 'tutor:' + str(run_id), fingerprint(request.dump()), 'answer', canonical(result), time.time()))
            return
        # 源题干不是纯算式，不能把局部算式的核验结果冒充整题答对。
        if self.catalogue.config:
            return
        observations = {o['tool']: o['result'] for o in state['observations']}
        checked = observations.get('review_arithmetic') or observations.get('worker_review27b')
        if not checked or checked['status'] != 'correct' or not self._numeric_work_complete(request):
            return
        row = self.db.execute("SELECT id,item_id FROM practice_assignments WHERE student=? AND session=?", (identity.student, identity.session)).fetchone()
        if not row:
            return
        entry = self.catalogue.item(row['item_id'])
        if request.expression.replace(' ', '').replace('×', '*').replace('÷', '/') != entry['expression'].replace(' ', ''):
            return
        prior = self.db.execute("SELECT kind,data FROM practice_events WHERE student=? AND assignment=? ORDER BY id", (identity.student, row['id'])).fetchall()
        if any(e['kind'] == 'answer' and json.loads(e['data'])['correct'] for e in prior):
            return
        submitted = request.steps[-1]['equation'].split('=')[1].strip()
        numeric_answer(submitted)
        # 学生在辅导中真实提交的完整作答与练习使用同一事件，不从助手解法反推答对。
        assignment = self.practice_assignment(identity.student, row['id'])
        result = {**self._practice_feedback(identity.student, assignment, submitted, exclude_run=run_id),
                  'text': '辅导中提交的完整数值作答已通过核验。', 'source': 'verified_tutoring_work'}
        payload = {'run_id': run_id, 'request': request.dump()}
        self.db.execute("INSERT INTO practice_events(student,assignment,request_id,payload_hash,kind,data,at) VALUES(?,?,?,?,?,?,?)", (identity.student, row['id'], 'tutor:' + str(run_id), fingerprint(payload), 'answer', canonical(result), time.time()))
