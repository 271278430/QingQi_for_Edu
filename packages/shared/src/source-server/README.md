# source-server

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 source server 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                                                                  |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [compatibility.ts](compatibility.ts)       | \* 远端服务支持设备卡停止 / 重启合同（`zcode stop --wait` 等，RDLC-01）的首个版本，桌面端据此做版本门禁。                                                 |
| [connectionErrors.ts](connectionErrors.ts) | Bug 原因：在线断连后的自动恢复经懒连接 probe 抛出 ECONNRESET；码表缺它时被                                                                                |
| [connectionLog.ts](connectionLog.ts)       | 裸路径可能含空格，不能把空格后的用户名/目录当成正文放行。只保留机器可识别的                                                                               |
| [contracts.ts](contracts.ts)               | 升级授权只绑定执行身份，不携带凭据或可变 Profile 内容。                                                                                                   |
| [errorCodes.ts](errorCodes.ts)             | 同一设备的更新进行中，本次连接在写状态和日志之前被拒绝；更新完成后可重试（R3 §6.3）。                                                                     |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                                                                        |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                                                                          |
| [release.ts](release.ts)                   | 实现或公开接口：SOURCE_SERVER_RELEASE_TARGETS、SOURCE_SERVER_RELEASE_DESCRIPTOR_FILE_NAME、sourceServerArtifactPolicySchema、SourceServerArtifactPolicy。 |

<!-- qingqi-directory-index:end -->
