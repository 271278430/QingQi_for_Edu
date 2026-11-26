# api

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 api 实现源码。

### 文件

| 文件                                                   | 简要说明                                                                                 |
| ------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| [apiEndpoints.ts](apiEndpoints.ts)                     | 实现或公开接口：ZCODE_CLIENT_SCENES_URL、ZAI_API_HOST。                                  |
| [apiJson.ts](apiJson.ts)                               | 实现或公开接口：readApiJson。                                                            |
| [apiKeyHeaders.ts](apiKeyHeaders.ts)                   | 用户复制 API key 时可能把中文备注一并粘进输入框。                                        |
| [index.ts](index.ts)                                   | index 的实现文件。                                                                       |
| [networkErrorClassifier.ts](networkErrorClassifier.ts) | feedback 与模型连通性曾分别维护错误码列表，导致 Undici 建连超时只在部分链路被识别。      |
| [nodeApiClient.ts](nodeApiClient.ts)                   | 仅返回已核实当前关联业务请求的刷新闭包；调用不得重放原业务请求。                         |
| [nodeApiNetwork.ts](nodeApiNetwork.ts)                 | 本次连接是否经 HTTP 代理（来自与 fetch 相同的选路结果）                                  |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                         |
| [requestIdHeaders.ts](requestIdHeaders.ts)             | 实现或公开接口：REQUEST_ID_HEADER_NAME、withRequestIdHeader、withRequestIdHeaderRecord。 |

<!-- qingqi-directory-index:end -->
