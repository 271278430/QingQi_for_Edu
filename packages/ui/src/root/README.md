# root

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 root 实现源码。

### 文件

| 文件                                                                                   | 简要说明                                                                                                                                                                     |
| -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [accountConnectionLossSuggestion.ts](accountConnectionLossSuggestion.ts)               | 只计算建议，不替用户保存；闭包固定按钮展示的那个目标，点击时重新校验。                                                                                                       |
| [accountConnectionRefreshObserver.ts](accountConnectionRefreshObserver.ts)             | 新账号/新连接/恢复可用会立即废弃旧建议，包括其在途查询。                                                                                                                     |
| [botsTaskBroadcast.ts](botsTaskBroadcast.ts)                                           | Bugfix: /model、/mode、/think 这类 Bot 配置更新只同步 task 元数据/configOptions，                                                                                            |
| [botsTaskStreamBroadcast.ts](botsTaskStreamBroadcast.ts)                               | 实现或公开接口：resolveBotTaskStreamBroadcast。                                                                                                                              |
| [DiffsWorkerPoolProvider.tsx](DiffsWorkerPoolProvider.tsx)                             | 实现或公开接口：DiffsWorkerPoolProvider。                                                                                                                                    |
| [GlobalDatabaseStartupLoading.tsx](GlobalDatabaseStartupLoading.tsx)                   | 新 attempt 会作废仍在打包的旧导出结果，避免迟到结果落到下一次失败页。                                                                                                        |
| [oauthCachedSessionRestore.ts](oauthCachedSessionRestore.ts)                           | 启动过期和运行时撤销使用同一登录恢复入口，不重启进程或保留头像展示。                                                                                                         |
| [oauthLoginAttemptGuard.ts](oauthLoginAttemptGuard.ts)                                 | 同一轮登录已经成功或正在完成成功回调时，忽略另一条路径的迟到失败。                                                                                                           |
| [oauthProviderFamilySelectionRefresh.ts](oauthProviderFamilySelectionRefresh.ts)       | 登录/启动检查属于套餐只读查询。静态 mode 会经执行期 current 解析，                                                                                                           |
| [oauthTeamPricing.ts](oauthTeamPricing.ts)                                             | 两个账号域均须按自身 Family 查询；失败与明确空列表分开，不能据此自动改掉已有连接。                                                                                           |
| [openWorkspaceFolderEntry.ts](openWorkspaceFolderEntry.ts)                             | Web/server 根节点没有系统目录选择框，继续调用 selectDirectory 只会返回 null。                                                                                                |
| [PostUpdateReleaseNotesDialog.tsx](PostUpdateReleaseNotesDialog.tsx)                   | M5②.5 store 耦合剥离：MessageResponse 不再自取 store，主题/代码预览设置由调用方传入。                                                                                        |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                                                                                                                                             |
| [reconnectingRemoteWorkspaceLogs.ts](reconnectingRemoteWorkspaceLogs.ts)               | 旧版本日志没有 requestId，只能靠 target label 前缀兜底。                                                                                                                     |
| [reconnectRemoteWorkspaceHistoryEntry.ts](reconnectRemoteWorkspaceHistoryEntry.ts)     | 目录当前 tab 上仍在线的 owner session；没有或已失效时返回 undefined。                                                                                                        |
| [remoteWorkspaceSessionPersistence.ts](remoteWorkspaceSessionPersistence.ts)           | 窗口只拥有活动选择；项目集合与旧版凭据快照由 Host 派生。                                                                                                                     |
| [rootPlatformWorkspaceSync.ts](rootPlatformWorkspaceSync.ts)                           | workspace 同步只有一个完整快照入口，不依赖远控是否已有 runtime。                                                                                                             |
| [RootShell.tsx](RootShell.tsx)                                                         | Web 远控在手机浏览器里不能用固定 100vh，                                                                                                                                     |
| [RootStartupLoading.tsx](RootStartupLoading.tsx)                                       | Web 端全局 html/body/#root 为 Electron 透明背景让路，React 接管后会替换 HTML 启动壳。                                                                                        |
| [RootWorkspaceContent.tsx](RootWorkspaceContent.tsx)                                   | Bugfix：工作区内的设置层显式转发 props，漏掉它会让分享管理解析到会话却不显示「跳转对话」。                                                                                   |
| [rootWorkspaceShellTarget.ts](rootWorkspaceShellTarget.ts)                             | 当前窗口全部 workspace tab；Settings 等非 workspace tab 激活时用来找回被覆盖的那个 tab。                                                                                     |
| [shareImportIntent.ts](shareImportIntent.ts)                                           | 实现或公开接口：ShareImportIntentStatus、ShareImportIntent、createShareImportIntent、isShareImportIntentSame。                                                               |
| [sourceServerUpdateNotifications.ts](sourceServerUpdateNotifications.ts)               | 向导在发起连接前接管目标；不能等 needs-upgrade 到达后再抑制，否则会先弹出重复操作。                                                                                          |
| [types.ts](types.ts)                                                                   | 账号级设备导航由 Web 入口注入，不通过 workspace bridge/RPC 访问。                                                                                                            |
| [useAccountConnectionLossNotification.ts](useAccountConnectionLossNotification.ts)     | 根层只观察一次；页面/文案变化不重新建立账号基线。                                                                                                                            |
| [useBotBroadcastEffects.ts](useBotBroadcastEffects.ts)                                 | Bugfix: Bot /mode 不经过 ChatInputToolbar/useTaskStreamEvents。                                                                                                              |
| [useConversationWorkspaceActions.ts](useConversationWorkspaceActions.ts)               | 对话工作区是 app 管理的独立 cwd，不属于用户项目：不走跨窗口项目激活，                                                                                                        |
| [useDesktopNativeThemeSync.ts](useDesktopNativeThemeSync.ts)                           | 原生窗口主题会影响 macOS vibrancy；启动 loading 阶段先不写 nativeTheme，                                                                                                     |
| [useProviderAvailabilityLoginEntryGuard.ts](useProviderAvailabilityLoginEntryGuard.ts) | 未登录且没有可用模型配置时必须引导用户连接账号或填写 API Key。                                                                                                               |
| [useReconnectingRemoteWorkspaceLogs.ts](useReconnectingRemoteWorkspaceLogs.ts)         | 已结束的失败日志仍由此 owner 持有，下一次请求 reset 或移除项目时释放。                                                                                                       |
| [useRemoteWorkspaceHistory.ts](useRemoteWorkspaceHistory.ts)                           | 实现或公开接口：updateRemoteWorkspaceRecoveringKeys、shouldAttemptStartupReconnectForSourceState、shouldAttemptStartupReconnectForTabChange、isRemoteWorkspaceCloseFailure。 |
| [useRemoteWorkspaceTabLifecycle.ts](useRemoteWorkspaceTabLifecycle.ts)                 | 仍带 remoteSessionId 的 tab 会由本 hook 下方的正常移除流程释放，                                                                                                             |
| [useRootOAuthEffects.ts](useRootOAuthEffects.ts)                                       | 账号已完成登录；自动初始化冲突或权益查询失败不能回滚主身份。                                                                                                                 |
| [useRootPlatformEffects.ts](useRootPlatformEffects.ts)                                 | IntlProvider 是否已从持久化设置确定语言；未确定前 locale 只是占位初值。                                                                                                      |
| [useRootProviderSettingsSnapshot.ts](useRootProviderSettingsSnapshot.ts)               | 实现或公开接口：useRootProviderSettingsSnapshot。                                                                                                                            |
| [useRootProviderStateRefresh.ts](useRootProviderStateRefresh.ts)                       | Provider Runtime 统一刷新 Config、Account Source 与 Registry；Root 不再维护旧快照。                                                                                          |
| [useRootWorkspaceActions.ts](useRootWorkspaceActions.ts)                               | 新任务落点：identity 缺省一律归一化为 null，供只读校验、focus/addTab 统一消费。                                                                                              |
| [WorkspaceSettingsLayer.tsx](WorkspaceSettingsLayer.tsx)                               | 实现或公开接口：WorkspaceSettingsLayer。                                                                                                                                     |
| [zcodeJwtInvalidRestartMarker.ts](zcodeJwtInvalidRestartMarker.ts)                     | 该标记只服务于本次重启；如果不在读取时删除，后续正常启动仍会被强制带回登录页。                                                                                               |

<!-- qingqi-directory-index:end -->
