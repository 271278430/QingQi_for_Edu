"""Persisted Web projections over the single teaching Store owner."""
from __future__ import annotations
import json
import time
import uuid
import re
from pathlib import Path
from .agent import PROJECT
from .contracts import Denied, Identity
from .storage import Store
from .projection import project_observations, project_response, safe_route
from .tutor_images import legacy_recognition_failure


class WebStore:
    def __init__(self, root: Path):
        self.root = root.resolve()
        if not self.root.is_relative_to(PROJECT / "runs"):
            raise Denied("web persistence outside owned runs")
        self.owner = Store(self.root)
        self.db = self.owner.db
        self.db.execute("CREATE TABLE IF NOT EXISTS web_sessions(id TEXT PRIMARY KEY,student TEXT,title TEXT,created REAL,updated REAL)")
        self.db.commit()

    def close(self):
        self.owner.close()

    def start_practice(self, student, payload):
        from .contracts import fingerprint
        entry = self.owner.catalogue.item(payload["item_id"])
        if self.owner.catalogue.config and entry['grade'] != self.owner.catalogue.initial['grade']:
            raise Denied('practice outside student grade')
        digest = fingerprint(payload)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            previous = self.db.execute('SELECT assignment AS id,payload_hash FROM practice_starts WHERE student=? AND request_id=? UNION ALL SELECT id,payload_hash FROM practice_assignments WHERE student=? AND request_id=? LIMIT 1', (student, payload['request_id'], student, payload['request_id'])).fetchone()
            if previous:
                if previous["payload_hash"] != digest:
                    raise Denied("practice start request_id payload conflict")
                assignment_id = previous["id"]
            else:
                from .catalogue import complete_item
                from .contracts import ContractError
                if not complete_item(entry):
                    raise ContractError('题干缺少图表或公式不完整，暂不支持新练习。')
                existing = self.db.execute('SELECT id,created FROM practice_assignments WHERE student=? AND item_id=? AND version=? ORDER BY created DESC LIMIT 1', (student, entry['id'], self.owner.catalogue.version)).fetchone()
                ongoing = self.owner.practice_assignment(student, existing['id']) if existing else None
                # 同题重新点开不能制造新会话，也不能清除帮助记录来伪装首次独立作答。
                if ongoing and (not (ongoing['feedback'] or {}).get('correct') or time.time() - existing['created'] < 3 * 86400):
                    assignment_id = existing['id']
                else:
                    session_id, assignment_id, now = uuid.uuid4().hex, uuid.uuid4().hex, time.time()
                    self.db.execute("INSERT INTO web_sessions VALUES(?,?,?,?,?)", (session_id, student, self._practice_title(entry), now, now))
                    self.db.execute("INSERT INTO practice_assignments VALUES(?,?,?,?,?,?,?,?)", (assignment_id, student, session_id, entry["id"], self.owner.catalogue.version, payload["request_id"], digest, now))
                self.db.execute('INSERT INTO practice_starts VALUES(?,?,?,?)', (student, payload['request_id'], digest, assignment_id))
            value = self.owner.practice_assignment(student, assignment_id)
            self.db.commit()
            return value
        except Exception:
            self.db.rollback()
            raise

    def sessions(self, student):
        return [self._session_view(student, dict(r)) for r in self.db.execute("SELECT id,title,created,updated FROM web_sessions WHERE student=? ORDER BY updated DESC", (student,))]

    @staticmethod
    def _practice_title(entry):
        from .catalogue import complete_item
        stem = re.sub(r'[$\\{}]|\s+', '', entry['expression'])
        equations = [value for value in re.findall(r'\$([^$]+)\$', entry['expression']) if '=' in value and not value.strip().endswith('=')]
        snippet = '和谐方程 ' + (equations[-1] if equations else '') if '和谐方程' in stem else stem[:14] + ('…' if len(stem) > 14 else '')
        if not complete_item(entry):
            snippet = '原题不完整 · ' + snippet
        return entry['title'] + ' · ' + snippet

    def _session_view(self, student, meta):
        row = self.db.execute('SELECT item_id FROM practice_assignments WHERE student=? AND session=? ORDER BY created DESC LIMIT 1', (student, meta['id'])).fetchone()
        if row:
            meta['practice_item'] = row['item_id']
            meta['title'] = self._practice_title(self.owner.catalogue.item(row['item_id']))
        return meta

    def create(self, student, title="新的学习对话", initialize=None):
        id = uuid.uuid4().hex
        with self.db:
            self.db.execute("INSERT INTO web_sessions VALUES(?,?,?,?,?)", (id, student, title[:100], time.time(), time.time()))
            if initialize:initialize(id)
        return {"id": id, "title": title[:100]}

    def practice_history(self, student):
        from .learning import public_item
        from .catalogue import complete_item
        items = {}
        for row in self.db.execute("SELECT a.item_id,a.session,e.data,e.at FROM practice_events e JOIN practice_assignments a ON a.id=e.assignment WHERE e.student=? AND e.kind='answer' ORDER BY e.id DESC", (student,)):
            if row['item_id'] not in items:
                items[row['item_id']] = {'item': public_item(self.owner.catalogue.item(row['item_id'])), 'session': row['session'], 'source': '本产品作答', 'correct': json.loads(row['data'])['correct'], 'last_at': row['at']}
        for item_id in [] if self.owner.history_status()['suppress_imported'] else self.owner.catalogue.initial.get('historical_items', []):
            entry = self.owner.catalogue.bank.get(item_id)
            if item_id not in items and entry and complete_item(entry) and entry.get('grade') == self.owner.catalogue.initial.get('grade'):
                items[item_id] = {'item': public_item(entry), 'session': None, 'source': '导入历史作答 · 示例学生', 'correct': None, 'last_at': None}
        return list(items.values())[:100]

    def own(self, student, session):
        row = self.db.execute("SELECT * FROM web_sessions WHERE id=? AND student=?", (session, student)).fetchone()
        if not row:
            raise Denied("session not owned by selected student")
        return dict(row)

    def admit_teaching(self,student,session):
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            self.own(student,session)
            return self.owner.history_status()['epoch']

    def touch(self, student, session, question):
        self.own(student, session)
        with self.db:
            self.db.execute("UPDATE web_sessions SET updated=?,title=CASE WHEN title='新的学习对话' THEN ? ELSE title END WHERE id=? AND student=?", (time.time(), question[:26] or "学习对话", session, student))

    def detail(self, student, session):
        meta = self._session_view(student, self.own(student, session))
        messages = []
        for r in self.db.execute("SELECT id,request_id,request,state,response FROM runs WHERE student=? AND session=? ORDER BY id", (student, session)):
            state = json.loads(r["state"])
            request = json.loads(r["request"])
            effective = state.get('effective_request', request)
            display_input = {**request, **{k: effective[k] for k in ('expression', 'steps', 'course_query', 'subject') if k in effective}}
            response = project_response(json.loads(r["response"]),state) if r["response"] else None
            error_code=state.get('error_code') or ('model_protocol' if state.get('error') == 'protocol repair budget exhausted' or legacy_recognition_failure(state,request.get('images')) else None)
            usage=state.get('model_usage') or []
            if not response and state.get('annotation_source') and error_code=='model_protocol' and usage and usage[-1].get('finish_reason')=='length' and not usage[-1].get('tool_call_count'):
                # 旧自然标注截断记录只读升级分类，让用户保留原图重新回答；原失败账本不改。
                error_code='model_truncated'
            observations = project_observations(state.get("observations", []))
            events = [{"id": e["id"], "kind": e["kind"], "at": e["at"]} for e in self.db.execute("SELECT id,kind,at FROM events WHERE run_id=? ORDER BY id", (r["id"],))]
            messages.append({"request_id": r["request_id"], "input": display_input, "original_input": request, "response": response,
                             **({'partial_response':state['partial_text']} if not response and state.get('partial_text') else {}),
                             'images': [self.owner.image(student, image_id)['public'] for image_id in request.get('images', [])], 'recognized_question': state.get('vision', {}).get('text', ''),
                             "phase": state["phase"], "trace": {"route": safe_route(state.get("route")), "skills": list(state.get("skill_hashes", {})),
                             "observations": observations, "context": {"metrics": state.get("context", {}).get("metrics", {})}, "events": events,
                             "input_provenance": state.get('input_provenance', []),
                             "error": state.get("error_type"), "error_code": error_code}})
        row = self.db.execute('SELECT id FROM practice_assignments WHERE student=? AND session=? ORDER BY created DESC LIMIT 1', (student, session)).fetchone()
        # 历史 assignment 不等于当前教学任务，投影必须服从同一个已提交的任务态。
        detached = bool(self.owner.dialogue(Identity(student,session)).get('practice_detached'))
        if detached and row:
            # 旧版误解绑可由同一Store恢复原题，原题栏也必须服从恢复后的资源归属。
            current=self.owner.current_problem(Identity(student,session)) or {}
            if current.get('source')=='owned_catalogue_question' and current.get('assignment_id')==row['id']:detached=False
        return {"session": meta, "messages": messages, 'practice': self.owner.practice_assignment(student, row['id']) if row and not detached else None}

    def memory(self, student):
        episodes = [dict(r) for r in self.db.execute("SELECT kind,text,provenance,at,session FROM episodes WHERE student=? ORDER BY id DESC LIMIT 30", (student,))]
        facts = [dict(r) for r in self.db.execute("SELECT fact_key,value,source,trust,version,at FROM facts WHERE student=? ORDER BY id DESC LIMIT 20", (student,))]
        return {"episodes": episodes, "facts": facts}
