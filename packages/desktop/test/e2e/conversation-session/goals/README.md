# goals

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 goals 测试场景。

### 文件

| 文件                                                                                                           | 简要说明                                                                                                |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| [conversation-session-goal-interruptions.test.ts](conversation-session-goal-interruptions.test.ts)             | V4 的 Stop 控件和队列/目标投影是当前状态来源；旧 runtimeStatus 已不再写入。                             |
| [conversation-session-goal-queue.test.ts](conversation-session-goal-queue.test.ts)                             | B09a/B09e：goal 项原位冻结，编辑态显示 `/goal ...`；提交原地替换，ID、位置与 kind 不变。                |
| [conversation-session-goal-resume-stale-target.test.ts](conversation-session-goal-resume-stale-target.test.ts) | 旧用例写入已退役的 renderer queue，V4 从未收到该输入。这里由真实 Composer 入队。                        |
| [conversation-session-goal-run-cases.test.ts](conversation-session-goal-run-cases.test.ts)                     | conversation-session-goal-run-cases.test 的实现文件。                                                   |
| [conversation-session-goal-session-model.test.ts](conversation-session-goal-session-model.test.ts)             | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。                                     |
| [conversation-session-goal-timeline.test.ts](conversation-session-goal-timeline.test.ts)                       | 当前 V4 投影以 verified 表示 verifier 已确认完成，旧 complete 属于 legacy meta。                        |
| [conversation-session-goal.test.ts](conversation-session-goal.test.ts)                                         | 修复原因：GL/H02 验证 completed 下已有 goal 再更新；旧 case 通过 stop                                   |
| [conversation-session-total-tokens-reminder.test.ts](conversation-session-total-tokens-reminder.test.ts)       | TT01–TT10 token 预算提醒（docs/conversation-session-case-catalog.md「token 预算提醒」）。               |
| [conversation-session-v4-goal-background-queue.test.ts](conversation-session-v4-goal-background-queue.test.ts) | BG34：active goal 仅剩 background Agent 时输入直发；notification verifier 完成后自动消费 future queue。 |
| [conversation-session-v4-goal.test.ts](conversation-session-v4-goal.test.ts)                                   | M4 门禁：sendGoalCommand（v4 composer slash `/goal <目标>`）。                                          |
| [README.md](README.md)                                                                                         | 本目录用途、子目录与逐文件说明。                                                                        |

<!-- qingqi-directory-index:end -->
