# execution

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 execution 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                             | 简要说明                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| [conversation-session-r3-compact-goal.test.ts](conversation-session-r3-compact-goal.test.ts)                     | 手动 compact：/compact → 远端发起 compaction 模型请求（CRITICAL: Respond with TEXT ONLY）→ manual/success marker。 |
| [conversation-session-r3-file-local-actions.test.ts](conversation-session-r3-file-local-actions.test.ts)         | conversation-session-r3-file-local-actions.test 的实现文件。                                                       |
| [conversation-session-r3-media-preview.test.ts](conversation-session-r3-media-preview.test.ts)                   | 2x2 红色 PNG（有效、可解码），用于校验预览真实加载出像素尺寸。                                                     |
| [conversation-session-r3-queue-selection.test.ts](conversation-session-r3-queue-selection.test.ts)               | running（Model A 慢回合）→ 入队 Q。                                                                                |
| [conversation-session-r3-task-actions.test.ts](conversation-session-r3-task-actions.test.ts)                     | 本机对照任务必须真实存在，否则“本机不受影响”只是没有被验证的说明。                                                 |
| [conversation-session-r3-task-control.test.ts](conversation-session-r3-task-control.test.ts)                     | 1. running 窗口由 fixture 闸门保持到 Stop，避免排队/编辑期间自然结束。                                             |
| [conversation-session-r3-terminal.test.ts](conversation-session-r3-terminal.test.ts)                             | 远端 PTY shell 数：cwd 等于给定 workspace 的交互 shell（不含测试自身的 exec 会话）。                               |
| [conversation-session-ssh-remote-task-lifecycle.test.ts](conversation-session-ssh-remote-task-lifecycle.test.ts) | 移除仅删本机 membership，不关闭 Source attachment，也不删除远端项目/历史。                                         |
| [README.md](README.md)                                                                                           | 本目录用途、子目录与逐文件说明。                                                                                   |

<!-- qingqi-directory-index:end -->
