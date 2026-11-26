# node

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 node 实现源码。

### 文件

| 文件                                                         | 简要说明                                                                      |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| [atomicFileLock.ts](atomicFileLock.ts)                       | 非有限、负数或明显未来的 createdAt 会让 ownerless 锁永久达不到 stale。        |
| [genUiPaths.ts](genUiPaths.ts)                               | Execution Host supplies this process-scoped root; models never choose it.     |
| [lockInstanceObserver.ts](lockInstanceObserver.ts)           | 双重非法时间戳只能从当前锁实例首次被看见时起算 grace。                        |
| [networkCapture.ts](networkCapture.ts)                       | MCP 的 HTTP/SSE/OAuth 共用此异步上下文，不影响原 fetch 的代理与证书策略。     |
| [nodeSelfResourceTelemetry.ts](nodeSelfResourceTelemetry.ts) | \* host 与 scheduler 两个 utilityProcess 自采 CPU / 内存的共用换算逻辑        |
| [officialPluginCache.ts](officialPluginCache.ts)             | 缓存目录名，即官方插件 name。                                                 |
| [privateFilePersistence.ts](privateFilePersistence.ts)       | 登录等跨请求流程保留最初代次，不能在迟到响应写入时重新领取新代次。            |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                              |
| [subagentMarkdownMigration.ts](subagentMarkdownMigration.ts) | 共享原子导入边界：JSON 的旧字段只在这里解释，完成落盘后 reader 只读当前字段。 |

<!-- qingqi-directory-index:end -->
