# mcp-ui

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 mcp ui 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                                        |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| [appTools.ts](appTools.ts)                     | \* App-Provided Tools 登记表：会话内页面实例的工具、暴露给模型的集合与待执行调用的唯一 owner。                  |
| [appToolsContract.ts](appToolsContract.ts)     | * App-Provided Tools 的 renderer → agent 参数形状（与 `@zcode/shared` 的 `zcodeMcpUi*AppTool\*` schema 同构）。 |
| [appToolsProtocol.ts](appToolsProtocol.ts)     | \* App-Provided Tools 的四个协议方法。登记表按 agent 进程（context）唯一；信箱投递用 v4Gateway.ingest 的        |
| [callRaces.test.ts](callRaces.test.ts)         | callRaces.test 的实现文件。                                                                                     |
| [contract.example.ts](contract.example.ts)     | 一个只认识单个 server 的内存 session 视图，供契约测试与示例使用。                                               |
| [CONTRACT.md](CONTRACT.md)                     | 模块职责、公共接口、依赖方向和状态约定。                                                                        |
| [contract.test.ts](contract.test.ts)           | contract.test 的实现文件。                                                                                      |
| [contract.ts](contract.ts)                     | \* mcp-ui 契约：UI 发起的 MCP 资源读取与工具调用在 agent 侧的处理器接口。                                       |
| [handlers.ts](handlers.ts)                     | \* 进行中的 UI 工具调用，键 = sessionId + callId。唯一 owner；调用结束即删。                                    |
| [index.ts](index.ts)                           | index 的实现文件。                                                                                              |
| [instances.test.ts](instances.test.ts)         | instances.test 的实现文件。                                                                                     |
| [instances.ts](instances.ts)                   | 单一凭证 owner。撤销先从登记表移除，再触发取消；迟到结果无法重新获得执行权。                                    |
| [module.ts](module.ts)                         | \* mcp-ui 模块清单（architecture-governance managed 模块）。                                                    |
| [notifications.ts](notifications.ts)           | \* MCP server 通知 → 会话。                                                                                     |
| [protocol.ts](protocol.ts)                     | `mcp/readResource`：插件 UI 的 `ui://` 资源读取，走 session 自己的 mcpPort。                                    |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                                                |
| [resourceContract.ts](resourceContract.ts)     | \* mcp-ui 资源契约（）：resources/list、resources/templates/list 与订阅。                                       |
| [samplingCalls.test.ts](samplingCalls.test.ts) | samplingCalls.test 的实现文件。                                                                                 |
| [samplingCalls.ts](samplingCalls.ts)           | 终态账本与并发额度的唯一 owner。只在凭证失效时清账本，旧 operationId 不能被重放。                               |
| [samplingProtocol.ts](samplingProtocol.ts)     | 实现或公开接口：sampleMcpUi、cancelMcpUiSampling。                                                              |
| [sessionAccess.ts](sessionAccess.ts)           | \* 把 session record 收窄成处理器需要的最小视图。归属真相是本 session 的 MCP server 表                          |

<!-- qingqi-directory-index:end -->
