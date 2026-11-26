# zcode-protocol-v4

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 zcode protocol v4 实现源码。

### 子目录

| 目录                                          | 存放内容                                                 |
| --------------------------------------------- | -------------------------------------------------------- |
| [commands/](commands/README.md)               | @zcode/bootstrap 基础工程中的 commands 实现源码。        |
| [local-ttft/](local-ttft/README.md)           | @zcode/bootstrap 基础工程中的 local ttft 实现源码。      |
| [materialization/](materialization/README.md) | @zcode/bootstrap 基础工程中的 materialization 实现源码。 |

### 文件

| 文件                                                                                 | 简要说明                                                                                              |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| [assistant-feedback-persistence.ts](assistant-feedback-persistence.ts)               | transcript 是反馈持久权威；event 只负责把同一写入推进 live/cold projection。                          |
| [attachment-upload-registry.ts](attachment-upload-registry.ts)                       | \* CLI 进程内 attachment staging 权威表。                                                             |
| [cold-event-merge.ts](cold-event-merge.ts)                                           | shared_context 正文仍是 provider-only；这里只下发脱敏的 handover metadata。                           |
| [cold-file-change-summaries.ts](cold-file-change-summaries.ts)                       | 旧事件和缺失 user messageId 映射的普通 TurnStarted                                                    |
| [cold-session-resume.ts](cold-session-resume.ts)                                     | 冷恢复协调器：订阅落在「不在内存注册表、但可能已持久化」的会话时                                      |
| [command-inbox.ts](command-inbox.ts)                                                 | Command inbox：统一命令 admission 与查询入口。                                                        |
| [conversation-telemetry-facts.ts](conversation-telemetry-facts.ts)                   | 仅消费加载结果 metadata；请求参数不证明技能存在，不能进入遥测。                                       |
| [conversation-telemetry-workflow-facts.ts](conversation-telemetry-workflow-facts.ts) | 动态工作流子代理的归属事实（子代理 token 埋点）                                                       |
| [conversation-topic-publisher.ts](conversation-topic-publisher.ts)                   | Conversation topic 发布器（传输外壳）。                                                               |
| [conversation-workflow-run-deltas.ts](conversation-workflow-run-deltas.ts)           | publisher 对 `workflowRun.*` 键级增量的两条纯规则：旧消费者编码、以及快路径的增长上界                 |
| [create-session-command-fact.ts](create-session-command-fact.ts)                     | \* createSession 使用 global command bucket，但 firstInput 的 durable fact 落在新 session。           |
| [cua-app-snapshot.ts](cua-app-snapshot.ts)                                           | 同一 bundle 可能存在多个进程；没有 PID 时不能猜测具体进程身份。                                       |
| [cua-permission-observation.ts](cua-permission-observation.ts)                       | \* 将当前进程收到的可信 CUA ToolCallResult 投影为一次性权限观察。                                     |
| [event-normalizer.ts](event-normalizer.ts)                                           | \* 中枢直接启动已保存工作流的启动轮元数据（`inputSource === "workflow_launch"` 时在场）。             |
| [highspeed-metrics-persistence.ts](highspeed-metrics-persistence.ts)                 | \* live 投影中该 Turn 已产生的卡失效降级时刻。它只存在于 live 投影，终态持久化若不把它一并写入        |
| [index.ts](index.ts)                                                                 | ZCode Protocol v4 —— CLI 权威投影（M2）。                                                             |
| [interaction-registry.ts](interaction-registry.ts)                                   | v4 交互应答登记表（原生化，resolveInteraction）。                                                     |
| [local-ttft-clock.ts](local-ttft-clock.ts)                                           | 诊断采样不参与 admission；只有启用中的输入才创建，timer 不阻止 CLI 退出。                             |
| [local-ttft-compaction.ts](local-ttft-compaction.ts)                                 | Compact 的实际生命周期可以与 main attempt 交错，不能由主请求差额推算。                                |
| [mcp-elicitation.ts](mcp-elicitation.ts)                                             | \* MCP elicitation（server → client `elicitation/create`）与 ZCode 用户提问通道的映射                 |
| [model-config-mutation.ts](model-config-mutation.ts)                                 | \* 同一个 session App 的模型配置只有一个串行化临界区。                                                |
| [persistent-command-facts.ts](persistent-command-facts.ts)                           | cancelled 也是 durable terminal input fact：若这里只读 discarded，用户主动删除                        |
| [persistent-command-index.ts](persistent-command-index.ts)                           | commands/query 的 session-scoped lazy index。                                                         |
| [product-projection-bash-progress.ts](product-projection-bash-progress.ts)           | 进度只能更新已运行的 Bash，不创建行、不把终态或后台任务复活。                                         |
| [product-projection.ts](product-projection.ts)                                       | ProductProjection —— CLI 权威投影第二 reducer。                                                       |
| [projection-rows.ts](projection-rows.ts)                                             | SessionEvent payload → ConversationRow 的构造纯函数。                                                 |
| [projection-state.ts](projection-state.ts)                                           | ProductProjection 状态工厂与派生规则。                                                                |
| [queue-auto-drain.ts](queue-auto-drain.ts)                                           | \* 普通 queue 的唯一自动提升闸门。fail-open 不在这里开旁路：verifier 仍先把                           |
| [README.md](README.md)                                                               | 本目录用途、子目录与逐文件说明。                                                                      |
| [replay.ts](replay.ts)                                                               | // 下游回放页面在浏览器里用 CLI 自己的三段归约器把持久化的 MessageWithParts 重建成                    |
| [sessions-index-fanout-throttle.ts](sessions-index-fanout-throttle.ts)               | sessions-index fan-out 的高频事件节流（docs/v4-refactor/14-sessions-index.md「事件 fan-out 节奏」）。 |
| [sessions-index-projection.ts](sessions-index-projection.ts)                         | sessions-index topic 的 CLI 侧归约：把一个 workspace 名下各会话的                                     |
| [sessions-index-publisher-registry.ts](sessions-index-publisher-registry.ts)         | \* sessions-index publisher 的 workspace 级生命周期边界：同键异步操作串行，dispose 后禁止回写。       |
| [sessions-index-publisher.ts](sessions-index-publisher.ts)                           | sessions-index topic publisher：在 SessionsIndexProjection 之上做                                     |
| [stable-fork-target.ts](stable-fork-target.ts)                                       | \* projection 已证明 product turn 成功且 row 是轮尾 completed assistant；这里再以                     |
| [task-list-session-membership.ts](task-list-session-membership.ts)                   | \* 左侧任务列表的 session 类型投影。                                                                  |
| [topic-frame-reservation.ts](topic-frame-reservation.ts)                             | publisher 水位的两阶段提交句柄。                                                                      |
| [transcript-hydration.ts](transcript-hydration.ts)                                   | Transcript → SessionEvent 合成（「reduce(transcript) ≡ reduce(events)」）。                           |
| [v4-gateway.ts](v4-gateway.ts)                                                       | V4 conversation 网关（host 通道层 CLI 侧）。                                                          |
| [workspace-config-publisher.ts](workspace-config-publisher.ts)                       | workspace-config topic publisher（v4 additive 新增）：workspace 级配置目录（config options +          |

<!-- qingqi-directory-index:end -->
