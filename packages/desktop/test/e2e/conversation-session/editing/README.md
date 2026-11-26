# editing

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 editing 测试场景。

### 文件

| 文件                                                                                                               | 简要说明                                                                                                |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [conversation-session-composer-edit-mode.test.ts](conversation-session-composer-edit-mode.test.ts)                 | D21–D28 composer 编辑态（docs/ui/composer-edit-mode.md）：编辑 latest user query 采用底部 composer。    |
| [conversation-session-edit.test.ts](conversation-session-edit.test.ts)                                             | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。                                     |
| [conversation-session-v4-cold-failed-edit.test.ts](conversation-session-v4-cold-failed-edit.test.ts)               | PV4-06 × C07 pending：provider 在首 token 前失败后，必须从持久 transcript                               |
| [conversation-session-v4-edit.test.ts](conversation-session-v4-edit.test.ts)                                       | PV4-11：stable compact 覆盖 latest user query 后，edit 仍在原 session 做 branch cut。                   |
| [conversation-session-v4-rewind-compact-extended.test.ts](conversation-session-v4-rewind-compact-extended.test.ts) | PV4-18/PV4-19：compact-covered 附件 intent 重放，以及多 compact boundary 跨界 edit + cold restore。     |
| [conversation-session-v4-rewind-files.test.ts](conversation-session-v4-rewind-files.test.ts)                       | PV4-21/PV4-22：editUserQuery(workspaceMode=rewind) 的文件事务与冲突降级。                               |
| [conversation-session-v4-rewind-queue-background.test.ts](conversation-session-v4-rewind-queue-background.test.ts) | PV4-20/PV4-23：compact 期间 held queue 在 edit 后保持；被裁 turn 的后台 Bash 先取消再 bump generation。 |
| [README.md](README.md)                                                                                             | 本目录用途、子目录与逐文件说明。                                                                        |

<!-- qingqi-directory-index:end -->
