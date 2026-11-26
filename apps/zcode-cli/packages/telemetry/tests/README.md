# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/telemetry 基础工程中的 tests 验收与回归场景。

### 文件

| 文件                                                             | 简要说明                                                           |
| ---------------------------------------------------------------- | ------------------------------------------------------------------ |
| [agent-metrics.test.ts](agent-metrics.test.ts)                   | agent-metrics.test 的实现文件。                                    |
| [agent-trace-runtime.test.ts](agent-trace-runtime.test.ts)       | agent-trace-runtime.test 的实现文件。                              |
| [bootstrap.test.ts](bootstrap.test.ts)                           | bootstrap.test 的实现文件。                                        |
| [compatibility-adapters.test.ts](compatibility-adapters.test.ts) | compatibility-adapters.test 的实现文件。                           |
| [error-sanitizer.test.ts](error-sanitizer.test.ts)               | error-sanitizer.test 的实现文件。                                  |
| [model-api-recorder.test.ts](model-api-recorder.test.ts)         | model-api-recorder.test 的实现文件。                               |
| [otlp-cost-controls.test.ts](otlp-cost-controls.test.ts)         | otlp-cost-controls.test 的实现文件。                               |
| [otlp-integration.test.ts](otlp-integration.test.ts)             | 集成测试需要稳定拿到完整 Trace；生产默认采样率由独立配置测试覆盖。 |
| [provider-endpoint.test.ts](provider-endpoint.test.ts)           | provider-endpoint.test 的实现文件。                                |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                   |

<!-- qingqi-directory-index:end -->
