# background

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 background 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                       | 简要说明                                                                             |
| -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [conversation-session-background-bash-output.test.ts](conversation-session-background-bash-output.test.ts)                 | 合并适配：全局新任务落到独立聊天目录，Bash fixture 必须从 ZCodeProject 发起。        |
| [conversation-session-background-connection.test.ts](conversation-session-background-connection.test.ts)                   | 用例不稳定原因：点项目行的“新建任务”时鼠标停在行上，300ms 后弹出的项目悬停卡片会盖住 |
| [conversation-session-background-file-diff.test.ts](conversation-session-background-file-diff.test.ts)                     | BG41：background Agent 在父 launch turn 已 idle 后完成，独立 model-only turn         |
| [conversation-session-background-guide-steer.test.ts](conversation-session-background-guide-steer.test.ts)                 | conversation-session-background-guide-steer.test 的实现文件。                        |
| [conversation-session-background-notification-batch.test.ts](conversation-session-background-notification-batch.test.ts)   | conversation-session-background-notification-batch.test 的实现文件。                 |
| [conversation-session-background-subagent-rate-limit.test.ts](conversation-session-background-subagent-rate-limit.test.ts) | 第一个失败 child 在 429 之前写出的正文，失败通知把它作为部分报告放进 `<result>`。    |
| [conversation-session-background-task-browser-muted.test.ts](conversation-session-background-task-browser-muted.test.ts)   | conversation-session-background-task-browser-muted.test 的实现文件。                 |
| [conversation-session-background.test.ts](conversation-session-background.test.ts)                                         | conversation-session-background.test 的实现文件。                                    |
| [conversation-session-v4-background-work.test.ts](conversation-session-v4-background-work.test.ts)                         | M4 门禁：cancelBackgroundWork（v4 后台工作面板取消）。                               |
| [README.md](README.md)                                                                                                     | 本目录用途、子目录与逐文件说明。                                                     |

<!-- qingqi-directory-index:end -->
