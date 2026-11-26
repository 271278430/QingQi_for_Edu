# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                                                                     | 简要说明                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| [conversation-session-project-device-visibility-ssh.test.ts](conversation-session-project-device-visibility-ssh.test.ts)                                 | 项目已被用户改名且跨 Source 同名，任务归属必须按稳定身份验证，不能由目录名反推项目名。                        |
| [conversation-session-r3-project-entry.test.ts](conversation-session-r3-project-entry.test.ts)                                                           | conversation-session-r3-project-entry.test 的实现文件。                                                       |
| [conversation-session-r3-ui-pairwise.test.ts](conversation-session-r3-ui-pairwise.test.ts)                                                               | Electron 下 WebDriver setWindowSize 不可用（Browser.getWindowForTarget 缺失），改经 main 进程设置主窗口尺寸。 |
| [conversation-session-rdux-13-sidebar-device-level-connect.test.ts](conversation-session-rdux-13-sidebar-device-level-connect.test.ts)                   | 标题现为折叠按钮；用真实项目连接动作重复请求，握手闸门保证第二次发生在 pending 期间。                         |
| [conversation-session-rdux-14-device-online-restores-stale-tabs.test.ts](conversation-session-rdux-14-device-online-restores-stale-tabs.test.ts)         | 新版只恢复活动 B；直接设置权威活动字段的年龄，不能只修改旧兼容投影。                                          |
| [conversation-session-remote-accessibility.test.ts](conversation-session-remote-accessibility.test.ts)                                                   | 真正按 Tab 到目标，不用 focus()/click() 代替键盘流程。                                                        |
| [conversation-session-remote-device-search-list.test.ts](conversation-session-remote-device-search-list.test.ts)                                         | 清空走产品实际按钮，不能用 WebDriver 的空 setValue 代替 React 受控输入的清空动作。                            |
| [conversation-session-remote-project-handoff.test.ts](conversation-session-remote-project-handoff.test.ts)                                               | 真实 SSH/Host/Root；bind 返回屏障只控制时序，不伪造连接或导航结果。                                           |
| [conversation-session-remote-project-read-failed.test.ts](conversation-session-remote-project-read-failed.test.ts)                                       | 关闭项目 tab：重连设备时不再登记该项目，只留侧栏读取这一条登记路径。                                          |
| [conversation-session-remote-ui-walkthrough.test.ts](conversation-session-remote-ui-walkthrough.test.ts)                                                 | \* 远程连接 UI 走查：不是断言型用例，而是在真实 SSH 容器上按用户顺序走完向导、侧栏、                          |
| [conversation-session-remote-workspace-folder-thread-exhaustion-ssh.test.ts](conversation-session-remote-workspace-folder-thread-exhaustion-ssh.test.ts) | ZCT-2113660144497782784 的真实 SSH 验证（本机 Docker runner）：远端读取项目目录卡住，且每个卡住的调用真实占住 |
| [conversation-session-remote-workspace-folder-unresponsive-ssh.test.ts](conversation-session-remote-workspace-folder-unresponsive-ssh.test.ts)           | 3.16.2 远端回归 R8（#12）的真实 SSH 验证（本机 Docker runner）：远端读取项目目录永不返回时，                  |
| [conversation-session-ssh-remote-project-order.test.ts](conversation-session-ssh-remote-project-order.test.ts)                                           | conversation-session-ssh-remote-project-order.test 的实现文件。                                               |
| [README.md](README.md)                                                                                                                                   | 本目录用途、子目录与逐文件说明。                                                                              |

<!-- qingqi-directory-index:end -->
