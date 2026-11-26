# BotsDialog

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 BotsDialog 实现源码。

### 文件

| 文件                                                 | 简要说明                                                                                            |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [BotSummaryCard.tsx](BotSummaryCard.tsx)             | 修复原因：连接失败会直接阻断 /bind，不能再用“未绑定”覆盖真正的阻塞状态。                            |
| [BoundGroupsCard.tsx](BoundGroupsCard.tsx)           | 实现或公开接口：BoundGroupsList、BoundGroupsCard。                                                  |
| [PrivateDeliveryRetry.tsx](PrivateDeliveryRetry.tsx) | 实现或公开接口：PrivateDeliveryRetry。                                                              |
| [ProviderSettingsCard.tsx](ProviderSettingsCard.tsx) | 实现或公开接口：ProviderSettingsCard。                                                              |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                                    |
| [shared.tsx](shared.tsx)                             | 实现或公开接口：BindCodeState、FeishuRegistrationState、WeixinRegistrationState、BIND_CODE_TTL_MS。 |
| [WorkspaceAccessCard.tsx](WorkspaceAccessCard.tsx)   | 实现或公开接口：WorkspaceAccessCard。                                                               |

<!-- qingqi-directory-index:end -->
