# interfaces

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/contracts 基础工程中的 interfaces 实现源码。

### 文件

| 文件                                                                             | 简要说明                                                                                                                    |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| [automation.port.ts](automation.port.ts)                                         | Automation Port - scheduled task management boundary                                                                        |
| [browser-control.port.ts](browser-control.port.ts)                               | \* BrowserControlPort —— agent 侧浏览器控制端口。                                                                           |
| [context-source.port.ts](context-source.port.ts)                                 | Context Source Port - host/workspace context boundary                                                                       |
| [coordinator-response.port.ts](coordinator-response.port.ts)                     | child session/agent/parent identity 由 port closure 绑定，模型不能覆盖路由。                                                |
| [dynamic-workflow-run-hole.port.ts](dynamic-workflow-run-hole.port.ts)           | Dynamic Workflow Run Port - 留白（hole）的读面与补全面                                                                      |
| [dynamic-workflow-run-retune.port.ts](dynamic-workflow-run-retune.port.ts)       | Dynamic Workflow Run Port：就地改一个在飞 run 的并发上界                                                                    |
| [dynamic-workflow-run-roster.port.ts](dynamic-workflow-run-roster.port.ts)       | Dynamic Workflow Run 的**情势截面**：阶段 / 子代理 / 健康                                                                   |
| [dynamic-workflow-run-workspace.port.ts](dynamic-workflow-run-workspace.port.ts) | Dynamic Workflow Run Port：工作区 transcript 的读面类型                                                                     |
| [dynamic-workflow-run.port.ts](dynamic-workflow-run.port.ts)                     | Dynamic Workflow Run Port - dwf 引擎 run 的提交 / 观察 / 取消边界                                                           |
| [dynamic-workflow-snippet.port.ts](dynamic-workflow-snippet.port.ts)             | Dynamic Workflow Snippet Port - snippet 的同步编译执行边界                                                                  |
| [execution.port.ts](execution.port.ts)                                           | Execution Port - subprocess execution boundary                                                                              |
| [file-system.port.ts](file-system.port.ts)                                       | FileSystem Port - file I/O boundary                                                                                         |
| [http-client.port.ts](http-client.port.ts)                                       | HTTP Client Port - network I/O boundary                                                                                     |
| [image-processor.port.ts](image-processor.port.ts)                               | 实现或公开接口：ImageResizeRequest、ImageResizeResult、ImageProcessorErrorCode、ImageProcessorErrorDetails。                |
| [index.ts](index.ts)                                                             | Ports - interface definitions for adapters                                                                                  |
| [input-history.port.ts](input-history.port.ts)                                   | 实现或公开接口：InputHistoryKind、InputHistoryAttachment、InputHistoryEntry、RecordInputHistoryInput。                      |
| [mcp.port.ts](mcp.port.ts)                                                       | MCP Port - Model Context Protocol adapter boundary                                                                          |
| [model-catalog.port.ts](model-catalog.port.ts)                                   | Model Catalog Port - 宿主已配置模型的只读快照边界                                                                           |
| [off-peak.port.ts](off-peak.port.ts)                                             | Off-Peak Port - idle-time task creation boundary                                                                            |
| [pdf-document.port.ts](pdf-document.port.ts)                                     | 实现或公开接口：PdfDocumentPageCountRequest、PdfDocumentRenderPagesRequest、PdfDocumentRenderedPage、PdfDocumentErrorCode。 |
| [permission-full-access.ts](permission-full-access.ts)                           | 持久化 receipt 是授权重试事实源；损坏时拒绝重试，不能按当前队列重新扩大授权范围。                                           |
| [permission.port.ts](permission.port.ts)                                         | Permission Broker Port - async client permission boundary                                                                   |
| [plugin-discovery.port.ts](plugin-discovery.port.ts)                             | 会话刷新由独立实现接入；没有注入时绝不能把安装完成当作工具已经可用。                                                        |
| [provider-endpoint-routing.port.ts](provider-endpoint-routing.port.ts)           | \* 模型 provider transport 的动态 endpoint 决策边界。                                                                       |
| [README.md](README.md)                                                           | 本目录用途、子目录与逐文件说明。                                                                                            |
| [runtime-input-presentation.ts](runtime-input-presentation.ts)                   | 来源和实际消费形态的单一标记；缺失的旧历史不追溯转换。                                                                      |
| [session-mailbox.port.ts](session-mailbox.port.ts)                               | 实现或公开接口：SessionMailboxEnvelope、SessionMailboxPort。                                                                |
| [session-store.port.ts](session-store.port.ts)                                   | Session Store Port：为会话输入、消息和投影提供稳定的存储边界。                                                              |
| [session.port.ts](session.port.ts)                                               | Session Ports - Core interfaces for session management                                                                      |
| [shared.ts](shared.ts)                                                           | Shared types used across protocol                                                                                           |
| [subagent.port.ts](subagent.port.ts)                                             | Subagent Port - child agent execution boundary                                                                              |
| [tool-artifact-store.port.ts](tool-artifact-store.port.ts)                       | Tool Artifact Store Port - large tool result storage boundary                                                               |
| [topic-resource.port.ts](topic-resource.port.ts)                                 | 仅用于当前任务已经接收的话题附件，身份由可信输入解析，不能由模型指定。                                                      |
| [workflow-escalate.port.ts](workflow-escalate.port.ts)                           | Workflow Escalate Port - actor 向主代理升级阻塞问题的边界                                                                   |
| [workflow-submit.port.ts](workflow-submit.port.ts)                               | Workflow Submit Port - actor terminal-result verdict boundary                                                               |
| [workflow-web-search-budget.port.ts](workflow-web-search-budget.port.ts)         | Workflow WebSearch Budget Port - 动态工作流子代理每个 ask 的 WebSearch 次数预算                                             |
| [workflow.port.ts](workflow.port.ts)                                             | Workflow Port - background workflow launch boundary                                                                         |

<!-- qingqi-directory-index:end -->
