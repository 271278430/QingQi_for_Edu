# renderers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 renderers 实现源码。

### 文件

| 文件                                                                           | 简要说明                                                                                                    |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| [agent.tsx](agent.tsx)                                                         | 实现或公开接口：AgentToolCallBlock。                                                                        |
| [agentHelpers.ts](agentHelpers.ts)                                             | agent 工具块的语言包一旦漏配，SSR/静态渲染会把内部 i18n key 原样打到 UI 上，                                |
| [agentPromptSection.tsx](agentPromptSection.tsx)                               | 实现或公开接口：AgentPromptSection。                                                                        |
| [ask-question.tsx](ask-question.tsx)                                           | 实现或公开接口：AskQuestionToolCallBlock。                                                                  |
| [create-workflow.tsx](create-workflow.tsx)                                     | 没有 display 时交给草稿槽位的空诊断：模块级常量，免得每次渲染一个新数组打穿记忆。                           |
| [createWorkflowDisplay.ts](createWorkflowDisplay.ts)                           | \* CreateWorkflow 工具输出侧的读取规则（display 载荷与纯文本兜底）。从 `create-workflow.tsx`                |
| [createWorkflowHoleInput.ts](createWorkflowHoleInput.ts)                       | \* FillWorkflowHole 行的目标留白（docs/dynamic-workflow/presentation.md「The fill row」）：`run_id`         |
| [createWorkflowInput.ts](createWorkflowInput.ts)                               | \* CreateWorkflow 工具入参的读取规则。                                                                      |
| [cron-create.tsx](cron-create.tsx)                                             | 权威重复规则；卡片优先用它展示 cron 无法表达的真实间隔（如每50小时、每40天）。                              |
| [cua.tsx](cua.tsx)                                                             | cua server key 段为 computer_use（feat）或 plugin namespace 里的 computer_use（main v3.5.3）。              |
| [cuaAccessDetails.ts](cuaAccessDetails.ts)                                     | The runtime request_access response puts each permission's status object                                    |
| [cuaActionDetail.ts](cuaActionDetail.ts)                                       | 实现或公开接口：readCuaActionDetail。                                                                       |
| [cuaAppSummaryIcon.tsx](cuaAppSummaryIcon.tsx)                                 | \* 图标取不到时显示什么（平台无 resolver、Linux 无 locator、读取失败）。                                    |
| [cuaDetails.tsx](cuaDetails.tsx)                                               | 完整 tool call JSON 混入了面向用户的 CUA 详情，暴露内部生命周期字段并制造无效入口。                         |
| [cuaErrorDetails.ts](cuaErrorDetails.ts)                                       | 实现或公开接口：CuaErrorDetails、readCuaErrorDetails。                                                      |
| [cuaIcon.tsx](cuaIcon.tsx)                                                     | 兼容 CUA 分组摘要的语义名称；底层视觉仍统一使用同一个 fallback。                                            |
| [cuaListDetails.tsx](cuaListDetails.tsx)                                       | v4/replayable 的稳定事实源是 display；legacy 文本可能已被 head/tail 裁剪。                                  |
| [cuaResultState.ts](cuaResultState.ts)                                         | 部分 MCP 结果在有效主 JSON 后只追加空的 `Structured content:` 标记。                                        |
| [cuaScreenshotDetails.ts](cuaScreenshotDetails.ts)                             | 实现或公开接口：CuaScreenshotDetails、buildCuaScreenshotDetails。                                           |
| [CuaScreenshotSection.tsx](CuaScreenshotSection.tsx)                           | 实现或公开接口：CuaScreenshotSection。                                                                      |
| [cuaSummaryMessages.ts](cuaSummaryMessages.ts)                                 | 实现或公开接口：CUA_TOOL_SUMMARY_IDS。                                                                      |
| [edit.tsx](edit.tsx)                                                           | summary.filePath 是 fileDisplay 生成的目录展示路径，不是可打开的文件路径。                                  |
| [EditInlineDiffContent.tsx](EditInlineDiffContent.tsx)                         | \* 应用主题（store 耦合剥离）：决定 diff 高亮取 light/dark 主题。                                           |
| [escalate.tsx](escalate.tsx)                                                   | 折叠头部的单行概要上限：概要只是「大概问了什么」，整段问题在展开后的 body 里。                              |
| [eval-workflow-snippet.tsx](eval-workflow-snippet.tsx)                         | 三态摘要不放结果预览，展开内容按执行状态排序。                                                              |
| [execute.tsx](execute.tsx)                                                     | 实现或公开接口：getExecuteSecondaryText、ExecuteToolCallBlock。                                             |
| [ExecuteCommand.tsx](ExecuteCommand.tsx)                                       | 原命令区域只有限高和截断，没有阅读完整内容的入口；按实际换行测量，兼容窄屏与字号变化。                      |
| [ExecuteOutput.tsx](ExecuteOutput.tsx)                                         | 程序吸底后记录浏览器实际位置，避免尾窗变短时把程序滚动误判为上滚。                                          |
| [explore.tsx](explore.tsx)                                                     | 实现或公开接口：getLatestAgentChildSummaryFromChildren。                                                    |
| [fallback.tsx](fallback.tsx)                                                   | 实现或公开接口：FallbackToolCallBlock。                                                                     |
| [get-workflow-run-roster.tsx](get-workflow-run-roster.tsx)                     | \* GetWorkflowRun 工具卡的**子代理花名册**（情势截面的另一半，阶段轨与健康行在                              |
| [get-workflow-run-situation.tsx](get-workflow-run-situation.tsx)               | \* GetWorkflowRun 工具卡的**情势截面**：阶段轨 + 健康行（花名册在                                           |
| [get-workflow-run.tsx](get-workflow-run.tsx)                                   | 查询错误与 run 执行失败是两个状态层级；错误查询不能继续展示旧 display。                                     |
| [goal.tsx](goal.tsx)                                                           | 实现或公开接口：GoalToolCallBlock。                                                                         |
| [list-models.tsx](list-models.tsx)                                             | 分享页通过 ToolPresentation 采用本渲染器；从 thoughtLevelOptions 引入会经 display → CodingPlan 拉进         |
| [list-saved-workflows-presentation.tsx](list-saved-workflows-presentation.tsx) | \* 结果读取顺序：**display 通道优先**——v4 wire 上 output.text                                               |
| [list-saved-workflows.tsx](list-saved-workflows.tsx)                           | 桌面 fallback 依赖宿主服务，分享页只引用纯展示组件。                                                        |
| [list-workflow-runs.tsx](list-workflow-runs.tsx)                               | \* ListWorkflowRuns 的聊天卡。                                                                              |
| [mcp.tsx](mcp.tsx)                                                             | display 持久化上线前的 MCP 历史记录只剩协议执行名，通用 renderer                                            |
| [node-repl.tsx](node-repl.tsx)                                                 | Radix 会在浏览器工具及执行详情打开时立即测量高度；代码块默认的 200px 离屏占位                               |
| [nodeReplImageGrid.tsx](nodeReplImageGrid.tsx)                                 | 实现或公开接口：NodeReplImageGrid。                                                                         |
| [offpeak-create.tsx](offpeak-create.tsx)                                       | OffPeakCreate 的静态轮尾卡（cron-create 兄弟实现，样式契约一致）。                                          |
| [plan-guidance.tsx](plan-guidance.tsx)                                         | 实现或公开接口：PlanGuidanceToolCallBlock。                                                                 |
| [read-session-context.tsx](read-session-context.tsx)                           | 实现或公开接口：ReadSessionContextToolCallBlock。                                                           |
| [read.tsx](read.tsx)                                                           | 有些模型只在 rawInput 里给 filePath，但会在 rawOutput/content 里补充目录类型。                              |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                                                            |
| [resolve-workflow-question.tsx](resolve-workflow-question.tsx)                 | 折叠头部的单行概要上限：概要只是「大概答了什么」，整段答案在展开后的 body 里。                              |
| [respond-to-coordinator.tsx](respond-to-coordinator.tsx)                       | 实现或公开接口：RespondToCoordinatorToolCallBlock。                                                         |
| [resume-workflow-run.tsx](resume-workflow-run.tsx)                             | 紧凑 run 态卡的图标与 CreateWorkflow 同一枚（族内一致）；折叠态保留 RotateCcw 讲「恢复」。                  |
| [save-workflow.tsx](save-workflow.tsx)                                         | \* 覆盖徽标的样式：与 CreateWorkflow 结果卡的 compiled 小签同族（镌刻小签——rounded-xs +                     |
| [search.tsx](search.tsx)                                                       | WebFetch 同时带 url 和 prompt 时，权限/工具摘要展示 prompt 会遮住真正需要用户确认的目标地址。               |
| [send-message.tsx](send-message.tsx)                                           | summary 已改为可选：工具描述写明缺省时用 message 的第一行作预览，卡片标题与之一致。                         |
| [skill.tsx](skill.tsx)                                                         | 实现或公开接口：SkillToolCallBlock。                                                                        |
| [submit-result.tsx](submit-result.tsx)                                         | 折叠头部的单行概要上限：概要只是「大概提交了什么」，整段内容在展开后的 body 里。                            |
| [switch-mode.tsx](switch-mode.tsx)                                             | 卡片自身带 role=button，旧 closest 会让卡片任意位置都命中自己，                                             |
| [task-output.tsx](task-output.tsx)                                             | 类别标签只能说明这是 TaskOutput，不能替代 display 已确认的成功读取结果。                                    |
| [task-stop.tsx](task-stop.tsx)                                                 | 旧 snapshot 只保存了会重复 command/prompt 的标准成功文案。                                                  |
| [todo.tsx](todo.tsx)                                                           | 工具输出里的 todo running 状态会长时间留在页面上；                                                          |
| [web-fetch.tsx](web-fetch.tsx)                                                 | 内联 JSX 会让 memo 化的 ToolLayout 每次收到新引用；图标采用，标题仅在 URL 改变时重建。                      |
| [workflow-diagnostics.tsx](workflow-diagnostics.tsx)                           | 一条 TS 诊断（CreateWorkflow 与 EvalWorkflowSnippet 的 display 共用同一形状）。                             |
| [workflow-draft-row.tsx](workflow-draft-row.tsx)                               | \* 编译反馈行在 ToolLayout 各槽位里说的话。                                                                 |
| [workflow-fill-row.tsx](workflow-fill-row.tsx)                                 | \* 留白补全行在 create-workflow 渲染器里的那几样（docs/dynamic-workflow/presentation.md「The fill row」）。 |
| [workflow-run-compact-card.tsx](workflow-run-compact-card.tsx)                 | 卡片自身带 role=button，closest 会让卡片任意位置都命中自己，那样「点击卡片打开详情」                        |
| [workflow-snippet-presentation.ts](workflow-snippet-presentation.ts)           | handler 的 response 面向模型，含重复耗时/日志；只解包已知格式，未知/截断内容保留。                          |
| [WorkflowCardMetaLine.tsx](WorkflowCardMetaLine.tsx)                           | \* 工具卡卡体顶部的一行元信息：淡色标签 + 等宽值（来源文件名、run id……），可带一句淡色注记。                |
| [WorkflowRetuneRow.tsx](WorkflowRetuneRow.tsx)                                 | 就地生效的修订在转写里的那一行（docs/dynamic-workflow/concurrency.md）                                      |

<!-- qingqi-directory-index:end -->
