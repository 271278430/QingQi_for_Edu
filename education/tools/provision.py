"""Interactive local account provisioning; never print credentials."""
import argparse
import getpass
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service/src"))
from qingqi.product import password_hash

parser = argparse.ArgumentParser()
parser.add_argument("--id", required=True)
parser.add_argument("--name", required=True)
parser.add_argument("--role", choices=["student", "teacher"], required=True)
args = parser.parse_args()
target = Path(__file__).resolve().parents[1] / "service/config/accounts.local.json"
value = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {"accounts": {}}
if args.id in value["accounts"]:
    raise SystemExit("Account already exists; choose a new id or explicitly edit the deployment file.")
password = getpass.getpass("Password (at least 12 characters): ")
if len(password) < 12 or password != getpass.getpass("Confirm password: "):
    raise SystemExit("Password requirements not met.")
value["accounts"][args.id] = {"name": args.name, "role": args.role, "password_hash": password_hash(password)}
temporary = target.with_suffix(".tmp")
temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
temporary.replace(target)
print("Account provisioned. Restart the education service to enable account mode.")
