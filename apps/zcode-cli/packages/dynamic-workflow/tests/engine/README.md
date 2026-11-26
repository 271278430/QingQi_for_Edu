# engine

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 engine 验收与回归场景。

### 文件

| 文件                                                                               | 简要说明                                                                                                    |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [concurrency.test.ts](concurrency.test.ts)                                         | \* ConcurrencyController 的纯状态机用例（docs/dynamic-workflow/concurrency.md「The controller」             |
| [engine-artifacts.test.ts](engine-artifacts.test.ts)                               | \* 引擎侧的用户面产物（docs/dynamic-workflow/authoring.md「Journal rows and events」两行 + 错误码表）。     |
| [engine-ask-progress.test.ts](engine-ask-progress.test.ts)                         | \* ask 的两条「它在干什么」事实（docs/execution-engine.md「Events」/「Progress within an ask」）：          |
| [engine-concurrency-observations.test.ts](engine-concurrency-observations.test.ts) | \* 引擎侧的三个自适应并发观察事件（docs/dynamic-workflow/concurrency.md「What the driver observes」）。     |
| [engine-holes.test.ts](engine-holes.test.ts)                                       | \* 留白（docs/execution-engine.md「Holes」）：`hole` 铸序号、盖出生阶段、记 `hole-reached`、把              |
| [engine-resume-reads.test.ts](engine-resume-reads.test.ts)                         | \* resume 的 journal 读形状（docs/execution-engine.md「Reading the journal」）：                            |
| [engine-retune-concurrency.test.ts](engine-retune-concurrency.test.ts)             | \* 就地改本 run 自己的并发上界（`engine.setMaxConcurrency`，docs/dynamic-workflow/concurrency.md            |
| [engine.test.ts](engine.test.ts)                                                   | 一个基于 schema.required 的最小校验器（模拟真实 validator 的违规输出）。                                    |
| [fake-driver.ts](fake-driver.ts)                                                   | \* fake driver：以脚本化裁决 + 手动兑现的 promise 驱动引擎核心，不用 timer / 时钟 / 会话 / 磁盘。           |
| [imported-cache.test.ts](imported-cache.test.ts)                                   | \* amend-resume 的引擎侧：导入缓存的命中、分歧、会话种子与 world 内容匹配                                   |
| [journal-store.test.ts](journal-store.test.ts)                                     | 内存实现跑通共享契约；SQLite 实现在 @zcode/adapters 经 `@zcode/dynamic-workflow/testing` 跑同一份。         |
| [README.md](README.md)                                                             | 本目录用途、子目录与逐文件说明。                                                                            |
| [replay-settle-order.test.ts](replay-settle-order.test.ts)                         | \* Replay 的结算次序（docs/execution-engine.md「Replaying the settle order」）。                            |
| [site-phases.test.ts](site-phases.test.ts)                                         | \* 词法出生阶段（docs/execution-engine.md「Identity: sites, ordinals, phases」）：`EngineConfig.sitePhases` |
| [world-read-input.test.ts](world-read-input.test.ts)                               | world-read / world-run 节点的有界输入（docs/dynamic-workflow/transcript-and-notifications.md）：            |

<!-- qingqi-directory-index:end -->
