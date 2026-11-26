# workflows

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 workflows 验收与回归场景。

### 文件

| 文件                                             | 简要说明                                                                                    |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| [actor-names.ts](actor-names.ts)                 | Actor naming: every legal shape under the "named actors must be unique" rule                |
| [artifact-typo.ts](artifact-typo.ts)             | artifact-typo 的实现文件。                                                                  |
| [es-lib-globals.ts](es-lib-globals.ts)           | Exercises the embedded ES2022 stdlib closure end to end: if the compiler host               |
| [facade-misuse.ts](facade-misuse.ts)             | Facade misuse: ask() takes instructions text, agent() takes a name/persona.                 |
| [files-no-write.ts](files-no-write.ts)           | World inputs are read-only: files has no write().                                           |
| [git-log-vs-log.ts](git-log-vs-log.ts)           | git.log vs the top-level log(): the collision the world-read registry exists for.           |
| [glob-fanout.ts](glob-fanout.ts)                 | glob-fanout 的实现文件。                                                                    |
| [lean-prover-loop.ts](lean-prover-loop.ts)       | 改动说明：这一版怎么处理上一轮的反例                                                        |
| [phase-markers.ts](phase-markers.ts)             | phase() markers: presentation-only grouping, and every legal position for one.              |
| [planner-reviewer.ts](planner-reviewer.ts)       | 测试语料，**不是**作者范例：末尾 `findings.findings.map((f) => agent("judge")…)` 里那个静态 |
| [purity-ambient-apis.ts](purity-ambient-apis.ts) | Compile-time purity: ambient Node and web APIs do not exist in the script world.            |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                            |
| [two-errors-one-line.ts](two-errors-one-line.ts) | Two expected diagnostics on one line.                                                       |

<!-- qingqi-directory-index:end -->
