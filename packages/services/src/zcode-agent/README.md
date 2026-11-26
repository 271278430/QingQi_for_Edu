# zcode-agent

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 zcode agent 实现源码。

### 子目录

| 目录                                                  | 存放内容                                                    |
| ----------------------------------------------------- | ----------------------------------------------------------- |
| [resident-rows-range/](resident-rows-range/README.md) | @zcode/services 基础工程中的 resident rows range 实现源码。 |

### 文件

| 文件                                                                     | 简要说明                                                                                                                                          |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| [agentStderrCollector.ts](agentStderrCollector.ts)                       | stderr 的寿命独立于协议；child exit 时管道中仍可能有最后一行诊断。                                                                                |
| [agentTelemetryEnv.ts](agentTelemetryEnv.ts)                             | Desktop 原始账号只在 Host 凭据边界可见；Agent 仅收到不可读的 subject，                                                                            |
| [automationToolPolicy.ts](automationToolPolicy.ts)                       | 闲时派发轮只 deny OffPeakCreate（防止闲时任务递归自我派生、无限调度），OffPeakList 只读保留。                                                     |
| [botTopicAdmission.ts](botTopicAdmission.ts)                             | Host 在途发送屏障；accepted input 和 commandId 幂等仍由 CLI 管理。                                                                                |
| [contextCompositionClient.ts](contextCompositionClient.ts)               | App 侧 context 组成：查询、变更通知与模型请求指标通知（context-composition 模块）。                                                               |
| [cuaOperationTurnTracker.ts](cuaOperationTurnTracker.ts)                 | 当前是否存在仍在执行 Computer Use 工具的 turn。                                                                                                   |
| [groupAttachmentUpload.ts](groupAttachmentUpload.ts)                     | 内容寄存在目标 CLI，群队列只保存引用；远端不能直接使用桌面临时路径。                                                                              |
| [groupRuntimeSnapshot.ts](groupRuntimeSnapshot.ts)                       | Bot 控制操作临时读取 CLI 权威快照，不建立第二份输入队列。                                                                                         |
| [independentPlanSupport.ts](independentPlanSupport.ts)                   | Host 更新不代表远端 CLI 已更新；旧 CLI 会剥掉 Plan 字段，必须在发送前确认执行端。                                                                 |
| [inputPredictionSwitch.ts](inputPredictionSwitch.ts)                     | 手机远控输入预测（ghost hint）的 Host 侧总开关。                                                                                                  |
| [localRuntimeNetworkCapture.ts](localRuntimeNetworkCapture.ts)           | 仅由本机子进程 spawn 点登记；remote RPC/手机 attachment 不登记也不透传启停。                                                                      |
| [modelTrajectory.ts](modelTrajectory.ts)                                 | model-io 默认最多返回的调用条数（保留最近 N 条），避免长 session 把 UI 压垮。                                                                     |
| [modelTrajectoryFileTail.ts](modelTrajectoryFileTail.ts)                 | 32 MiB 足以覆盖常规最近调用，同时避免 64/256 MiB 诊断文件造成 Host 内存峰值。                                                                     |
| [pluginHostQueriesClient.ts](pluginHostQueriesClient.ts)                 | App 侧插件宿主查询：plugins/readUserOptions 与 plugins/mentionItems（plugin-host-queries 模块）。                                                 |
| [pluginReferenceCatalogRequest.ts](pluginReferenceCatalogRequest.ts)     | 旧协议严格校验响应；新展示字段走独立入口，只有 -32601 能证明旧 Agent 不支持。                                                                     |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                                                                  |
| [topicResourceBridge.ts](topicResourceBridge.ts)                         | 每个实际 CLI 连接拥有独立取消域，不能取消另一工作区或另一任务的读取。                                                                             |
| [topicResourcePeers.ts](topicResourcePeers.ts)                           | 共用 Server 只维护已鉴权连接的资源返回路由，不保存任务或队列状态。                                                                                |
| [topicResourceRelay.ts](topicResourceRelay.ts)                           | 只缓存有界附件字节；过载直接拒绝，不构成第二份执行队列。每条远程连接独立持有。                                                                    |
| [topicResourceRelayChannel.ts](topicResourceRelayChannel.ts)             | 只注册在已鉴权远程连接的反向 server 上，不暴露在 Renderer/手机 service collection。                                                               |
| [topicResourceRelayClient.ts](topicResourceRelayClient.ts)               | 单个 reverse RPC 只传一块，避免把完整 base64 附件塞进有帧上限的现有 stdio 连接。                                                                  |
| [topicResourceUpload.ts](topicResourceUpload.ts)                         | 反向请求绑定实际 CLI 连接；上传不能再次按路径选择运行时。                                                                                         |
| [zcodeAgent.ts](zcodeAgent.ts)                                           | 实现或公开接口：ZCodeAgentSessionTarget、ZCodeAgentResumeSessionParams、ZCodeAgentInitializeResult、ZCodeAgentRunAutomationNowResult。            |
| [zcodeAgentBrowserAmbientContext.ts](zcodeAgentBrowserAmbientContext.ts) | \* 只读收集 provider ambient state。失败时返回 undefined，不能让浏览器 UI 状态阻断真实 prompt。                                                   |
| [zcodeAgentConnectionScope.ts](zcodeAgentConnectionScope.ts)             | V4 connection-scoped service facade：每个 RPC attachment 独立持有 subscription                                                                    |
| [zcodeAgentErrors.ts](zcodeAgentErrors.ts)                               | 原始 -32602 文案来自旧 Agent schema，跨 RPC 后 UI 不能靠易变字符串识别能力缺失。                                                                  |
| [zcodeAgentPluginParams.ts](zcodeAgentPluginParams.ts)                   | 远程 workspace 的运行时会话身份；只用于隔离/路由，不能替代 workspacePath。                                                                        |
| [zcodeAgentPresentationSurface.ts](zcodeAgentPresentationSurface.ts)     | Main 已完成服务端单功能灰度裁决；未提供时保持历史 Host 装配语义。                                                                                 |
| [zcodeAgentProcessManager.ts](zcodeAgentProcessManager.ts)               | 本地配套 CLI bundle 的存储专用 Worker 入口；远端/自定义命令不推断能力。                                                                           |
| [zcodeAgentService.ts](zcodeAgentService.ts)                             | 实现或公开接口：supportsLegacyRemoteTaskAllowlist、toProtocolOffPeakTaskSnapshot、OFF_PEAK_INTERNAL_ERROR_CODE、OFF_PEAK_INTERNAL_ERROR_MESSAGE。 |
| [zcodeAgentSpawnCwd.ts](zcodeAgentSpawnCwd.ts)                           | 只选择执行目录，不捕获数据库错误；无可用备用目录时保留原路径供正常启动报错。                                                                      |
| [zcodeAgentWorkflowParams.ts](zcodeAgentWorkflowParams.ts)               | 已保存工作流的 GUI 中枢：五个 workspace 级、无会话的方法。                                                                                        |
| [zcodeConfigOptions.ts](zcodeConfigOptions.ts)                           | 历史 resume 曾经可能用 app 当前默认模型覆盖 settings.current，                                                                                    |
| [zcodeProtocolClient.ts](zcodeProtocolClient.ts)                         | 客户端可发的方法名：旧 zcodeProtocolMethods + v4/\*（M3 起并存，M5 波次 2 收敛为 v4）。                                                           |
| [zcodeProtocolTransport.ts](zcodeProtocolTransport.ts)                   | 实现或公开接口：ZCodeProtocolTransportKind、ZCodeProtocolTransportClosedEvent、ZCodeProtocolTransport。                                           |
| [zcodeSessionEventCoalescer.ts](zcodeSessionEventCoalescer.ts)           | 性能优化：后台工具 progress 只用于“还在跑”的可见摘要，保留最新状态即可。                                                                          |
| [zcodeStdioTapDevConfig.ts](zcodeStdioTapDevConfig.ts)                   | 开发态 stdio 抓包是高频原始协议帧，只能通过显式开关写旁路文件，避免误进生产日志。                                                                 |
| [zcodeStdioTransport.ts](zcodeStdioTransport.ts)                         | 当前未完成行的分片；只在遇到 LF 时 join 一次，见 handleStdoutData 注释。                                                                          |
| [zcodeStorageStartupGate.ts](zcodeStorageStartupGate.ts)                 | 一个 protocol client 对应一个进程代次，状态只来自该连接的合法控制帧。                                                                             |
| [zcodeTaskIndexSyncer.ts](zcodeTaskIndexSyncer.ts)                       | v4 订阅 connectionId 作用域：与 renderer 侧栏共 topic 不同代际（重订阅替换）。                                                                    |
| [zcodeTaskServiceAdapter.ts](zcodeTaskServiceAdapter.ts)                 | 实现或公开接口：createZCodeTaskServiceAdapter。                                                                                                   |
| [zcodeV4HostCommand.ts](zcodeV4HostCommand.ts)                           | host（services 层）侧的 v4 命令信封构造与 ACK 收口共用件（send/交互回执收敛）。                                                                   |

<!-- qingqi-directory-index:end -->
