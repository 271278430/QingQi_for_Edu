from __future__ import annotations

import hashlib
import json
import sqlite3
import unicodedata
from pathlib import Path


def norm(text: str) -> str:
    return "".join(unicodedata.normalize("NFKC", text).split()).casefold()


def lines(path: Path):
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def sha(path: Path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def build(source: Path, target: Path) -> dict:
    """Read existing source, build a separate index. Never modify original KG."""
    if target.exists():
        raise FileExistsError("index already exists; choose a new index path")
    target.parent.mkdir(parents=True, exist_ok=True)
    sources = {"nodes": source / "data_v1/nodes.jsonl", "edges": source / "data_v1/edges.jsonl",
               "prerequisite_candidates": source / "data/prerequisites_v1/haidian_prerequisite_candidates.jsonl"}
    db = sqlite3.connect(target)
    try:
        db.executescript("""
        CREATE TABLE nodes(id TEXT PRIMARY KEY,title TEXT,normalized TEXT,scope TEXT,type TEXT,description TEXT,source TEXT);
        CREATE INDEX node_title ON nodes(normalized);
        CREATE TABLE edges(id TEXT PRIMARY KEY,source TEXT,target TEXT,relation TEXT,provenance TEXT);
        CREATE INDEX edge_source ON edges(source,relation);
        CREATE INDEX edge_target ON edges(target,relation);
        CREATE TABLE prerequisites(id TEXT PRIMARY KEY,source TEXT,target TEXT,provenance TEXT);
        CREATE INDEX prereq_target ON prerequisites(target);
        CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT);
        """)
        counts = {}
        for n in lines(sources["nodes"]):
            attrs = n.get("attributes", {})
            desc = attrs.get("description", "")
            if not isinstance(desc, str):
                desc = json.dumps(desc, ensure_ascii=False)
            db.execute("INSERT INTO nodes VALUES(?,?,?,?,?,?,?)", (n["id"], n.get("title", ""), norm(n.get("title", "")), n["scope"], n["type"], desc, n["source_file"]))
        for e in lines(sources["edges"]):
            provenance = {k: e.get(k) for k in ("source_file", "row_index", "scope")}
            db.execute("INSERT INTO edges VALUES(?,?,?,?,?)", (e["id"], e["source"], e["target"], e["canonical_relation"], json.dumps(provenance, ensure_ascii=False)))
        if sources["prerequisite_candidates"].exists():
            for e in lines(sources["prerequisite_candidates"]):
                db.execute("INSERT INTO prerequisites VALUES(?,?,?,?)", (e["id"], e["source"], e["target"], json.dumps(e, ensure_ascii=False)))
        for table in ("nodes", "edges", "prerequisites"):
            counts[table] = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        report = {"counts": counts, "sources": {k: {"path": str(p.resolve()), "sha256": sha(p)} for k, p in sources.items() if p.exists()},
                  "prerequisite_policy": "title-aligned candidates only; NOT expert-confirmed prerequisites",
                  "dangling_edges": db.execute("SELECT COUNT(*) FROM edges e LEFT JOIN nodes s ON e.source=s.id LEFT JOIN nodes t ON e.target=t.id WHERE s.id IS NULL OR t.id IS NULL").fetchone()[0]}
        db.execute("INSERT INTO metadata VALUES('build',?)", (json.dumps(report, ensure_ascii=False),))
        db.commit()
        return report
    finally:
        db.close()


class Graph:
    def __init__(self, path: Path):
        self.db = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
        self.db.row_factory = sqlite3.Row

    def close(self):
        self.db.close()

    def search(self, query: str, subject: str = "", limit: int = 5) -> dict:
        q = norm(query)
        if not q:
            return {"matches": [], "ambiguous": False, "method": "empty_query"}
        pattern = "%" + q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        subject_pattern = "%" + subject.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
        rows = self.db.execute("SELECT id,title,scope,type,source,normalized FROM nodes WHERE normalized LIKE ? ESCAPE '\\' AND scope LIKE ? ESCAPE '\\' ORDER BY normalized=? DESC,length(title),id LIMIT ?",
                               (pattern, subject_pattern, q, limit + 1)).fetchall()
        exact = [r for r in rows if r["normalized"] == q]
        selected = exact if exact else rows
        return {"matches": [{k: r[k] for k in ("id", "title", "scope", "type", "source")} for r in selected[:limit]],
                "ambiguous": len(selected) > 1, "method": "exact_title" if exact else "title_substring"}

    def context(self, node_id: str) -> dict:
        root = self.db.execute("SELECT * FROM nodes WHERE id=?", (node_id,)).fetchone()
        if not root:
            raise ValueError("unknown graph node")
        evidence = [{"ref": "node:" + root["id"], "text": (root["title"] + "。" + root["description"])[:1200], "source": root["source"]}]
        ancestors, visited, frontier = [], {node_id}, [node_id]
        for _ in range(3):
            next_frontier = []
            for target in frontier:
                for e in self.db.execute("SELECT e.*,n.title,n.type,n.source AS node_source FROM edges e JOIN nodes n ON e.source=n.id WHERE e.target=? AND e.relation IN ('contains','maps_to') ORDER BY e.id LIMIT 12", (target,)):
                    if e["source"] in visited or len(ancestors) >= 12:
                        continue
                    visited.add(e["source"])
                    next_frontier.append(e["source"])
                    ancestors.append({"id": e["source"], "title": e["title"], "type": e["type"], "relation": e["relation"]})
                    evidence.append({"ref": "edge:" + e["id"], "text": f'{e["title"]} --{e["relation"]}--> {target}', "source": e["provenance"]})
            frontier = next_frontier
        prerequisites = []
        for p in self.db.execute("SELECT p.*,n.title FROM prerequisites p JOIN nodes n ON p.source=n.id WHERE p.target=? ORDER BY p.id LIMIT 12", (node_id,)):
            provenance = json.loads(p["provenance"])
            mounted = provenance.get('source_dataset') == 'mounted_math_textbooks'
            prerequisites.append({"id": p["source"], "title": p["title"], "status": "mounted_unverified_candidate" if mounted else "title_aligned_unverified_candidate"})
            evidence.append({"ref": "candidate:" + p["id"], "text": f'{p["title"]} → {root["title"]}（' + ('教材挂载先修候选' if mounted else '同名对齐候选') + '，未专家确认）', "source": provenance["source_dataset"] + "@" + provenance["source_revision"]})
        return {"node_id": node_id, "title": root["title"], "scope": root["scope"], "ancestors": ancestors,
                "prerequisite_candidates": prerequisites, "evidence": evidence,
                "prerequisite_status": "unverified_candidates" if prerequisites else "no_confirmed_evidence"}
