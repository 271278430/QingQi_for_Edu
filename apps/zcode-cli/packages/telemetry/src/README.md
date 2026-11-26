# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/telemetry 基础工程中的 src 实现源码。

### 子目录

| 目录                                                            | 存放内容                                                          |
| --------------------------------------------------------------- | ----------------------------------------------------------------- |
| [request-security-edition/](request-security-edition/README.md) | @zcode/telemetry 基础工程中的 request security edition 实现源码。 |

### 文件

| 文件                                                           | 简要说明                                                                                                       |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [agent-metrics.ts](agent-metrics.ts)                           | \* Metric 只接收已归一化、低基数的标签。高基数执行 ID 和原始业务内容只属于 Trace，                             |
| [agent-trace-runtime.ts](agent-trace-runtime.ts)               | 实现或公开接口：AgentTraceRuntimeOptions、AgentExecutionTelemetryRuntime、NoopAgentExecutionTelemetry。        |
| [agent-trace-support.ts](agent-trace-support.ts)               | Bug 根因：观测 Context Manager 理论上不应在业务返回后抛错；若第三方实现违反                                    |
| [bootstrap.ts](bootstrap.ts)                                   | 显式注入优先，Endpoint 永远不能覆盖宿主提供的进程级 Owner。                                                    |
| [compatibility-adapters.ts](compatibility-adapters.ts)         | _ 外部语义约定只在这里投影。`zcode._` 始终是内部查询的权威字段；                                               |
| [error-sanitizer.ts](error-sanitizer.ts)                       | 修复原因：链包含输入本身；没有独立嵌套对象时不能把同一个错误重复登记为 cause。                                 |
| [index.ts](index.ts)                                           | index 的实现文件。                                                                                             |
| [model-api-recorder.ts](model-api-recorder.ts)                 | \* 把 Transport 的实时事实直接写入仍然活动的 Model Call/Attempt Span。                                         |
| [otlp-exporter.ts](otlp-exporter.ts)                           | \* 该模块只由异步 Bootstrap 在 Telemetry 确认启用后动态加载。不要从公共入口静态导入，                          |
| [provider-endpoint.ts](provider-endpoint.ts)                   | 实现或公开接口：PROVIDER_ENDPOINT_SANITIZER_VERSION、ProviderEndpointIdentityCache、sanitizeProviderEndpoint。 |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                               |
| [request-observation-target.ts](request-observation-target.ts) | 实现或公开接口：RequestObservationTarget。                                                                     |

<!-- qingqi-directory-index:end -->
