"""Isolated, authored demonstration for reproducible public screenshots."""
import json
import sys
import threading
import uuid
from demo import prepare
from qingqi.agent import PROJECT
from qingqi.catalogue import Catalogue
from qingqi.product import server

root=prepare(PROJECT/'runs/media-demo'/uuid.uuid4().hex)
catalogue=Catalogue(root)
ids=['order-1','order-2','brackets-1','fractions-1','signed-1','decimals-1']
answers={id:catalogue.item(id)['key']['values'][0] for id in ids}
catalogue.close()
instance=server(0,root=root)
threading.Thread(target=instance.serve_forever,daemon=True).start()
print(json.dumps({'base':f'http://127.0.0.1:{instance.server_port}','answers':answers}),flush=True)
try:sys.stdin.buffer.read()
finally:instance.shutdown();instance.server_close()
