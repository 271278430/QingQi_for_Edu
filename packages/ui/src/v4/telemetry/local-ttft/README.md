# local-ttft

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 local ttft 实现源码。

### 文件

| 文件                                         | 简要说明                                                                      |
| -------------------------------------------- | ----------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)   | 桌面本地观测默认不进入云端出口。                                              |
| [CONTRACT.md](CONTRACT.md)                   | 模块职责、公共接口、依赖方向和状态约定。                                      |
| [contract.ts](contract.ts)                   | Renderer 独占发送与渲染时钟；调用方只报告实际边界。                           |
| [localTtftFacts.ts](localTtftFacts.ts)       | 累计事实只填空，不让重传的早期快照擦掉已知边界；请求 ID 随 attempt 单独保留。 |
| [localTtftObserver.ts](localTtftObserver.ts) | Renderer 独占点击总时钟；不使用 ACK 或旁路 telemetry 判定首输出。             |
| [localTtftRecord.ts](localTtftRecord.ts)     | 实现或公开接口：LocalTtftPending、buildLocalTtftRecord。                      |
| [module.ts](module.ts)                       | \* local-ttft-renderer 模块清单（architecture-governance managed 模块）。     |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                              |

<!-- qingqi-directory-index:end -->
