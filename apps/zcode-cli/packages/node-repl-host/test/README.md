# test

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/node-repl-host 基础工程中的 test 测试场景。

### 子目录

| 目录                                  | 存放内容                                                  |
| ------------------------------------- | --------------------------------------------------------- |
| [call-ledger/](call-ledger/README.md) | @zcode/node-repl-host 基础工程中的 call ledger 测试场景。 |

### 文件

| 文件                                                                   | 简要说明                                                                              |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [bundle-boundary.test.ts](bundle-boundary.test.ts)                     | 这份依赖边界守卫原先长在 browser-use-plugin/test/bundle-boundary.test.ts 上（entry 是 |
| [bundle-smoke.test.ts](bundle-smoke.test.ts)                           | Bug 原因：node_repl 的 MCP server 是 CLI spawn 的独立 stdio 子进程，plugin host 通过  |
| [computer-use-onboarding.test.ts](computer-use-onboarding.test.ts)     | \* CUA 的输出策略：参考按需取用，宿主不主动推。                                       |
| [cua-bridge.test.ts](cua-bridge.test.ts)                               | broker 只认本次调用的 token，会话信息取自账本条目，目标应用身份记入条目的 facts       |
| [mcp-server-process-guards.test.ts](mcp-server-process-guards.test.ts) | mcp-server-process-guards.test 的实现文件。                                           |
| [mcp-server.test.ts](mcp-server.test.ts)                               | 主线程账本里记下的可信事实（20-node-repl-call-ledger.md「结果组装」）。               |
| [no-progress-guard.test.ts](no-progress-guard.test.ts)                 | no-progress-guard.test 的实现文件。                                                   |
| [README.md](README.md)                                                 | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
