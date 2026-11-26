"""Private fixture for browser hint interactions; never binds the production database."""
import json
import sys
from grounded_hint_acceptance import fixture
from qingqi.storage import Store

root,instance,model,calls=fixture();owner=Store(root)
entry=next(e for e in owner.catalogue.bank.values() if 'mx-8=5x+n' in e['expression'].replace(' ','') and '个位' not in e['expression'])
print(json.dumps({'base':f'http://127.0.0.1:{instance.server_port}','item':entry['id']}),flush=True)
try:sys.stdin.buffer.read()
finally:owner.close();instance.shutdown();instance.server_close();model.shutdown();model.server_close()
