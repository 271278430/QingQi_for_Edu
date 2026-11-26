"""Real-data browser fixture; isolated history and no real model calls."""
import json
from student_data_acceptance import fixture_root, server
from qingqi.web_store import WebStore

root = fixture_root()
store = WebStore(root)
for index in range(8):
    store.create('edu-math-student', '复习记录 ' + str(index + 1))
entry = next(e for e in store.owner.catalogue.bank.values() if '和谐方程' in e['expression'] and '4x-2=x+10' in e['expression'].replace(' ', ''))
assignment = store.start_practice('edu-math-student', {'item_id': entry['id'], 'request_id': 'fixture-start'})
store.close()
instance = server(0, root=root)
print(json.dumps({'base': f'http://127.0.0.1:{instance.server_port}', 'assignment': assignment}, ensure_ascii=False), flush=True)
instance.serve_forever()
