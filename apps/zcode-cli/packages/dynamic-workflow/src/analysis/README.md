# analysis

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 analysis 实现源码。

### 文件

| 文件                                                         | 简要说明                                                                                             |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- | --- | --- |
| [actor-budgets.ts](actor-budgets.ts)                         | \* 子代理工具预算的编译期规则（docs/dynamic-workflow/authoring.md「A subagent's search budget」；    |
| [actor-graph.ts](actor-graph.ts)                             | \* The actor graph: a derived, presentation-level view of a {@link SiteGraph} with                   |
| [actor-models.ts](actor-models.ts)                           | \* 子代理模型的编译期规则（docs/dynamic-workflow/authoring.md「Choosing a model per subagent」；     |
| [actor-names.ts](actor-names.ts)                             | \* 具名 actor 重名的编译期 courtesy 诊断。                                                           |
| [analyze.ts](analyze.ts)                                     | \* Result of analyzing a workflow script: the same diagnostics `compileWorkflowScript`               |
| [array-methods.ts](array-methods.ts)                         | \* Per-element callback calls (the callback registry's `each` entries — `map` / `forEach`            |
| [artifact-types.ts](artifact-types.ts)                       | \* Producer-side artifact types for data edges. Every data edge's `from` is a producer               |
| [artifacts.ts](artifacts.ts)                                 | \* 产物（artifact）的编译期收集与诊断。                                                              |
| [assign.ts](assign.ts)                                       | \* Assignment transfer rules: plain `=`, compound / logical assignments (`+=`, `\\                   | \\  | =`, |
| [callbacks.ts](callbacks.ts)                                 | \* The callback-semantics registry: the ONE place that says what a library callee does with          |
| [calls.ts](calls.ts)                                         | _ Call and relay transfer rules: the facade sinks (`ask`, `files._`), the relay                      |
| [causality-graph-lanes.ts](causality-graph-lanes.ts)         | causality-graph.ts 顶到 oxlint max-lines 上限（400 行），把成品图上的机械改写与                      |
| [causality-graph-types.ts](causality-graph-types.ts)         | causality-graph.ts 顶到 oxlint max-lines 上限（400 行），把因果图的公开类型                          |
| [causality-graph.ts](causality-graph.ts)                     | Re-exported so the causality vocabulary is importable from one module.                               |
| [causality-order-bindings.ts](causality-order-bindings.ts)   | 走查按调用点的绑定解析「经参数应用」的函数（docs/analysis.md「The call oracle」「Inlining」）。      |
| [causality-order-calls.ts](causality-order-calls.ts)         | causality-order.ts 顶到 oxlint max-lines 上限（400 行），把调用这一组（调用表达式                    |
| [causality-order-functions.ts](causality-order-functions.ts) | causality-order.ts 顶到 oxlint max-lines 上限（400 行），把函数解析类的纯辅助                        |
| [causality-order-loops.ts](causality-order-loops.ts)         | causality-order.ts 顶到 oxlint max-lines 上限（400 行），把循环语句的访问器                          |
| [causality-order-settle.ts](causality-order-settle.ts)       | causality-order.ts 顶到 oxlint max-lines 上限（400 行），把 await 屏障与神谕读取                     |
| [causality-order-state.ts](causality-order-state.ts)         | causality-order.ts 顶到 oxlint max-lines 上限（400 行），把 traceOrder 原本以                        |
| [causality-order-strands.ts](causality-order-strands.ts)     | 走查原本只有一个全局 `settled` 集合，于是内联的 `async` 体里的 `await` 会替整个                      |
| [causality-order-types.ts](causality-order-types.ts)         | causality-order.ts 顶到 oxlint max-lines 上限（400 行），把追踪产物的类型                            |
| [causality-order-walk.ts](causality-order-walk.ts)           | causality-order.ts 顶到 oxlint max-lines 上限（400 行），把节点访问器本体                            |
| [causality-order.ts](causality-order.ts)                     | 追踪词汇（区域种类、跳转种类、兜底阶段 id）定义在 constants.ts——那个文件不 import                    |
| [causality-reduce.ts](causality-reduce.ts)                   | \* Type-aware transitive reduction over the happens-before relation. With one arrow                  |
| [classes.ts](classes.ts)                                     | \* Class modeling: one shared abstract instance per class, evaluated flow-insensitively.             |
| [constants.ts](constants.ts)                                 | \* 追踪词汇：区域种类、跳转种类与兜底阶段 id。它们原本住在 causality-order.ts，但那个文件            |
| [control-flow.ts](control-flow.ts)                           | \* Loop / iteration statement handlers: `for`, `for-of`, and `for-in`. Split out of the core         |
| [core-json.ts](core-json.ts)                                 | \* `AnalysisCore` 的 JSON 编解码。                                                                   |
| [core.ts](core.ts)                                           | \* The analysis core: the single, self-contained artifact one interpretation of a                    |
| [domain.ts](domain.ts)                                       | \* The abstract domain of the taint pass and the pure algebra over it. See taint.ts                  |
| [facade-misuse.ts](facade-misuse.ts)                         | \* The facade-siting diagnostic. Kept in its own module,                                             |
| [fanout-cardinality.ts](fanout-cardinality.ts)               | \* fan-out 的**字面量基数**：                                                                        |
| [flow-graph.ts](flow-graph.ts)                               | \* The control-flow projection: "where can                                                           |
| [flow-phase.ts](flow-phase.ts)                               | \* The phase quotient of the control-flow graph — the control-flow counterpart of                    |
| [flow-strands.ts](flow-strands.ts)                           | \* Where a strand's exits wait between the `fork` that starts it and the `join` that                 |
| [flow-tree.ts](flow-tree.ts)                                 | \* The trace's leaf stream re-read as the STRUCTURED CONTROL TREE that the control-flow              |
| [graph.ts](graph.ts)                                         | \* The site-graph projection: graph assembly and edge emission over the                              |
| [handoff-graph.ts](handoff-graph.ts)                         | \* 交接图：板面第二层的主体。每个阶段                                                                |
| [heap-ops.ts](heap-ops.ts)                                   | \* In-place heap-mutation transfers: `Object.assign` and the receiver-mutating array                 |
| [hole-id.ts](hole-id.ts)                                     | \* 留白站点 id（docs/analysis.md「Sites」的 Hole sites 段）：`hole#<8 位十六进制>`，键是留白的       |
| [hole-sites.ts](hole-sites.ts)                               | \* 留白站点（docs/dynamic-workflow/authoring.md「Holes: `hole<T>()`」，docs/analysis.md「Sites」）： |
| [hole-splice.ts](hole-splice.ts)                             | \* 补全服务的两件纯文本工具（execution-engine.md「The fill service's checks」）：把函数体拼进        |
| [interpret.ts](interpret.ts)                                 | \* The fused interpreter: ONE interpretation of                                                      |
| [literals.ts](literals.ts)                                   | \* Array- and object-literal evaluation, split out of the core evaluator (taint.ts) like             |
| [mermaid.ts](mermaid.ts)                                     | \* Pure mermaid emitters for the site graph and its derived actor graph. String                      |
| [patterns.ts](patterns.ts)                                   | \* Destructuring / aliasing bind machinery, split out of the core evaluator (taint.ts) like          |
| [phase-graph.ts](phase-graph.ts)                             | \* 阶段视图：作者用 `phase("名字")` 标记施加的分组，以及它在因果图上的\*\*商图                       |
| [phases.ts](phases.ts)                                       | \* `phase("…")` 标记的编译期校验。                                                                   |
| [promise-ops.ts](promise-ops.ts)                             | \* Promise and constructor transfer rules, split out of calls.ts (max-lines): the unknown-`new`      |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                     |
| [relays.ts](relays.ts)                                       | \* Facade sink and relay transfers: `Agent.ask`, `files.glob`/`read` (world reads), and              |
| [serialize.ts](serialize.ts)                                 | Quote a type string for a `type=`/`types=` field: embedded `"` escaped as `\"`.                      |
| [site-phases.ts](site-phases.ts)                             | \* 站点 → 出生阶段**名**的编译期表（docs/analysis.md「Phases」；引擎侧见 execution-engine.md         |
| [sites-labels.ts](sites-labels.ts)                           | sites.ts 顶到 oxlint max-lines 上限（400 行），把名字 / 标签辅助（ask 标签与模板                     |
| [sites.ts](sites.ts)                                         | 拆分：本文件顶到 oxlint max-lines 上限（400 行）。名字 / 标签辅助与符号解析                          |
| [state.ts](state.ts)                                         | \* The mutable fixpoint state of the taint pass: the site lookups, the global                        |
| [taint.ts](taint.ts)                                         | \* The taint pass: a gen-only, may-flow dataflow analysis over the typed AST that                    |
| [types.ts](types.ts)                                         | \* The site-graph types: the may-flow digraph over facade call sites emitted by the                  |
| [world-run.ts](world-run.ts)                                 | \* world.run 的编译期命令收集。                                                                      |

<!-- qingqi-directory-index:end -->
