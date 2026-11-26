# zcode-protocol

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 zcode protocol 实现源码。

### 子目录

| 目录                                                  | 存放内容                                                     |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| [context-composition/](context-composition/README.md) | @zcode/bootstrap 基础工程中的 context composition 实现源码。 |
| [mcp-ui/](mcp-ui/README.md)                           | @zcode/bootstrap 基础工程中的 mcp ui 实现源码。              |
| [session-data/](session-data/README.md)               | @zcode/bootstrap 基础工程中的 session data 实现源码。        |

### 文件

| 文件                                                               | 简要说明                                                                                                          |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| [account-provider-config.ts](account-provider-config.ts)           | \* 更新进程级 Account Provider Config。                                                                           |
| [ai-sdk-warning-logger.ts](ai-sdk-warning-logger.ts)               | AI SDK 默认 warning logger 第一次会用 console.info 写 stdout；                                                    |
| [automation-port.ts](automation-port.ts)                           | 归属会话解析器：automation-port 是按 session 构造的，直接绑定「自己所服务的 session                               |
| [background-work-owner.ts](background-work-owner.ts)               | 只查询现存执行器，绝不为查看输出恢复 runtime。                                                                    |
| [browser-control-broker.ts](browser-control-broker.ts)             | \* 一个 server context 的 broker 状态。同一 context 里 broker 被造两次——进程级 node_repl broker 用的              |
| [computer-use-operation-event.ts](computer-use-operation-event.ts) | \* 这个 cell 是否在用 Computer Use。                                                                              |
| [dynamic-workflow-policy.ts](dynamic-workflow-policy.ts)           | \* 动态工作流灰度门。判定权在 Host：                                                                              |
| [fork-model-selection.ts](fork-model-selection.ts)                 | 会话派生（stable fork / 编辑前分叉 / 辅助对话）的常驻 Selection 推导。                                            |
| [input-prediction-handler.ts](input-prediction-handler.ts)         | v4/conversation/inputPrediction 的 CLI 侧处理器（手机远控 ghost hint）。                                          |
| [interaction-broker.ts](interaction-broker.ts)                     | 协议错误只在适配层翻译；core 不识别传输错误码，也不能把基础设施故障当用户拒绝。                                   |
| [interaction-preferences.ts](interaction-preferences.ts)           | \* 应用 Host 全局交互偏好。共享 CLI 内各工作区收到相同设置，registry 是进程内                                     |
| [interaction-response-race.ts](interaction-response-race.ts)       | \* 让 legacy 反向 RPC（interaction/requestPermission 等）与 v4 resolveInteraction 命令                            |
| [mapper.ts](mapper.ts)                                             | mapper 的实现文件。                                                                                               |
| [mcp.ts](mcp.ts)                                                   | 设置页的本地 MCP 列表由 desktop main 解析 `.zcode` / `.agents` fallback，                                         |
| [message-mapper.ts](message-mapper.ts)                             | 历史读取和搜索索引同走此出口，旧尾块采用 CLI 解码器，不改持久正文。                                               |
| [model-execution.ts](model-execution.ts)                           | model-execution 的实现文件。                                                                                      |
| [model-io-preferences.ts](model-io-preferences.ts)                 | \* ModelIO 写盘策略是 App 全局偏好，但每个 resident session 持有独立 adapter。                                    |
| [model-mapper.ts](model-mapper.ts)                                 | 未绑定 App 的 getModel() 返回空值；读取协议不能把合法的空状态重新变成恢复异常。                                   |
| [off-peak-tool-policy.ts](off-peak-tool-policy.ts)                 | \* Off-Peak 工具面门禁为灰度有效且本地 workspace。共享池只包含本地 workspace，支持条件一致；                      |
| [official-mcp-auth-port.ts](official-mcp-auth-port.ts)             | Agent 侧的官方 MCP 身份头端口。                                                                                   |
| [offpeak-port.ts](offpeak-port.ts)                                 | \* Off-Peak 协议端口。与 automation-port 的取舍：                                                                 |
| [permission-options.ts](permission-options.ts)                     | permission-options 的实现文件。                                                                                   |
| [plugin-discovery-port.ts](plugin-discovery-port.ts)               | 发现、安装与会话初始化使用同一 Host 身份及插件准备缓存。                                                          |
| [plugin-install-interaction.ts](plugin-install-interaction.ts)     | 先登记再发布；卡片动作只认 install，未知/迟到应答绝不能批准。                                                     |
| [plugin-mention-items.ts](plugin-mention-items.ts)                 | `plugins/mentionItems`：输入框 `@` 面板里 `tool` target 的候选项。                                                |
| [plugin-reference-catalog.ts](plugin-reference-catalog.ts)         | Plugin 对话引用 catalog 的协议 handler。                                                                          |
| [plugin-ui-surfaces.ts](plugin-ui-surfaces.ts)                     | `plugins/listUiSurfaces`：工作区级只读投影，                                                                      |
| [plugin-user-options.ts](plugin-user-options.ts)                   | `plugins/readUserOptions`：扩展 settings 能力读本插件 user 层的有效值（含敏感值）。                               |
| [plugins.ts](plugins.ts)                                           | 把 CLI 的 PluginMetadata 投影成协议可序列化的 ZCodePluginInfo (只保留 UI 需要的字段)。                            |
| [process-child-processes.ts](process-child-processes.ts)           | \* `process/childProcesses`：把 MCP 进程注册表内存里的子进程映射整理成协议结果。                                  |
| [protocol-mcp-config.ts](protocol-mcp-config.ts)                   | ZCode Protocol 的 mcpServers 是 session/runtime 和状态查询的完整覆盖配置。                                        |
| [provider-runtime-headers.ts](provider-runtime-headers.ts)         | 无应答方时 UI 的 SDK 超时不会启动；端口总时限同时覆盖排队与凭据解析。                                             |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                                  |
| [resource-sampler.ts](resource-sampler.ts)                         | 本地内存诊断日志：采用同一 60s 节拍，                                                                             |
| [runtime-cleanup.ts](runtime-cleanup.ts)                           | 共用绝对 deadline；某项失败/挂起不阻止其余资源被尝试，也不逐项续时。                                              |
| [runtime-resources.ts](runtime-resources.ts)                       | 持有 app 资源而非业务 session；临时 workspace app、尚未登记的 app 也归此 owner。                                  |
| [saved-workflows-run.ts](saved-workflows-run.ts)                   | 从一次 run 出发的两个方法（docs/dynamic-workflow/transcript-and-notifications.md                                  |
| [saved-workflows.ts](saved-workflows.ts)                           | 已保存工作流的 GUI 中枢：workspace 级、无会话的方法。                                                             |
| [server-operations.ts](server-operations.ts)                       | 实现或公开接口：createSession、createSessionRecordForV4、ActivatedSessionForResume、discardFailedSessionResume。  |
| [server-types.ts](server-types.ts)                                 | \* 每个 session record 的内存 event store 工厂。                                                                  |
| [server.ts](server.ts)                                             | 实现或公开接口：notifyWorkspaceHookTrustGrantSessions、ZCodeProtocolPostResponseBatch、ZCodeProtocolAgentServer。 |
| [session-debug.ts](session-debug.ts)                               | 旁路记录跟随 CLI record 回收，不挂到聊天投影、轮次事实或已提交输入队列上。                                        |
| [session-mapper.ts](session-mapper.ts)                             | runtime projection 是运行期 eventStore reducer，恢复历史 session 时可能没有                                       |
| [session-residency.ts](session-residency.ts)                       | Session 常驻池的真实事实适配与去激活执行面。                                                                      |
| [session-resident-pool.ts](session-resident-pool.ts)               | CLI session 常驻池。                                                                                              |
| [skill-reference-catalog.ts](skill-reference-catalog.ts)           | Composer Skill 只读 catalog。                                                                                     |
| [slash-commands.ts](slash-commands.ts)                             | \* 动态工作流灰度门（docs/dynamic-workflow/launch.md「Gray release」）。\*\*只有显式 false                        |
| [startup-resource.ts](startup-resource.ts)                         | 关闭信号不能等卡住的初始化 Promise；迟到资源由创建边界负责释放。                                                  |
| [storage-startup.ts](storage-startup.ts)                           | 不能先写入 JS 缓冲后立即阻塞执行 SQL；等待 Writable 确认控制帧已交给传输层。                                      |
| [subagent-session-query.ts](subagent-session-query.ts)             | 父 tool part 是后台 launch ACK（纯文本）：它的 completed 只表示「已启动」，不是 child 的终态。                    |
| [topic-resource-port.ts](topic-resource-port.ts)                   | 原因：Core trace 含 sessionId 等额外字段，原样发送会让 Host 严格校验失败并断开整个 CLI。                          |
| [transport.test.ts](transport.test.ts)                             | transport.test 的实现文件。                                                                                       |
| [transport.ts](transport.ts)                                       | 生命周期由 session owner 自己串行化。若排在长请求后，查询看不到 starting/stopping，                               |
| [usage-stats-builder.ts](usage-stats-builder.ts)                   | 用 Intl 计算 timeZone 在 atMs 时刻相对 UTC 的偏移（ms）。无法解析时回退 0。                                       |
| [v4-bridge.ts](v4-bridge.ts)                                       | 定位：ConversationV4Gateway 是域无关的通道运行时，本文件把它绑到协议服务器上下文：                                |
| [v4-workspace-config.ts](v4-workspace-config.ts)                   | v4 workspace-config 只承载 workspace presentation；模型候选与首选项由目标 Host                                    |
| [workflow-settings-answer.ts](workflow-settings-answer.ts)         | 工作流确认窗应答里的设置调整 → broker 结果的 inputAdjustments                                                     |
| [workspace-hook-trust.ts](workspace-hook-trust.ts)                 | \* 没有 task/session 时的 workspace 级 Trust authority。                                                          |
| [workspace-model-runtime.ts](workspace-model-runtime.ts)           | 灰度门是 Host 判定的 workspace 级事实，目录装配读进程缓存。                                                       |
| [workspace.ts](workspace.ts)                                       | \* 将 V4 workspaceId 的本地路径/远程 identity 双形态统一还原为 workspace ref。                                    |

<!-- qingqi-directory-index:end -->
