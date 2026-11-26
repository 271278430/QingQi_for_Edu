# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 tests 验收与回归场景。

### 子目录

| 目录                                      | 存放内容                                                            |
| ----------------------------------------- | ------------------------------------------------------------------- |
| [engine/](engine/README.md)               | @zcode/dynamic-workflow 基础工程中的 engine 验收与回归场景。        |
| [graphs/](graphs/README.md)               | @zcode/dynamic-workflow 基础工程中的 graphs 验收与回归场景。        |
| [helpers/](helpers/README.md)             | @zcode/dynamic-workflow 基础工程中的 helpers 验收与回归场景。       |
| [holes/](holes/README.md)                 | @zcode/dynamic-workflow 基础工程中的 holes 验收与回归场景。         |
| [lowering/](lowering/README.md)           | @zcode/dynamic-workflow 基础工程中的 lowering 验收与回归场景。      |
| [schema-errors/](schema-errors/README.md) | @zcode/dynamic-workflow 基础工程中的 schema errors 验收与回归场景。 |
| [schemas/](schemas/README.md)             | @zcode/dynamic-workflow 基础工程中的 schemas 运行时数据结构。       |
| [smoke/](smoke/README.md)                 | @zcode/dynamic-workflow 基础工程中的 smoke 验收与回归场景。         |
| [workflows/](workflows/README.md)         | @zcode/dynamic-workflow 基础工程中的 workflows 验收与回归场景。     |

### 文件

| 文件                                                               | 简要说明                                                                                          |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| [actor-budgets.test.ts](actor-budgets.test.ts)                     | 子代理 WebSearch 预算（9013，docs/dynamic-workflow/authoring.md「A subagent's search budget」）： |
| [actor-models.test.ts](actor-models.test.ts)                       | 子代理模型名集合的封闭性（9010，docs/dynamic-workflow/authoring.md「Choosing a model per          |
| [actor-names.test.ts](actor-names.test.ts)                         | 字面量 actor 重名的编译期 courtesy 诊断（docs/execution-engine.md 的                              |
| [actor-submit-profiles.test.ts](actor-submit-profiles.test.ts)     | 每个 actor 站点的 submit profile（docs/execution-engine.md「Submit                                |
| [analysis.test.ts](analysis.test.ts)                               | Unit coverage for the analysis substrate where a full fixture snapshot would be                   |
| [artifacts.test.ts](artifacts.test.ts)                             | \* 用户面产物（docs/dynamic-workflow/authoring.md）的编译侧：站点身份、lowering、编译期诊断与     |
| [callback-invocation.test.ts](callback-invocation.test.ts)         | \* Callback invocation (docs/analysis.md): the ordering walk inlines                              |
| [causality.test.ts](causality.test.ts)                             | \* Behavioural tests for the causality graph. The fixture snapshots in graphs.test.ts             |
| [compile.test.ts](compile.test.ts)                                 | Script-shaped cases live in tests/workflows/ (fixture suite with `// error`                       |
| [control-flow-projection.test.ts](control-flow-projection.test.ts) | \* Scale pins for the control-flow projection (docs/analysis.md, 追记 2026-09-03).                |
| [convergence.test.ts](convergence.test.ts)                         | \* Fixpoint convergence pins (docs/analysis.md, "Convergence": the canonical-heap rule).          |
| [core-json.test.ts](core-json.test.ts)                             | `AnalysisCore` 的 JSON 往返（docs/chat/workflow-portfolio.md「样例包格式」）：作品集把 core       |
| [facade-dts.test.ts](facade-dts.test.ts)                           | 注释只写参考层：做什么、返回什么、何时拒绝或让 run 失败、上限、实参的编译期规则                   |
| [graphs.test.ts](graphs.test.ts)                                   | Fixture-driven site-graph tests: every tests/graphs/\*.ts file must typecheck                     |
| [hole-sites.test.ts](hole-sites.test.ts)                           | 留白的编译面（docs/dynamic-workflow/authoring.md「Holes」，docs/analysis.md「Sites」）：站点收集  |
| [lowering.test.ts](lowering.test.ts)                               | Lowering 快照 + 语义断言。快照是契约：人类可读的 lowered JS 落在 expected/<base>.js。             |
| [phases.test.ts](phases.test.ts)                                   | phase() 标记的编译面（docs/analysis.md「Phases」）：                                              |
| [projections-barrel.test.ts](projections-barrel.test.ts)           | `@zcode/dynamic-workflow/projections` 是给作品集浏览器包用的纯投影桶                              |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                  |
| [registry.test.ts](registry.test.ts)                               | \* world-read 注册表：(facade 容器, 成员) → op 的唯一真源（docs/execution-engine.md 的            |
| [schema-errors.test.ts](schema-errors.test.ts)                     | Fixture-driven schema-REJECTION suite. A sibling of tests/workflows/, but driven by               |
| [schema-synth.test.ts](schema-synth.test.ts)                       | 合成侧单测：用便捷入口 synthesizeWorkflowSchemas 从脚本文本一站式合成，精确断言                   |
| [schema-validate.test.ts](schema-validate.test.ts)                 | 校验器单测：逐个覆盖我们发射的每种 schema 构造，外加违规格式化（path/expected/got）、             |
| [schemas.test.ts](schemas.test.ts)                                 | Fixture-driven schema-synthesis snapshots: every tests/schemas/\*.ts file must                    |
| [smoke.test.ts](smoke.test.ts)                                     | \* Smoke corpus: real, production-scale workflow scripts that must ANALYZE CLEAN — no throw,      |
| [streams.test.ts](streams.test.ts)                                 | \* 流水线原语 channel / future 的编译期行为（docs/dynamic-workflow/authoring.md「Streams」、      |
| [workflows.test.ts](workflows.test.ts)                             | Fixture-driven compiler tests: every tests/workflows/\*.ts file is compiled;                      |

<!-- qingqi-directory-index:end -->
