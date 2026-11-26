# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                                           | 简要说明                                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| [conversation-session-r3-attachments.test.ts](conversation-session-r3-attachments.test.ts)                                     | 最小合法 PDF（单页空白），足以让远端识别为 PDF 并做 mime/扩展名校验。                                    |
| [conversation-session-r3-shared-waiters.test.ts](conversation-session-r3-shared-waiters.test.ts)                               | 在线：项目 a、项目 b 共享一个 Source 连接（同一 target）。                                               |
| [conversation-session-r3-subagent.test.ts](conversation-session-r3-subagent.test.ts)                                           | 远端用例前置：Server 启动时设置 ZCODE_DYNAMIC_WORKFLOW_MODE=alwaysOn；WDIO 也为本文件开启。              |
| [conversation-session-r3-task-faults.test.ts](conversation-session-r3-task-faults.test.ts)                                     | 429 必须真实注入并核对网络结果；不能用 401 代替限流覆盖。                                                |
| [conversation-session-remote-shared-root-peer-host-ssh.test.ts](conversation-session-remote-shared-root-peer-host-ssh.test.ts) | 两台主机共享 home 时的真实 SSH 验证（本机 Docker runner --systemd）：同一容器里再注册一个 user service， |
| [conversation-session-share-ssh-artifact.test.ts](conversation-session-share-ssh-artifact.test.ts)                             | 远端 Agent 的 loopback 不是 Desktop；固定 replay 端口需反向隧道。                                        |
| [conversation-session-ssh-remote-attachment-races.test.ts](conversation-session-ssh-remote-attachment-races.test.ts)           | conversation-session-ssh-remote-attachment-races.test 的实现文件。                                       |
| [README.md](README.md)                                                                                                         | 本目录用途、子目录与逐文件说明。                                                                         |

<!-- qingqi-directory-index:end -->
