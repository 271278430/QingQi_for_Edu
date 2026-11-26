# remote-startup-failures-3-16

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

remote startup failures 3 16 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                                           | 简要说明                                                          |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| [01-source-server-startup-failure-triage.md](01-source-server-startup-failure-triage.md)       | 3.16.2 Source Server 启动阶段失败：工单分诊与修复记录：说明文档。 |
| [02-service-registration-failure-fallback.md](02-service-registration-failure-fallback.md)     | SSH service 注册失败后不回退 fallback：说明文档。                 |
| [03-corrupted-release-recovery.md](03-corrupted-release-recovery.md)                           | 已安装 release 损坏后无法自愈：说明文档。                         |
| [04-shared-home-across-hosts.md](04-shared-home-across-hosts.md)                               | 多台主机共享 home 时 ingress token 被覆盖：说明文档。             |
| [05-unexplained-ssh-timeouts-and-token-read.md](05-unexplained-ssh-timeouts-and-token-read.md) | SSH 启动超时与 ingress-token 读取失败的未知原因：说明文档。       |
| [06-legacy-lock-pid-reuse-after-upgrade.md](06-legacy-lock-pid-reuse-after-upgrade.md)         | 3.16.2 旧格式锁在升级后的 PID 采用残留：说明文档。                |
| [README.md](README.md)                                                                         | 本目录用途、子目录与逐文件说明。                                  |

<!-- qingqi-directory-index:end -->
