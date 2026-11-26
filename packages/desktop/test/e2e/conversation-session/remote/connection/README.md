# connection

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 connection 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                           | 简要说明                                                                                           |
| ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| [conversation-session-r3-ack-loss.test.ts](conversation-session-r3-ack-loss.test.ts)                                           | 只暂挂本例原始输入，不伪造 RPC 结果，也不拦截发送前的配置查询。                                    |
| [conversation-session-r3-boundary-ack.test.ts](conversation-session-r3-boundary-ack.test.ts)                                   | 冷重启失败需区分“未保存”与“启动时丢失”；证据只记录存在性，不保存 key 或口令正文。                  |
| [conversation-session-r3-recovery-guards.test.ts](conversation-session-r3-recovery-guards.test.ts)                             | REC-02：显式断开 → offline 收口；等待 30 秒确认没有自动重开（迟到快照不重开）；open history 保留。 |
| [conversation-session-r3-renderer-reload.test.ts](conversation-session-r3-renderer-reload.test.ts)                             | 分别解析日志，不能用拼接换行把一个文件尚未写完的尾行变成完整 ACK。                                 |
| [conversation-session-r3-stale-generation.test.ts](conversation-session-r3-stale-generation.test.ts)                           | Desktop 经代理连接；模型回放隧道走直连（tunnel 用户），避免 hold 影响远端模型请求。                |
| [conversation-session-remote-connection-log-contract.test.ts](conversation-session-remote-connection-log-contract.test.ts)     | conversation-session-remote-connection-log-contract.test 的实现文件。                              |
| [conversation-session-remote-draft-prewarm.test.ts](conversation-session-remote-draft-prewarm.test.ts)                         | 同时读取实际 Composer、workspace owner 与真实命令回执，不用模拟 createSession 结果。               |
| [conversation-session-remote-offline-icons.test.ts](conversation-session-remote-offline-icons.test.ts)                         | 未连通记录现在默认折叠且用连接行展示，旧 case 按设备卡的 p 标题读取会漏掉它们。                    |
| [conversation-session-ssh-disconnect-experience.test.ts](conversation-session-ssh-disconnect-experience.test.ts)               | 走原空白页路径：会话 -> 设置设备卡断开 -> 返回原会话。                                             |
| [conversation-session-ssh-remote-banner-reconnect.test.ts](conversation-session-ssh-remote-banner-reconnect.test.ts)           | \* forward：透传到真实 sshd；reset：现有连接发 RST，新连接收到客户端数据后发 RST；                 |
| [conversation-session-ssh-remote-connection-management.test.ts](conversation-session-ssh-remote-connection-management.test.ts) | conversation-session-ssh-remote-connection-management.test 的实现文件。                            |
| [conversation-session-ssh-remote-connection-p0.test.ts](conversation-session-ssh-remote-connection-p0.test.ts)                 | conversation-session-ssh-remote-connection-p0.test 的实现文件。                                    |
| [conversation-session-ssh-remote-development-p0.test.ts](conversation-session-ssh-remote-development-p0.test.ts)               | Bugfix：远端 E2E fixture 也必须落在专用隔离根目录，不能写入系统临时目录。                          |
| [conversation-session-ssh-remote-local-download-proxy.test.ts](conversation-session-ssh-remote-local-download-proxy.test.ts)   | 从当前 spec 回到 desktop，避免把 mock-cdn 定位到仓库根目录。                                       |
| [conversation-session-ssh-remote-p0.test.ts](conversation-session-ssh-remote-p0.test.ts)                                       | conversation-session-ssh-remote-p0.test 的实现文件。                                               |
| [conversation-session-ssh-remote-server-fault.test.ts](conversation-session-ssh-remote-server-fault.test.ts)                   | 故障注入前先记下两个 tab 的 sessionId：只有和超时时的值对比，才能区分                              |
| [README.md](README.md)                                                                                                         | 本目录用途、子目录与逐文件说明。                                                                   |

<!-- qingqi-directory-index:end -->
