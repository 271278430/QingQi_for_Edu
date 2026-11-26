# server-core

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server-cli 基础工程中的 server core 实现源码。

### 文件

| 文件                                             | 简要说明                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------- |
| [core.ts](core.ts)                               | Bug 原因：Agent 的模型请求头从 ZCODE_APP_VERSION 读 App 版本，缺失时回退到 CLI 包版本 |
| [entry.ts](entry.ts)                             | 与 core.ts 的 shutdown 路径同理——启动失败往往发生在服务已部分初始化                   |
| [hostCapability.ts](hostCapability.ts)           | 与 packages/server/src/hostCapability.ts 保持一致的一次性短期 ticket 语义。           |
| [http.ts](http.ts)                               | HTTP server.close() 不会收敛已经 upgrade 的 WebSocket，活跃 desktop                   |
| [ingressToken.ts](ingressToken.ts)               | 实现或公开接口：createIngressToken。                                                  |
| [parentDisconnect.ts](parentDisconnect.ts)       | \* 注册 Core 对 Supervisor IPC 断连的清理钩子。                                       |
| [proxyStdio.ts](proxyStdio.ts)                   | stdout 必须保持纯字节通道；错误只由 CLI 写 stderr，桥内不注入任何 framing。           |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                      |
| [serverIdentity.ts](serverIdentity.ts)           | \* 读取安装级 Server identity。真实 Supervisor 启动必须提供 server root；未提供时     |
| [taskActivityTracker.ts](taskActivityTracker.ts) | 实现或公开接口：TaskActivityTracker、createTaskActivityTracker。                      |

<!-- qingqi-directory-index:end -->
