# remote-tickets-3-16-2-1022

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

remote tickets 3 16 2 1022 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                                                     | 简要说明                                                                                 |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [01-ticket-triage.md](01-ticket-triage.md)                                                               | 3.16.2 远程连接工单分诊（2026-10-22 批次）：说明文档。                                   |
| [02-startup-reconnect-cancel-hangs-ssh-flight.md](02-startup-reconnect-cancel-hangs-ssh-flight.md)       | 启动重连取消后 SSH flight 永久挂起，设备一直“连接中”：说明文档。                         |
| [03-install-confirm-drops-ssh-password.md](03-install-confirm-drops-ssh-password.md)                     | 安装确认交接丢失 SSH 密码，报“SSH 认证失败”：说明文档。                                  |
| [04-wsl-stale-failure-handoff-and-profile-split.md](04-wsl-stale-failure-handoff-and-profile-split.md)   | WSL 过期失败交接为 “Connection failed”，迁移 Profile 与新 Profile 分裂：说明文档。       |
| [05-local-setting-lock-blocks-remote-admission.md](05-local-setting-lock-blocks-remote-admission.md)     | 本机设置锁不能回收，远程连接准入失败并被误报为“连接超时”：说明文档。                     |
| [06-orphan-supervisor-after-server-root-replaced.md](06-orphan-supervisor-after-server-root-replaced.md) | server root 被替换后孤儿 Supervisor 写出 ready，Desktop 读不到 ingress-token：说明文档。 |
| [07-systemd-user-service-without-linger.md](07-systemd-user-service-without-linger.md)                   | systemd user service 未开启 linger：断线后 Core、Agent 与任务一起被停止：说明文档。      |
| [08-first-provisioning-barrier-on-slow-remote.md](08-first-provisioning-barrier-on-slow-remote.md)       | 慢远端上首次 Provider Provisioning 屏障无截止，远程项目长时间打不开：说明文档。          |
| [09-remote-devices-settings-typography.md](09-remote-devices-settings-typography.md)                     | 远程设备设置页字号小于其他设置页：说明文档。                                             |
| [README.md](README.md)                                                                                   | 本目录用途、子目录与逐文件说明。                                                         |

<!-- qingqi-directory-index:end -->
