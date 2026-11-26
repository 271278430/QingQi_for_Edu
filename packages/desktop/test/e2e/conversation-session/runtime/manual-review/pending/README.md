# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                       | 简要说明                                                                         |
| ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| [conversation-session-migration-dialog-race.test.ts](conversation-session-migration-dialog-race.test.ts)   | 仅截留真实 RPC 的返回时机；UI 操作与首启查询仍经过产品链路。                     |
| [conversation-session-profile-secret-decrypt.test.ts](conversation-session-profile-secret-decrypt.test.ts) | LRCD-02：已有 SSH Profile 的保存密码在本机无法解密（~/.zcode 换机 / 换用户）。   |
| [conversation-session-release-3163-upgrade.test.ts](conversation-session-release-3163-upgrade.test.ts)     | 只在旧 Electron 已完整退出的屏障内替换本次运行副本，保留同一 HOME 和浏览器数据。 |
| [conversation-session-runtime-restart.test.ts](conversation-session-runtime-restart.test.ts)               | conversation-session-runtime-restart.test 的实现文件。                           |
| [conversation-session-shared-cli.test.ts](conversation-session-shared-cli.test.ts)                         | 虚拟列表收到新回复后可能移除旧行，可见数量不增长；用末条回复身份确认本轮结果。   |
| [conversation-session-snapshot-retention.test.ts](conversation-session-snapshot-retention.test.ts)         | 生产 renderer 的独立 CDP E2E；使用 node:test，不能放入 WDIO/Docker preset。      |
| [README.md](README.md)                                                                                     | 本目录用途、子目录与逐文件说明。                                                 |

<!-- qingqi-directory-index:end -->
