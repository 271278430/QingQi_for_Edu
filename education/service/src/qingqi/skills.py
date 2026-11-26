from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .contracts import Denied, fingerprint


@dataclass(frozen=True)
class Skill:
    id: str
    intents: tuple[str, ...]
    tools: tuple[str, ...]
    instructions: str
    digest: str


class Skills:
    def __init__(self, root: Path, runtime=None):
        self.root = root.resolve()
        self.index = json.loads((self.root / "index.json").read_text(encoding="utf-8"))
        self.runtime = runtime

    def load(self, intents: tuple[str, ...], ceiling: set[str]) -> list[Skill]:
        selected = []
        for meta in self.index:
            if not set(meta["intents"]) & set(intents):
                continue
            directory = (self.root / meta["id"]).resolve()
            if not directory.is_relative_to(self.root):
                raise Denied("skill path escaped root")
            manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
            instructions = (directory / "SKILL.md").read_text(encoding="utf-8")
            if manifest["id"] != meta["id"] or manifest["intents"] != meta["intents"]:
                raise Denied("skill identity mismatch")
            digest = fingerprint({"manifest": manifest, "instructions": instructions})
            if digest != meta["sha256"]:
                raise Denied("skill integrity mismatch")
            if not set(manifest["tools"]) <= ceiling:
                raise Denied("skill cannot grant new capabilities")
            optional = set(manifest.get("optional_tools", [])) & ceiling
            selected.append(Skill(manifest["id"], tuple(manifest["intents"]), tuple(manifest["tools"]) + tuple(sorted(optional)), instructions, digest))
        if selected and self.runtime:
            loaded = self.runtime.rpc("skills", {"names": [skill.id for skill in selected]})["skills"]
            content = {item["name"]: item["content"] for item in loaded}
            if set(content) != {skill.id for skill in selected}:
                raise Denied("upstream skill discovery differs from pinned skills")
            selected = [Skill(skill.id, skill.intents, skill.tools, content[skill.id], skill.digest) for skill in selected]
        return selected
