"""Private, bounded adapter to the actual ZCode public runtime capabilities."""
from __future__ import annotations

import os
import queue
import shutil
import signal
import subprocess
import sys
import threading
from dataclasses import asdict
from pathlib import Path

from .contracts import ContractError, Denied, canonical, fingerprint, validate

VERSION = "zcode_education_capabilities_v1"
MAX_FRAME = 512000


class RuntimeFailure(RuntimeError):
    def __init__(self, code, message, recoverable=False, retry_after=None):
        super().__init__(message)
        self.code, self.recoverable, self.retry_after = code, recoverable, retry_after


class ZCodeRuntime:
    def __init__(self, graph, specs, handlers, root):
        self.service = Path(__file__).resolve().parents[2]
        self.repo = self.service.parents[1]
        self.graph, self.specs, self.handlers, self.root = graph, specs, handlers, root
        self.process, self.counter = None, 0
        self.messages = queue.Queue()
        self.scope = {"trace_id": fingerprint({"root": str(root)}), "session_id": "education-runtime"}
        self.callback_trace = None

    def bind_scope(self, identity, request_id):
        if self.process:
            self.close()
        self.scope = {"trace_id": fingerprint({"student": identity.student, "session": identity.session, "request": request_id}),
                      "session_id": "edu-" + fingerprint({"student": identity.student, "session": identity.session})[:24]}

    def start(self):
        if self.process and self.process.poll() is None:
            return
        script = self.service.parent / "runtime/dist/server.js"
        if not script.is_file():
            raise RuntimeFailure("runtime_not_built", "请先构建教育后台运行能力。")
        bundled = self.repo / "tmp/node24" / ("node.exe" if os.name == "nt" else "bin/node")
        node = os.environ.get("QINGQI_NODE") or (str(bundled) if bundled.is_file() else shutil.which("node"))
        if not node:
            raise RuntimeFailure("runtime_unavailable", "教育后台需要 Node 24。")
        self.messages = queue.Queue()
        self.process = subprocess.Popen([node, str(script)], cwd=self.repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1,
                                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                                        start_new_session=os.name != "nt")
        process = self.process
        def read():
            try:
                for line in process.stdout:
                    if len(line.encode()) > MAX_FRAME:
                        raise RuntimeFailure("runtime_protocol", "后台消息过大。")
                    import json
                    self.messages.put(json.loads(line))
            except Exception as error:
                self.messages.put(error)
            finally:
                self.messages.put(EOFError("runtime closed"))
        threading.Thread(target=read, daemon=True).start()
        self.rpc("init", {"python": sys.executable, "root": str(self.root), "graph_path": str(self.graph.resolve()), **self.scope, "specs": [asdict(spec) for spec in self.specs.values()]}, start=False)

    def _write(self, value):
        raw = canonical(value)
        if len(raw.encode()) > MAX_FRAME:
            raise ContractError("runtime frame exceeds bound")
        try:
            self.process.stdin.write(raw + "\n")
            self.process.stdin.flush()
        except (OSError, ValueError) as error:
            # Node 在启动/执行边界退出时管道可能先断；应返回稳定后台错误而不是 HTTP 500。
            raise RuntimeFailure("runtime_unavailable", "教学后台连接中断，进度已保留。", True) from error

    def rpc(self, op, value, timeout=30, *, start=True):
        if start:
            self.start()
        self.counter += 1
        request_id = self.counter
        self._write({"id": request_id, "op": op, "input": value})
        while True:
            try:
                response = self.messages.get(timeout=timeout)
            except queue.Empty:
                self.close(force=True)
                raise RuntimeFailure("runtime_timeout", "教学后台超时，已保留请求进度。") from None
            if isinstance(response, Exception):
                if isinstance(response, RuntimeFailure):
                    raise response
                raise RuntimeFailure("runtime_unavailable" if isinstance(response, EOFError) else "runtime_protocol",
                                     "教学后台未返回有效协议结果，进度已保留。", isinstance(response, EOFError)) from response
            if "callback" in response:
                callback = response["callback"]
                try:
                    name, args = response["name"], response["arguments"]
                    # Node 只能执行当前已授权调用；回调不能另开工具或改写本轮输入。
                    # JS 序列化 2.0 会返回 2；按 JSON 数值语义比较，仍保留 bool/数值和所有字段边界。
                    def wire_json(item):
                        if isinstance(item,float) and item.is_integer():return int(item)
                        if isinstance(item,list):return [wire_json(v) for v in item]
                        if isinstance(item,dict):return {k:wire_json(v) for k,v in item.items()}
                        return item
                    if op != "call" or name != value["name"] or canonical(wire_json(args)) != canonical(wire_json(value["arguments"])) or name not in self.handlers:
                        raise Denied("runtime callback differs from authorized call")
                    validate(args, self.specs[name].input_schema)
                    self.callback_trace = response.get("trace")
                    result = self.handlers[name](**args)
                    validate(result, self.specs[name].output_schema)
                    self._write({"callback": callback, "result": result})
                except Exception as error:
                    self._write({"callback": callback, "error": {"code": getattr(error, "code", "model_failed"), "message": str(error)[:200], "recoverable": getattr(error, "recoverable", False), "retry_after": getattr(error, "retry_after", None)}})
                continue
            if response.get("id") != request_id:
                raise RuntimeFailure("runtime_protocol", "后台消息编号不符。")
            if "error" in response:
                error = response["error"]
                raise RuntimeFailure(error["code"], error["message"], error.get("recoverable", False), error.get("retry_after"))
            return response["result"]

    def call(self, name, args, timeout):
        return self.rpc("call", {"name": name, "arguments": args, "timeout_ms": timeout * 1000}, timeout=timeout + 20)

    def close(self, force=False):
        process = self.process
        if not process:
            return
        if not force and process.poll() is None:
            try:
                self.rpc("close", {}, timeout=5, start=False)
                process.stdin.close()
                process.wait(timeout=5)
            except (Exception,):
                force = True
        if process.poll() is None:
            # 仅结束本轮创建的 Node/MCP 子树；模型服务器与其他进程不属于此树。
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW, timeout=5)
            else:
                os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=5)
        self.process = None
