# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                                           | 简要说明                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| [conversation-session-r3-connectivity-test.test.ts](conversation-session-r3-connectivity-test.test.ts)                         | 在设置页选中目标 provider 卡片后点“测试模型”按钮（title 文案），返回随后出现的提示文本。                       |
| [conversation-session-r3-docker-transport.test.ts](conversation-session-r3-docker-transport.test.ts)                           | Composer 的旧远程入口已退役；与 SSH 一样从项目创建进入 transport 选择。                                        |
| [conversation-session-r3-soak-dual.test.ts](conversation-session-r3-soak-dual.test.ts)                                         | Linux e2e 服务器上没有 macOS 版 Chrome：用 R3_MOBILE_CHROME 指向该机 playwright 下载的                         |
| [conversation-session-r3-soak-reconnect.test.ts](conversation-session-r3-soak-reconnect.test.ts)                               | 切 tab：本地 → 远端 A → 远端 B → 远端 A。                                                                      |
| [conversation-session-r3-source-lines.test.ts](conversation-session-r3-source-lines.test.ts)                                   | 先确认夹具确为符号链接且指向目标，不能把目录准备失败误报为 canonical 身份缺陷。                                |
| [conversation-session-r3-transport-loss.test.ts](conversation-session-r3-transport-loss.test.ts)                               | \* 只切断 Desktop（用户 dev）的 SSH 会话：模型回放反向隧道由独立用户 tunnel 承载，必须保留，                   |
| [conversation-session-remote-composer-plan-reselect.test.ts](conversation-session-remote-composer-plan-reselect.test.ts)       | ZCT-2118278184274395136：SSH 工作区里「个人套餐 → 普通 API → 同一个人套餐」每次切回 1.5～8 秒。                |
| [conversation-session-remote-restart-stale-lock-docker.test.ts](conversation-session-remote-restart-stale-lock-docker.test.ts) | 3.16.2 远端回归 R7（#13）的真实 Docker transport 验证（本机 Docker runner）：容器重启后                        |
| [conversation-session-remote-zombie-lock-docker.test.ts](conversation-session-remote-zombie-lock-docker.test.ts)               | R3-ISSUE-034（ZCT-2117275161536565248）的真实 Docker transport 验证（本机 Docker runner）：容器 PID 1          |
| [conversation-session-ssh-remote-app-exit-running.test.ts](conversation-session-ssh-remote-app-exit-running.test.ts)           | 必须在旧 Electron 进程树退出后、新 Electron 启动前取证；不能用 renderer reload 代替关闭应用。                  |
| [conversation-session-ssh-remote-cancel-retry.test.ts](conversation-session-ssh-remote-cancel-retry.test.ts)                   | 失败录像显示取消已返回项目草稿；旧断言仍等待关闭向导内的“已取消”，误报为错误。                                 |
| [conversation-session-ssh-remote-cold-reconnect.test.ts](conversation-session-ssh-remote-cold-reconnect.test.ts)               | browser.reloadSession 才会重启 Electron/Main/Host/CLI；renderer reload 不足以证明冷恢复。                      |
| [conversation-session-ssh-remote-colon-username.test.ts](conversation-session-ssh-remote-colon-username.test.ts)               | 缺陷曾在本地身份解析时终止连接；错误密码应到达真实 SSH 认证，并保留可读的失败状态。                            |
| [conversation-session-ssh-remote-core-start-failure.test.ts](conversation-session-ssh-remote-core-start-failure.test.ts)       | 3.16.2 远端超时工单的真实 SSH 验证（本机 Docker runner）：远端 Core 启动失败时，连接错误只有                   |
| [conversation-session-ssh-remote-core-unresponsive.test.ts](conversation-session-ssh-remote-core-unresponsive.test.ts)         | ZCT-2113570821476302848 的真实 SSH 验证（本机 Docker runner）：远端 Core 的事件循环被同步工作占满后，          |
| [conversation-session-ssh-remote-crash-loop-detail.test.ts](conversation-session-ssh-remote-crash-loop-detail.test.ts)         | R3-ISSUE-031 / R3-ISSUE-035 的真实 SSH 验证（本机 Docker runner）：Core 在 ready 后被连续结束，Supervisor 耗尽 |
| [conversation-session-ssh-remote-directory-resilience.test.ts](conversation-session-ssh-remote-directory-resilience.test.ts)   | 目录可用性由 Host stat 派生。撤销独占父目录的遍历权限才能真实触发 EACCES，                                     |
| [conversation-session-ssh-remote-host-capacity.test.ts](conversation-session-ssh-remote-host-capacity.test.ts)                 | 同批用例共用远端容器；独立目录避免后续 P0 的同名项目被自动追加名称后缀。                                       |
| [conversation-session-ssh-remote-retry-budget.test.ts](conversation-session-ssh-remote-retry-budget.test.ts)                   | 浮层可能盖住其他入口；移到视口右上角，确保鼠标真正离开触发区域和浮层。                                         |
| [conversation-session-ssh-remote-symlink-reconnect.test.ts](conversation-session-ssh-remote-symlink-reconnect.test.ts)         | 用户现场：项目根目录是 symlink（例如 /home/dev/projects/app → /data/projects/app），                           |
| [README.md](README.md)                                                                                                         | 本目录用途、子目录与逐文件说明。                                                                               |

<!-- qingqi-directory-index:end -->
