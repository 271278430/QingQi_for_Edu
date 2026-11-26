# fixtures

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 fixtures 测试夹具与样例。

### 文件

| 文件                                                                                 | 简要说明                                                                                                  |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------- |
| [bash-direct-probe.cjs](bash-direct-probe.cjs)                                       | 实际 adapter 的跨平台验证：node bash-direct-probe.cjs <bundled-adapter.cjs> [report.json]                 |
| [bash-output-benchmark.cjs](bash-output-benchmark.cjs)                               | node --expose-gc bash-output-benchmark.cjs <adapter.cjs> <concurrency:1\\                                 | 4> [bash\\ | cmd] [expectedArtifactBytes:default=256MiB] |
| [bash-windows-flags-probe.cjs](bash-windows-flags-probe.cjs)                         | Windows 负对照：node bash-windows-flags-probe.cjs；不依赖 adapter，保留旧 append 故障证据。               |
| [credential-recovery-reader.ts](credential-recovery-reader.ts)                       | credential-recovery-reader 的实现文件。                                                                   |
| [mcp-oauth-child-driver.ts](mcp-oauth-child-driver.ts)                               | \* 跨进程 E2E 的子进程驱动。                                                                              |
| [provider-builtin-analyze-image-mcp.sse](provider-builtin-analyze-image-mcp.sse)     | provider-builtin-analyze-image-mcp 模块的资源或工程文件。                                                 |
| [provider-builtin-analyze-image.sse](provider-builtin-analyze-image.sse)             | provider-builtin-analyze-image 模块的资源或工程文件。                                                     |
| [provider-migration-unrelated-tables.ts](provider-migration-unrelated-tables.ts)     | 独立于新版 Repo 写入，播种合法原始行；迁移不得改变这些表的任一列。                                        |
| [README.md](README.md)                                                               | 本目录用途、子目录与逐文件说明。                                                                          |
| [session-migration-crash-process.ts](session-migration-crash-process.ts)             | 持续连接 IPC 让父进程在真实事务边界终止此子进程。                                                         |
| [session-store-concurrent-process.ts](session-store-concurrent-process.ts)           | session-store-concurrent-process 的实现文件。                                                             |
| [session-transaction-process.ts](session-transaction-process.ts)                     | session-transaction-process 的实现文件。                                                                  |
| [session-transaction-race.ts](session-transaction-race.ts)                           | 不在这些调用之间 await：旧实现会在 fork 内部让出执行，使其他会话加入同一事务。                            |
| [shared-credentials-concurrent-process.ts](shared-credentials-concurrent-process.ts) | shared-credentials-concurrent-process 的实现文件。                                                        |
| [staging-backup-model-readers.mjs](staging-backup-model-readers.mjs)                 | 冻结旧版实际 Reader（esbuild 移除类型/打包实际调用依赖），来源 790884b1ce4b990583ab40625b5f283e2169eb36。 |
| [streaming-migration-backup-process.ts](streaming-migration-backup-process.ts)       | streaming-migration-backup-process 的实现文件。                                                           |

<!-- qingqi-directory-index:end -->
