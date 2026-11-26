# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                                                             | 简要说明                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| [conversation-session-data-sync-migration-entry.test.ts](conversation-session-data-sync-migration-entry.test.ts)                                 | DSYNC-16：迁移入口移到数据同步页（docs/remote/data-sync.md「迁移入口」）。                                        |
| [conversation-session-remote-data-sync-builtin-subagent-runtime.test.ts](conversation-session-remote-data-sync-builtin-subagent-runtime.test.ts) | DSYNC-09-05：推送内置 Explore 的模型覆盖后，远端已有 task 的下一轮 Explore 子请求使用推送的模型                   |
| [conversation-session-remote-data-sync-command-push.test.ts](conversation-session-remote-data-sync-command-push.test.ts)                         | DSYNC-10：设置 → 数据同步 → 设备 → 推送命令（docs/remote/data-sync.md「命令」）。                                 |
| [conversation-session-remote-data-sync-demo-walkthrough.test.ts](conversation-session-remote-data-sync-demo-walkthrough.test.ts)                 | \* DSYNC-DEMO：数据同步功能演示走查（docs/remote/data-sync.md）。不是断言型用例：在本机 Docker 远端上             |
| [conversation-session-remote-data-sync-device-connect.test.ts](conversation-session-remote-data-sync-device-connect.test.ts)                     | DSYNC-05：数据同步页的设备状态与连接（docs/remote/data-sync.md「设备列表与设备同步状态」）。                      |
| [conversation-session-remote-data-sync-hook-push.test.ts](conversation-session-remote-data-sync-hook-push.test.ts)                               | DSYNC-11：设置 → 数据同步 → 设备 → 推送钩子（docs/remote/data-sync.md「钩子」）。                                 |
| [conversation-session-remote-data-sync-legacy-entries.test.ts](conversation-session-remote-data-sync-legacy-entries.test.ts)                     | DSYNC-14：旧同步入口统一打开数据同步弹窗（docs/remote/data-sync.md「旧入口」）。                                  |
| [conversation-session-remote-data-sync-marketplace-plugin-push.test.ts](conversation-session-remote-data-sync-marketplace-plugin-push.test.ts)   | DSYNC-08：设置 → 数据同步 → 设备 → 推送 marketplace 插件（docs/remote/data-sync.md「插件 · marketplace 插件」）。 |
| [conversation-session-remote-data-sync-mcp-push.test.ts](conversation-session-remote-data-sync-mcp-push.test.ts)                                 | DSYNC-06：设置 → 数据同步 → 设备 → 推送 MCP 服务器（docs/remote/data-sync.md「MCP 服务器」）。                    |
| [conversation-session-remote-data-sync-plugin-push.test.ts](conversation-session-remote-data-sync-plugin-push.test.ts)                           | DSYNC-07：设置 → 数据同步 → 设备 → 推送 inline 插件（docs/remote/data-sync.md「插件」）。                         |
| [conversation-session-remote-data-sync-provider-retry.test.ts](conversation-session-remote-data-sync-provider-retry.test.ts)                     | DSYNC-13：数据同步页「模型提供商」只读分类与失败重试（docs/remote/data-sync.md「模型提供商（只读）」）。          |
| [conversation-session-remote-data-sync-runtime-usage.test.ts](conversation-session-remote-data-sync-runtime-usage.test.ts)                       | DSYNC-17：推送内容在远端会话中的可用时机（docs/remote/data-sync.md「Seam ③：桌面 E2E」）。                        |
| [conversation-session-remote-data-sync-scope-by-device.test.ts](conversation-session-remote-data-sync-scope-by-device.test.ts)                   | DSYNC-15：设置页 Scope 菜单按设备分组（docs/remote/data-sync.md「Scope 菜单按设备分组」）。                       |
| [conversation-session-remote-data-sync-skill-push.test.ts](conversation-session-remote-data-sync-skill-push.test.ts)                             | DSYNC-04：设置 → 数据同步 → 设备 → 推送技能（docs/remote/data-sync.md）。                                         |
| [conversation-session-remote-data-sync-subagent-push.test.ts](conversation-session-remote-data-sync-subagent-push.test.ts)                       | DSYNC-09：设置 → 数据同步 → 设备 → 推送子智能体（docs/remote/data-sync.md「子智能体」）。                         |
| [README.md](README.md)                                                                                                                           | 本目录用途、子目录与逐文件说明。                                                                                  |

<!-- qingqi-directory-index:end -->
