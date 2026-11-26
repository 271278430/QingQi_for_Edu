# hooks

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 hooks 生命周期与操作入口。

### 文件

| 文件                                                                                   | 简要说明                                                                                                        |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| [clientScenesVisibilityRecovery.ts](clientScenesVisibilityRecovery.ts)                 | Page Visibility 恢复协调器：同一 authority 可有多个 React 消费方，每次重开只执行一个回调。                      |
| [index.ts](index.ts)                                                                   | \* Hooks barrel export                                                                                          |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                                                                                |
| [RemoteProjectPresentationContext.tsx](RemoteProjectPresentationContext.tsx)           | 仅向消费界面传递 Root 现有恢复 owner 的事实，不缓存或接管恢复时序。                                             |
| [useAlertDialog.ts](useAlertDialog.ts)                                                 | 实现或公开接口：useAlertDialog。                                                                                |
| [useAppKeyboard.ts](useAppKeyboard.ts)                                                 | window 通道快捷键的处理器表：命令 ID → 回调；null/缺失表示该命令当前不可用。                                    |
| [useAppPanels.ts](useAppPanels.ts)                                                     | 保活：side pane terminal 跨 workspace 会话上移到模块级 registry。                                               |
| [useAutomationProjectOptions.ts](useAutomationProjectOptions.ts)                       | 定义选择 Host 的虚拟项目；空项目在提交时初始化目录，不随打开的 tab 增减。                                       |
| [useBackgroundBashOutput.ts](useBackgroundBashOutput.ts)                               | 隐藏后重新打开时，旧请求仍可能在途；等其结束，但绝不应用旧响应。                                                |
| [useBotBoundGroups.ts](useBotBoundGroups.ts)                                           | 迟到的失败不能覆盖广播触发的新读取结果。                                                                        |
| [useBotGroupMemberNames.ts](useBotGroupMemberNames.ts)                                 | 切换群或授权后立即隐藏旧缓存，不等 effect 清理完成。                                                            |
| [useBotGroupTask.ts](useBotGroupTask.ts)                                               | 首次准备还没有 accepted source，渠道名称取当前机器人配置，不默认猜作飞书。                                      |
| [useBotPrivateDeliveryRetry.ts](useBotPrivateDeliveryRetry.ts)                         | 实现或公开接口：useBotPrivateDeliveryRetry。                                                                    |
| [useBrowserSitePermissions.ts](useBrowserSitePermissions.ts)                           | main 站点权限 store 是唯一授权状态源；hook 只持有读取投影和用户操作的进度。                                     |
| [useBuiltinAgentCli.ts](useBuiltinAgentCli.ts)                                         | 实现或公开接口：useBuiltinAgentCli。                                                                            |
| [useCancelPendingRemoteConnection.ts](useCancelPendingRemoteConnection.ts)             | 实现或公开接口：useCancelPendingRemoteConnection。                                                              |
| [useClaudeSessionMigration.ts](useClaudeSessionMigration.ts)                           | 关键业务逻辑：Claude 原生历史迁移读取的是“当前机器上的 ~/.claude/projects”。                                    |
| [useClientScenesResource.ts](useClientScenesResource.ts)                               | macOS 点击关闭只 hide BrowserWindow，renderer 与 SWR 缓存不会销毁；                                             |
| [useCodingPlanEntryPlanList.ts](useCodingPlanEntryPlanList.ts)                         | 不传当前选中的团队上下文，四种 Start/个人连接分别使用已有权益缓存。                                             |
| [useCodingPlanQuotaResetUi.ts](useCodingPlanQuotaResetUi.ts)                           | 只替换目标类型的槽位，另一类型保持不变；显式分支避免 union 计算键的类型收窄问题。                               |
| [useCommands.ts](useCommands.ts)                                                       | service 曾隐式取自 useServices()，而 workspacePath 由调用方按 Scope target 传入，                               |
| [useComposerConnectionSwitch.ts](useComposerConnectionSwitch.ts)                       | 根因：连接刷新先于选模完成，旧实现只锁菜单，发送仍可冻结旧 provider。                                           |
| [useConfirmDialog.ts](useConfirmDialog.ts)                                             | 只包装显式入口；scope 必须稳定，并随原状态 owner 的目标换代而改变。                                             |
| [useCredentials.ts](useCredentials.ts)                                                 | \* useCredentials —— 凭据服务 hooks                                                                             |
| [useCuaComposerEntry.ts](useCuaComposerEntry.ts)                                       | \* CUA 输入框常驻入口按钮的数据编排。                                                                           |
| [useCuaPermissionStatus.ts](useCuaPermissionStatus.ts)                                 | Computer Use Helper 的 macOS 权限状态。状态来自 Helper 当前 runtime preflight，                                 |
| [useDesktopUpdateMenu.ts](useDesktopUpdateMenu.ts)                                     | main 持有更新状态；先订阅，避免较慢的初始快照覆盖已经收到的新状态。                                             |
| [useDeveloperToolsVisibility.ts](useDeveloperToolsVisibility.ts)                       | 实现或公开接口：useDeveloperToolsVisibility。                                                                   |
| [useDynamicWorkflowAvailability.ts](useDynamicWorkflowAvailability.ts)                 | 只读，不触发请求：取数由 Root 里的 loader 唯一负责。消费方（自动化页、run 面板）可能位于                        |
| [useEnsureWorkspaceMcpLoaded.ts](useEnsureWorkspaceMcpLoaded.ts)                       | 修复说明：这里曾把当前 tab 的 mcpSyncService 设为 store 的全局目录服务，设置页 Scope                            |
| [useFileContextActions.ts](useFileContextActions.ts)                                   | 交互语义：审查面板里的“在文件管理器中打开”用于回到文件所在目录，                                                |
| [useFileService.ts](useFileService.ts)                                                 | \* useFileService —— 文件服务 hooks                                                                             |
| [useFileWatcherService.ts](useFileWatcherService.ts)                                   | \* useFileWatcherService —— 文件系统监视 hooks                                                                  |
| [useGenUi.ts](useGenUi.ts)                                                             | 实现或公开接口：useGenUi。                                                                                      |
| [useGitActions.ts](useGitActions.ts)                                                   | 实现或公开接口：useGitActions。                                                                                 |
| [useGitAutoRefresh.ts](useGitAutoRefresh.ts)                                           | agent 批量写文件时，150ms watcher 防抖 + 350ms Git 防抖仍会把长批次拆成多轮                                     |
| [useGitBranchSwitcher.ts](useGitBranchSwitcher.ts)                                     | gitSummary 是 HEAD 的真实来源(由文件 watcher 实时回灌)。传入它的当前分支/HEAD 类型，                            |
| [useGitRepository.ts](useGitRepository.ts)                                             | 实现或公开接口：GitPaneFileChange、GitPaneSection、GitPaneDataset、GitPaneSourceOption。                        |
| [useGlobalTaskList.ts](useGlobalTaskList.ts)                                           | workspaceSignature 是标准化后的 scope 值签名，避免父组件重建 tabs 数组时重复查询。                              |
| [useImageFilePreview.ts](useImageFilePreview.ts)                                       | 从当前 workspace 的 Host 读取原目标，绝不按展示文件名猜路径或调用本机文件 API。                                 |
| [useInterfaceMode.ts](useInterfaceMode.ts)                                             | 实现或公开接口：useIsOfficeMode。                                                                               |
| [useModelProviders.ts](useModelProviders.ts)                                           | 本地 Provider Settings 的连通性测试使用的本地 cwd；不采用远程激活路径。                                         |
| [useModelSelectionView.ts](useModelSelectionView.ts)                                   | 首读的临时 IO 失败未必产生 Provider 变化事件；只重读两次，不轮询业务状态或重试写操作。                          |
| [useModelTrajectory.ts](useModelTrajectory.ts)                                         | \* 读取某个 task/session 的模型调用轨迹（model-io）。                                                           |
| [useModelTrajectoryOpenBridge.ts](useModelTrajectoryOpenBridge.ts)                     | \* 订阅“打开模型调用轨迹”请求并交给当前 workspace 的侧边栏控制器。                                              |
| [useOAuth.ts](useOAuth.ts)                                                             | \* useOAuth —— OAuth 登录流程 hook                                                                              |
| [useOffPeakEligibility.ts](useOffPeakEligibility.ts)                                   | 两个闲时入口共享初始化/连接/Registry 通知边界，不在组件中另存资格。                                             |
| [useOffPeakTaskNotifications.ts](useOffPeakTaskNotifications.ts)                       | 闲时任务系统通知（通知；权威路径应用内、通知点击跳 session；样式待设计补）。                                    |
| [useOnboardingRecordService.ts](useOnboardingRecordService.ts)                         | \* Onboarding 完成记录服务（本地持久化，后续上传服务器）。                                                      |
| [usePlanIdentitySnapshot.ts](usePlanIdentitySnapshot.ts)                               | 实现或公开接口：usePlanIdentitySnapshot。                                                                       |
| [usePlatform.tsx](usePlatform.tsx)                                                     | \* usePlatform —— 通过 React Context 提供 IPlatformService                                                      |
| [usePluginReferenceCatalog.ts](usePluginReferenceCatalog.ts)                           | 显式重试代次；菜单重开时重新查询，关闭菜单不清空已加载的目录。                                                  |
| [usePlugins.ts](usePlugins.ts)                                                         | 无活动工作区时保留上一份插件缓存，会让 Discover 仍可点安装但 store.workspacePath 为空而静默失败。               |
| [usePluginStoreOrder.ts](usePluginStoreOrder.ts)                                       | 只持有当前页面投影；请求合并与 TTL 统一归 Host 配置服务管理。                                                   |
| [usePptxFileWatch.ts](usePptxFileWatch.ts)                                             | 文件监听只负责自动刷新；注册失败时仍允许首次读取和手动重新打开文件。                                            |
| [usePreviewViewerLabels.ts](usePreviewViewerLabels.ts)                                 | \* 两个重量级叶子查看器（PDF / PPTX）的本地化标签。                                                             |
| [useProviderSettingsView.ts](useProviderSettingsView.ts)                               | 提交 mutation 返回的权威 View；不依赖异步 onDidChange 事件才能收敛 UI。                                         |
| [useRemoteConnectionEntryVisibility.ts](useRemoteConnectionEntryVisibility.ts)         | SSH 入口之前采用了 internal-only gate，生产态外网环境会被一并隐藏。                                             |
| [useRemoteConnectionForm.ts](useRemoteConnectionForm.ts)                               | Bugfix: Server remote 目前只是本地开发能力。之前无条件放入可选列表，                                            |
| [useRemoteConnectionLogs.ts](useRemoteConnectionLogs.ts)                               | Source Server phase 是 bootstrap UI 的正式状态，不是通用日志前缀，必须保留。                                    |
| [useRemoteConnectionProfileEditor.ts](useRemoteConnectionProfileEditor.ts)             | 编辑框只保留表单草稿；打开时按当前展示状态关联的连接读取权威记录。                                              |
| [useResolvedRemoteWorkspaceSessionId.ts](useResolvedRemoteWorkspaceSessionId.ts)       | 缺少 identity 也可能是 local workspace，不能一律伪造成旧 remote tab。                                           |
| [useRunningBackgroundTaskElapsedClock.ts](useRunningBackgroundTaskElapsedClock.ts)     | 单个任务完成不应重启整组计时器，否则剩余任务的秒数会短暂停顿后跳变。                                            |
| [useServices.tsx](useServices.tsx)                                                     | \* useServices —— 通过 React Context 提供 IServiceAccessor                                                      |
| [useSessionDebug.ts](useSessionDebug.ts)                                               | 调试查询按完成节拍刷新，不重叠请求；切任务后的旧结果不能覆盖新任务。                                            |
| [useSessionSubagents.ts](useSessionSubagents.ts)                                       | 新完成项会插入 ended 顶部。多取同样数量的旧项，避免刷新时把用户已经                                             |
| [useSettingService.ts](useSettingService.ts)                                           | \* useSettingService —— 设置服务 hooks                                                                          |
| [useSettingsSync.ts](useSettingsSync.ts)                                               | 首启自动检测与设置页手动重开对“空 discovery”的处理不同。                                                        |
| [useSkills.ts](useSkills.ts)                                                           | \* Composer 的 Skill catalog。                                                                                  |
| [useSlashCommands.ts](useSlashCommands.ts)                                             | \* ZCode Agent Slash Commands 便捷 hook                                                                         |
| [useSourceServerDisplayNames.ts](useSourceServerDisplayNames.ts)                       | 实现或公开接口：useSourceServerDisplayNames。                                                                   |
| [useSourceServerManagementSnapshot.ts](useSourceServerManagementSnapshot.ts)           | 统计完成也会触发目录事件；只有显式进入/刷新页面才主动重读，避免事件反馈形成轮询。                               |
| [useSourceServerOperationLogs.ts](useSourceServerOperationLogs.ts)                     | 事件只触发重读，关闭页面后仍从同一个 Host owner 查询；不在 UI 累积历史。                                        |
| [useSourceServerStatuses.ts](useSourceServerStatuses.ts)                               | 管理快照中全部设备的展示输入（按 sourceServerId）；Web / 手机没有管理服务时为空。                               |
| [useStableAccountAccess.ts](useStableAccountAccess.ts)                                 | Schema 解析会为同一份 Account Access 生成新对象；hook 依赖必须按配置值稳定。                                    |
| [useStartPlanEntitlement.ts](useStartPlanEntitlement.ts)                               | 消费目标 Host 的原账号视图和权益 owner；不另存余额或登录状态。                                                  |
| [useStartPlanRecommendation.ts](useStartPlanRecommendation.ts)                         | 推荐只编辑本次提交的选择；设置与额度仍由 App/Host 的原服务拥有。                                                |
| [useSubagents.ts](useSubagents.ts)                                                     | 远程 workspace 断连或 session 尚未重挂时，@ 面板会随输入框挂载预加载子智能体。                                  |
| [useSystemService.ts](useSystemService.ts)                                             | \* useSystemService —— 系统服务 hooks                                                                           |
| [useTabPersistence.ts](useTabPersistence.ts)                                           | \* useTabPersistence —— 标签页持久化                                                                            |
| [useTaskInteractionAutoResolutionSnooze.ts](useTaskInteractionAutoResolutionSnooze.ts) | \* 侧栏 task 可能来自本地、远端、timeline 或 pinned 列表；暂停命令必须按 workspace identity                     |
| [useTaskNativeSessionLogFile.ts](useTaskNativeSessionLogFile.ts)                       | \* useWorkspaceActiveTaskState 的导出返回类型间接引用此接口，声明生成要求它可导出。                             |
| [useTaskNotifications.ts](useTaskNotifications.ts)                                     | \* v4 重构删掉旧 renderer background monitor 后，platform 通知通道仍在，                                        |
| [useTaskSessionFilePath.ts](useTaskSessionFilePath.ts)                                 | \* useWorkspaceActiveTaskState 的导出返回类型间接引用此接口，声明生成要求它可导出。                             |
| [useTerminalService.ts](useTerminalService.ts)                                         | \* useTerminalService —— 终端服务 hooks                                                                         |
| [useTextSelection.ts](useTextSelection.ts)                                             | 统一鼠标、键盘和触控选区的监听；作用域变化后旧选区不能路由到新任务。                                            |
| [useTokenRefresh.ts](useTokenRefresh.ts)                                               | \* useTokenRefresh —— Token 刷新 hook（常驻层）                                                                 |
| [useToolPresentationHostCapabilities.ts](useToolPresentationHostCapabilities.ts)       | 宿主能力只在 App 装配；公开 renderer 不读取用户配置或平台服务。                                                 |
| [useUsageEntitlement.ts](useUsageEntitlement.ts)                                       | 侧栏、工具栏、设置页和 Usage 页会在启动/打开设置时同时读取同一份                                                |
| [useUsageStats.ts](useUsageStats.ts)                                                   | App Usage 与 Coding Plan 共用同一个 hook 实例。                                                                 |
| [useVulnerabilityReportUrl.ts](useVulnerabilityReportUrl.ts)                           | 缓存由公共配置服务持有，菜单只投影本次打开的结果。                                                              |
| [useWebElementPicker.ts](useWebElementPicker.ts)                                       | \* 传输无关的脚本执行出口：把选择脚本送到目标网页并回传结果。                                                   |
| [useWebRemoteControlStatus.ts](useWebRemoteControlStatus.ts)                           | 相同值的 updater 虽不触发 render，仍会留在 React pending 队列；空闲轮询会持续累积。                             |
| [useWebRemoteControlTaskOpen.ts](useWebRemoteControlTaskOpen.ts)                       | 未读写入失败不能阻止用户打开任务；返回首页后由权威 tasks-index 快照恢复蓝点。                                   |
| [useWorkflowRunArtifactBytes.ts](useWorkflowRunArtifactBytes.ts)                       | \* 内容产物（`file` / `markdown`）的字节读取。                                                                  |
| [useWorkflowRunArtifactData.ts](useWorkflowRunArtifactData.ts)                         | \* 不变式：**看板是 journal 的投影**。这里读的是 `kind = "report"` 且 `artifact_id` 相符的                      |
| [useWorkflowRunArtifacts.ts](useWorkflowRunArtifacts.ts)                               | \* ⚠ 术语：本模块的 artifact 是                                                                                 |
| [useWorkflowRunJournalSummaries.ts](useWorkflowRunJournalSummaries.ts)                 | \* dwf run 的发现查询。                                                                                         |
| [useWorkflowRunNodeResult.ts](useWorkflowRunNodeResult.ts)                             | \* 一个工作区节点的正文（docs/dynamic-workflow/transcript-and-notifications.md「The panel」）：卡片展开时才取， |
| [useWorkflowRunWorkspace.ts](useWorkflowRunWorkspace.ts)                               | \* 一个 workflow run 的脚本 transcript 清单。                                                                   |
| [useWorkflowSubagentModelProviderName.ts](useWorkflowSubagentModelProviderName.ts)     | \* 子代理模型的 provider 名从哪儿来：会话的模型清单                                                             |
| [useWorkspaceActiveTaskState.ts](useWorkspaceActiveTaskState.ts)                       | \* 任务元数据只读 Host 的 tasks-index（唯一数据源）：先订阅再读取，任务列表或项目变化时重读。                   |
| [useWorkspaceHomePath.ts](useWorkspaceHomePath.ts)                                     | 实现或公开接口：buildWorkspaceHomeCacheKey、resetWorkspaceHomePathCacheForTests、useWorkspaceHomePath。         |
| [useWorkspaceOpenInEditorTarget.ts](useWorkspaceOpenInEditorTarget.ts)                 | 修复原因：远程文件动作以前只携带 Linux path，renderer 无法判断它属于哪个 SSH/WSL 目标；                         |
| [useWorkspacePrepare.ts](useWorkspacePrepare.ts)                                       | useWorkspacePrepare 的实现文件。                                                                                |
| [useWorkspaceProviderConfigFile.ts](useWorkspaceProviderConfigFile.ts)                 | Bugfix: 远程 workspace 下如果误回退到 workspaceZCodeService，                                                   |
| [useWorkspaceServices.tsx](useWorkspaceServices.tsx)                                   | 断连代理曾自行维护普通事件白名单，新增 onAgentRuntimeRestarted 后被误判成                                       |
| [useZCodeAgentService.ts](useZCodeAgentService.ts)                                     | 实现或公开接口：useZCodeAgentService。                                                                          |
| [useZCodeConfig.ts](useZCodeConfig.ts)                                                 | \* ZCode Agent ConfigOptions 便捷 hooks                                                                         |
| [useZCodeSessionService.ts](useZCodeSessionService.ts)                                 | 实现或公开接口：useZCodeSessionService。                                                                        |
| [useZCodeTaskService.ts](useZCodeTaskService.ts)                                       | 内存诊断计数器：WeakMap 无法枚举，记住最近一个                                                                  |
| [workspacePrepareRpc.ts](workspacePrepareRpc.ts)                                       | \* workspace prepare 的协议 RPC 收口。                                                                          |

<!-- qingqi-directory-index:end -->
