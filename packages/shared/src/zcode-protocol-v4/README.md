# zcode-protocol-v4

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 zcode protocol v4 实现源码。

### 子目录

| 目录                                                  | 存放内容                                                  |
| ----------------------------------------------------- | --------------------------------------------------------- |
| [context-composition/](context-composition/README.md) | @zcode/shared 基础工程中的 context composition 实现源码。 |
| [input-prediction/](input-prediction/README.md)       | @zcode/shared 基础工程中的 input prediction 实现源码。    |
| [session-data/](session-data/README.md)               | @zcode/shared 基础工程中的 session data 实现源码。        |

### 文件

| 文件                                                                       | 简要说明                                                                                                                                             |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [apply.ts](apply.ts)                                                       | Delta 应用语义的规范实现（纯函数）。                                                                                                                 |
| [attachment-faults.ts](attachment-faults.ts)                               | 附件读取/探测的结构化错误码（share 预检与发布的分类依据）。                                                                                          |
| [attachment-ref.ts](attachment-ref.ts)                                     | 仅承载已提交内容引用与展示元信息；内容本体不进入 command/topic frame。                                                                               |
| [coalesce.ts](coalesce.ts)                                                 | Coalesce 纯函数：CLI flush buffer 使用的合并规则。                                                                                                   |
| [command.ts](command.ts)                                                   | Command 层：信封 / ACK / 命令全集 payload。                                                                                                          |
| [controller.ts](controller.ts)                                             | 侧栏工作流运行行；无 run 时缺席。                                                                                                                    |
| [core.ts](core.ts)                                                         | ZCode Protocol v4 —— 数据模型草稿（未冻结，schema 定型以黄金测试为准）。                                                                             |
| [create-session-config.ts](create-session-config.ts)                       | Bugfix：createSession.config 表达“请求覆盖字段”，不能采用 snapshot 的                                                                                |
| [create-workflow-display.ts](create-workflow-display.ts)                   | CreateWorkflow 的工具卡 display 载荷（rows.ts 的 toolCallDisplaySchema 成员）                                                                        |
| [cuaPermission.ts](cuaPermission.ts)                                       | 实现或公开接口：cuaRequestAccessStatusSchema、CuaRequestAccessStatus、requiredCuaPermissionsForRequestAccessStatus、cuaPermissionObservationSchema。 |
| [delta.ts](delta.ts)                                                       | ConversationDelta：快照增量与插件 UI 的 live-only 通知，操作集合封闭（10-protocol-spec §4.5）。                                                      |
| [fork.ts](fork.ts)                                                         | V4 stable assistant fork 的固定 logical-turn 边界。                                                                                                  |
| [index.ts](index.ts)                                                       | ZCode Protocol v4 —— 数据模型草稿。                                                                                                                  |
| [input-intent.ts](input-intent.ts)                                         | CLI admission 后的自包含输入事实。                                                                                                                   |
| [pluginInstall.ts](pluginInstall.ts)                                       | 旧实现只截每条译文，条目数与转义后的字节数仍可撑大持久化事件。入口与发布共用此边界。                                                                 |
| [profiles.ts](profiles.ts)                                                 | Delivery profile 过滤纯函数。                                                                                                                        |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                                                                                     |
| [rows.ts](rows.ts)                                                         | ConversationRow：行类型自包含。                                                                                                                      |
| [session-config.ts](session-config.ts)                                     | Session 接受并持久化的稀疏选择意图；provider/model/thought 仅为 UI effective 投影。                                                                  |
| [sessions-index-workflow-activity.ts](sessions-index-workflow-activity.ts) | sessions-index 的工作流运行摘要                                                                                                                      |
| [sessions-index.ts](sessions-index.ts)                                     | sessions-index topic：列表活性数据源；conflated 最新态，永不溢出。                                                                                   |
| [shared-context-import.ts](shared-context-import.ts)                       | shareUrl 硬绑 /cn/share/<code>。将来换域名、或改用英文站 /share/<code> 作为                                                                          |
| [shared-context-ref.ts](shared-context-ref.ts)                             | 实现或公开接口：sharedContextRefSchema、SharedContextRef。                                                                                           |
| [snapshot.ts](snapshot.ts)                                                 | oxlint-disable max-lines -- v4 snapshot schema is a frozen cross-process contract; additions stay grouped here.                                      |
| [submission.ts](submission.ts)                                             | Composer 可以显式提交的 Agent mode；auto 是 Runtime 内部状态，不进入用户 Submission。                                                                |
| [telemetry.ts](telemetry.ts)                                               | 会话创建期采用的 App Memory 开关，不表示记忆读写结果。                                                                                               |
| [toolDisplay.ts](toolDisplay.ts)                                           | zcode-protocol-v4 toolCall 的展示层 schema。                                                                                                         |
| [transport.ts](transport.ts)                                               | 传输外壳：连接握手 / 订阅 / 帧信封。                                                                                                                 |
| [wire-assembler.ts](wire-assembler.ts)                                     | V4 incremental physical assembler：ownership 过滤后逐片接纳，只在                                                                                    |
| [wire-binary.ts](wire-binary.ts)                                           | V4 wire 的跨 Node/browser 二进制纯函数。独立成小模块，避免 codec 主文件                                                                              |
| [wire-codec.ts](wire-codec.ts)                                             | V4 physical wire encoder：按调用方真实 JSON/RPC envelope 计量，logical frame                                                                         |
| [wire-fault.ts](wire-fault.ts)                                             | V4 physical assembly fault 的分类：**内容确定性失败** vs 瞬态失败。                                                                                  |
| [wire-reassembly.ts](wire-reassembly.ts)                                   | V4 physical wire reassembly：所有 fragment 只进入 staging；bytes、checksum、                                                                         |
| [wire.ts](wire.ts)                                                         | V4 physical wire schema：logical topic frame 保持原子 seq 语义，超大帧只在                                                                           |
| [workflow-artifact.ts](workflow-artifact.ts)                               | \* workflow run 里**任意脚本值**（顶层返回的产物、`report(item)` 的条目）→ 给模型或读者看的                                                          |
| [workflow-artifacts.ts](workflow-artifacts.ts)                             | 用户面产物（artifact）的协议词汇表                                                                                                                   |
| [workflow-command-rejections.ts](workflow-command-rejections.ts)           | 动态工作流命令的拒绝词表与 fault 前缀：从 command.ts 拆出（该文件在 max-lines 上限），                                                               |
| [workflow-observation-display.ts](workflow-observation-display.ts)         | 观察类工作流工具（GetWorkflowRun / ListWorkflowRuns / EvalWorkflowSnippet                                                                            |
| [workflow-row-meta.ts](workflow-row-meta.ts)                               | workflow 轮的行级元数据（rows.ts 的 turnHeader / userInput 成员）                                                                                    |
| [workflow-run-settings-command.ts](workflow-run-settings-command.ts)       | amendWorkflowRunSettings：从 GUI 改一个 run 的两项设置                                                                                               |
| [workflow-runs-actor-session.ts](workflow-runs-actor-session.ts)           | actor 的 `sessionId`：持有这个子代理转录的那条会话（workflowRuns 归约的一条规则）                                                                    |
| [workflow-runs-actor-status.ts](workflow-runs-actor-status.ts)             | actor 三态的**派生**（workflowRuns 归约的一条规则）                                                                                                  |
| [workflow-runs-artifacts.ts](workflow-runs-artifacts.ts)                   | workflowRuns 归约里的用户面产物部分                                                                                                                  |
| [workflow-runs-caps.ts](workflow-runs-caps.ts)                             | 界留下的痕迹：被拒实例的计数器、整键的条目预算、以及读面唯一的步数读法                                                                               |
| [workflow-runs-concurrency.ts](workflow-runs-concurrency.ts)               | workflowRuns 归约里的自适应并发部分                                                                                                                  |
| [workflow-runs-delta.ts](workflow-runs-delta.ts)                           | workflowRuns 的键级增量：diff（生产侧）、apply（消费侧）与规范键序                                                                                   |
| [workflow-runs-entries.ts](workflow-runs-entries.ts)                       | 出生事实的读法：脚本作者写的那些字符串怎么按线上界落成一个 actor 条目                                                                                |
| [workflow-runs-eviction.ts](workflow-runs-eviction.ts)                     | 表满时腾位：谁可以让位、什么时候入座、以及被腾掉的东西怎么继续可数                                                                                   |
| [workflow-runs-holes.ts](workflow-runs-holes.ts)                           | workflowRuns 归约的留白分支：`hole-reached` / `hole-filled`，以及阶段表上的留白下标                                                                  |
| [workflow-runs-legacy.ts](workflow-runs-legacy.ts)                         | 给**没有** `workflowRunDeltas` 能力的消费者的 workflowRuns 裁剪                                                                                      |
| [workflow-runs-lineage.ts](workflow-runs-lineage.ts)                       | lineage 字段的读法：reducer 从进度载荷上                                                                                                             |
| [workflow-runs-node-progress.ts](workflow-runs-node-progress.ts)           | 一次 ask 的**任务与进度读数**：node-queued 的 instructionsHead + node-progress 的三个计数                                                            |
| [workflow-runs-phases.ts](workflow-runs-phases.ts)                         | \* `phase-entered` 的归约：控制流经过了                                                                                                              |
| [workflow-runs-reducer.ts](workflow-runs-reducer.ts)                       | workflowRuns 的纯归约：一条 dwf 进度事件 → 新的 workflowRuns 状态                                                                                    |
| [workflow-runs-started.ts](workflow-runs-started.ts)                       | workflowRuns 归约的 `run-started` 分支                                                                                                               |
| [workflow-runs-tables.ts](workflow-runs-tables.ts)                         | workflowRuns 里几张**有界表**的 upsert 语义                                                                                                          |
| [workflow-runs-unlisted.ts](workflow-runs-unlisted.ts)                     | 表外条目的归属账：`unlistedByPhase` 的每一格怎么加、怎么减、什么时候整格消失                                                                         |
| [workflow-runs.ts](workflow-runs.ts)                                       | workflowRuns：dwf 引擎 run 的实时运行态 schema（snapshot.ts 的 workflowRuns 键）                                                                     |
| [workflow-workspace.ts](workflow-workspace.ts)                             | 工作区 transcript 的协议词汇表                                                                                                                       |
| [workspace-config.ts](workspace-config.ts)                                 | workspace-config topic（v4 additive 新增）：workspace 级配置目录的活性数据源。                                                                       |
| [workspace-hook-review.ts](workspace-hook-review.ts)                       | 软门禁：按需开审核 flow 的命令 target。                                                                                                              |

<!-- qingqi-directory-index:end -->
