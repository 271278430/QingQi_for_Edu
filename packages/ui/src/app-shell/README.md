# app-shell

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 app shell 实现源码。

### 子目录

| 目录                                                | 存放内容                                             |
| --------------------------------------------------- | ---------------------------------------------------- |
| [workflow-artifacts/](workflow-artifacts/README.md) | @zcode/ui 基础工程中的 workflow artifacts 实现源码。 |

### 文件

| 文件                                                                       | 简要说明                                                                                                         |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [AnimatedSidePanePanel.tsx](AnimatedSidePanePanel.tsx)                     | 实现或公开接口：AnimatedSidePanePanel。                                                                          |
| [animatedSidePanePanelModel.ts](animatedSidePanePanelModel.ts)             | 「打开标签页」里内置的 Sites 入口打开的官方插件（只有一个 surface）。                                            |
| [AnimatedTerminalPanel.tsx](AnimatedTerminalPanel.tsx)                     | 终端面板拖拽时会产生连续 ResizeObserver 回调。                                                                   |
| [BackgroundBashOutputSidePane.tsx](BackgroundBashOutputSidePane.tsx)       | 实现或公开接口：BackgroundBashOutputSidePane。                                                                   |
| [BrowserTabFavicon.tsx](BrowserTabFavicon.tsx)                             | renderer 直接加载 guest favicon 时会携带 localhost Referer，                                                     |
| [BrowserUseTabIcon.tsx](BrowserUseTabIcon.tsx)                             | 实现或公开接口：BrowserUseTabIcon。                                                                              |
| [PlanDetailSidePane.tsx](PlanDetailSidePane.tsx)                           | provider 接口已收敛为仅按 scope 做连接路由，不再接受                                                             |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                                                 |
| [SelectionSideChatPane.tsx](SelectionSideChatPane.tsx)                     | 父级 tabs.map 原来为每个 memo pane 创建内联闭包，任意父级渲染都会                                                |
| [sidePaneLayout.ts](sidePaneLayout.ts)                                     | 实现或公开接口：SIDE_PANE_DEFAULT_EXPANDED_SIZE、SIDE_PANE_DEFAULT_EXPANDED_RATIO、resolveSidePaneTabsOverflow。 |
| [SidePaneTabOverview.tsx](SidePaneTabOverview.tsx)                         | 实现或公开接口：SidePaneTabOverview。                                                                            |
| [sidePaneTabPresentation.ts](sidePaneTabPresentation.ts)                   | 扩展日志标签（docs/plugins/extension-host.md §16.8）。                                                           |
| [sidePaneTabSearch.ts](sidePaneTabSearch.ts)                               | 实现或公开接口：buildSearchFields、normalizeSearchQuery、filterAndRankSearchItems。                              |
| [SidePaneTabTitleTooltip.tsx](SidePaneTabTitleTooltip.tsx)                 | 拖拽开始后清掉已打开状态，避免拖拽结束时在旧 tab 上恢复 tooltip。                                                |
| [SidePaneTabTrigger.tsx](SidePaneTabTrigger.tsx)                           | tab 默认按 156px 等宽排列；空间不足时以相同 grow/shrink 参数平均收缩到 60px，                                    |
| [SubagentDirectorySidePane.tsx](SubagentDirectorySidePane.tsx)             | 实现或公开接口：buildSubagentDirectoryOpenRequest、SubagentDirectorySidePane。                                   |
| [SubagentSessionSidePane.tsx](SubagentSessionSidePane.tsx)                 | 实现或公开接口：SubagentSessionSidePane。                                                                        |
| [taskNavigationWorkspace.ts](taskNavigationWorkspace.ts)                   | 远程 workspace 的 identity 只表达隔离身份，不能据此重建 SSH/WSL/Docker                                           |
| [types.ts](types.ts)                                                       | Renderer 发起方租约；异步准备期间取消或换草稿后不得导航。                                                        |
| [useAnimatedResizablePanel.ts](useAnimatedResizablePanel.ts)               | 显隐仍由原开关派生；动画只管理临时样式，不维护第二份开关状态。                                                   |
| [useAppChromeState.ts](useAppChromeState.ts)                               | 旧的 UpdateReady 事件只会告诉 renderer “某版本 ready”，不会告诉它后续                                            |
| [useTaskSidePaneMemoryBridge.ts](useTaskSidePaneMemoryBridge.ts)           | Git pane 的 source 和 Browser URL 都属于 workspace 级 side pane UI 状态。                                        |
| [useWorkflowRunPaneSettings.ts](useWorkflowRunPaneSettings.ts)             | 从 WorkflowRunSidePane.tsx 拆出（max-lines 门）：弹层宿主、开关与锚点、以及 Apply 被接受之后                     |
| [useWorkspaceMainViewSettingsExit.ts](useWorkspaceMainViewSettingsExit.ts) | 插件市场已经打开时，从设置页再次点击“新建”，主视图值仍是                                                         |
| [useWorkspaceSessionReload.ts](useWorkspaceSessionReload.ts)               | Header 与错误条都可触发 reload，会出现短时间双击/连点并发重建。                                                  |
| [useWorkspaceShellLifecycle.ts](useWorkspaceShellLifecycle.ts)             | Root 之前依赖按 workspacePath 改 key 来"切工作区就整棵重建 App"，                                                |
| [useWorkspaceShellZCodeState.ts](useWorkspaceShellZCodeState.ts)           | App 之前直接订阅整个 workspaceZCodeState，streaming 每个 chunk 都会改 taskMessagesByTaskId。                     |
| [useWorkspaceTaskNavigation.ts](useWorkspaceTaskNavigation.ts)             | 跨 workspace 选择会先同步切换 tab，但本次 React render 捕获的 ambient                                            |
| [webRemoteNavigationLayout.ts](webRemoteNavigationLayout.ts)               | Bugfix: 远控顶部区域折叠时如果把 sidebar panel 从布局树里移除，                                                  |
| [WorkflowActorSessionSidePane.tsx](WorkflowActorSessionSidePane.tsx)       | \* 未启动占位。从卡上一枚还没启动的药丸点开的 tab 落地就是它。                                                   |
| [WorkflowArtifactSidePane.tsx](WorkflowArtifactSidePane.tsx)               | \* 稳定引用的空摘要列表：`artifacts` 键在零产物时**缺席**，坍缩成一个每帧新造的 `[]`                             |
| [workflowRunActionRejection.ts](workflowRunActionRejection.ts)             | 详情页 Cancel / Resume 被拒时的结构化解释                                                                        |
| [WorkflowRunArtifactsSection.tsx](WorkflowRunArtifactsSection.tsx)         | \* workflow run 详情页的产物区。                                                                                 |
| [WorkflowRunDirectorySidePane.tsx](WorkflowRunDirectorySidePane.tsx)       | \* 一条对话的 workflow run 目录。三步形状与 subagent 目录逐字同构：任务列表页脚行 → 这一页 → `workflow-run`      |
| [WorkflowRunFillFrames.tsx](WorkflowRunFillFrames.tsx)                     | \* 侧板上补全的框（docs/dynamic-workflow/presentation.md「The pane」）：与卡上同一个框竖着画——同墨、同圆角、     |
| [WorkflowRunHoleParts.tsx](WorkflowRunHoleParts.tsx)                       | \* 侧板脊线上的留白零件（docs/dynamic-workflow/presentation.md「Holes on the timeline」的「The pane」）。        |
| [workflowRunLaunchProvenance.ts](workflowRunLaunchProvenance.ts)           | \* 直接启动的来龙去脉：作用域、说明、实参与                                                                      |
| [workflowRunPanel.ts](workflowRunPanel.ts)                                 | \* workflow run 详情页的纯逻辑：Cancel 可用性、结果/失败面板判定、事件日志行摘要。                               |
| [WorkflowRunPhaseList.tsx](WorkflowRunPhaseList.tsx)                       | \* 运行详情页的脊线：卡上的横向时间线在                                                                          |
| [WorkflowRunPhasePills.tsx](WorkflowRunPhasePills.tsx)                     | \* 详情页脊线上药丸的接线（docs/dynamic-workflow/presentation.md「The spine」）。从                              |
| [WorkflowRunProvenance.tsx](WorkflowRunProvenance.tsx)                     | 从 WorkflowRunSidePaneSections.tsx 拆出（max-lines 门）。两种 run 有这一块：中枢直接启动的                       |
| [WorkflowRunQuestionRow.tsx](WorkflowRunQuestionRow.tsx)                   | \* 一条升级问题：挂在提问者那一行下面。                                                                          |
| [workflowRunQuestions.ts](workflowRunQuestions.ts)                         | \* 待答问题（升级问答）的纯展示规则。                                                                            |
| [WorkflowRunSectionToggle.tsx](WorkflowRunSectionToggle.tsx)               | \* workflow run 详情页里可折叠分区的表头栏。                                                                     |
| [WorkflowRunSidePane.tsx](WorkflowRunSidePane.tsx)                         | \* 稳定引用的空列表：pendingQuestions 键会**来回**进出（问题一被作答就整键消失），                               |
| [WorkflowRunSidePaneSections.tsx](WorkflowRunSidePaneSections.tsx)         | WorkflowRunSidePane 的分区子组件（状态头 / 终态结果区）                                                          |
| [workflowRunSpine.ts](workflowRunSpine.ts)                                 | \* 脊线的排布（docs/dynamic-workflow/presentation.md「The spine」）：把时间线模型翻译成\*\*每一节                |
| [WorkflowRunSpineParts.tsx](WorkflowRunSpineParts.tsx)                     | 从 WorkflowRunPhaseList.tsx 拆出（max-lines 400）：清单文件承载展开状态、问题归属与药丸接线，                    |
| [workflowRunThrottle.ts](workflowRunThrottle.ts)                           | \* dwf run 详情页的自适应并发观察面（docs/dynamic-workflow/concurrency.md「Protocol and UI」）：                 |
| [WorkflowWorkspaceCard.tsx](WorkflowWorkspaceCard.tsx)                     | 脚本 transcript 的一个条目                                                                                       |
| [WorkflowWorkspaceCardBody.tsx](WorkflowWorkspaceCardBody.tsx)             | 脚本 transcript 条目的展开面板                                                                                   |
| [workflowWorkspaceLogbook.ts](workflowWorkspaceLogbook.ts)                 | 脚本 transcript 的「日志簿」形态：将卡片组织为章节（阶段）、时间标尺和命令输出尾部。                             |
| [WorkflowWorkspacePeek.tsx](WorkflowWorkspacePeek.tsx)                     | 收起的 Terminal 卡下面露出 stdout 最后三行，不用点开就知道命令说了什么。正文在卡**滚进视口**时                   |
| [WorkflowWorkspaceSidePane.tsx](WorkflowWorkspaceSidePane.tsx)             | 脚本 transcript 面板。                                                                                           |
| [workflowWorkspaceTranscript.ts](workflowWorkspaceTranscript.ts)           | 脚本 transcript 的纯模型                                                                                         |
| [workspaceRpcTarget.ts](workspaceRpcTarget.ts)                             | 实现或公开接口：resolveAppWorkspaceRpcTarget。                                                                   |
| [WorkspaceShellLayout.tsx](WorkspaceShellLayout.tsx)                       | 保活：workspace tab 真正关闭时，按 workspaceKey 回收 side pane terminal 的常驻 PTY/xterm。                       |
| [workspaceShellWindowChrome.ts](workspaceShellWindowChrome.ts)             | 忽略 macOS 版本会让 Sequoia 的内层 12px 圆角与原生窗口小圆角不协调。                                             |

<!-- qingqi-directory-index:end -->
