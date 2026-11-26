# workflows

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 workflows 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                                                           | 简要说明                                                                                                 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [conversation-session-dynamic-workflow-gray-always-on-amend.test.ts](conversation-session-dynamic-workflow-gray-always-on-amend.test.ts)                       | 修订在跑的工作流（docs/dynamic-workflow/launch.md「The `AmendWorkflow` tool」「Amending this             |
| [conversation-session-dynamic-workflow-gray-always-on-artifacts.test.ts](conversation-session-dynamic-workflow-gray-always-on-artifacts.test.ts)               | 工作流产物（docs/dynamic-workflow/authoring.md「Artifacts: what the user keeps」、                       |
| [conversation-session-dynamic-workflow-gray-always-on-compile.test.ts](conversation-session-dynamic-workflow-gray-always-on-compile.test.ts)                   | 编不过的脚本、技能门与草稿文件（docs/dynamic-workflow/launch.md「Failures that never reach the           |
| [conversation-session-dynamic-workflow-gray-always-on-confirm.test.ts](conversation-session-dynamic-workflow-gray-always-on-confirm.test.ts)                   | CreateWorkflow 确认窗的选项（docs/dynamic-workflow/launch.md「The confirmation window」：The options、   |
| [conversation-session-dynamic-workflow-gray-always-on-cross-session.test.ts](conversation-session-dynamic-workflow-gray-always-on-cross-session.test.ts)       | run 与别的会话（docs/dynamic-workflow/launch.md「Amending this session's runs」、`FillWorkflowHole` 的   |
| [conversation-session-dynamic-workflow-gray-always-on-english-dark.test.ts](conversation-session-dynamic-workflow-gray-always-on-english-dark.test.ts)         | 工作流主链路的英文界面与深色主题（docs/dynamic-workflow/launch.md「The confirmation window」、           |
| [conversation-session-dynamic-workflow-gray-always-on-lookup.test.ts](conversation-session-dynamic-workflow-gray-always-on-lookup.test.ts)                     | 查询工作流实例的两张工具卡（docs/dynamic-workflow/launch.md「Run introspection tools」                   |
| [conversation-session-dynamic-workflow-gray-always-on-notify.test.ts](conversation-session-dynamic-workflow-gray-always-on-notify.test.ts)                     | run 自己结束时主代理怎么知道（docs/dynamic-workflow/transcript-and-notifications.md「Notifications」     |
| [conversation-session-dynamic-workflow-gray-always-on-overflow.test.ts](conversation-session-dynamic-workflow-gray-always-on-overflow.test.ts)                 | 时间线的溢出与并行结构（docs/dynamic-workflow/presentation.md「Drawing the timeline」：「Rails and       |
| [conversation-session-dynamic-workflow-gray-always-on-questions.test.ts](conversation-session-dynamic-workflow-gray-always-on-questions.test.ts)               | 子代理升级问题（docs/dynamic-workflow/authoring.md 的 `escalate` 与「When a subagent escalates」、       |
| [conversation-session-dynamic-workflow-gray-always-on-restart.test.ts](conversation-session-dynamic-workflow-gray-always-on-restart.test.ts)                   | 重启与重载（docs/dynamic-workflow/presentation.md「Cold replay」「Joining cards to runs」、              |
| [conversation-session-dynamic-workflow-gray-always-on-resume.test.ts](conversation-session-dynamic-workflow-gray-always-on-resume.test.ts)                     | 恢复一次停下的 run（docs/dynamic-workflow/presentation.md「The run card」「The run pane」、              |
| [conversation-session-dynamic-workflow-gray-always-on-run-pane-details.test.ts](conversation-session-dynamic-workflow-gray-always-on-run-pane-details.test.ts) | run 侧板的细节与「配置」弹层（docs/dynamic-workflow/presentation.md「The run pane」「The run state       |
| [conversation-session-dynamic-workflow-gray-always-on-run-permissions.test.ts](conversation-session-dynamic-workflow-gray-always-on-run-permissions.test.ts)   | run 里的权限（docs/dynamic-workflow/launch.md「Permissions inside a run」）：子代理跑在发起 run 的会话的 |
| [conversation-session-dynamic-workflow-gray-always-on-run.test.ts](conversation-session-dynamic-workflow-gray-always-on-run.test.ts)                           | 模型发起的工作流主链路（docs/dynamic-workflow/launch.md「The `CreateWorkflow` tool」「The confirmation   |
| [conversation-session-dynamic-workflow-gray-always-on-save-from-chat.test.ts](conversation-session-dynamic-workflow-gray-always-on-save-from-chat.test.ts)     | 从对话保存工作流（docs/dynamic-workflow/launch.md「Saved workflows」、                                   |
| [conversation-session-dynamic-workflow-gray-always-on-save-window.test.ts](conversation-session-dynamic-workflow-gray-always-on-save-window.test.ts)           | 保存确认窗的长内容（docs/dynamic-workflow/launch.md「`SaveWorkflow`」第 4 步）：窗口上限与问答窗相同，   |
| [conversation-session-dynamic-workflow-gray-always-on-snippet.test.ts](conversation-session-dynamic-workflow-gray-always-on-snippet.test.ts)                   | EvalWorkflowSnippet：工作流创作的试验台（docs/dynamic-workflow/authoring.md「EvalWorkflowSnippet」       |
| [conversation-session-dynamic-workflow-gray-always-on-stop.test.ts](conversation-session-dynamic-workflow-gray-always-on-stop.test.ts)                         | 用户从 GUI 停止一次在跑的 run（docs/dynamic-workflow/presentation.md「The run card」「The run pane」     |
| [conversation-session-dynamic-workflow-gray-always-on-transcript.test.ts](conversation-session-dynamic-workflow-gray-always-on-transcript.test.ts)             | 脚本 transcript（docs/dynamic-workflow/transcript-and-notifications.md「The script transcript」          |
| [conversation-session-dynamic-workflow-gray-always-on-user-choice.test.ts](conversation-session-dynamic-workflow-gray-always-on-user-choice.test.ts)           | DWG-23（docs/dynamic-workflow/launch.md「The user's choice」）：服务端下发 alwaysOn（文件名命中          |
| [conversation-session-dynamic-workflow-gray-always-on.test.ts](conversation-session-dynamic-workflow-gray-always-on.test.ts)                                   | DWG-08（alwaysOn 档）：服务端 /client/configs 下发 dynamicWorkflow.mode = "alwaysOn"，                   |
| [conversation-session-dynamic-workflow-gray-disabled.test.ts](conversation-session-dynamic-workflow-gray-disabled.test.ts)                                     | DWG-08（disabled 档）：服务端 /client/configs 不下发 dynamicWorkflow key，                               |
| [conversation-session-dynamic-workflow-gray-on-demand.test.ts](conversation-session-dynamic-workflow-gray-on-demand.test.ts)                                   | 灰度档 onDemand（docs/dynamic-workflow/launch.md「What each mode means」「On demand: activation」）：    |
| [conversation-session-dynamic-workflow-holes.test.ts](conversation-session-dynamic-workflow-holes.test.ts)                                                     | 留白（docs/dynamic-workflow/presentation.md「Holes on the timeline」、docs/dynamic-workflow/launch.md    |
| [README.md](README.md)                                                                                                                                         | 本目录用途、子目录与逐文件说明。                                                                         |

<!-- qingqi-directory-index:end -->
