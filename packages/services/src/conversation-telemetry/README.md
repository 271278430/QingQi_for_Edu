# conversation-telemetry

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 conversation telemetry 实现源码。

### 文件

| 文件                                                             | 简要说明                                                                                 |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                       | 实现或公开接口：remoteTurnExample。                                                      |
| [CONTRACT.md](CONTRACT.md)                                       | 模块职责、公共接口、依赖方向和状态约定。                                                 |
| [contract.ts](contract.ts)                                       | contract 的实现文件。                                                                    |
| [conversationTelemetry.ts](conversationTelemetry.ts)             | \* 对话埋点的 workspace 级只读服务面。它只包装已完成 clientMode 鉴权的 connection-scoped |
| [module.ts](module.ts)                                           | 实现或公开接口：moduleDefinition。                                                       |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                         |
| [remoteConversationTelemetry.ts](remoteConversationTelemetry.ts) | 只消费执行服务的 live facts，不依赖手机 attachment 或桌面 pane 的寿命。                  |

<!-- qingqi-directory-index:end -->
