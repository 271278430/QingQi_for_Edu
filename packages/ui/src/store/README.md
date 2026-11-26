# store

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 store 界面状态。

### 文件

| 文件                                                                       | 简要说明                                                                                                     |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [alertDialogStore.ts](alertDialogStore.ts)                                 | 并发请求不会采用已有弹窗；返回 false 让破坏性动作（如重启）保持未确认状态。                                  |
| [automationManagementStore.ts](automationManagementStore.ts)               | 定时任务(automation)管理 store：走 zcode-agent RPC（列表 / 创建 / 编辑 / 启停 / 重跑 / 删除 + 运行历史）。   |
| [browserRecentVisitsStore.ts](browserRecentVisitsStore.ts)                 | 损坏的单个 scope 不影响其他会话的访问记录。                                                                  |
| [codeCommentPreviewStore.ts](codeCommentPreviewStore.ts)                   | 实现或公开接口：buildCodeCommentPreviewBucketKey、useCodeCommentPreviewStore。                               |
| [codingPlanQuotaResetState.ts](codingPlanQuotaResetState.ts)               | 同一 renderer 生命周期内，用户由未登录进入登录态时递增的鉴权会话序号。                                       |
| [commandsStore.ts](commandsStore.ts)                                       | 远端「用户」的 cacheAuthorityKey（`source-settings:<id>`）；项目与本机为 null。                              |
| [composerAttachmentUploadStore.ts](composerAttachmentUploadStore.ts)       | \* composer-owned 仍处于上传/暂存生命周期；session-owned 是从权威 queue 撤回的既有 ref。                     |
| [confirmDialogStore.ts](confirmDialogStore.ts)                             | 已由调用方脱敏的只读代码，与说明分区展示。                                                                   |
| [conversationShareSelectionStore.ts](conversationShareSelectionStore.ts)   | 没有服务端 issues 时展示的、按错误类型解析出的可行动文案。                                                   |
| [dynamicWorkflowAvailabilityStore.ts](dynamicWorkflowAvailabilityStore.ts) | 动态工作流灰度快照在 renderer 的唯一副本                                                                     |
| [embeddedBrowserPermissionStore.ts](embeddedBrowserPermissionStore.ts)     | \* 内置浏览器权限弹窗队列：main 经 IPC 推送请求，用户操作后由组件回传决策并出队。                            |
| [hooksStore.ts](hooksStore.ts)                                             | \* refresh 必须显式传入发起时的 target（path/identity/service 三元组）。                                     |
| [index.ts](index.ts)                                                       | \* Zustand Store —— 全局状态管理                                                                             |
| [mcpStore.ts](mcpStore.ts)                                                 | \* MCP (Model Context Protocol) UI State Store                                                               |
| [mcpStoreDesktop.ts](mcpStoreDesktop.ts)                                   | 实现或公开接口：McpPlatformService、McpDirectoryService、MigrateLegacyResult、persistCliMcpToUserDirectory。 |
| [mcpStoreHelpers.ts](mcpStoreHelpers.ts)                                   | ignore storage errors                                                                                        |
| [mcpStoreMigration.ts](mcpStoreMigration.ts)                               | 旧通用 MCP 保存在 localStorage，不迁移就直接去掉 common 读取会让用户配置从设置页和运行时消失。               |
| [mcpStoreStatusList.ts](mcpStoreStatusList.ts)                             | 未授权是明确状态，不能降为状态未知或提示用户重启 Agent。                                                     |
| [modelTrajectoryStore.ts](modelTrajectoryStore.ts)                         | \* 打开“模型调用轨迹”侧边栏的请求桥接 store。                                                                |
| [offPeakTaskStore.ts](offPeakTaskStore.ts)                                 | 闲时任务管理 store（与 automationManagementStore 独立）：走 IOffPeakTaskService RPC。                        |
| [pluginManagementStore.ts](pluginManagementStore.ts)                       | 市场详情按需拉取的组件清单缓存：按 pluginId 记 loading/data/error，避免重复请求与切换闪烁。                  |
| [pluginManagementStoreEnabled.ts](pluginManagementStoreEnabled.ts)         | 启停 RPC 和后续列表刷新存在可感知延迟。先投影最终状态，让开关立刻响应；失败时                                |
| [pluginManagementStoreLoading.ts](pluginManagementStoreLoading.ts)         | 只共享同服务、同身份、同配置投影的在途查询；每个视图仍独立写回和保存错误态。                                 |
| [pluginStore.ts](pluginStore.ts)                                           | 实现或公开接口：usePluginStore。                                                                             |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                                             |
| [remoteWorkspaceSessionStore.ts](remoteWorkspaceSessionStore.ts)           | Desktop bind 返回的旧 route tab rekey 提示；不参与 remote session 路由。                                     |
| [savedWorkflowStore.ts](savedWorkflowStore.ts)                             | 按 workspaceKey 分片；磁盘仍是唯一权威（不变式 2）——缓存只服务同一页内的重渲染，                             |
| [serviceAuthorityKey.ts](serviceAuthorityKey.ts)                           | Bug 原因：同路径/identity 可以同时存在于 Controller 与多个 Source；只按路径分桶会让                          |
| [skillStore.ts](skillStore.ts)                                             | 复制/移除技能到通用目录后 refresh 必须拿到最新结果。                                                         |
| [sourceServerDisplayNameRegistry.ts](sourceServerDisplayNameRegistry.ts)   | 实现或公开接口：SourceServerDisplayNameRegistry、getSourceServerDisplayNameRegistry。                        |
| [sourceServerStatusRegistry.ts](sourceServerStatusRegistry.ts)             | Registry lifetime follows the management service; the service owns disposal of its event.                    |
| [sourceSettingsServiceStore.ts](sourceSettingsServiceStore.ts)             | Bug 原因：旧 attachment 的 close 可能晚于新一代注册；只按 Source 删除会误删当前服务。                        |
| [StoreProvider.tsx](StoreProvider.tsx)                                     | \* StoreProvider —— 初始化 Zustand store 并通过 React Context 提供                                           |
| [subagentsContextStore.ts](subagentsContextStore.ts)                       | 实现或公开接口：SubagentsContextSnapshot、getSubagentsContextKey、useSubagentsContextStore。                 |
| [subagentsStore.ts](subagentsStore.ts)                                     | 正在操作的 agent ID（用于 UI 状态指示）                                                                      |
| [subagentsStoreLoading.ts](subagentsStoreLoading.ts)                       | 实现或公开接口：loadAgentsOnce、nextAgentLoadRequestId、isLatestAgentLoadRequest。                           |
| [tabStore.ts](tabStore.ts)                                                 | \* Tab Store —— 多标签页状态管理                                                                             |
| [TabStoreProvider.tsx](TabStoreProvider.tsx)                               | \* TabStoreProvider —— 初始化 Tab Zustand store 并通过 React Context 提供                                    |
| [tabWorkspaceIdentity.ts](tabWorkspaceIdentity.ts)                         | 实现或公开接口：isSameWorkspaceTab。                                                                         |
| [taskQueryCacheStore.ts](taskQueryCacheStore.ts)                           | 覆盖正在提交或等待 membership 确认的 unreadAt 字段；null 表示清除。                                          |
| [whiteboardStore.ts](whiteboardStore.ts)                                   | 实现或公开接口：useWhiteboardStore。                                                                         |
| [workflowRunSavedStore.ts](workflowRunSavedStore.ts)                       | 「这次 run 对应哪个已保存工作流」的读缓存（docs/dynamic-workflow/transcript-and-notifications.md             |
| [workspaceHookReviewStore.ts](workspaceHookReviewStore.ts)                 | review 单调性裁决单一来源；store 的应用策略是 cross_flow 接受新 Runtime 权威                                 |
| [zcodeSessionStore.ts](zcodeSessionStore.ts)                               | \* ZCode session UI 状态 store                                                                               |
| [zcodeSessionStoreNavigation.ts](zcodeSessionStoreNavigation.ts)           | \* ZCode Session Store 导航切片 —— 任务前进/后退历史管理                                                     |
| [zcodeSessionStoreSelectors.ts](zcodeSessionStoreSelectors.ts)             | \* ZCode Session Store 选择器与内部辅助函数                                                                  |
| [zcodeSessionStoreTaskSlice.ts](zcodeSessionStoreTaskSlice.ts)             | 同一 requestId 可能被连续投递成不同对象。raw 只用于展示预览，协议上 requestId 才是权限请求身份；             |
| [zcodeSessionStoreTypes.ts](zcodeSessionStoreTypes.ts)                     | \* ZCode Session Store 类型定义、接口、常量与默认值工厂                                                      |
| [zcodeSessionStoreWorkspaceSlice.ts](zcodeSessionStoreWorkspaceSlice.ts)   | 模型切换竞态里 thought_level 可能短暂为空；store 统一归一，避免工具栏 Select 进入空选中态。                  |

<!-- qingqi-directory-index:end -->
