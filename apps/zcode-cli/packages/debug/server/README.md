# server

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

debug 基础工程中的 server 模块文件。

### 文件

| 文件                                           | 简要说明                                                                                                                      |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [analyzer.ts](analyzer.ts)                     | 实现或公开接口：listTraces、inspectTrace。                                                                                    |
| [index.ts](index.ts)                           | 实现或公开接口：createDebugApp、startDebugServer。                                                                            |
| [network-capture.ts](network-capture.ts)       | 实现或公开接口：NetworkCaptureService、disabledNetworkCaptureStatus、createNetworkCaptureServiceFromEnv、extractAttribution。 |
| [observation-events.ts](observation-events.ts) | 实现或公开接口：createObservationEventStream、fingerprintObservationSources。                                                 |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                                                              |
| [sources.ts](sources.ts)                       | 实现或公开接口：defaultLogDir、defaultDbPath、loadLogs、loadEventLog。                                                        |
| [types.ts](types.ts)                           | 实现或公开接口：ObservationOptions、JsonRecord、SourceLoadResult、LogRecord。                                                 |

<!-- qingqi-directory-index:end -->
