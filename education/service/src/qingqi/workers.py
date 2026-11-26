"""Typed model tools with original-format specialist serving adapters.

Serving wrappers must translate the ORIGINAL adapter's training format to these
contracts. Do not silently assume course and teaching LoRA use the same checkpoint.
"""
from __future__ import annotations

from dataclasses import asdict

from .contracts import Denied, SHORT, TEXT, ToolSpec, fingerprint, obj, validate
from .domain_tools import SPECS
from .providers import JSONModel


COURSE_OUT = obj({"suggested_titles": {"type": "array", "items": SHORT, "maxItems": 12}, "status": {"type": "string", "enum": ["candidate_requires_graph_confirmation"]}})
COURSE_IN = obj({"query": SHORT, "candidates": {"type": "array", "items": obj({"id": SHORT, "title": TEXT}), "minItems": 1, "maxItems": 5}})


def model_version(client):
    endpoint = getattr(client, "endpoint", None)
    return fingerprint(asdict(endpoint)) if endpoint else "synthetic_contract_fixture"


def model_timeout(client):
    return getattr(getattr(client, "endpoint", None), "timeout", 10)


def make_workers(models: dict[str, JSONModel]):
    registered = {}
    if "review27b" in models:
        old = SPECS["review_arithmetic"]
        spec = ToolSpec("worker_review27b", "Qwen3.5-27B original-format review plus independently checked numeric steps. Disagreement is rejected.", old.input_schema, old.output_schema, "model", retries=0, timeout=model_timeout(models["review27b"]), version=model_version(models["review27b"]))

        def review_worker(**args):
            value = models["review27b"].generate("Review only actual student work, locate the FIRST error, protect correct work and respect help mode. Return JSON only.", args, spec.output_schema)
            if value["mode"] != args["mode"] or len(value["checks"]) != len(args["steps"]) or value["first_error"] >= len(args["steps"]):
                raise Denied("review worker output does not match submitted work")
            if [c["index"] for c in value["checks"]] != list(range(len(args["steps"]))):
                raise Denied("review worker reordered/duplicated step indices")
            invalid = [c["index"] for c in value["checks"] if not c["valid"]]
            first = invalid[0] if invalid else -1
            expected_status = "no_steps" if not args["steps"] else "incorrect" if invalid else "correct"
            if any(c["reason"].startswith("unsupported_step:") for c in value["checks"]):
                first, expected_status = -1, "unsupported"
            if value["first_error"] != first or value["status"] != expected_status:
                raise Denied("review worker decision contradicts its step checks")
            expected = [{"ref": f"step:{i}", "text": s["equation"], "source": "current_student_work"} for i, s in enumerate(args["steps"])]
            if value["evidence"] != expected:
                raise Denied("review worker evidence differs from actual student steps")
            return value
        review_worker.model_client = models["review27b"]
        registered[spec.name] = (spec, review_worker)
    if "difficulty8b" in models:
        old = SPECS["difficulty_candidates"]
        spec8 = ToolSpec("worker_difficulty8b", "8B teaching adapter: local difficulty candidates, evidence and suggested teaching strategy.", old.input_schema, old.output_schema, "model", retries=0, timeout=model_timeout(models["difficulty8b"]), version=model_version(models["difficulty8b"]))

        def difficulty_worker(**args):
            value = models["difficulty8b"].generate("Extract learning difficulty CANDIDATES from actual history, quote evidence, ask for confirmation. Never infer permanent mastery from one work sample. Return JSON only.", args, spec8.output_schema)
            if value["certainty"] != "candidate_requires_confirmation":
                raise Denied("difficulty worker cannot assert confirmed mastery")
            known = {f"history:{i}": h for i, h in enumerate(args["history"])}
            review_refs = {e["ref"] for e in args.get("review", {}).get("evidence", [])}
            for evidence in value["evidence"]:
                ref = evidence["ref"]
                if ref in known:
                    if evidence["text"] not in known[ref]["text"] or evidence["source"] != known[ref]["kind"]:
                        raise Denied("difficulty worker altered history evidence")
                elif ref not in review_refs:
                    raise Denied("difficulty worker cites nonexistent evidence")
            return value
        difficulty_worker.model_client = models["difficulty8b"]
        registered[spec8.name] = (spec8, difficulty_worker)
    if "course8b" in models:
        specc = ToolSpec("worker_course8b", "8B trained course checkpoint suggests chapter names. Suggestions require subsequent graph confirmation and cannot authorize node IDs.", COURSE_IN, COURSE_OUT, "model", retries=0, timeout=model_timeout(models["course8b"]), version=model_version(models["course8b"]))

        def course_worker(**args):
            value = models["course8b"].generate("Suggest curriculum chapter names in the original trained format. Names are candidates and require graph confirmation.", args, specc.output_schema)
            validate(value, COURSE_OUT)
            return value
        course_worker.model_client = models["course8b"]
        registered[specc.name] = (specc, course_worker)
    return registered
