# saved-workflows

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 saved workflows 实现源码。

### 文件

| 文件                                                                     | 简要说明                                                                                       |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| [automationsPageTabMemory.ts](automationsPageTabMemory.ts)               | 自动化页顶级标签的记忆：记在 sessionStorage，                                                  |
| [AutomationsPageTitleSwitch.tsx](AutomationsPageTitleSwitch.tsx)         | 自动化页的两个顶级标签。                                                                       |
| [globalWorkflowGroupHelpers.ts](globalWorkflowGroupHelpers.ts)           | 全局工作流组的纯逻辑。与组件分文件以守住 max-lines 400，                                       |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                               |
| [savedWorkflowArgsForm.ts](savedWorkflowArgsForm.ts)                     | 已保存工作流的实参表单与元数据实参表。                                                         |
| [SavedWorkflowArgsTable.tsx](SavedWorkflowArgsTable.tsx)                 | 详情页「参数」声明表：可增删行，默认值按类型出控件。                                           |
| [SavedWorkflowArtifactChips.tsx](SavedWorkflowArtifactChips.tsx)         | \* 中枢里的产物条：运行历史行的状态词之后用小号药丸，                                          |
| [SavedWorkflowCard.tsx](SavedWorkflowCard.tsx)                           | 卡片「上次运行」徽标：四态 + 尚未运行。沿用定时任务卡的徽标形状（rounded-lg，20px 图标槽）。   |
| [savedWorkflowContract.ts](savedWorkflowContract.ts)                     | 已保存工作流中枢的跨组件类型契约。                                                             |
| [SavedWorkflowDetailHeader.tsx](SavedWorkflowDetailHeader.tsx)           | 标题旁的归属小标：项目名，全局档为「全局」。                                                   |
| [SavedWorkflowDetailView.tsx](SavedWorkflowDetailView.tsx)               | 项目档传 workspace target；全局档传 `{ scope: "global" }`（get/updateMeta 直接透传）。         |
| [SavedWorkflowGlobalGroup.tsx](SavedWorkflowGlobalGroup.tsx)             | 页级刷新计数器；变化（非首挂）时绕过缓存重拉。                                                 |
| [SavedWorkflowLaunchDialog.tsx](SavedWorkflowLaunchDialog.tsx)           | 实参控件的 DOM id：label 的 htmlFor 与校验失败后的聚焦都认它。                                 |
| [savedWorkflowLaunchPrompt.ts](savedWorkflowLaunchPrompt.ts)             | 中枢的「通过对话创建 / 在对话里修订」预填文案。                                                |
| [SavedWorkflowMetaForm.tsx](SavedWorkflowMetaForm.tsx)                   | \* 详情页「基本信息」表单：说明 / 何时使用 / 参数表                                            |
| [SavedWorkflowMoveDialog.tsx](SavedWorkflowMoveDialog.tsx)               | 被移动的工作流名（用作对话描述）；null 时不渲染标题上下文。                                    |
| [SavedWorkflowProjectGroup.tsx](SavedWorkflowProjectGroup.tsx)           | 组把加载态回报给页的类型定义在 savedWorkflowContract；这里再导出，历史 import 路径不变。       |
| [savedWorkflowRunHistory.ts](savedWorkflowRunHistory.ts)                 | 归属只按 `dwf_run.name === 工作流名`；模型另起名字的 run 不归任何工作流，而不是猜。            |
| [SavedWorkflowRunHistoryPanel.tsx](SavedWorkflowRunHistoryPanel.tsx)     | 详情页某一行运行记录对应的项目（全局工作流跨 cwd 时用；cwd 命中已打开项目才能「查看实例」）。  |
| [SavedWorkflowsSection.tsx](SavedWorkflowsSection.tsx)                   | 深链目标：默认 project（缺 scope 兼容旧调用），或 global（无 workspaceKey）。                  |
| [useSavedWorkflowGlobalGroup.ts](useSavedWorkflowGlobalGroup.ts)         | 全局工作流组的状态与动作。抽成 hook 让组件文件守住                                             |
| [useSavedWorkflowLauncher.ts](useSavedWorkflowLauncher.ts)               | 不再合成对话文案：在目标项目里建一个空会话 → 向它发 startSavedWorkflow 命令 →                  |
| [useSavedWorkflowProjectTargets.ts](useSavedWorkflowProjectTargets.ts)   | RPC target（含 remoteSessionId），供 store / 服务方法调用。                                    |
| [useSavedWorkflowPromote.ts](useSavedWorkflowPromote.ts)                 | // 项目档→全局档不是搬文件：项目工作流大多引用本仓库的路径 / 命令 / 约定，逐字节搬过去就是一个 |
| [useSavedWorkflowRunOpeners.ts](useSavedWorkflowRunOpeners.ts)           | 一行运行记录归属的项目（项目档恒定，全局档按 `run.cwd` 反查）。                                |
| [useSavedWorkflowsDirectoryWatch.ts](useSavedWorkflowsDirectoryWatch.ts) | workspacePath 可能是 Windows 路径；沿用它自己的分隔符拼子目录，别把 `/` 混进 `\\` 路径。       |

<!-- qingqi-directory-index:end -->
