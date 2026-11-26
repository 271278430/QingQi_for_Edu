# runtime

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 runtime 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                       | 简要说明                                                                                 |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [conversation-session-config-and-multisession.test.ts](conversation-session-config-and-multisession.test.ts)               | 修复原因：慢流式 fixture 在部分环境可能已经完成，不能把固定等待后的                      |
| [conversation-session-config-independent-startup.test.ts](conversation-session-config-independent-startup.test.ts)         | SCB01/02：配置网关在 beforeSession 就保持 pending，不启用 ZCODE_OFFPEAK_MOCK。           |
| [conversation-session-configurable-data-directory.test.ts](conversation-session-configurable-data-directory.test.ts)       | conversation-session-configurable-data-directory.test 的实现文件。                       |
| [conversation-session-database-startup.test.ts](conversation-session-database-startup.test.ts)                             | GLOBALDB-02/08/11：真实 DB 写锁作为屏障，不用伪造 renderer migrationReady。              |
| [conversation-session-id-compatibility.test.ts](conversation-session-id-compatibility.test.ts)                             | conversation-session-id-compatibility.test 的实现文件。                                  |
| [conversation-session-local-config-runtime-usage.test.ts](conversation-session-local-config-runtime-usage.test.ts)         | DSYNC-18：本机配置变更在本机会话中的生效时机，作为 DSYNC-17（远端推送）的对照。          |
| [conversation-session-local-conversation-identity.test.ts](conversation-session-local-conversation-identity.test.ts)       | 只构造离线 open-set，不连接 SSH；调用真实 store 的 add/activate，复现新 tab 置顶的顺序。 |
| [conversation-session-settings-connection-completion.test.ts](conversation-session-settings-connection-completion.test.ts) | 用真实 ClipboardEvent 模拟粘贴，覆盖主机框的 onPaste 拆分（RDUX-27）。                   |
| [conversation-session-sse-stall-diagnostic.test.ts](conversation-session-sse-stall-diagnostic.test.ts)                     | conversation-session-sse-stall-diagnostic.test 的实现文件。                              |
| [conversation-session-unbound-resume.test.ts](conversation-session-unbound-resume.test.ts)                                 | 残缺历史恢复需要合法 high/max 目标；通用 seed 默认仅 disabled，不能用它验证重选。        |
| [conversation-session-upstream-workspace-smoke.test.ts](conversation-session-upstream-workspace-smoke.test.ts)             | 修复原因：waitForWorkspaceApp 已同时兼容路径徽标和侧栏 workspace item。                  |
| [README.md](README.md)                                                                                                     | 本目录用途、子目录与逐文件说明。                                                         |

<!-- qingqi-directory-index:end -->
