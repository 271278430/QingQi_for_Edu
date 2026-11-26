# automations

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 automations 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                               | 简要说明                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [conversation-session-automation-cron-create.test.ts](conversation-session-automation-cron-create.test.ts)                         | 与 fixtures/upstream/conversation-session/conversation-session-automation-cron-create.json 对齐：          |
| [conversation-session-automation-cron-relative.test.ts](conversation-session-automation-cron-relative.test.ts)                     | 与 fixtures/upstream/conversation-session/conversation-session-automation-cron-relative.json 对齐：        |
| [conversation-session-automation-cron-update.test.ts](conversation-session-automation-cron-update.test.ts)                         | 与同名 upstream fixture 对齐：CronList 返回 UI 创建任务的真实 automationId，                               |
| [conversation-session-automation-pause-self.test.ts](conversation-session-automation-pause-self.test.ts)                           | 与同名 upstream fixture 对齐：执行轮首个响应固定调用无参数 CronPauseSelf，                                 |
| [conversation-session-automation-run-title-stable.test.ts](conversation-session-automation-run-title-stable.test.ts)               | 卡片运行次数/下次运行是本 case 的可见证据；显式固定中文 locale，避免 WDIO                                  |
| [conversation-session-off-peak-invalid-ticket.test.ts](conversation-session-off-peak-invalid-ticket.test.ts)                       | \* 让真实闲时 scheduler 收到 3106：任务必须明确失败并停止自动补号，不能把这次请求                          |
| [conversation-session-off-peak-team-plan.test.ts](conversation-session-off-peak-team-plan.test.ts)                                 | 账号 Family 由 Start Plan 固定节点承载；旧 API Key 模板已不再是账号导航入口。                              |
| [conversation-session-offpeak-create-existing-session.test.ts](conversation-session-offpeak-create-existing-session.test.ts)       | 与 fixtures/upstream/conversation-session/conversation-session-offpeak-create-existing-session.json 对齐。 |
| [conversation-session-offpeak-create.test.ts](conversation-session-offpeak-create.test.ts)                                         | 与 fixtures/upstream/conversation-session/conversation-session-offpeak-create.json 对齐：                  |
| [conversation-session-offpeak-subagent-model-inheritance.test.ts](conversation-session-offpeak-subagent-model-inheritance.test.ts) | 只保留注入窗口，避免另一个 Host 先抢到闲时任务，使故障边界没有被执行。                                     |
| [README.md](README.md)                                                                                                             | 本目录用途、子目录与逐文件说明。                                                                           |

<!-- qingqi-directory-index:end -->
