# compact

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 compact 实现源码。

### 文件

| 文件                               | 简要说明                                                                                                                                                                    |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [index.ts](index.ts)               | index 的实现文件。                                                                                                                                                          |
| [manual.ts](manual.ts)             | assistant toolCalls 独立保存在 content 之外，旧估算只读取 content，                                                                                                         |
| [microcompact.ts](microcompact.ts) | 实现或公开接口：MICROCOMPACT_CLEARED_TOOL_RESULT_PREFIX、MICROCOMPACT_CLEARED_TOOL_RESULT_MESSAGE、DEFAULT_MICROCOMPACT_KEEP_RECENT_TOOL_RESULTS、DEFAULT_MICROCOMPACT_IDLE |
| [policy.ts](policy.ts)             | 正常请求默认输出已收敛到 32K，auto compact 必须预留同一目标；                                                                                                               |
| [prompt.ts](prompt.ts)             | 实现或公开接口：buildCompactPrompt、formatCompactSummary、buildCompactSummaryMessage。                                                                                      |
| [README.md](README.md)             | 本目录用途、子目录与逐文件说明。                                                                                                                                            |
| [rounds.ts](rounds.ts)             | 实现或公开接口：groupByAssistantStartedRounds。                                                                                                                             |

<!-- qingqi-directory-index:end -->
