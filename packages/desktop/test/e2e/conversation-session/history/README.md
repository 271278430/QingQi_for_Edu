# history

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 history 测试场景。

### 文件

| 文件                                                                                                                               | 简要说明                                                                               |
| ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [conversation-session-anthropic-reasoning-history-replay.test.ts](conversation-session-anthropic-reasoning-history-replay.test.ts) | conversation-session-anthropic-reasoning-history-replay.test 的实现文件。              |
| [conversation-session-chat-loading-live-tail.test.ts](conversation-session-chat-loading-live-tail.test.ts)                         | 运行时已有 ChatLoading，旧的过程标题不能同时显示第二份 Working。                       |
| [conversation-session-file-summary-cold-start.test.ts](conversation-session-file-summary-cold-start.test.ts)                       | O16：完整重启 Electron / Host / CLI 后，已完成轮次的文件变更摘要仍需从持久数据冷物化。 |
| [conversation-session-history-first-migration.test.ts](conversation-session-history-first-migration.test.ts)                       | 先观察迁移启动的 hook，再打开任务，确保不是订阅先到的普通历史场景。                    |
| [conversation-session-history-first.test.ts](conversation-session-history-first.test.ts)                                           | conversation-session-history-first.test 的实现文件。                                   |
| [conversation-session-v4-load-older.test.ts](conversation-session-v4-load-older.test.ts)                                           | HLP02/M5④ 门禁：长历史无感分页（顶部历史可达 + prepend 不跳）。                        |
| [README.md](README.md)                                                                                                             | 本目录用途、子目录与逐文件说明。                                                       |

<!-- qingqi-directory-index:end -->
