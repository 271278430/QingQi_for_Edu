# providers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 providers 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                                                                |
| ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| [bigmodelSubscriptionProvider.ts](bigmodelSubscriptionProvider.ts) | 实现或公开接口：fetchBigModelSubscriptionSummary。                                                                                      |
| [bigmodelUsageMonitorMapper.ts](bigmodelUsageMonitorMapper.ts)     | 把 BigModel monitor 接口数据(model-usage / tool-usage)转成 ZCode 内部统一                                                               |
| [bigmodelUsageMonitorRange.ts](bigmodelUsageMonitorRange.ts)       | 实现或公开接口：resolveUsageTimeRange、resolveCodingPlanUsageTimeRange。                                                                |
| [bigmodelUsageQuotaMapper.ts](bigmodelUsageQuotaMapper.ts)         | 实现或公开接口：BigModelSubscriptionListEnvelope、BigModelSubscriptionListItem、BigModelUsageQuotaEnvelope、BigModelUsageQuotaPayload。 |
| [bigmodelUsageQuotaProvider.ts](bigmodelUsageQuotaProvider.ts)     | 实现或公开接口：UsageApiAuthorizationRequest、UsageApiAuthorization、BigModelUsageQuotaProvider。                                       |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                                                        |
| [zcodeMcpQuotaProvider.ts](zcodeMcpQuotaProvider.ts)               | ZCode 官方 Server MCP 的调用额度读取（`GET /api/v1/mcp/usage`）。                                                                       |

<!-- qingqi-directory-index:end -->
