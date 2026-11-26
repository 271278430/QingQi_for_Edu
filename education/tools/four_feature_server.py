"""Isolated four-feature browser fixture using the real product server."""
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service/src"))
from qingqi.agent import PROJECT
from qingqi.product import server
from qingqi.learning import BANK
from qingqi.domain_tools import number

instance = server(0, root=PROJECT / "runs/four-feature-browser" / uuid.uuid4().hex)
print(json.dumps({"base": f"http://127.0.0.1:{instance.server_port}", "answers": {i: str(number(e['expression'])) for i, e in BANK.items()}}), flush=True)
try:
    instance.serve_forever()
finally:
    instance.server_close()
