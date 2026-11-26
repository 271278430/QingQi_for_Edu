# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                                   | 简要说明                                                                               |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [conversation-session-r3-mobile-permission.test.ts](conversation-session-r3-mobile-permission.test.ts)                 | Linux e2e 服务器上没有 macOS 版 Chrome：用 R3_MOBILE_CHROME 指向该机 playwright 下载的 |
| [conversation-session-r3-mobile-startup-restore.test.ts](conversation-session-r3-mobile-startup-restore.test.ts)       | WebDriver 把返回对象的 error 字段当成协议错误；序列化后再在测试端还原真实状态。        |
| [conversation-session-r3-mobile.test.ts](conversation-session-r3-mobile.test.ts)                                       | Linux e2e 服务器上没有 macOS 版 Chrome：用 R3_MOBILE_CHROME 指向该机 playwright 下载的 |
| [conversation-session-web-remote-project-directory.test.ts](conversation-session-web-remote-project-directory.test.ts) | 新 Source 有独立引导记录；先通过真实 UI 完成前置，不能把引导遮挡误判成目录丢失。       |
| [conversation-session-web-remote-terminal.test.ts](conversation-session-web-remote-terminal.test.ts)                   | conversation-session-web-remote-terminal.test 的实现文件。                             |
| [conversation-session-web-remote-unread.test.ts](conversation-session-web-remote-unread.test.ts)                       | conversation-session-web-remote-unread.test 的实现文件。                               |
| [README.md](README.md)                                                                                                 | 本目录用途、子目录与逐文件说明。                                                       |

<!-- qingqi-directory-index:end -->
