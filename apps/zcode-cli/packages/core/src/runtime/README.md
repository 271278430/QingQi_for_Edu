# runtime

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 runtime 实现源码。

### 子目录

| 目录                                                                | 存放内容                                                       |
| ------------------------------------------------------------------- | -------------------------------------------------------------- |
| [context-composition/](context-composition/README.md)               | @zcode/core 基础工程中的 context composition 实现源码。        |
| [conversation-quote-context/](conversation-quote-context/README.md) | @zcode/core 基础工程中的 conversation quote context 实现源码。 |
| [helpers/](helpers/README.md)                                       | @zcode/core 基础工程中的 helpers 实现源码。                    |
| [methods/](methods/README.md)                                       | @zcode/core 基础工程中的 methods 实现源码。                    |
| [off-peak/](off-peak/README.md)                                     | @zcode/core 基础工程中的 off peak 实现源码。                   |
| [provider-tool-rounds/](provider-tool-rounds/README.md)             | @zcode/core 基础工程中的 provider tool rounds 实现源码。       |
| [session-features/](session-features/README.md)                     | @zcode/core 基础工程中的 session features 实现源码。           |
| [session-fork-commit/](session-fork-commit/README.md)               | @zcode/core 基础工程中的 session fork commit 实现源码。        |
| [tool-result-settlement/](tool-result-settlement/README.md)         | @zcode/core 基础工程中的 tool result settlement 实现源码。     |

### 文件

| 文件                                                         | 简要说明                                                                           |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| [agent-runtime.ts](agent-runtime.ts)                         | 实现或公开接口：AgentRuntime。                                                     |
| [command-queue.ts](command-queue.ts)                         | admission 已建立的 reservation；执行阶段不得再次创建/竞争 turn。                   |
| [deps.ts](deps.ts)                                           | 实现或公开接口：createQueryId、createChildTraceContext、traceContextToLogContext。 |
| [execution-state.ts](execution-state.ts)                     | 权限与 Plan 是一个已消费状态；保存失败不发布成功快照，也不提前改内存。             |
| [internal-hook-methods.ts](internal-hook-methods.ts)         | 从 internal-methods.ts 拆出，避免该文件越过                                        |
| [internal-methods.ts](internal-methods.ts)                   | 实现或公开接口：AgentRuntimeCoreMethods。                                          |
| [internal-turn-methods.ts](internal-turn-methods.ts)         | 实现或公开接口：AgentRuntimeTurnMethods。                                          |
| [internal.ts](internal.ts)                                   | 首次装配选定的会话工具运行位置；分支刷新采用它，不能回落到另一种实现。             |
| [model-selection.ts](model-selection.ts)                     | 实现或公开接口：cloneModelSelection。                                              |
| [permission-full-access.ts](permission-full-access.ts)       | 完全访问只改当前任务；receipt 固定目标集合，发布失败后不能重新抓取后来队列。       |
| [permission-grant-recovery.ts](permission-grant-recovery.ts) | 不保存第二份权限/队列，只记录事务已提交但事件尚未发布的恢复动作。                  |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                   |
| [session-mode-port.ts](session-mode-port.ts)                 | 实现或公开接口：createRuntimeSessionModePort。                                     |
| [types.ts](types.ts)                                         | shared-host CUA request routing metadata; desktop is the safe default.             |

<!-- qingqi-directory-index:end -->
