"""Build a private, versioned mathematics catalogue from user-provided sources."""
import argparse
import collections
import csv
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service/src"))
from qingqi.agent import PROJECT
from qingqi.catalogue import answer_key, missing_context, normalized, stem_key, text
from qingqi.contracts import canonical
from qingqi.graph import norm, sha

MATH_SUBJECTS = {"数学", "小学数学", "初中数学", "高中数学"}
SCHEMA = """
CREATE TABLE nodes(id TEXT PRIMARY KEY,title TEXT,normalized TEXT,scope TEXT,type TEXT,description TEXT,source TEXT);
CREATE INDEX node_title ON nodes(normalized);
CREATE TABLE edges(id TEXT PRIMARY KEY,source TEXT,target TEXT,relation TEXT,provenance TEXT);
CREATE INDEX edge_source ON edges(source,relation);
CREATE INDEX edge_target ON edges(target,relation);
CREATE TABLE prerequisites(id TEXT PRIMARY KEY,source TEXT,target TEXT,provenance TEXT);
CREATE INDEX prereq_target ON prerequisites(target);
CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT);
CREATE TABLE items(id TEXT PRIMARY KEY,eligible INTEGER,data TEXT);
CREATE TABLE aliases(qid TEXT PRIMARY KEY,item_id TEXT,reason TEXT);
"""


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def jsonlines(path):
    with path.open(encoding="utf-8-sig") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def graph_import(db, root):
    books, nodes, edges, sources = [], {}, {}, []
    kps, grade7 = {}, set()
    dangling = ambiguous = 0
    for manifest in sorted(root.glob("*/manifest.json")):
        m = read(manifest)
        book = m["book"]
        if book.get("subject") not in MATH_SUBJECTS:
            continue
        books.append(book)
        sources.append(sha(manifest))
        book_id = str(book.get("bookId", book["id"]))
        local = collections.defaultdict(list)
        scope = "数学 / " + book.get("grade", "") + " / " + book["name"].removesuffix(".pdf")
        for kind, info in m["entityFiles"].items():
            path = manifest.parent / info["path"]
            sources.append(sha(path))
            for e in read(path)["entities"]:
                source_id = str(e["id"])
                node_id = ("kp:" if kind == "KnowledgeItem" else "tp:" if kind == "TestingPoint" else book_id + ":" + kind + ":") + source_id
                local[source_id].append(node_id)
                nodes.setdefault(node_id, (node_id, e["name"], norm(e["name"]), scope, kind, text(e.get("path", "")), "math_textbook_graph@" + book_id))
                if kind == "KnowledgeItem":
                    kps[node_id] = {"id": node_id, "title": e["name"], "objective": "理解并运用“" + e["name"] + "”，通过实际作答确认起点。", "requires": [], "graph_id": node_id}
                    if "七年级" in book.get("grade", "") or "七年级" in book["name"]:
                        grade7.add(node_id)
        # 部分教材只提供实体清单；不凭文件夹名称补造先修关系。
        for relation, info in m.get("relationFiles", {}).items():
            path = manifest.parent / info["path"]
            sources.append(sha(path))
            for e in read(path)["edges"]:
                left, right = local[str(e["source"])], local[str(e["target"])]
                if not left or not right:
                    dangling += 1
                    continue
                if len(left) != 1 or len(right) != 1:
                    ambiguous += 1
                    continue
                source, target = left[0], right[0]
                edge_id = digest([source, target, relation])
                edges.setdefault(edge_id, (edge_id, source, target, relation, canonical({"source_dataset": "mounted_math_textbooks", "source_revision": "local_v1", "book": book_id, "relation": relation})))
    db.executemany("INSERT INTO nodes VALUES(?,?,?,?,?,?,?)", nodes.values())
    db.executemany("INSERT INTO edges VALUES(?,?,?,?,?)", edges.values())
    prereqs = [e for e in edges.values() if e[3] in {"concept_prereq_of", "apply_prereq_of", "step_prereq_of"}]
    db.executemany("INSERT INTO prerequisites VALUES(?,?,?,?)", [(e[0], e[1], e[2], e[4]) for e in prereqs])
    for e in prereqs:
        if e[1] in kps and e[2] in kps:
            if e[1] not in kps[e[2]]["requires"]:
                kps[e[2]]["requires"].append(e[1])
    return kps, grade7, sources, {"math_books": len(books), "nodes": len(nodes), "edges": len(edges), "prerequisite_candidates": len(prereqs), "dangling_edges_skipped": dangling, "ambiguous_edges_skipped": ambiguous}


def question_import(db, path, kps, version):
    groups = collections.defaultdict(list)
    records = jsonlines(path)
    for q in records:
        # 此文件本身是成功输出，status 是标注流水线状态而不是统一 success 枚举。
        groups[digest([stem_key(q["stem"]), [normalized(o) for o in q.get("options") or []], q.get("images")])].append(q)
    counts = collections.Counter()
    topics_with_items = set()
    for group_id, rows in groups.items():
        q = rows[0]
        opts = [text(o) for o in q.get("options") or []]
        keys = [answer_key(r.get("answer"), opts) for r in rows]
        comparisons = [canonical(k) if k else canonical([normalized(a) for a in (r.get("answer") if isinstance(r.get("answer"), list) else [r.get("answer")])]) for r, k in zip(rows, keys)]
        conflict = len(set(comparisons)) > 1
        ids = sorted({"kp:" + str(p["kpoint_id"]) for row in rows for p in row.get("kpoints") or []} & kps.keys())
        stem = text(q["stem"])
        has_image = missing_context(q['stem']) or any(missing_context(o) for o in q.get('options') or []) or bool((q.get("images") or {}).get("stem")) or bool((q.get("images") or {}).get("options"))
        # 自动标注成功不等于答案正确；冲突或图形缺失整组退出自动计分。
        reason = "answer_conflict" if conflict else "grade_conflict" if len({r['grade'] for r in rows}) > 1 else "unmapped_math_topic" if not ids else "image_required" if has_image else "unsupported_answer" if not keys[0] else "low_confidence" if not any(r.get('status') == '成功' for r in rows) else "eligible"
        counts[reason] += 1
        item_id = "q:" + group_id[:24]
        topic = max(ids, key=lambda i: len(kps[i]['title']) if normalized(kps[i]['title']) in normalized(stem) else 0) if ids else ""
        difficulty = float(q.get("difficulty") or .5)
        entry = {"id": item_id, "topic": topic, "topics": ids, "title": kps[topic]["title"] if topic else "数学", "expression": stem,
                 "options": opts, "form": q.get("form", ""), "level": 1 if difficulty <= .35 else 3 if difficulty >= .65 else 2,
                 "grade": str(q.get("grade", "")), "version": version, "key": keys[0], "answer_kind": keys[0]["kind"] if keys[0] else "pending",
                 "answer_count": len(keys[0]["values"]) if keys[0] else 0, "analysis": text(q.get("analysis")), "source": "题库自动标注（未教研确认）", "source_qids": [r["qid"] for r in rows]}
        eligible = reason == "eligible"
        db.execute("INSERT INTO items VALUES(?,?,?)", (item_id, int(eligible), canonical(entry)))
        db.executemany("INSERT INTO aliases VALUES(?,?,?)", [(r["qid"], item_id, reason) for r in rows])
        if eligible and entry["grade"] == "7":
            topics_with_items.add(topic)
    return topics_with_items, {"source_questions": len(records), "unique_content": len(groups), "duplicates_merged": len(records)-len(groups), "question_quality": dict(counts)}


def student_import(profiles, conversations, db):
    candidates = [p for p in jsonlines(profiles) if p.get("subject") == "数学"]
    profile = max(candidates, key=lambda p: p["n_attempts"])
    kp_stats = {"kp:" + str(p["kpoint_id"]): p for p in profile["kp_stats"]}
    qids = {q for p in profile["kp_stats"] for q in p["questions"]}
    seen = [r[0] for r in db.execute("SELECT DISTINCT item_id FROM aliases WHERE qid IN (" + ",".join("?" for _ in qids) + ")", sorted(qids))]
    with conversations.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        columns = sorted((c for c in reader.fieldnames if re.fullmatch(r"output.content\[0\].content\[\d+\].text", c)), key=lambda c: int(re.findall(r"\[(\d+)\]", c)[1]))
        by_user = collections.defaultdict(list)
        for row in reader:
            prompt = text(row.get("input.prompt"))
            output = "\n".join(text(row.get(c)) for c in columns if row.get(c))
            if re.search(r"英语|语文|物理|化学|生物|历史|地理|电流|电压|牛顿|速度|受力|古诗|单词|阅读理解", prompt + output):
                continue
            if not re.search(r"数学|方程|有理数|分数|整式|因式分解|二次函数|一元|代数|几何|三角形|数轴|绝对值|通分|解不等式|科学[计记]数法", prompt + output):
                continue
            by_user[row["user.id"]].append({"source_id": row["_id"], "prompt": prompt, "response": output, "created_at": row.get("created_at", "")})
    user, selected = max(by_user.items(), key=lambda pair: len(pair[1]))
    initial = {"identity": "示例学生（画像与会话来源未关联）", "grade": str(profile["grade"]), "subject": "数学", "as_of": profile["as_of"], "n_attempts": profile["n_attempts"], "topics": kp_stats,
               "historical_items": seen, "history_count": len(selected), "identity_link": "unlinked_example", "source": "数学画像初始化（源模型估计）"}
    return initial, selected, {"math_profiles": len(candidates), "initial_attempts": profile["n_attempts"], "initial_topics": len(kp_stats), "conversation_math_records": len(selected), "identity_link": "unlinked_example"}, {"profile_student_id": profile["student_id"], "csv_user_id": user}


def build(args):
    report_path = PROJECT.parent / ".local/reports/student-data-import.json"
    # 创建独立版本目录；任何失败不会修改正在使用的 registry。
    source_hashes = [sha(args.questions), sha(args.profiles), sha(args.conversations)]
    manifests = sorted(p for p in args.books.glob("*/manifest.json") if read(p)["book"].get("subject") in MATH_SUBJECTS)
    for manifest in manifests:
        m = read(manifest)
        source_hashes.append(sha(manifest))
        source_hashes.extend(sha(manifest.parent / i["path"]) for i in [*m["entityFiles"].values(), *m.get("relationFiles", {}).values()])
    version = "math_student_v1_" + digest(["import_rules_v5", source_hashes])[:16]
    folder = PROJECT / "data" / version
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "catalogue.sqlite"
    if not target.exists():
        stage = folder / "catalogue.tmp.sqlite"
        if stage.exists():
            stage.unlink()
        db = sqlite3.connect(stage)
        try:
            db.executescript(SCHEMA)
            kps, grade7, _, graph_report = graph_import(db, args.books)
            available, question_report = question_import(db, args.questions, kps, version)
            if not available:
                raise ValueError("没有同年级可自动核验的数学题，禁止发布空题库。")
            initial, history, student_report, identity = student_import(args.profiles, args.conversations, db)
            selected = available | (initial["topics"].keys() & kps.keys())
            topics = [dict(kps[i], requires=[r for r in kps[i]["requires"] if r in selected]) for i in sorted(selected)]
            # 多标签题只储存一次；主标签必须位于可用同年级数学主题。
            report = {"version": version, **graph_report, **question_report, **student_report, "grade": initial["grade"], "selectable_topics": len(topics), "graph_grade7_topics": len(grade7), "source_hashes": source_hashes}
            report['eligible_by_grade'] = dict(collections.Counter(json.loads(r[0])['grade'] for r in db.execute('SELECT data FROM items WHERE eligible=1')))
            report['initial_topics_mapped'] = len(initial['topics'].keys() & kps.keys())
            coverage = f"数学教材 {graph_report['math_books']} 本 · 去重题库 {question_report['unique_content']} 题 · 七年级个性化学习"
            metadata = {"version": version, "student_initial": initial, "student_history": history, "topics": topics, "coverage": coverage, "import_report": report}
            db.executemany("INSERT INTO metadata VALUES(?,?)", [(k, canonical(v)) for k, v in metadata.items()])
            db.commit()
            (folder / "identity.local.json").write_text(canonical(identity), encoding="utf-8")
        finally:
            db.close()
        stage.replace(target)
    else:
        with sqlite3.connect(target) as db:
            report = json.loads(db.execute("SELECT value FROM metadata WHERE key='import_report'").fetchone()[0])
    args.root.mkdir(parents=True, exist_ok=True)
    registry = {"path": str(target.resolve()), "version": version, "profile": "math-student", "student": "edu-math-student", "name": "我的数学学习"}
    existing = args.root / "agent.sqlite"
    if existing.exists():
        with sqlite3.connect(existing) as db:
            versions = [r[0] for r in db.execute("SELECT DISTINCT version FROM practice_assignments WHERE student='edu-math-student'")]
            if any(v != version for v in versions):
                raise ValueError("已有练习依赖旧数据版本；请选择新的学生运行目录。")
    pending = args.root / "catalogue.tmp"
    pending.write_text(canonical(registry), encoding="utf-8")
    pending.replace(args.root / "catalogue.local.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "source_hashes"}, ensure_ascii=False))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    # 公开导入入口不绑定开发者磁盘；明确选择资料，避免新机器误用本机路径。
    p.add_argument("--books", type=Path, required=True)
    p.add_argument("--questions", type=Path, required=True)
    p.add_argument("--profiles", type=Path, required=True)
    p.add_argument("--conversations", type=Path, required=True)
    p.add_argument("--root", type=Path, default=PROJECT / "runs/product")
    build(p.parse_args())
