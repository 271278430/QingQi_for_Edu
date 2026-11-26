# conversation-telemetry

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 conversation telemetry 实现源码。

### 文件

| 文件                                                             | 简要说明                                                                                  |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                       | 实现或公开接口：remoteCompletionExample。                                                 |
| [CONTRACT.md](CONTRACT.md)                                       | 模块职责、公共接口、依赖方向和状态约定。                                                  |
| [contract.ts](contract.ts)                                       | contract 的实现文件。                                                                     |
| [conversationTelemetryEngine.ts](conversationTelemetryEngine.ts) | 用户触发原始发送动作的 renderer 时钟。                                                    |
| [index.ts](index.ts)                                             | index 的实现文件。                                                                        |
| [messageTelemetry.ts](messageTelemetry.ts)                       | 独立 background wake 轮的来源：Agent 工具的后台子代理，或 dynamic-workflow run 的通知。   |
| [module.ts](module.ts)                                           | 实现或公开接口：moduleDefinition。                                                        |
| [providerTelemetryIdentity.ts](providerTelemetryIdentity.ts)     | Provider 重构拆分了执行身份，但旧报表仍按原桶统计；只在事件构造处使用，禁止回流业务配置。 |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                          |
| [remoteTelemetryEvent.ts](remoteTelemetryEvent.ts)               | 同一 Source 的多个 Host relay 可广播同一结果，PC 最终出站必须合并。                       |
| [runtimeModelTelemetry.ts](runtimeModelTelemetry.ts)             | 实现或公开接口：resolveLegacyRuntimeModelValue。                                          |

<!-- qingqi-directory-index:end -->
