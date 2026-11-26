# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 src 实现源码。

### 子目录

| 目录                                                              | 存放内容                                                           |
| ----------------------------------------------------------------- | ------------------------------------------------------------------ |
| [active-transcript/](active-transcript/README.md)                 | @zcode/bootstrap 基础工程中的 active transcript 实现源码。         |
| [app/](app/README.md)                                             | @zcode/bootstrap 基础工程中的 app 实现源码。                       |
| [cli-session-control/](cli-session-control/README.md)             | @zcode/bootstrap 基础工程中的 cli session control 实现源码。       |
| [lib/](lib/README.md)                                             | @zcode/bootstrap 基础工程中的 lib 实现源码。                       |
| [official-command-endpoint/](official-command-endpoint/README.md) | @zcode/bootstrap 基础工程中的 official command endpoint 实现源码。 |
| [plugin-discovery/](plugin-discovery/README.md)                   | @zcode/bootstrap 基础工程中的 plugin discovery 实现源码。          |
| [plugin-startup-budget/](plugin-startup-budget/README.md)         | @zcode/bootstrap 基础工程中的 plugin startup budget 实现源码。     |
| [runtime-subagents/](runtime-subagents/README.md)                 | @zcode/bootstrap 基础工程中的 runtime subagents 实现源码。         |
| [session-control/](session-control/README.md)                     | @zcode/bootstrap 基础工程中的 session control 实现源码。           |
| [session-execution/](session-execution/README.md)                 | @zcode/bootstrap 基础工程中的 session execution 实现源码。         |
| [session-lifecycle/](session-lifecycle/README.md)                 | @zcode/bootstrap 基础工程中的 session lifecycle 实现源码。         |
| [workspace-mcp-trust/](workspace-mcp-trust/README.md)             | @zcode/bootstrap 基础工程中的 workspace mcp trust 实现源码。       |
| [zcode-protocol/](zcode-protocol/README.md)                       | @zcode/bootstrap 基础工程中的 zcode protocol 实现源码。            |
| [zcode-protocol-v4/](zcode-protocol-v4/README.md)                 | @zcode/bootstrap 基础工程中的 zcode protocol v4 实现源码。         |

### 文件

| 文件                                                                                       | 简要说明                                                                                                                                  |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [auth-login-abort.ts](auth-login-abort.ts)                                                 | Stop awaiting cancelled I/O even when an injected transport ignores its signal.                                                           |
| [auth-login-contract.ts](auth-login-contract.ts)                                           | BigModel 与 Z.ai 共用服务端轮询登录，只是 providerId 固定为 bigmodel。                                                                    |
| [auth-login-polling.ts](auth-login-polling.ts)                                             | Match App polling: transient network and server failures retry at the server interval.                                                    |
| [auth-login.ts](auth-login.ts)                                                             | \* Z.ai 与 BigModel 共用服务端轮询登录：init 拿授权地址，浏览器授权后轮询到 ready，                                                       |
| [builtin-prompt-command.ts](builtin-prompt-command.ts)                                     | \* 动态工作流灰度门（docs/dynamic-workflow/launch.md「Gray release」）。\*\*只有显式 false 才挡下                                         |
| [builtin-workflow-command.ts](builtin-workflow-command.ts)                                 | \* 内置 `/workflow` 命令（docs/dynamic-workflow/authoring.md「The `/workflow` command and the skill」）。                                 |
| [custom-command-prompt.ts](custom-command-prompt.ts)                                       | 保留名（含内置 `workflow`）在这里直接返回 undefined，与「命令不存在」同形：内置命令由                                                     |
| [custom-commands.ts](custom-commands.ts)                                                   | 实现或公开接口：ListZCodeCustomCommandsOptions、InspectZCodeCustomCommandOptions、ZCodeCustomCommandInspection、listZCodeCustomCommands。 |
| [index.ts](index.ts)                                                                       | Bootstrap public API surface.                                                                                                             |
| [log-retention.ts](log-retention.ts)                                                       | 实现或公开接口：scheduleStartupLogRetentionCleanup。                                                                                      |
| [mcp-config.ts](mcp-config.ts)                                                             | 保留环境变量名供旧诊断脚本读取；迁移后的配置路径不会据此启动独立 CUA MCP。                                                                |
| [model-config.ts](model-config.ts)                                                         | \* X-Client-Language 优先取 Desktop spawn 时下发的界面语言（ZCODE_CLIENT_LANGUAGE）。                                                     |
| [model-factory.ts](model-factory.ts)                                                       | Model factory - creates model adapter with config                                                                                         |
| [permission-options.ts](permission-options.ts)                                             | 普通交互 permission 的用户拒绝需要明确告知模型工具未执行，                                                                                |
| [plugin-secrets.ts](plugin-secrets.ts)                                                     | 敏感插件选项：读取时按配置层叠加私有文件，保存、重置、卸载时维护私有文件。                                                                |
| [plugins.ts](plugins.ts)                                                                   | 所有写入入口（包括独立 CLI）共用此边界。组合操作显式传递当次锁，避免递归等待。                                                            |
| [process-resource-sampler.ts](process-resource-sampler.ts)                                 | 采样周期与 app 侧聚合共用 shared 的同一个常量，避免两侧节拍各自漂移。                                                                     |
| [provider-endpoint-routing-source-headers.ts](provider-endpoint-routing-source-headers.ts) | 与模型请求同一取值规则：先认 Desktop 下发的界面语言，再回落 Intl。                                                                        |
| [provider-endpoint-routing.ts](provider-endpoint-routing.ts)                               | App-managed CLI 必须采用宿主凭据端口；不能与 standalone 的本地 Store 混用缓存。                                                           |
| [README.md](README.md)                                                                     | 本目录用途、子目录与逐文件说明。                                                                                                          |
| [runtime-platform-headers.ts](runtime-platform-headers.ts)                                 | 实现或公开接口：createRuntimePlatformHeaders、normalizePrintableHeaderValue。                                                             |
| [session-transcript.ts](session-transcript.ts)                                             | goal continuation 等 runtime 内部输入需要保留在 raw history 供模型恢复，                                                                  |
| [sessions.ts](sessions.ts)                                                                 | 实现或公开接口：resolveLatestSession、listZCodeSessions。                                                                                 |
| [skill-command-overrides.ts](skill-command-overrides.ts)                                   | 实现或公开接口：EnableOverride、collectDisabledPaths。                                                                                    |
| [skills.ts](skills.ts)                                                                     | 协议宿主草稿目录使用；CLI 命令缺省关闭。                                                                                                  |
| [slash-command-surface.ts](slash-command-surface.ts)                                       | \* App `/` 面板与加号菜单按本顺序展示（UI 不维护排序白名单）。`workflow` 紧随 `goal`：两者都是                                            |
| [startup-logging.ts](startup-logging.ts)                                                   | 实现或公开接口：StartupTimer、startupNow。                                                                                                |
| [subagents.ts](subagents.ts)                                                               | 来自已完成存储迁移的启动快照；不在插件 loader 另读磁盘或查询账号。                                                                        |
| [telemetry-bootstrap.ts](telemetry-bootstrap.ts)                                           | \* 官方 CLI 异步入口在创建同步 App 之前调用；只把准备出的 device MID 放回业务 env，                                                       |
| [tool-call-product-visibility.ts](tool-call-product-visibility.ts)                         | \* 空工具名恢复只服务于模型 continuation，不应物化为用户可见工具行。                                                                      |
| [workspace-hook-trust-cli.ts](workspace-hook-trust-cli.ts)                                 | 解析受管 worktree 的数据根目录（ZCODE_DATA_BASE_DIR）；缺省 process.env。                                                                 |
| [zcode-protocol-entrypoint.ts](zcode-protocol-entrypoint.ts)                               | \* 进程级 Registry 已就绪后，它就是当前 Environment 的模型事实源。                                                                        |

<!-- qingqi-directory-index:end -->
