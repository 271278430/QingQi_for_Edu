# telemetry

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/contracts 基础工程中的 telemetry 实现源码。

### 文件

| 文件                                     | 简要说明                                                                    |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| [agent-execution.ts](agent-execution.ts) | \* 可跨异步/进程边界保存的因果引用。SpanContext 字段保持 OTel 原义；        |
| [index.ts](index.ts)                     | 调用点只声明用户/业务请求的 reasoning 意图，Provider Adapter 决定最终事实。 |
| [README.md](README.md)                   | 本目录用途、子目录与逐文件说明。                                            |

<!-- qingqi-directory-index:end -->
