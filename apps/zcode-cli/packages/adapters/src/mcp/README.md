# mcp

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 mcp 实现源码。

### 文件

| 文件                                                   | 简要说明                                                                                                                     |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| [appConnections.test.ts](appConnections.test.ts)       | appConnections.test 的实现文件。                                                                                             |
| [descriptor.ts](descriptor.ts)                         | 插件 UI：tools/list 的 `_meta` 只在这里读一次，归一化成 descriptor.ui；下游不再碰原始 \_meta。                               |
| [index.ts](index.ts)                                   | 存活探测只允许占用很短的时间：它挂在设置页刷新的同步路径上，超时即判死并触发重连。                                           |
| [network.ts](network.ts)                               | remote Agent 由 ~/.zcode/server/node 启动，但登录环境 PATH 不含该目录，                                                      |
| [node-fallback.ts](node-fallback.ts)                   | \* 桌面 agent 跑在 Electron Node 上时，stdio MCP 的 `node` / `npm` / `npx` 在用户机器没装 Node 时                            |
| [oauth-credentials.ts](oauth-credentials.ts)           | \* canonical credential pair。                                                                                               |
| [oauth-errors.ts](oauth-errors.ts)                     | \* 用 `Symbol.for` 注册到全局 symbol registry：bundler 双装或版本偏斜导致同进程存在两份                                      |
| [oauth-interactive.ts](oauth-interactive.ts)           | 授权事务的全局寿命。与 caller 等待预算（session 15s）无关，由 caller 侧独立收口。                                            |
| [oauth-lease.ts](oauth-lease.ts)                       | \* 授权 lease 的竞争等待预算。                                                                                               |
| [oauth-provider.ts](oauth-provider.ts)                 | \* Phase 1 运行期 AuthProvider。                                                                                             |
| [oauth-refresh.ts](oauth-refresh.ts)                   | \* refresh 锁的获取预算。                                                                                                    |
| [oauth-shared.ts](oauth-shared.ts)                     | discovery metadata 缓存寿命。过期后重新发现，避免长期使用换过端点的旧 AS metadata。                                          |
| [oauth.ts](oauth.ts)                                   | 实现或公开接口：McpOAuthRuntimeOptions、McpOAuthSession、createMcpAuthorizationCodeOAuthSession、createCredentialKeyPrefix。 |
| [official-auth.ts](official-auth.ts)                   | 官方 Server MCP 的逐请求动态身份头注入与失败分类。                                                                           |
| [pool.ts](pool.ts)                                     | 同一 entry 的并发存活校验共享一次探测，避免重复 ping / 重复重连。                                                            |
| [process-tree.ts](process-tree.ts)                     | 实现或公开接口：McpStdioProcessTreeTerminatorOptions、terminateMcpStdioProcessTree。                                         |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                                                             |
| [resource-subscriptions.ts](resource-subscriptions.ts) | \* MCP 资源订阅登记表（纯内存，无 IO）。                                                                                     |
| [resource-telemetry.ts](resource-telemetry.ts)         | 探针 await 期间重启或注销的旧实例不能贡献资源或修改 tracker。                                                                |
| [stdio-transport.ts](stdio-transport.ts)               | \* 官方 stdio MCP 的逐消息身份载荷提供器。它作为 spawn 参数的非执行字段保留，确保 SDK                                        |
| [telemetry.ts](telemetry.ts)                           | \* 资源管理器用的 MCP 子进程视图：只回 pid 与归属，不含任何采样值。                                                          |
| [timeout.ts](timeout.ts)                               | \* 只限制当前 waiter，不取消传入的共享 promise。底层任务是否取消由自己的 owner signal 决定。                                 |
| [windows-job-object.ts](windows-job-object.ts)         | 原生句柄关闭失败也不能阻断既有 taskkill 回退。                                                                               |

<!-- qingqi-directory-index:end -->
