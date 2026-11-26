# tracing

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/contracts 基础工程中的 tracing 实现源码。

### 文件

| 文件                                                   | 简要说明                                                                        |
| ------------------------------------------------------ | ------------------------------------------------------------------------------- |
| [local-turn-preparation.ts](local-turn-preparation.ts) | 仅保存观察回调，不保存业务输入或阶段事实；CLI recorder 独占事实与订阅生命周期。 |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                |
| [tracer.ts](tracer.ts)                                 | Tracing - Trace context propagation                                             |

<!-- qingqi-directory-index:end -->
