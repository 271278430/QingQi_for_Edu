# execution

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 execution 测试场景。

### 文件

| 文件                                                                                                                   | 简要说明                                                                            |
| ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| [conversation-session-command-unknown-recovery.test.ts](conversation-session-command-unknown-recovery.test.ts)         | 提示也包含回答 marker，必须以 assistant 正文确认前置会话已完成，避免过早刷新。      |
| [conversation-session-empty-completion-retry.test.ts](conversation-session-empty-completion-retry.test.ts)             | 无账号回放只需 Personal Provider；通用准备流程会要求模型不支持的 high 档位。        |
| [conversation-session-interrupted-actions.test.ts](conversation-session-interrupted-actions.test.ts)                   | 原因：旧 Stop/Edit/Fork selector 已退役，且快速完成分支会直接跳过核心断言。         |
| [conversation-session-modified-submit-delivery.test.ts](conversation-session-modified-submit-delivery.test.ts)         | 被抢占的 base prompt 还没有输出：新消息仍排在它之后，按人类输入的时间顺序。         |
| [conversation-session-running-actions.test.ts](conversation-session-running-actions.test.ts)                           | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。                 |
| [conversation-session-running-guide-steer.test.ts](conversation-session-running-guide-steer.test.ts)                   | 修复原因：同一 worker 的前一条 steer/stop 会留下 completed 或 interrupted session； |
| [conversation-session-running-task-archive-blocked.test.ts](conversation-session-running-task-archive-blocked.test.ts) | conversation-session-running-task-archive-blocked.test 的实现文件。                 |
| [conversation-session-send-message-resume-stop.test.ts](conversation-session-send-message-resume-stop.test.ts)         | 测试修复原因：resume 会原地更新同一 subagent projection；若等 resume 后再读         |
| [conversation-session-stop-empty.test.ts](conversation-session-stop-empty.test.ts)                                     | V4 的 Stop 控件和队列/目标投影是当前状态来源；旧 runtimeStatus 已不再写入。         |
| [conversation-session-stop-tool-results.test.ts](conversation-session-stop-tool-results.test.ts)                       | PreToolUse 尚未返回，Read 未进入 call.started，因此不会产生 call.failed 日志。      |
| [conversation-session-turn-error-history-activity.test.ts](conversation-session-turn-error-history-activity.test.ts)   | 进程退出后再改时间，避免旧 Host/Agent 的迟到写回覆盖回归样本。                      |
| [conversation-session-turn-steer-probe.test.ts](conversation-session-turn-steer-probe.test.ts)                         | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。                 |
| [README.md](README.md)                                                                                                 | 本目录用途、子目录与逐文件说明。                                                    |

<!-- qingqi-directory-index:end -->
