"""Launch real models with credentials only in process environment."""
from __future__ import annotations
import getpass
import json
import os
import queue
import shlex
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

EDUCATION = Path(__file__).resolve().parents[1]
connection = EDUCATION / "server/connection.local.json"
configuration = EDUCATION / "service/config/models.local.json"


def wait_for_workers(tunnel, key):
    configured = json.loads(configuration.read_text(encoding="utf-8-sig"))["models"]
    # vision 与 glm 使用云 API 凭据；把它们纳入专项检查会错用 SSH 令牌并返回 401。
    targets = [options for role, options in configured.items() if role in {"course8b", "difficulty8b", "review27b"} and options.get("enabled")]
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    deadline = time.monotonic() + 25
    last_error = "not_ready"
    while time.monotonic() < deadline:
        if tunnel.poll() is not None:
            raise SystemExit("SSH tunnel exited before specialist services became ready.")
        try:
            for options in targets:
                request = urllib.request.Request(options["base_url"].rstrip("/") + "/models", headers={"Authorization": "Bearer " + key})
                with opener.open(request, timeout=min(2, max(0.1, deadline - time.monotonic()))) as response:
                    data = json.load(response)
                if options["model"] not in {item["id"] for item in data["data"]}:
                    raise ValueError("unexpected specialist deployment")
            return
        except (OSError, ValueError, KeyError) as error:
            last_error = type(error).__name__ + (f" HTTP {error.code}" if hasattr(error, "code") else "")
            time.sleep(0.25)
    raise SystemExit("Specialist connections unavailable (" + last_error + "). Check SSH and retry.")


def start_tunnel(settings):
    target = f'{settings["user"]}@{settings["host"]}'
    ssh = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "-o", "ServerAliveInterval=30", "-o", "ServerAliveCountMax=3", "-p", str(settings["port"])]
    forwards = [part for port in (18008, 18009, 18027) for part in ("-L", f"127.0.0.1:{port}:127.0.0.1:{port}")]
    # 同一SSH连接读取凭据并承载转发；显式管道保持远端会话，关闭连接即退出远端读取进程。
    remote = "import sys; from pathlib import Path; print(Path(" + repr(settings["token_file"]) + ").read_text().strip(), flush=True); sys.stdin.buffer.read()"
    tunnel = subprocess.Popen([*ssh, "-o", "ExitOnForwardFailure=yes", *forwards, target, "python3 -c " + shlex.quote(remote)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    replies = queue.Queue()
    def read_credential():
        try:
            replies.put(tunnel.stdout.readline(513))
        except OSError:
            replies.put(b"")
    threading.Thread(target=read_credential, daemon=True).start()
    try:
        value = replies.get(timeout=20)
        if not value.endswith(b"\n") or not value.strip() or len(value) > 512:
            raise ValueError("invalid credential channel")
        return tunnel, value.decode("ascii").strip()
    except (queue.Empty, ValueError):
        tunnel.terminate()
        tunnel.wait(timeout=10)
        raise SystemExit("SSH credential connection failed. Check server connectivity and retry.")


def main():
    if not configuration.is_file():
        raise SystemExit("Configure service/config/models.local.json first.")
    env = dict(os.environ)
    if "--key-stdin" in sys.argv:
        print("Waiting for GLM credential on stdin (not saved).", flush=True)
        env["EDU_GLM_API_KEY"] = sys.stdin.readline().strip()
    else:
        env["EDU_GLM_API_KEY"] = env.get("EDU_GLM_API_KEY") or getpass.getpass("GLM API key (not saved): ")
    tunnel = None
    if connection.is_file():
        settings = json.loads(connection.read_text(encoding="utf-8-sig"))
        tunnel, env["EDU_WORKER_KEY"] = start_tunnel(settings)
    env.update(PYTHONPATH=str(EDUCATION / "service/src"), PYTHONIOENCODING="utf-8")
    arguments = [sys.executable, "-m", "qingqi.product", "--port", env.get("QINGQI_PORT", "18772"), "--config", str(configuration), "--origin", "http://127.0.0.1:18773", "--origin", "http://localhost:5173", "--origin", "http://127.0.0.1:5173"]
    accounts = EDUCATION / "service/config/accounts.local.json"
    if accounts.is_file():
        arguments += ["--accounts", str(accounts)]
    try:
        if tunnel:
            # 端口转发进程创建不代表模型已连接；认证模型列表通过后才启动产品HTTP入口。
            wait_for_workers(tunnel, env["EDU_WORKER_KEY"])
        subprocess.run(arguments, cwd=EDUCATION / "service", env=env, check=True)
    finally:
        if tunnel:
            tunnel.stdin.close()
            tunnel.terminate()
            tunnel.wait(timeout=10)


if __name__ == "__main__":
    main()
