# server

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/stream-animate 基础工程中的 server 实现源码。

### 文件

| 文件                                   | 简要说明                                                            |
| -------------------------------------- | ------------------------------------------------------------------- |
| [cli.ts](cli.ts)                       | cli 的实现文件。                                                    |
| [dataStore.ts](dataStore.ts)           | 实现或公开接口：DATA_DIR_NAME、createRunId、getDataDir、getRunDir。 |
| [deepseekRunner.ts](deepseekRunner.ts) | 实现或公开接口：executeDeepseekRun。                                |
| [frameBuckets.ts](frameBuckets.ts)     | 实现或公开接口：TimedCharEvent、buildFrameScenario。                |
| [frameForecast.ts](frameForecast.ts)   | 实现或公开接口：buildFrameForecast。                                |
| [http.ts](http.ts)                     | 实现或公开接口：startStreamAnimateServer、getPackageRoot。          |
| [index.ts](index.ts)                   | index 的实现文件。                                                  |
| [README.md](README.md)                 | 本目录用途、子目录与逐文件说明。                                    |

<!-- qingqi-directory-index:end -->
