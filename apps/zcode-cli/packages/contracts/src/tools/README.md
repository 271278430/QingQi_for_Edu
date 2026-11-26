# tools

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/contracts 基础工程中的 tools 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                                                                                 |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [agent.ts](agent.ts)                                               | Agent Tool - Subagent orchestration tool                                                                                                                 |
| [amend-workflow.ts](amend-workflow.ts)                             | AmendWorkflow Tool - revise a run: stop it if it is still going, import its finished work, start the revision                                            |
| [apply-patch.ts](apply-patch.ts)                                   | ApplyPatch Tool - Structured patch editing tool                                                                                                          |
| [ask-user-question.ts](ask-user-question.ts)                       | AskUserQuestion Tool - user clarification questions                                                                                                      |
| [automation.ts](automation.ts)                                     | Cron automation tools - session-level scheduled task management                                                                                          |
| [bash.ts](bash.ts)                                                 | Bash Tool - Shell Execution Tool                                                                                                                         |
| [contract.ts](contract.ts)                                         | Tool Contract - shared tool declaration surface                                                                                                          |
| [create-workflow.ts](create-workflow.ts)                           | CreateWorkflow Tool - typecheck a dynamic-workflow script and start a background run                                                                     |
| [deferred-tool-call.ts](deferred-tool-call.ts)                     | 原始目标名称与参数由调用本身保存；仅记录还原模型协议所需的包装标记。                                                                                     |
| [edit.ts](edit.ts)                                                 | Edit Tool - File Editing Tool                                                                                                                            |
| [escalate.ts](escalate.ts)                                         | escalate Tool - actor 把阻塞问题升级给主代理                                                                                                             |
| [eval-workflow-snippet.ts](eval-workflow-snippet.ts)               | EvalWorkflowSnippet Tool - 同步编译并运行一段动态工作流片段（scratch facade）                                                                            |
| [fill-workflow-hole.ts](fill-workflow-hole.ts)                     | FillWorkflowHole Tool - 给一个正在等代码的留白补上函数体                                                                                                 |
| [get-workflow-run-roster.ts](get-workflow-run-roster.ts)           | GetWorkflowRun 的**情势截面** schema：阶段 / 子代理 / 健康                                                                                               |
| [get-workflow-run.ts](get-workflow-run.ts)                         | GetWorkflowRun Tool - 单 workflow run 的自适应详情（进度摘要 / 产物 / 失败）                                                                             |
| [glob.ts](glob.ts)                                                 | Glob Tool - File Pattern Matching Tool                                                                                                                   |
| [grep.ts](grep.ts)                                                 | Grep Tool - Content Search Tool                                                                                                                          |
| [index.ts](index.ts)                                               | Tools Index - Core tool definitions                                                                                                                      |
| [json-schema.ts](json-schema.ts)                                   | Zod -> provider-neutral JSON Schema for tool contracts                                                                                                   |
| [list-models.ts](list-models.ts)                                   | ListModels Tool - 列出本宿主已配置的模型                                                                                                                 |
| [list-saved-workflows.ts](list-saved-workflows.ts)                 | ListSavedWorkflows Tool - 枚举本项目保存的 dwf 定义                                                                                                      |
| [list-workflow-runs.ts](list-workflow-runs.ts)                     | ListWorkflowRuns Tool - 按项目（cwd）枚举 workflow run，含跨会话历史                                                                                     |
| [node-repl.ts](node-repl.ts)                                       | 同一模型 schema 同时服务 persistent core REPL 与 fresh-kernel Browser Use MCP；                                                                          |
| [off-peak.ts](off-peak.ts)                                         | Off-Peak tools - session-level idle-time task creation                                                                                                   |
| [performance.ts](performance.ts)                                   | \* 只允许公开 Registry 中的可执行文件名或固定低基数桶；禁止放入原始命令或参数。                                                                          |
| [plan-mode.ts](plan-mode.ts)                                       | Plan Mode Tools - plan approval flow                                                                                                                     |
| [plugin-discovery.ts](plugin-discovery.ts)                         | 实现或公开接口：SEARCH_PLUGINS_TOOL_NAME、SUGGEST_PLUGIN_INSTALL_TOOL_NAME、PLUGIN_DISCOVERY_PAGE_SIZE、PluginDiscoveryCandidateSchema。                 |
| [read-pdf.ts](read-pdf.ts)                                         | Read PDF Contract                                                                                                                                        |
| [read-state.ts](read-state.ts)                                     | Read State Contract                                                                                                                                      |
| [read.ts](read.ts)                                                 | Read Tool - File Reading Tool                                                                                                                            |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                                                                         |
| [resolve-workflow-question.ts](resolve-workflow-question.ts)       | ResolveWorkflowQuestion Tool - 主代理回答 actor 升级上来的阻塞问题                                                                                       |
| [respond-to-coordinator.ts](respond-to-coordinator.ts)             | 实现或公开接口：RESPOND_TO_COORDINATOR_TOOL_NAME、RESPOND_TO_COORDINATOR_MAX_CONTENT_CHARS、RespondToCoordinatorInputSchema、RespondToCoordinatorInput。 |
| [resume-workflow-run.ts](resume-workflow-run.ts)                   | ResumeWorkflowRun Tool - 恢复一个 cancelled / Interrupted 的 workflow run                                                                                |
| [save-workflow.ts](save-workflow.ts)                               | SaveWorkflow Tool - 把一段 dwf 脚本连同元数据存成项目里的可采用定义                                                                                      |
| [saved-workflow.ts](saved-workflow.ts)                             | Saved workflows - 保存的 dwf 定义的共享词汇表                                                                                                            |
| [send-message.ts](send-message.ts)                                 | summary 可选；provider schema 声明上限，运行时超长截断而不是拒绝。                                                                                       |
| [skill.ts](skill.ts)                                               | Skill Tool - load reusable local instructions on demand                                                                                                  |
| [submit-result.ts](submit-result.ts)                               | submit_result Tool - actor terminal structured-result submission                                                                                         |
| [target.ts](target.ts)                                             | Goal Tools - session-local long-running goal                                                                                                             |
| [task-output.ts](task-output.ts)                                   | 的 provider schema 仍要求模型显式传入 task_id、block 和 timeout。                                                                                        |
| [task-stop.ts](task-stop.ts)                                       | 实现或公开接口：TASK_STOP_TOOL_NAME、TaskStopInputSchema、TaskStopInput、TaskStopInputJsonSchema。                                                       |
| [todo.ts](todo.ts)                                                 | Todo Tools - session task checklist                                                                                                                      |
| [tool-result-metadata.ts](tool-result-metadata.ts)                 | CreateWorkflow display 诊断的限长常量与条目 schema 已移至 create-workflow.ts                                                                             |
| [tool-search.ts](tool-search.ts)                                   | 转换器会把带默认值的字段视为可选；模型侧要求显式传入，执行侧仍先补默认值。                                                                               |
| [webfetch.ts](webfetch.ts)                                         | WebFetch Tool - URL fetch and extraction                                                                                                                 |
| [websearch.ts](websearch.ts)                                       | WebSearch Tool - provider-visible wrapper and internal provider-native schema definitions                                                                |
| [workflow-observation-display.ts](workflow-observation-display.ts) | \* 观察类工作流工具（GetWorkflowRun / ListWorkflowRuns / EvalWorkflowSnippet                                                                             |
| [workflow-settings.ts](workflow-settings.ts)                       | 确认窗里可调的两项 run 设置（CreateWorkflow / AmendWorkflow 共用）                                                                                       |
| [workflow.ts](workflow.ts)                                         | Workflow Tool - deterministic multi-agent workflow launcher                                                                                              |
| [write.ts](write.ts)                                               | Write Tool - File Writing Tool                                                                                                                           |

<!-- qingqi-directory-index:end -->
