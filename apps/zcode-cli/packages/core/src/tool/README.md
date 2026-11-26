# tool

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 tool 实现源码。

### 子目录

| 目录                                                    | 存放内容                                                 |
| ------------------------------------------------------- | -------------------------------------------------------- |
| [channel-reply/](channel-reply/README.md)               | @zcode/core 基础工程中的 channel reply 实现源码。        |
| [executor/](executor/README.md)                         | @zcode/core 基础工程中的 executor 实现源码。             |
| [handlers/](handlers/README.md)                         | @zcode/core 基础工程中的 handlers 实现源码。             |
| [search/](search/README.md)                             | @zcode/core 基础工程中的 search 实现源码。               |
| [session-control/](session-control/README.md)           | @zcode/core 基础工程中的 session control 实现源码。      |
| [topic-resource/](topic-resource/README.md)             | @zcode/core 基础工程中的 topic resource 实现源码。       |
| [workflow-entrypoints/](workflow-entrypoints/README.md) | @zcode/core 基础工程中的 workflow entrypoints 实现源码。 |

### 文件

| 文件                                                                   | 简要说明                                                                                                               |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| [bash-timeout-policy.ts](bash-timeout-policy.ts)                       | 实现或公开接口：BashTimeoutPolicy、DEFAULT_BASH_TIMEOUT_MS、DEFAULT_BASH_MAX_TIMEOUT_MS、DEFAULT_BASH_TIMEOUT_POLICY。 |
| [compat.ts](compat.ts)                                                 | 实现或公开接口：AGENT_TOOL_NAME、TASK_TOOL_NAME、isSubagentDispatchToolName、hookMatcherToolNamesForTool。             |
| [deferred-call.ts](deferred-call.ts)                                   | 调度、流式准入与 executor 共用同一解析边界；失败保持包装身份，不触发目标生命周期。                                     |
| [diff.ts](diff.ts)                                                     | 实现或公开接口：createStructuredPatch、countPatchLines。                                                               |
| [edit-matchers.ts](edit-matchers.ts)                                   | 实现或公开接口：findEditMatch、normalizeLineEndings、normalizeReplacementForMatch、preserveQuoteStyle。                |
| [executor.ts](executor.ts)                                             | executor 的实现文件。                                                                                                  |
| [index.ts](index.ts)                                                   | index 的实现文件。                                                                                                     |
| [input-normalization.ts](input-normalization.ts)                       | Note: some model adapters and hook/broker paths can surface tool                                                       |
| [input-validation-model-content.ts](input-validation-model-content.ts) | runtime issues 判断错误是否真实存在，JSON issues 提供目标字段结构。                                                    |
| [json-schema.ts](json-schema.ts)                                       | Minimal JSON Schema validator for tool contract boundaries                                                             |
| [model-contract.ts](model-contract.ts)                                 | 实现或公开接口：resolveToolEntryModelContract、projectToolModelContract。                                              |
| [patch-apply.ts](patch-apply.ts)                                       | 实现或公开接口：derivePatchedContent。                                                                                 |
| [patch-parser.ts](patch-parser.ts)                                     | 实现或公开接口：ParsedPatch、PatchChunk、parseStructuredPatch。                                                        |
| [path-normalization.ts](path-normalization.ts)                         | Tool Path Normalization Helpers                                                                                        |
| [path-policy.ts](path-policy.ts)                                       | Tool Path Policy                                                                                                       |
| [provider-visible-order.ts](provider-visible-order.ts)                 | 名单内的工具按名字排序，名单外的工具按注册顺序在其后；                                                                 |
| [read-file-state-metadata.ts](read-file-state-metadata.ts)             | `CreateWorkflow` / `AmendWorkflow` / `FillWorkflowHole`：内联草稿（或 fill 文件）的字节就是模型那次                    |
| [read-file-state.ts](read-file-state.ts)                               | Read File State Helpers                                                                                                |
| [README.md](README.md)                                                 | 本目录用途、子目录与逐文件说明。                                                                                       |
| [registry.ts](registry.ts)                                             | Tool Registry - Tool registration and lookup                                                                           |
| [result-persistence-format.ts](result-persistence-format.ts)           | Artifact strategy uses resultBudget as the persistence trigger; once persisted, this independent                       |
| [scheduler.ts](scheduler.ts)                                           | Tool Scheduler - Tool execution scheduling                                                                             |
| [tool-input-validation-issues.ts](tool-input-validation-issues.ts)     | 这些字段的插入顺序会直接进入 provider-visible JSON fallback，                                                          |
| [tool-visibility.ts](tool-visibility.ts)                               | 实现或公开接口：normalizeToolNameAlias、getToolRuleName、createToolRuleNameSet、isToolNameDisallowed。                 |
| [types.ts](types.ts)                                                   | Tool Types - Core tool types for registry and executor                                                                 |
| [webfetch-preapproved.ts](webfetch-preapproved.ts)                     | 实现或公开接口：isWebFetchPreapprovedUrl。                                                                             |

<!-- qingqi-directory-index:end -->
