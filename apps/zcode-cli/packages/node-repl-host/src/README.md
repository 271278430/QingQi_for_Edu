# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/node-repl-host 基础工程中的 src 实现源码。

### 子目录

| 目录                                  | 存放内容                                                  |
| ------------------------------------- | --------------------------------------------------------- |
| [call-ledger/](call-ledger/README.md) | @zcode/node-repl-host 基础工程中的 call ledger 实现源码。 |

### 文件

| 文件                                         | 简要说明                                                                                                          |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [browser-bridge.ts](browser-bridge.ts)       | 只加载 broker 协议；shared 总入口会在每个 Worker 中初始化无关领域的 schema。                                      |
| [cua-bridge.ts](cua-bridge.ts)               | Worker 连 CUA broker 用的地址和本次调用的 token（由主线程账本签发）。                                             |
| [cua-broker.ts](cua-broker.ts)               | 只有地址；token 每次调用由账本签发（20-node-repl-call-ledger.md「账本与 token」）。                               |
| [no-progress-guard.ts](no-progress-guard.ts) | js 永不因「没有进展」而失败，弱模型会在一个 turn 内反复调用直到额度耗尽；core 的重复调用提醒按完整                |
| [process-lifecycle.ts](process-lifecycle.ts) | \* REPL cell 的同步错误由 NodeReplSession 兜底，但 fire-and-forget 的异步错误                                     |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                                                                  |
| [result.ts](result.ts)                       | \* 一个 cell 里多次带截图的观察，只把**最后一张** raster 交给模型。                                               |
| [runtime-bridge.ts](runtime-bridge.ts)       | 实现或公开接口：NODE_REPL_BROWSER_BRIDGE_SYMBOL、NodeReplBrowserRuntimeBridge、readNodeReplBrowserRuntimeBridge。 |
| [server.ts](server.ts)                       | 值导入必须走 @zcode/core/repl 这条深路径：barrel 会把 core 的整张图拖进 bundle                                    |
| [tool-contract.ts](tool-contract.ts)         | 旧默认值与模型常用的 30 秒页面等待相同，发送等副作用成功后会在结果读取前被中止。                                  |

<!-- qingqi-directory-index:end -->
