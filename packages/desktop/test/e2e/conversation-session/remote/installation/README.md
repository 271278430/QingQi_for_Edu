# installation

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 installation 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                     | 简要说明                                                                                                            |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| [conversation-session-r3-install-faults.test.ts](conversation-session-r3-install-faults.test.ts)                         | 从当前 spec 回到 desktop，保持隔离 mock-cdn 与版本文件定位正确。                                                    |
| [conversation-session-r3-provisioning-gui.test.ts](conversation-session-r3-provisioning-gui.test.ts)                     | fixture r3-provisioning-gui-reconnect-main 的回复正文不带 E2E\_ 前缀，与 lifecycle helper 的 replyMarker 约定一致。 |
| [conversation-session-r3-uninstall.test.ts](conversation-session-r3-uninstall.test.ts)                                   | 新项目 section 自身包含任务列表；旧 li 祖先已不存在，不能因此把旧历史读成空列表。                                   |
| [conversation-session-remote-install-progress.test.ts](conversation-session-remote-install-progress.test.ts)             | harness 的目标 suffix 支持命名批次，不限十六进制；仍只允许其独立容器命名空间。                                      |
| [conversation-session-ssh-provisioning-failure.test.ts](conversation-session-ssh-provisioning-failure.test.ts)           | 首装会停在安装确认；先驱动该步骤，才能观察真正的 provisioning 失败。                                                |
| [conversation-session-ssh-remote-provisioning-ready.test.ts](conversation-session-ssh-remote-provisioning-ready.test.ts) | 根因：seed helper 已改读 runtime Base URL，旧环境变量覆盖不再生效；远端误连本机 loopback 端口。                     |
| [conversation-session-wsl-required-update.test.ts](conversation-session-wsl-required-update.test.ts)                     | 只替换远端输入：真实 Electron IPC、Root、向导、RPC 和按钮照常执行。                                                 |
| [README.md](README.md)                                                                                                   | 本目录用途、子目录与逐文件说明。                                                                                    |

<!-- qingqi-directory-index:end -->
