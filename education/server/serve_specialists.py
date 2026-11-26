"""Loopback OpenAI adapter for original training formats; one model per process.

Deployment owns paths, GPU and authentication. Student input cannot select them.
Numerical review combines real 27B inference with an independent exact checker.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from qingqi.contracts import validate
from qingqi.domain_tools import number, review
from qingqi.workers import COURSE_IN, COURSE_OUT
from qingqi.domain_tools import SPECS

LABELS = {"Recall Failure": "recall_failure_candidate", "Conceptual Gap": "conceptual_gap_candidate", "Procedural Error": "procedural_error_candidate", "Transfer Deficit": "transfer_deficit_candidate"}
STRATEGIES = {"Recall Failure": "请回忆一道做对过的类似题，说明你当时采用的步骤，再核对本题。", "Conceptual Gap": "请先用自己的话解释相关概念并举一个例子，我再根据你的解释提供提示。", "Procedural Error": "请逐步说明你怎样确定运算顺序，我们先检查第一处有疑问的步骤。", "Transfer Deficit": "请找一道相似的已学例题，比较条件与解法，再尝试把方法应用到本题。"}


def native_messages(role, args, system):
    if role == "course8b":
        user = f'在 K12-KGraph 的数学义教教材图谱中，“{args["query"]}”对应的课程章节有哪些？'
    elif role == "review27b":
        user = json.dumps({"problem": "计算：" + args["expression"], "student_steps": [{"step_id": i + 1, "claim": s["equation"]} for i, s in enumerate(args["steps"])], "help_mode": "socratic" if args["mode"] == "socratic" else "explain", "curriculum_evidence": []}, ensure_ascii=False)
    else:
        history = "\n".join(f'[{i+1}]\n来源: {h["kind"]}\n{h["text"]}' for i, h in enumerate(args["history"]))
        checked = args.get("review")
        current = "当前没有可核验作答。" if not checked else f'已独立核验：{checked["status"]}；首错从0开始={checked["first_error"]}。实际步骤：' + json.dumps(checked["evidence"], ensure_ascii=False)
        user = f"### INTERACTION HISTORY\n{history or 'Unknown'}\n### CURRENT QUESTION\n{current}\n### MEMORY QUERIES\n- Q1: 学生实际报告了哪些困难？\n- Q2: 已有记录能否证明此前掌握？\n- Q3: 是否有足够证据确认长期学情？\nAnalyze the data and generate the JSON response."
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def normalize(role, args, text):
    text = text.strip()
    if text.startswith("```json") and text.endswith("```"):
        text = text[7:-3].strip()
    if role == "course8b":
        names = list(dict.fromkeys(n.strip() for n in re.split(r"[；;\n]+", text) if n.strip()))
        value = {"suggested_titles": names, "status": "candidate_requires_graph_confirmation"}
        validate(value, COURSE_OUT)
        return value
    native = json.loads(text)
    if role == "review27b":
        checked = review(**args)
        if checked["status"] == "unsupported":
            raise ValueError("numeric_domain_unsupported")
        first = None if checked["first_error"] == -1 else checked["first_error"] + 1
        correct = checked["status"] in {"correct", "no_steps"}
        expected_action = "confirm" if correct else "probe" if args["mode"] == "socratic" else "explain"
        if type(native.get("work_correct")) is not bool or native["work_correct"] != correct or native.get("first_error_step") != first or native.get("action") != expected_action or number(str(native.get("correct_answer", ""))) != number(checked["answer"]):
            raise ValueError("review_model_symbolic_disagreement")
        # 原生27B只有首错；不能冒充它输出了逐步checks，checks来自独立核验。
        return checked
    label = native.get("diagnosis")
    if label not in LABELS or not isinstance(native.get("content"), str) or not isinstance(native.get("reason"), str):
        raise ValueError("native_diagnosis_contract")
    evidence = [{"ref": f"history:{i}", "text": h["text"], "source": h["kind"]} for i, h in enumerate(args["history"])]
    if args.get("review"):
        evidence += args["review"]["evidence"]
    # 8B生成的memory/content不覆盖学生事实；只公开候选及与分类对应的追问策略。
    return {"candidates": [LABELS[label]] if evidence else ["insufficient_evidence"], "certainty": "candidate_requires_confirmation", "strategy": STRATEGIES[label], "evidence": evidence[:40]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--role", choices=["course8b", "difficulty8b", "review27b"], required=True)
    options = parser.parse_args()
    config = json.loads(options.config.read_text())
    item = config["models"][options.role]
    os.environ.update(CUDA_VISIBLE_DEVICES=str(item["gpu"]), HF_HUB_OFFLINE="1", TOKENIZERS_PARALLELISM="false", PYTHONDONTWRITEBYTECODE="1")
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, Qwen3_5ForConditionalGeneration
    from peft import PeftModel
    torch.set_num_threads(4)
    tokenizer = AutoTokenizer.from_pretrained(item["base"], local_files_only=True)
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    cls = Qwen3_5ForConditionalGeneration if options.role == "review27b" else AutoModelForCausalLM
    model = cls.from_pretrained(item["base"], local_files_only=True, dtype=torch.bfloat16, device_map={"": 0}, attn_implementation="sdpa")
    if item.get("adapter"):
        model = PeftModel.from_pretrained(model, item["adapter"], is_trainable=False)
    model.eval()
    token = Path(config["token_file"]).read_text().strip()
    if len(token) < 32:
        raise ValueError("service credential required")
    gate = threading.Lock()
    schema = COURSE_IN if options.role == "course8b" else SPECS["review_arithmetic" if options.role == "review27b" else "difficulty_candidates"].input_schema

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, code, value):
            raw = json.dumps(value, ensure_ascii=False, allow_nan=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            try:
                self.wfile.write(raw)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def authenticated(self):
            return hmac.compare_digest(self.headers.get("Authorization", ""), "Bearer " + token)

        def do_GET(self):
            if not self.authenticated():
                return self.reply(401, {"error": "unauthorized"})
            return self.reply(200, {"object": "list", "data": [{"id": item["name"], "object": "model", "owned_by": "qingqi"}]}) if self.path == "/v1/models" else self.reply(404, {"error": "not_found"})

        def do_POST(self):
            if not self.authenticated():
                return self.reply(401, {"error": "unauthorized"})
            if self.path != "/v1/chat/completions":
                return self.reply(404, {"error": "not_found"})
            if not gate.acquire(blocking=False):
                return self.reply(429, {"error": "specialist_busy"})
            try:
                self.connection.settimeout(15)
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 64000:
                    raise ValueError("input_bound")
                body = json.loads(self.rfile.read(size))
                if body.get("model") != item["name"] or body.get("stream"):
                    raise ValueError("unsupported_request")
                args = json.loads(body["messages"][-1]["content"])["input"]
                validate(args, schema)
                messages = native_messages(options.role, args, item["system"])
                prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
                inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
                if inputs["input_ids"].shape[1] > 8192:
                    raise ValueError("context_bound")
                started = time.monotonic()
                with torch.inference_mode():
                    generated = model.generate(**inputs, do_sample=False, max_new_tokens={"course8b": 512, "review27b": 768, "difficulty8b": 1536}[options.role], max_time=85, pad_token_id=tokenizer.pad_token_id)
                ids = generated[0, inputs["input_ids"].shape[1]:]
                raw_text = tokenizer.decode(ids, skip_special_tokens=True)
                value = normalize(options.role, args, raw_text)
                self.reply(200, {"model": item["name"], "choices": [{"index": 0, "message": {"role": "assistant", "content": json.dumps(value, ensure_ascii=False)}, "finish_reason": "stop"}], "usage": {"prompt_tokens": inputs["input_ids"].shape[1], "completion_tokens": len(ids), "total_tokens": inputs["input_ids"].shape[1] + len(ids), "native_output_sha256": hashlib.sha256(raw_text.encode()).hexdigest(), "native_format": options.role, "duration_seconds": round(time.monotonic()-started, 3), "review_checks_source": "independent_symbolic" if options.role == "review27b" else None}})
            except (ValueError, KeyError, TypeError) as error:
                self.reply(422, {"error": str(error)[:200]})
            except Exception:
                self.reply(500, {"error": "inference_failed"})
            finally:
                gate.release()

    print(json.dumps({"status": "ready", "role": options.role, "model": item["name"], "port": item["port"]}), flush=True)
    ThreadingHTTPServer(("127.0.0.1", item["port"]), Handler).serve_forever()


if __name__ == "__main__":
    main()
