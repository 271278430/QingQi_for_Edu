from __future__ import annotations

import time

from .contracts import ContractError, Denied, canonical, validate
from .domain_tools import SPECS, difficulty
from .visual_teaching import TOOL as VISUAL_TOOL, render_visuals
from .geometry_solver import TOOL as GEOMETRY_TOOL, solve_geometry, prepare_geometry
from .function_solver import TOOL as FUNCTION_TOOL, analyze_function
from .zcode_runtime import ZCodeRuntime
from .student_task_tools import StudentTaskTools, SPECS as STUDENT_SPECS


class Registry:
    def __init__(self, graph, workers=None, *, root, student_store=None):
        prepare_geometry()
        self.specs = dict(SPECS)
        self.specs[VISUAL_TOOL.name] = VISUAL_TOOL
        self.specs[GEOMETRY_TOOL.name] = GEOMETRY_TOOL
        self.specs[FUNCTION_TOOL.name] = FUNCTION_TOOL
        self.local = {"difficulty_candidates": difficulty, VISUAL_TOOL.name: render_visuals,GEOMETRY_TOOL.name:solve_geometry}
        self.local[FUNCTION_TOOL.name]=analyze_function
        self.specs.update(STUDENT_SPECS)
        self.student_tasks=StudentTaskTools(student_store)
        self.local.update(self.student_tasks.handlers())
        self.workers = workers or {}
        for name, (spec, function) in self.workers.items():
            self.specs[name] = spec
            self.local[name] = function
        self.runtime = ZCodeRuntime(graph, self.specs, self.local, root)

    def authorize(self, name: str, args: dict, allowed: set[str]):
        if name not in allowed or name not in self.specs:
            raise Denied("tool outside capability intersection: " + name)
        spec = self.specs[name]
        if spec.effect != "read":
            raise Denied("this deployment permits read-only capability tools only")
        validate(args, spec.input_schema)
        if len(canonical(args).encode()) > 32000:
            raise Denied("tool arguments too large")

    def call(self, name: str, args: dict, allowed: set[str]) -> dict:
        self.authorize(name, args, allowed)
        spec = self.specs[name]
        start = time.perf_counter()
        executed = self.runtime.call(name, args, spec.timeout)
        result = executed["result"]
        validate(result, spec.output_schema)
        if len(canonical(result).encode()) > 64000:
            raise ContractError("tool output too large")
        return {"tool": name, "version": spec.version, "transport": spec.transport, "result": result,
                "duration_ms": round((time.perf_counter() - start) * 1000, 3), "trust": "untrusted_evidence", "runtime": executed["runtime"]}

    def model_contracts(self, names):
        return self.runtime.rpc("contracts", {"names": list(names)})["tools"]

    def close(self):
        self.runtime.close()
