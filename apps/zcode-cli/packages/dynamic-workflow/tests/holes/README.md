# Known soundness holes (staging area for adversarial rounds)

**Round 3 (2026-08-14) is complete: this directory is empty of fixtures.** All 38
confirmed bugs it held were fixed and promoted — soundness repros into
`tests/graphs/`, the facade-retyping escapes into the `facade-siting diagnostics`
block of `tests/analysis.test.ts`. The rules that closed them are the ones described in
`docs/analysis.md`; the per-bug trace lived in `docs/adversarial-round3-findings.md`
until 2026-09-13 and is in git history.

This directory is a reusable landing zone for the next adversarial round, kept
(rather than deleted) because it is wired into the tooling: it is excluded from
oxlint like the other fixture dirs, and no test suite reads it, so a work-in-
progress repro here neither breaks the build nor gets snapshot-tested.

**Workflow for a fix round.** A `.ts` file placed here is a minimized,
skeptic-verified repro of a confirmed soundness bug: it typechecks clean (or, for
a facade-siting escape, wrongly _fails to produce_ a diagnostic) and its analyzed
graph is missing a genuine may-flow edge, so it must NOT be snapshot-tested yet —
a snapshot would enshrine the buggy output. Each file's header comment states the
missing runtime flow and the root cause. Run one through the debug harness:

```sh
node scratch/run.mjs tests/holes/<name>.ts
```

Fix a root cause, re-run its repros, then PROMOTE each fixed fixture into
`tests/graphs/` (or, for a facade-siting escape, into `tests/analysis.test.ts`)
with a hand-reviewed snapshot, and delete it here. This directory should be
fixture-empty again when a round's hardening is complete.

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 holes 验收与回归场景。

### 文件

| 文件                   | 简要说明                         |
| ---------------------- | -------------------------------- |
| [README.md](README.md) | 本目录用途、子目录与逐文件说明。 |

<!-- qingqi-directory-index:end -->
