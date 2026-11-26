from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any


class ContractError(ValueError):
    pass


class Denied(ContractError):
    pass


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def validate(value: Any, schema: dict, path: str = "$") -> None:
    """Strict subset of JSON Schema used by this project's published contracts."""
    if 'oneOf' in schema:
        matches, errors = 0, []
        for candidate in schema['oneOf']:
            try:validate(value,candidate,path)
            except ContractError as error:errors.append((candidate,str(error)))
            else:matches+=1
        if matches != 1:
            detail=next((error for candidate,error in errors if isinstance(value,dict) and value.get('kind') in candidate.get('properties',{}).get('kind',{}).get('enum',[])), '')
            raise ContractError(f'{path}: expected exactly one valid schema; {detail}')
        return
    kind = schema.get("type")
    types = {"object": dict, "array": list, "string": str, "integer": int, "number": (int, float), "boolean": bool}
    if kind in types and (not isinstance(value, types[kind]) or kind in {"integer", "number"} and isinstance(value, bool)):
        raise ContractError(f"{path}: expected {kind}")
    if "enum" in schema and value not in schema["enum"]:
        raise ContractError(f"{path}: invalid enum")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        if missing := set(schema.get("required", [])) - value.keys():
            raise ContractError(f"{path}: missing {sorted(missing)}")
        if schema.get("additionalProperties") is False and (extra := value.keys() - props.keys()):
            raise ContractError(f"{path}: unknown {sorted(extra)}")
        for key, item in value.items():
            if key in props:
                validate(item, props[key], f"{path}.{key}")
    if isinstance(value, list):
        if len(value) > schema.get("maxItems", 10000):
            raise ContractError(f"{path}: too many items")
        if len(value) < schema.get("minItems", 0):
            raise ContractError(f"{path}: too few items")
        for i, item in enumerate(value):
            validate(item, schema.get("items", {}), f"{path}[{i}]")
    if isinstance(value, str) and not schema.get("minLength", 0) <= len(value) <= schema.get("maxLength", 100000):
        raise ContractError(f"{path}: invalid string length")
    if kind in {"integer", "number"} and not schema.get("minimum", -float("inf")) <= value <= schema.get("maximum", float("inf")):
        raise ContractError(f"{path}: outside range")


def obj(properties: dict, required: list | None = None) -> dict:
    return {"type": "object", "properties": properties, "required": list(properties) if required is None else required, "additionalProperties": False}


TEXT = {"type": "string", "maxLength": 2000}
SHORT = {"type": "string", "minLength": 1, "maxLength": 200}
EVIDENCE = obj({"ref": SHORT, "text": TEXT, "source": TEXT})
STEP = obj({"equation": {"type": "string", "maxLength": 120, "minLength": 1}})
HISTORY = obj({"text": TEXT, "kind": {"type": "string", "enum": ["self_report", "student_work"]}})
MODEL_CHOICE_SCHEMA = obj({'model_id':SHORT,'model_version':{'type':'integer','minimum':0},'reasoning_level':{'type':'string','minLength':1,'maxLength':40}})
MODEL_SELECTION_SCHEMA = obj({'text':MODEL_CHOICE_SCHEMA,'vision':MODEL_CHOICE_SCHEMA},[])
REQUEST_SCHEMA = obj({
    "request_id": SHORT, "question": TEXT, "subject": {"type": "string", "maxLength": 200},
    "course_query": TEXT, "mode": {"type": "string", "enum": ["auto", "socratic", "heuristic", "explain", "answer"]},
    "expression": {"type": "string", "maxLength": 120},
    "steps": {"type": "array", "items": STEP, "maxItems": 30},
    "history": {"type": "array", "items": HISTORY, "maxItems": 20},
    "images": {"type": "array", "items": SHORT, "maxItems": 3},
    "visual_context":obj({'run_id':{'type':'integer','minimum':1},'visual_index':{'type':'integer','minimum':0,'maximum':1}}),
    "model_selection":MODEL_SELECTION_SCHEMA,
}, ["request_id", "question"])


@dataclass(frozen=True)
class Identity:
    # Supplied by authenticated entry point, NEVER by LLM/tool arguments.
    student: str
    session: str

    def __post_init__(self):
        for value in (self.student, self.session):
            if not value or len(value) > 100:
                raise ContractError("invalid identity")


@dataclass(frozen=True)
class Request:
    request_id: str
    question: str
    subject: str = ""
    course_query: str = ""
    mode: str = "auto"
    expression: str = ""
    steps: list[dict] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    visual_context: dict = field(default_factory=dict)
    model_selection: dict = field(default_factory=dict)

    @classmethod
    def parse(cls, value: dict) -> Request:
        validate(value, REQUEST_SCHEMA)
        return cls(**value)

    def dump(self):
        result = asdict(self)
        if not self.images:
            result.pop('images')
        if not self.visual_context:result.pop('visual_context')
        if not self.model_selection:result.pop('model_selection')
        return result


@dataclass(frozen=True)
class Route:
    intents: tuple[str, ...]
    basis: tuple[str, ...]
    clarify: str = ""
    method: str = "structured_and_rules_v1"
    layers: tuple[dict, ...] = ()
    task_dag: dict = field(default_factory=dict)
    continuity: str = "new_task"
    command: str = ""
    unresolved_clauses: tuple[str, ...] = ()

    def dump(self):
        return asdict(self)


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict
    output_schema: dict
    transport: str = "local"
    effect: str = "read"
    timeout: float = 5.0
    retries: int = 1
    version: str = "1"

    def mcp(self):
        return {"name": self.name, "description": self.description, "inputSchema": self.input_schema,
                "outputSchema": self.output_schema,
                "annotations": {"readOnlyHint": self.effect == "read", "destructiveHint": False, "idempotentHint": True}}
