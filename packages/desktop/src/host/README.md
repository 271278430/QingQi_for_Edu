# host

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 host 实现源码。

### 子目录

| 目录                                                    | 存放内容                                                    |
| ------------------------------------------------------- | ----------------------------------------------------------- |
| [database-startup/](database-startup/README.md)         | @zcode/desktop 基础工程中的 database startup 实现源码。     |
| [pluginSandbox/](pluginSandbox/README.md)               | @zcode/desktop 基础工程中的 pluginSandbox 实现源码。        |
| [topic-resource-relay/](topic-resource-relay/README.md) | @zcode/desktop 基础工程中的 topic resource relay 实现源码。 |

### 文件

| 文件                                                                               | 简要说明                                                                                                                            |
| ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| [automationModelSelection.ts](automationModelSelection.ts)                         | 在 Automation Select 转为一次 Submission 的边界固定模型身份。                                                                       |
| [botGroupTaskScope.ts](botGroupTaskScope.ts)                                       | 群控制采用已验证 attachment，不能由 RPC 调用方声明另一条远程会话。                                                                  |
| [botRemoteWorkspaceResolver.ts](botRemoteWorkspaceResolver.ts)                     | Bot 与 Renderer 共用 Directory/Registry 的事实，旧回退快照不再决定 R3 路由。                                                        |
| [browserControlMainBridge.ts](browserControlMainBridge.ts)                         | \* host↔main browser 执行桥。host 侧把一条命令经 parentPort 发给 main（WebContentsView+CDP 执行），                                 |
| [browserRecordingArtifactMaterializer.ts](browserRecordingArtifactMaterializer.ts) | \* main 只返回短期 WebM；Host 按当前 workspace authority 落盘。本地使用同目录 rename，远端                                          |
| [connectDesktopSourceServer.ts](connectDesktopSourceServer.ts)                     | Desktop 私有回查与设置初始化跟随物理 Source 连接，每次重连重新建立。                                                                |
| [connectSourceServerTarget.ts](connectSourceServerTarget.ts)                       | Host 手动连接入口：目录持有 profile/凭据，Manager 决定实际连接归属。                                                                |
| [conversationShareAttachmentService.ts](conversationShareAttachmentService.ts)     | conversationShareAttachmentService 的实现文件。                                                                                     |
| [cronBotDelivery.ts](cronBotDelivery.ts)                                           | \* 在 prompt 派发前完成 Bot 终态订阅，避免快速任务先完成、后注册 listener 而漏回推。                                                |
| [cronRunLifecycle.ts](cronRunLifecycle.ts)                                         | 派发失败清理永不覆盖调用方持有的原始 dispatch error。                                                                               |
| [databaseStartupCoordinator.ts](databaseStartupCoordinator.ts)                     | 每窗口一个启动所有者。失败只由显式 retry 推进，刷新和重复请求不重新执行 SQL。                                                       |
| [e2eCoverage.ts](e2eCoverage.ts)                                                   | host 的退出由 main 调度，异常或强制回收时不保证 Node 自动写盘；                                                                     |
| [electronPort.d.ts.map](electronPort.d.ts.map)                                     | electronPort.d.ts 模块的资源或工程文件。                                                                                            |
| [electronPort.js](electronPort.js)                                                 | \* 将 Electron MessagePortMain 适配为 RPC 层的 MessagePortLike 接口。                                                               |
| [electronPort.js.map](electronPort.js.map)                                         | electronPort.js 模块的资源或工程文件。                                                                                              |
| [electronPort.ts](electronPort.ts)                                                 | \* 将 Electron MessagePortMain 适配为 RPC 层的 MessagePortLike 接口。                                                               |
| [hostAgentResourceTelemetry.ts](hostAgentResourceTelemetry.ts)                     | \* CLI 资源样本的 Host 转发。                                                                                                       |
| [hostInitialization.ts](hostInitialization.ts)                                     | transport 在 ServiceCollection 接管前就会被启动预热请求使用；初始化中途抛错时，                                                     |
| [hostLog.ts](hostLog.ts)                                                           | Error 被 JSON.stringify 时会变成 {}，导致远端握手失败只剩空对象。                                                                   |
| [hostMcpResourceTelemetry.ts](hostMcpResourceTelemetry.ts)                         | main 已退出或 IPC 关闭时只丢当前资源事实，不影响 MCP 生命周期。                                                                     |
| [hostMcpTelemetry.ts](hostMcpTelemetry.ts)                                         | main 已退出或 IPC 不可用时只丢当前遥测，不影响 MCP 生命周期。                                                                       |
| [hostMemoryDiagnosticsLog.ts](hostMemoryDiagnosticsLog.ts)                         | services 层的领域计数器（`collectServiceMemoryDiagnostics`）。                                                                      |
| [hostMessagePortGuard.ts](hostMessagePortGuard.ts)                                 | rejection cleanup 是 best effort；close 异常不能遮蔽原始 schema/初始化错误。                                                        |
| [hostNetworkCapture.ts](hostNetworkCapture.ts)                                     | 观测丢弃，不影响 Host 主链路                                                                                                        |
| [hostNetworkTelemetry.ts](hostNetworkTelemetry.ts)                                 | 遥测批次失败不应影响 host 主流程                                                                                                    |
| [hostRemoteWorkspaceProxyState.ts](hostRemoteWorkspaceProxyState.ts)               | \* 保存 shared remote Host 代理层持有的 workspace 资源。                                                                            |
| [hostResourceTelemetryEnvironment.ts](hostResourceTelemetryEnvironment.ts)         | 同规格远端环境不能合并；只传规范环境身份的哈希，原始地址不进入遥测旁路。                                                            |
| [hostResourceUsage.ts](hostResourceUsage.ts)                                       | Host 直管的内置插件进程（如 Windows CUA Helper）：pid → 插件名                                                                      |
| [hostSelfResourceTelemetry.ts](hostSelfResourceTelemetry.ts)                       | \* Host 进程自身的资源遥测。                                                                                                        |
| [hostServiceResourceTelemetry.ts](hostServiceResourceTelemetry.ts)                 | 本地默认支持；所有远端须按 server-info 能力声明显式传入。                                                                           |
| [hostSessionCreateTelemetry.ts](hostSessionCreateTelemetry.ts)                     | 仅实际新建并完成首发 admission 的派发分支调用；不从恢复订阅推断创建。                                                               |
| [hostShutdownPhases.ts](hostShutdownPhases.ts)                                     | 实现或公开接口：HostShutdownPhase、HostShutdownResult、runHostShutdownPhases。                                                      |
| [hostToolExecResourceTelemetry.ts](hostToolExecResourceTelemetry.ts)               | main 退出或通道关闭只丢当前完成事实，不影响 Bash 生命周期。                                                                         |
| [hostUncaughtExceptionGuard.ts](hostUncaughtExceptionGuard.ts)                     | Electron 内置 Node 在 TLS 握手中把 peer certificate 投影成 JS 对象时，                                                              |
| [hostWorkspaceTaskTracker.ts](hostWorkspaceTaskTracker.ts)                         | sendPrompt resolve 只是 ACK，不能代表 Agent 已空闲。计数只由 task ready                                                             |
| [index.ts](index.ts)                                                               | \* Host Process 入口 —— 每个窗口对应一个独立的 host process                                                                         |
| [offPeakDispatchPlan.ts](offPeakDispatchPlan.ts)                                   | - resume：conversation_id 已回填 = 已跑过，续跑同一 session 并发续跑提示词；                                                        |
| [promptAttachmentTransferService.ts](promptAttachmentTransferService.ts)           | 只有 owning attachment 持有暂存记录；Source 业务服务与登录态保持远端权威。                                                          |
| [README.md](README.md)                                                             | 本目录用途、子目录与逐文件说明。                                                                                                    |
| [remoteDynamicWorkflowUserMode.ts](remoteDynamicWorkflowUserMode.ts)               | \* 把动态工作流的用户选择推给远程 Host（docs/dynamic-workflow/launch.md「The user's choice」）。                                    |
| [remoteMediaPreviewProxy.ts](remoteMediaPreviewProxy.ts)                           | 并发检查与递增之间一旦出现远端 await，多请求会同时越过 per-lease 上限。                                                             |
| [remoteMediaPreviewProxyHelpers.ts](remoteMediaPreviewProxyHelpers.ts)             | 只等待 drain 时，客户端在背压期间 close 不会结算 Promise，最终无法释放 Host 全局槽位。                                              |
| [remotePromptAttachments.ts](remotePromptAttachments.ts)                           | 上传成功但 chmod/后续提交失败时，远端文件已经存在；若只抛错会一直                                                                   |
| [remoteProviderProvisioningService.ts](remoteProviderProvisioningService.ts)       | Window Host 私有执行能力；不会随 ServiceCollection 暴露到 Renderer RPC。                                                            |
| [remoteWorkspacePreparation.ts](remoteWorkspacePreparation.ts)                     | Bug 原因（ZCT-2113660144497782784）：截止只结束 Desktop 的等待，远端那次 readdir 仍占着 Core 的一个                                 |
| [remoteWorkspaceRpcContract.ts](remoteWorkspaceRpcContract.ts)                     | \* 合同内的 channel 一律按“远端必须提供”收口：IServiceAccessor 上可选的 mediaPreviewService                                         |
| [remoteWorkspaceServiceCollection.ts](remoteWorkspaceServiceCollection.ts)         | 实现或公开接口：REMOTE_WORKSPACE_RPC_REGISTRATIONS、resolveServerProjectService、createServerRemoteWorkspaceServiceCollection。     |
| [rpcLogLevel.ts](rpcLogLevel.ts)                                                   | \* host 之前把 RPC 日志统一走 error，主日志里看起来像所有 RPC 都失败了。                                                            |
| [serverRemoteConnection.ts](serverRemoteConnection.ts)                             | 实现或公开接口：ServerRemoteEndpoints、ServerRemoteConnection、ServerRemoteConnectionOptions、ServerRemoteDuplexConnectionOptions。 |
| [serverRemoteDuplexTransport.ts](serverRemoteDuplexTransport.ts)                   | 原因：ssh2 ClientChannel 与 child stdio 都满足 Duplex，但 ws 在 upgrade 完成时会调用                                                |
| [sourceServerConnectionManager.ts](sourceServerConnectionManager.ts)               | 本次调用采用物理连接时的实际脱敏目标；不写入在线 owner。                                                                            |
| [sourceServerDirectory.ts](sourceServerDirectory.ts)                               | 远端 identity 被 canonical 覆盖等非错误诊断信息；生产环境应注入 no-op。                                                             |
| [sourceServerManagementService.ts](sourceServerManagementService.ts)               | 实现或公开接口：SourceServerManagementService、createSourceServerManagementService。                                                |
| [sourceServerMigrationCounts.ts](sourceServerMigrationCounts.ts)                   | Host 管理服务持有的统计投影；远端读取不阻塞本机目录，连接换代后旧结果失效。                                                         |
| [sourceServerOperationLogs.ts](sourceServerOperationLogs.ts)                       | 每类设备操作的开始与成功文案；失败文案来自归一化错误。                                                                              |
| [sourceServerRecoveryPolicy.ts](sourceServerRecoveryPolicy.ts)                     | 实现或公开接口：isSourceServerAutomaticRecoveryTerminalState、createSourceServerRecoveryCloseEvent。                                |
| [sourceServerReleaseResolver.ts](sourceServerReleaseResolver.ts)                   | release 解析的调用方上下文：本机请求响应取消，本机下载按 `download` 阶段写进度（R3 §6.3）。                                         |
| [sourceServerStartupReconnect.ts](sourceServerStartupReconnect.ts)                 | \* Host 启动静默重连批次的唯一门禁编排（合同 §8.2）：                                                                               |
| [sourceSettingsServiceCollection.ts](sourceSettingsServiceCollection.ts)           | 只有 online generation 可继续服务设置，updating 也可能已经 dispose 旧连接。                                                         |
| [startupDiskSampler.ts](startupDiskSampler.ts)                                     | 仅查询已知目录元数据；dev 只在首次解析时读取，周期内只做 statfs。                                                                   |
| [taskRealtimeBridge.ts](taskRealtimeBridge.ts)                                     | host typecheck 之前未覆盖 realtime bridge，schema 推导里 stream event payload 比                                                    |
| [windowHostAttachmentRegistry.ts](windowHostAttachmentRegistry.ts)                 | scope 必须先由 Host registry 验证；验证失败时不能影响同 attachmentId 的现有端口。                                                   |
| [windowHostAttachmentRpcPolicy.ts](windowHostAttachmentRpcPolicy.ts)               | 手机终端此前被白名单挡在服务调用前并超时；已配对 attachment 采用原终端服务。                                                        |
| [windowHostControllerProjection.ts](windowHostControllerProjection.ts)             | live overlay 缺失表示当前没有可证明的 run                                                                                           |
| [windowHostControllerService.ts](windowHostControllerService.ts)                   | 实现或公开接口：ResolvedWindowHostControllerSource、createWindowHostControllerRuntime。                                             |
| [windowHostSessionsIndexObserver.ts](windowHostSessionsIndexObserver.ts)           | \* Window Host 的被动 sessions-index 观察器。它只使用 existing-only，缺少 runtime 时保持                                            |
| [windowRemoteConnectionRegistry.ts](windowRemoteConnectionRegistry.ts)             | 同一 Source transport 自动重连完成；services/capabilities getter 已切到新连接。                                                     |
| [windowTopicResourceRelay.ts](windowTopicResourceRelay.ts)                         | 反向请求必须属于发起它的物理连接，并仍绑定当前 logical session，不能只比较文件路径。                                                |

<!-- qingqi-directory-index:end -->
