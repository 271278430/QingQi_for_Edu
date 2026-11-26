# coding-plan-subscription

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 coding plan subscription 实现源码。

### 文件

| 文件                                                                                   | 简要说明                                                                                    |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [bigmodelCodingPlanSubscriptionProvider.ts](bigmodelCodingPlanSubscriptionProvider.ts) | 合并时曾丢失秒到毫秒的边界转换，导致客户端用本机时间误判待生效权益。                        |
| [codingPlanSubscription.ts](codingPlanSubscription.ts)                                 | mock 演示强制通道：真实路径不下发，UI 使用 Host 的 Account support。                        |
| [codingPlanSubscriptionService.ts](codingPlanSubscriptionService.ts)                   | \* 用户在设置里选的动态工作流模式（launch.md「The user's choice」）。只有拥有设置权威的装配 |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                                                            |
| [zaiCodingPlanSubscriptionProvider.ts](zaiCodingPlanSubscriptionProvider.ts)           | \* ZaiCodingPlanSubscriptionProvider                                                        |

<!-- qingqi-directory-index:end -->
