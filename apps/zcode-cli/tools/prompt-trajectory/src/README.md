# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/prompt-trajectory 基础工程中的 src 实现源码。

### 子目录

| 目录                                                                          | 存放内容                                                                         |
| ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [tool-search-comparison-contract/](tool-search-comparison-contract/README.md) | @zcode/prompt-trajectory 基础工程中的 tool search comparison contract 实现源码。 |

### 文件

| 文件                                                         | 简要说明                                                                                                                             |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| [cli.ts](cli.ts)                                             | cli 的实现文件。                                                                                                                     |
| [derive.ts](derive.ts)                                       | 实现或公开接口：DerivedTrajectoryResult、deriveTrajectoriesFromJsonlFile、writeDerivedTrajectories、deriveTrajectoriesFromEntries。  |
| [fixture.ts](fixture.ts)                                     | 覆盖录制用 Registry 模型的能力声明，例如打开 supportsNativeWebSearch 以暴露 WebSearch。                                              |
| [message-continuity.ts](message-continuity.ts)               | response 摘要没有 thinking/签名；公告过滤可能改变索引，必须在同一比较视图中定位回复。                                                |
| [message-ledger.ts](message-ledger.ts)                       | 实现或公开接口：MessageLedger。                                                                                                      |
| [model-io.ts](model-io.ts)                                   | 实现或公开接口：ModelIoJsonlEntry、ModelIoTrajectoryOptions、writeModelIoAnthropicTrajectory、deriveTrajectoriesFromModelIoEntries。 |
| [openai-provider-proxy.ts](openai-provider-proxy.ts)         | 修复原因：compact 摘要等请求固定走流式；按 JSON 回复时 SDK 读到空流，                                                                |
| [openai-response-assembler.ts](openai-response-assembler.ts) | 实现或公开接口：assembleNonStreamingAssistantMessage、assembleStreamingAssistantMessage。                                            |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                                                     |
| [record.ts](record.ts)                                       | 每个 case 用独立的家目录与存储目录：会话库、插件、用户 skill 与 AGENTS.md 都不读写真实用户目录。                                     |
| [testcases.ts](testcases.ts)                                 | 实现或公开接口：PromptTrajectoryCase、SharedModelOptions、discoverPromptTrajectoryCases、createTimestampedRunDirectory。             |
| [tool-search-comparison.ts](tool-search-comparison.ts)       | 删除公告按原因分段（断连、会话内不可用、本轮隐藏）；离线工具同时识别新旧文案，避免关闭搜索后误判历史断链。                           |
| [types.ts](types.ts)                                         | 实现或公开接口：JsonObject、TrajectoryDerivationOptions、OpenAiMessage、RequestEntry。                                               |

<!-- qingqi-directory-index:end -->
