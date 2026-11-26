# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                                                       | 简要说明                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| [conversation-session-r3-daemon-detached.test.ts](conversation-session-r3-daemon-detached.test.ts)                                         | 容器没有 systemd user manager：只能是 detached daemon，且不得伪装成已注册服务。                           |
| [conversation-session-r3-daemon-service-fallback.test.ts](conversation-session-r3-daemon-service-fallback.test.ts)                         | R3A-BLD-08：带常驻 user manager 的 SSH 目标（run-local-docker.mjs --systemd）。                           |
| [conversation-session-r3-docker-daemon-unavailable.test.ts](conversation-session-r3-docker-daemon-unavailable.test.ts)                     | R3A-TRN-02：本机 Docker daemon 不可用（socket 不存在、socket 没有权限）时连接 Docker 容器。               |
| [conversation-session-r3-install-environment.test.ts](conversation-session-r3-install-environment.test.ts)                                 | old-glibc-runtime 需要真实 glibc < 2.28 的远端镜像，不注入 getconf。服务器队列没有该档位，                |
| [conversation-session-r3-reinstall-damaged-release.test.ts](conversation-session-r3-reinstall-damaged-release.test.ts)                     | 重装要上传完整 archive 再启动远端服务；本机 Docker 远端通常一分钟内完成，留足余量。                       |
| [conversation-session-r3-restart-remote-service.test.ts](conversation-session-r3-restart-remote-service.test.ts)                           | \* 在渲染进程里记录设备卡状态标签的每一次变化：重启期间的“连接中”只持续数秒，轮询可能错过。               |
| [conversation-session-r3-server-update.test.ts](conversation-session-r3-server-update.test.ts)                                             | 上传/解压期间容器 sshd 在 x64 模拟下会拒绝或拖慢新握手；只读探针改走 docker exec，不经 sshd。             |
| [conversation-session-r3-stop-remote-service.test.ts](conversation-session-r3-stop-remote-service.test.ts)                                 | 连接管理器的在线重试档位为 2/4/8 秒；多等一段余量，覆盖完整一个自动重试周期。                             |
| [conversation-session-r3-update-cancel.test.ts](conversation-session-r3-update-cancel.test.ts)                                             | 与 harness/remote/remote-wdio-env.mjs 的 TEST_CDN_SPEC_MARKERS 一致：本机缓存目录按该标记隔离。           |
| [conversation-session-r3-update-inflight.test.ts](conversation-session-r3-update-inflight.test.ts)                                         | 远端安装切换 current.json 的瞬间可能读到中间态；轮询里按“尚未完成”处理。                                  |
| [conversation-session-remote-restart-stale-daemon-ssh.test.ts](conversation-session-remote-restart-stale-daemon-ssh.test.ts)               | 3.16.2 远端回归 R7（#14–#16）的真实 SSH 验证（本机 Docker runner）：远端环境重启后，                      |
| [conversation-session-remote-server-root-replaced-ssh.test.ts](conversation-session-remote-server-root-replaced-ssh.test.ts)               | A4（ZCT-2112854001415753728）的真实 SSH 验证（本机 Docker runner --systemd）：daemon 以 OS 用户服务运行时 |
| [conversation-session-ssh-probe-validation.test.ts](conversation-session-ssh-probe-validation.test.ts)                                     | 只影响本次容器 dev 用户的探测命令：正常执行仍进入原登录 shell，SFTP、安装与 daemon 不替换。               |
| [conversation-session-ssh-remote-daemon-starting-reuse.test.ts](conversation-session-ssh-remote-daemon-starting-reuse.test.ts)             | 3.16.2 远端回归的真实 SSH 验证（本机 Docker runner）：                                                    |
| [conversation-session-ssh-remote-install-killed.test.ts](conversation-session-ssh-remote-install-killed.test.ts)                           | 3.16.2 远端回归 R1 的真实 SSH 验证（本机 Docker runner）：远端安装命令被信号杀死时，                      |
| [conversation-session-ssh-remote-legacy-install-handoff.test.ts](conversation-session-ssh-remote-legacy-install-handoff.test.ts)           | 3.16.2 工单的真实 SSH 验证（本机 Docker runner）：                                                        |
| [conversation-session-ssh-remote-startup-reconnect-slow-auth.test.ts](conversation-session-ssh-remote-startup-reconnect-slow-auth.test.ts) | 3.16.2 工单 ZCT-2112827425880723456 的真实 SSH 验证（本机 Docker runner）：                               |
| [conversation-session-ssh-remote-supervisor-lock-failure.test.ts](conversation-session-ssh-remote-supervisor-lock-failure.test.ts)         | R3-ISSUE-035（ZCT-2117253090228297728 等）的真实 SSH 验证（本机 Docker runner）：Supervisor 在写出第一份  |
| [conversation-session-ssh-remote-upgrade-history.test.ts](conversation-session-ssh-remote-upgrade-history.test.ts)                         | conflict：canonical 与 source 的身份冲突；conflict-sources：canonical 不含该任务，两个 source 之间冲突。  |
| [conversation-session-ssh-remote-version-policy.test.ts](conversation-session-ssh-remote-version-policy.test.ts)                           | 只点击向导错误面板内的按钮，避免误点设置页或横幅中的同名动作。                                            |
| [conversation-session-ssh-unsupported-target-errors.test.ts](conversation-session-ssh-unsupported-target-errors.test.ts)                   | 折叠的“详细信息”里必须保留的原始诊断片段。                                                                |
| [README.md](README.md)                                                                                                                     | 本目录用途、子目录与逐文件说明。                                                                          |

<!-- qingqi-directory-index:end -->
