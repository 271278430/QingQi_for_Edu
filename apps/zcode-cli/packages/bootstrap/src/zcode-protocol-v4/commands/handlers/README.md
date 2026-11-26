# handlers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 handlers 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                                  |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [assistant-feedback.ts](assistant-feedback.ts)           | 实现或公开接口：assistantFeedbackHandlers。                                               |
| [canonical-intent-replay.ts](canonical-intent-replay.ts) | edit/retry 的 canonical intent 重发原语：rewind 截断之后，把 projection resolver 解析出的 |
| [file-rewind.ts](file-rewind.ts)                         | 实现或公开接口：fileRewindHandlers。                                                      |
| [fork-edit-retry.ts](fork-edit-retry.ts)                 | fork/edit/retry 命令组：forkAssistant / editUserQuery / retryTurn。                       |
| [goal-compact.ts](goal-compact.ts)                       | goal/compact 命令组：compact / sendGoalCommand / pauseGoal / resumeGoal。                 |
| [highspeed-metrics.ts](highspeed-metrics.ts)             | 实现或公开接口：highspeedMetricsHandlers。                                                |
| [index.ts](index.ts)                                     | 原生 handler 注册表（每组加一行 spread）。                                                |
| [interaction-background.ts](interaction-background.ts)   | 权限/后台命令组：resolveInteraction / cancelBackgroundWork。                              |
| [model-config.ts](model-config.ts)                       | 模型配置命令组：switchModelConfig（自旧 server-operations.switchModelConfig 语义搬运）    |
| [queue.ts](queue.ts)                                     | queue 命令组：deleteQueueItem / editQueueItem / lockQueueItemEdit / releaseQueueItemEdit  |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                          |
| [selection-side-session.ts](selection-side-session.ts)   | child 已在 host 中注册后再启动首条输入；输入只落到 child，父会话的                        |
| [session-flow.ts](session-flow.ts)                       | 会话流命令组：sendText / stop（模式样板）。                                               |
| [session-mgmt.ts](session-mgmt.ts)                       | 会话管理命令组：createSession / renameSession / deleteSession。                           |

<!-- qingqi-directory-index:end -->
