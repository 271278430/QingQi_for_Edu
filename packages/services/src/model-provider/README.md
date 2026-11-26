# model-provider

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 model provider 实现源码。

### 文件

| 文件                                                                               | 简要说明                                                                                          |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [accountProjectTokenClient.ts](accountProjectTokenClient.ts)                       | 本地与旧远程附加入口采用同一 HTTP/ID 存储约束，每个鉴权 owner 只持有一个实例。                    |
| [accountProviderApiClient.ts](accountProviderApiClient.ts)                         | BigModel 部分业务接口成功时返回 code=200，而不是 code=0。                                         |
| [accountProviderApiKeyResolver.ts](accountProviderApiKeyResolver.ts)               | Team Plan 项目会和个人项目一起返回；个人 Key 只能从非团队项目解析。                               |
| [accountProviderApiTypes.ts](accountProviderApiTypes.ts)                           | 实现或公开接口：AccountApiProviderId、RemoteEnvelope、RemoteProjectInfo、RemoteOrganizationInfo。 |
| [accountProviderConnectionResolver.ts](accountProviderConnectionResolver.ts)       | Host 旧连接导入尚不能确定身份；仅运行时事实，不写入配置或协议。                                   |
| [accountProviderCredentialKey.ts](accountProviderCredentialKey.ts)                 | \* Credential Store 的私有物理 key。                                                              |
| [accountProviderCredentialService.ts](accountProviderCredentialService.ts)         | 旧方法名兼容私有调用契约；返回值现在是请求期 Token，绝不读写长期 Key 缓存。                       |
| [accountProviderCredentialStore.ts](accountProviderCredentialStore.ts)             | \* 保存 Account Provider 的请求期凭据。                                                           |
| [accountProviderInvalidation.ts](accountProviderInvalidation.ts)                   | \* 把会改变账号连接选择的 Settings 变化收敛为 AccountProviderService 刷新。                       |
| [accountProviderRequestAuthService.ts](accountProviderRequestAuthService.ts)       | 私有传输字段兼容旧命名；套餐 OAuth 实际传入短期 Project Token。                                   |
| [accountProviderTeamPlanRequestKey.ts](accountProviderTeamPlanRequestKey.ts)       | BigModel /api/biz 只接受登录 access token，不能使用旧版本误存的 ZCode JWT。                       |
| [accountRequestAuthService.ts](accountRequestAuthService.ts)                       | \* 请求期 Account 鉴权边界。                                                                      |
| [bigmodelStartPlanZcodeJwt.ts](bigmodelStartPlanZcodeJwt.ts)                       | zcode JWT 必须在 BigModel OAuth callback 阶段用授权码 body 落盘。                                 |
| [codingPlanProviderAvailability.ts](codingPlanProviderAvailability.ts)             | ZAI 测试环境业务 token 只能请求配置的 ZAI Business origin。                                       |
| [legacyModelProviderSerialized.ts](legacyModelProviderSerialized.ts)               | \* 各 ZCode Agent Provider 的模型槽位映射（按 provider 区分）。                                   |
| [legacyPersonalProviderConfigImporter.ts](legacyPersonalProviderConfigImporter.ts) | \* 从旧 Effective Store 中只提取仍能确认的 Personal 用户意图。                                    |
| [legacyTeamOrganizationResolver.ts](legacyTeamOrganizationResolver.ts)             | 仅供旧连接导入：只读 OAuth 用户信息，不依赖当前 Provider，也不申请团队 Key。退役旧版后删除。      |
| [legacyZCodeConfigProviderReader.ts](legacyZCodeConfigProviderReader.ts)           | 旧配置可能保存生产域名；测试环境的 Team Plan Key 无法调用生产网关。                               |
| [offPeakModelSelectionView.ts](offPeakModelSelectionView.ts)                       | Off-Peak 只投影固定隐藏 Provider，不向普通用户选择面开放隐藏候选。                                |
| [providerConfigRuntime.ts](providerConfigRuntime.ts)                               | \* Services 装配层：提供 App 配置目录和已发布旧配置的一次性迁移入口。                             |
| [providerFacadeServices.ts](providerFacadeServices.ts)                             | 测试已经保存并进入目标 Environment Registry 的正式 Model。                                        |
| [providerProvisioning.ts](providerProvisioning.ts)                                 | 仅供 Window Host 调用的远端 Environment target，不加入 IServiceAccessor。                         |
| [providerProvisioningSource.ts](providerProvisioningSource.ts)                     | v3 的 OAuth 会话组；旧信封不允许声明新增字段。                                                    |
| [providerProvisioningTarget.ts](providerProvisioningTarget.ts)                     | 运行在目标 Environment 内的 Provisioning target；负责写正式 Store 并在失败时回滚。                |
| [providerRuntime.ts](providerRuntime.ts)                                           | \* 普通 API Provider 可以在账号能力尚未装配时独立运行。                                           |
| [providerSettingsConnectivity.ts](providerSettingsConnectivity.ts)                 | \* 设置页只负责把已经落盘并进入 Registry 的 ModelSelection 交给目标 Environment。                 |
| [README.md](README.md)                                                             | 本目录用途、子目录与逐文件说明。                                                                  |
| [zaiStartPlanBilling.ts](zaiStartPlanBilling.ts)                                   | user_plan_id 标识用户套餐实例；额度提醒用它关联同一实例的 entitlement 周期类型。                  |
| [zcodeBuiltinRemoteConfig.ts](zcodeBuiltinRemoteConfig.ts)                         | Services 仅注入既有网络装配；URL、预算与 Release 校验由 provider-node 唯一实现。                  |

<!-- qingqi-directory-index:end -->
