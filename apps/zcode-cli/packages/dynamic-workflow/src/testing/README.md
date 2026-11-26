# testing

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 testing 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                                                                                                                 |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [index.ts](index.ts)                                           | \* `@zcode/dynamic-workflow/testing`：面向 JournalStorePort 实现方的共享测试资产。                                                                                       |
| [journal-contract-artifacts.ts](journal-contract-artifacts.ts) | \* 修复原因：journal-contract.ts 顶到 oxlint max-lines 上限（400 行），把用户面产物行（kind: "artifact"、artifactId 列、report 标签）的用例拆到本文件；                  |
| [journal-contract-events.ts](journal-contract-events.ts)       | \* 修复原因：journal-contract.ts 顶到 oxlint max-lines 上限（400 行），把事件（追加序号、resume 续号、cursor 分页、按 run 隔离）的用例拆到本文件；                       |
| [journal-contract-helpers.ts](journal-contract-helpers.ts)     | \* 修复原因：journal-contract.ts 顶到 oxlint max-lines 上限（400 行），把各主题模块共用的                                                                                |
| [journal-contract-isolation.ts](journal-contract-isolation.ts) | \* 修复原因：journal-contract.ts 顶到 oxlint max-lines 上限（400 行），把存储边界隔离与按 runId 作用域的收尾用例拆到本文件；                                             |
| [journal-contract-nodes.ts](journal-contract-nodes.ts)         | \* 修复原因：journal-contract.ts 顶到 oxlint max-lines 上限（400 行），把actor 记录与节点记录（ask / world / report 行、缺席键、messageBoundary 回填）的用例拆到本文件； |
| [journal-contract-reads.ts](journal-contract-reads.ts)         | \* 读面选项的契约用例（docs/execution-engine.md「Reading the journal」）：kinds / withResult                                                                             |
| [journal-contract-runs.ts](journal-contract-runs.ts)           | \* 修复原因：journal-contract.ts 顶到 oxlint max-lines 上限（400 行），把run 记录（建 run / 结算袋 / 元数据列 / 用量）的用例拆到本文件；                                 |
| [journal-contract-script.ts](journal-contract-script.ts)       | \* `updateRunScript` 的契约用例（docs/execution-engine.md「Holes」→「The engine's part」）：它是                                                                         |
| [journal-contract.ts](journal-contract.ts)                     | \* JournalStorePort 契约套件：写一次、跑多次。阶段一对内存实现运行，阶段二对 SQLite 实现采用。                                                                           |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                                                                                         |

<!-- qingqi-directory-index:end -->
