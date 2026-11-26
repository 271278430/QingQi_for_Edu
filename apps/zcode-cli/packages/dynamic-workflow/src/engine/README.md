# engine

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 engine 实现源码。

### 文件

| 文件                                                       | 简要说明                                                                                            |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [artifact-spec.ts](artifact-spec.ts)                       | \* 预置产物 spec 的形状校验。                                                                       |
| [ask-observation-types.ts](ask-observation-types.ts)       | \* driver 对一条 ask 的**观察**词汇表：用量（{@link AskStats}）与进度（{@link AskProgress}）——      |
| [cached-ask-facts.ts](cached-ask-facts.ts)                 | \* ask 的**出生事实**：`node-queued` 带的那几样，以及缓存命中的 `node-settled` 重发的同一份         |
| [concurrency.ts](concurrency.ts)                           | \* 自适应并发控制器：一个 provider key 上的纯 AIMD 状态机。                                         |
| [engine-artifacts-primary.ts](engine-artifacts-primary.ts) | \* 修复原因：engine-artifacts.ts 顶到 oxlint max-lines 上限（400 行）。拆出来的是一个完整的         |
| [engine-artifacts.ts](engine-artifacts.ts)                 | _ engine.ts 顶到 oxlint max-lines 上限（400 行），把**用户面产物**（`artifact._`）的                |
| [engine-config.ts](engine-config.ts)                       | \* 引擎构造配置（{@link EngineConfig}）。定义从 engine.ts 迁到本文件：那个文件顶到 oxlint           |
| [engine-holes.ts](engine-holes.ts)                         | \* 留白（docs/execution-engine.md「Holes」）：脚本向主代理要一段代码，run 停在那一处等它。          |
| [engine-launch.ts](engine-launch.ts)                       | run-launched：发起 run 那一轮的宿主元数据 → 事件                                                    |
| [engine-phase-stamp.ts](engine-phase-stamp.ts)             | \* 出生阶段坐标的两个打戳函数（docs/dynamic-workflow/presentation.md 追记 2026-09-09）。            |
| [engine-report.ts](engine-report.ts)                       | \* engine.ts 顶到 oxlint max-lines 上限（400 行），把 `report()` 的发布路径（序列化探针、           |
| [engine-resume.ts](engine-resume.ts)                       | \* resume 分支从 journal 恢复的 run 级状态（docs/execution-engine.md「Resume by replay」与          |
| [engine-settlement.ts](engine-settlement.ts)               | \* engine.ts 顶到 oxlint max-lines 上限（400 行），把 run 的三条终态路径                            |
| [engine-state.ts](engine-state.ts)                         | \* engine.ts 顶到 oxlint max-lines 上限（400 行），把引擎私有状态的显式接缝拆到本文件；             |
| [engine-world.ts](engine-world.ts)                         | \* engine.ts 顶到 oxlint max-lines 上限（400 行），把 world 节点（world-read / world-run）          |
| [engine.ts](engine.ts)                                     | \* 执行引擎的确定性状态机（Boundary A 的实现 + 向下驱动 Boundary B + 向上回报 sink）。              |
| [errors.ts](errors.ts)                                     | \* 引擎的结构化错误（docs/execution-engine.md「Errors are first-class」）：稳定错误码、             |
| [hash-mismatch.ts](hash-mismatch.ts)                       | \* replay 命中但 inputHash 不一致时的 run 级错误。ask、世界读取、报告、产物四条 replay 路径共用它。 |
| [hash.ts](hash.ts)                                         | \* 包内自带的确定性哈希：FNV-1a（32 位）作用在规范化 JSON 上。                                      |
| [imported-cache-types.ts](imported-cache-types.ts)         | amend-resume 的导入缓存                                                                             |
| [imported-cache.ts](imported-cache.ts)                     | \* amend-resume 导入缓存的**消费态**。                                                              |
| [index.ts](index.ts)                                       | \* @zcode/dynamic-workflow 执行引擎核心的模块导出。                                                 |
| [journal-memory.ts](journal-memory.ts)                     | \* 内存版 {@link JournalStorePort}：阶段一用于 fake-driver 测试与 replay/resume。                   |
| [journal-read-types.ts](journal-read-types.ts)             | \* journal 读面的选项词汇表（docs/execution-engine.md「Reading the journal」）。                    |
| [persona.ts](persona.ts)                                   | actor persona 的两个纯函数：规范化（createActor）与缓存身份（matchImportedActor）                   |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                                    |
| [replay-order.ts](replay-order.ts)                         | \* Replay 的**结算次序闸**（docs/execution-engine.md「Replaying the settle order」）。              |
| [run-terminal.ts](run-terminal.ts)                         | 从 types.ts 拆出（那份文件抵 400 行 lint 门）：`ProviderStop` 错误码的明细与 run 级停滞观察         |
| [scheduler-submit.ts](scheduler-submit.ts)                 | \* scheduler.ts 顶到 oxlint max-lines 上限（400 行），把 Boundary B 的两条向上回报                  |
| [scheduler-types.ts](scheduler-types.ts)                   | \* scheduler.ts 顶到 oxlint max-lines 上限（400 行），把调度器的内部类型（Deferred                  |
| [scheduler.ts](scheduler.ts)                               | \* ask 调度器：把"每 actor FIFO + hold 规则 + 并发上限派发 + ask 结算"从引擎主体拆出，              |
| [types.ts](types.ts)                                       | \* 执行引擎的边界类型（boundary types）。                                                           |
| [world-read-input.ts](world-read-input.ts)                 | world-read / world-run 节点的有界输入                                                               |

<!-- qingqi-directory-index:end -->
