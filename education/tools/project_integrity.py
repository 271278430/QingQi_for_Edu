"""Read-only fingerprints for cleanup verification; never emits student contents or credentials."""
from pathlib import Path
import hashlib
import json
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / 'education/.local/reports'


def snapshot():
    paths = set()
    for folder in ('service/config', 'server'):
        paths.update((ROOT / 'education' / folder).glob('*.local.json'))
    paths.update(p for p in (ROOT/'education/service/data').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    paths.update(p for p in (ROOT/'education/service/runs/product').rglob('*') if p.is_file() and not p.name.endswith(('-wal', '-shm')))
    result = {}
    for p in sorted(paths):
        with p.open('rb') as file:
            signature = file.read(16)
        if signature == b'SQLite format 3\x00' and 'product' in p.parts:
            with sqlite3.connect(p.as_uri()+'?mode=ro', uri=True) as db:
                tables = {}
                for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
                    name = '"'+table.replace('"', '""')+'"'
                    hashes = []
                    for row in db.execute('SELECT * FROM '+name):
                        hashes.append(hashlib.sha256(repr(tuple(row)).encode('utf-8')).hexdigest())
                    tables[table] = {'rows':len(hashes), 'sha256':hashlib.sha256('\n'.join(sorted(hashes)).encode()).hexdigest()}
                result[str(p.relative_to(ROOT))] = {'tables':tables}
        else:
            with p.open('rb') as file:
                result[str(p.relative_to(ROOT))] = {'sha256':hashlib.file_digest(file, 'sha256').hexdigest(), 'bytes':p.stat().st_size}
    return result


if __name__ == '__main__':
    REPORTS.mkdir(parents=True, exist_ok=True)
    mode = sys.argv[1] if len(sys.argv)>1 else 'before'
    if mode not in {'before', 'after'}: raise SystemExit('Use before or after')
    data = snapshot()
    (REPORTS/f'project-integrity-{mode}.local.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    if mode == 'after':
        before = json.loads((REPORTS/'project-integrity-before.local.json').read_text(encoding='utf-8'))
        different = [p for p in sorted(set(before)|set(data)) if before.get(p) != data.get(p)]
        print(json.dumps({'protected_files':len(data), 'unchanged':not different, 'changed_paths':different}, ensure_ascii=False))
        if different: raise SystemExit(1)
    else:
        print(json.dumps({'protected_files':len(data), 'snapshot':'before', 'read_only':True}))
