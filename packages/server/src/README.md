# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server 基础工程中的 src 实现源码。

### 子目录

| 目录                                      | 存放内容                                            |
| ----------------------------------------- | --------------------------------------------------- |
| [remote/](remote/README.md)               | @zcode/server 基础工程中的 remote 实现源码。        |
| [source-server/](source-server/README.md) | @zcode/server 基础工程中的 source server 实现源码。 |

### 文件

| 文件                                                                         | 简要说明                                                                |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [bundledZCodeBuiltinProviderConfig.ts](bundledZCodeBuiltinProviderConfig.ts) | 返回构建时嵌入远端 Server 的 ZCode Built-in Provider Config。           |
| [entry-http.ts](entry-http.ts)                                               | entry-http 的实现文件。                                                 |
| [entry-stdio.ts](entry-stdio.ts)                                             | In stdio mode, all logging goes to stderr                               |
| [hostCapability.ts](hostCapability.ts)                                       | 短期、一次性 desktop host capability；只在 HTTP server 进程内存中存在。 |
| [http.ts](http.ts)                                                           | 用日志中间件包装，统一记录所有 RPC 调用                                 |
| [index.ts](index.ts)                                                         | index 的实现文件。                                                      |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                        |
| [stdio-lifecycle.ts](stdio-lifecycle.ts)                                     | timer 不能 unref，否则外部 Promise 永久 pending 时它无法独立保证收口。  |
| [stdio.ts](stdio.ts)                                                         | \* Wrap process.stdin/stdout as an ISocket for RPC communication.       |
| [stdioDeviceMid.ts](stdioDeviceMid.ts)                                       | 仅测试注入；生产固定使用 services 的 ensureTelemetryDeviceMid。         |
| [stdioServices.ts](stdioServices.ts)                                         | 旧 stdio 入口也必须在发布 ready 前验证存储，不能在同步到一半时才失败。  |

<!-- qingqi-directory-index:end -->
