# model-provider-section

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 model provider section 实现源码。

### 文件

| 文件                                                                             | 简要说明                                                                                                                                                              |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [ApiKeyInput.tsx](ApiKeyInput.tsx)                                               | 实现或公开接口：ApiKeyInput。                                                                                                                                         |
| [BigModelRegistrationHint.tsx](BigModelRegistrationHint.tsx)                     | 实现或公开接口：BigModelRegistrationHint、isBigModelUnregisteredAuthError。                                                                                           |
| [codingPlanEmbeddedWebview.ts](codingPlanEmbeddedWebview.ts)                     | \* App locale（zh-CN / en-US）→ 官网 URL lang 段（cn / en）。                                                                                                         |
| [codingPlanEnterpriseTiers.ts](codingPlanEnterpriseTiers.ts)                     | 2026-09: 原生购买面板（CodingPlanPurchasePanel）整体下线，购买流程切换为内嵌官网                                                                                      |
| [codingPlanPricingCards.ts](codingPlanPricingCards.ts)                           | 死代码清理：原生购买组件 CodingPlanPricingCards 及其配套 resolver 已随                                                                                                |
| [codingPlanProductPresentation.ts](codingPlanProductPresentation.ts)             | 修复原因：套餐卡片的运营文案现在由静态配置的 description 控制；                                                                                                       |
| [codingPlanPurchaseAuth.ts](codingPlanPurchaseAuth.ts)                           | 实现或公开接口：CodingPlanPurchaseAuthStatus、isCodingPlanPurchaseAuthPending、readCodingPlanPurchaseTokenState、normalizeCodingPlanProviderId。                      |
| [CodingPlanStatusActions.tsx](CodingPlanStatusActions.tsx)                       | 购买/升级入口必须先打开面板，OAuth 失效恢复由面板在用户选择                                                                                                           |
| [CodingPlanStatusMeta.tsx](CodingPlanStatusMeta.tsx)                             | setTimeout 存在约 24.8 天上限；长排期分段唤醒，到点后再切换刷新按钮。                                                                                                 |
| [codingPlanStatusPanelViewState.ts](codingPlanStatusPanelViewState.ts)           | 这两个状态都来自已解析的 entitlement snapshot。后台刷新时继续展示                                                                                                     |
| [constants.ts](constants.ts)                                                     | 实现或公开接口：generateId、PRESET_SUBSCRIPTION_TIMEOUT_MS、BIGMODEL_REGISTRATION_URL、BIGMODEL_CODING_PLAN_PERSONAL_MANAGE_URL。                                     |
| [Detail.tsx](Detail.tsx)                                                         | 实现或公开接口：resolveTeamScopedPlanNavItem、resolveTeamPlanInspectionAccess、resolvePlanSettingsProvider、ModelProviderSectionDetail。                              |
| [enterpriseCodingPlanProducts.ts](enterpriseCodingPlanProducts.ts)               | \* 该企业套餐所属的 family（zai / bigmodel）。                                                                                                                        |
| [InlineEditableProviderCard.tsx](InlineEditableProviderCard.tsx)                 | 显式弹窗在原草稿中重试，不让外部通知另起一次脱离编辑事务的保存。                                                                                                      |
| [ModelConfigHelp.tsx](ModelConfigHelp.tsx)                                       | 帮助按钮必须是 label 的兄弟，避免抢走输入关联和标题点击焦点。                                                                                                         |
| [ModelEditorAdvanced.tsx](ModelEditorAdvanced.tsx)                               | 错误位置随布局变化：最大输出已在基础区；推理等级和映射必须展开才能修正。                                                                                              |
| [modelEditorControlStyle.ts](modelEditorControlStyle.ts)                         | 模型编辑器专用：边框仅标记覆盖，Hover/焦点用同一底色，不修改全站控件。                                                                                                |
| [modelProviderActions.ts](modelProviderActions.ts)                               | Model Provider 顶部刷新是账号权益刷新入口。                                                                                                                           |
| [Navigation.tsx](Navigation.tsx)                                                 | 侧栏会裁切水平溢出；排序只改变纵向位置，拖动时也必须保持 x=0。                                                                                                        |
| [oauthActions.ts](oauthActions.ts)                                               | 实现或公开接口：startPresetSubscriptionLogin、reportPresetSubscriptionSuccess。                                                                                       |
| [PresetProviderApiKeyBanner.tsx](PresetProviderApiKeyBanner.tsx)                 | 获取入口不区分个人／团队；两个按钮和专用字段会偏离单一控制台入口的预期。                                                                                              |
| [ProviderApiFormatSelect.tsx](ProviderApiFormatSelect.tsx)                       | 实现或公开接口：PROVIDER_CONNECTION_API_FORMATS、resolveProviderConnectionApiFormatOptions、resolveProviderConnectionApiFormatDisplayLabel、ProviderApiFormatSelect。 |
| [ProviderCardSections.tsx](ProviderCardSections.tsx)                             | 向Web教育产品公开原模型设置组件，共用同一实现及草稿契约。                                                                                                             |
| [ProviderDetailFeedback.tsx](ProviderDetailFeedback.tsx)                         | 连接测试成功使用语义绿；保存/删除沿用中性反馈，不按文案或 key 推断操作。                                                                                              |
| [ProviderDraftSave.ts](ProviderDraftSave.ts)                                     | 旧设置页曾把完整 Base URL 再作为 path 拼接；仅折叠两段完全相同的安全形态。                                                                                            |
| [providerFamilyConnectionVisibility.ts](providerFamilyConnectionVisibility.ts)   | \* 官方 Server MCP 额度（服务端下发的总额度）。它不在 quota.limits[] 里，只在有套餐快照的分支填充；                                                                   |
| [ProviderFamilyModeHeader.tsx](ProviderFamilyModeHeader.tsx)                     | Bug 原因：容器允许 flex-wrap 却固定 h-8，标题与连接方式在窄面板（手机 Web、桌面 480px 窗口）换行后，                                                                  |
| [ProviderFormControls.tsx](ProviderFormControls.tsx)                             | 外部 View 每次投影会产生新对象；编辑事务固定打开时的模型与 revision，不能跟随对象刷新重置。                                                                           |
| [ProviderLogo.tsx](ProviderLogo.tsx)                                             | 这里只负责把 Config 中的资源 key 解析为打包素材；禁止加入 Provider ID、名称或排序逻辑。                                                                               |
| [ProviderModelDraftState.ts](ProviderModelDraftState.ts)                         | 只投影未覆盖控件；Host 是推荐规则的唯一解析者，草稿不保存第二份可写 Effective Config。                                                                                |
| [ProviderModelMetadata.ts](ProviderModelMetadata.ts)                             | 仅在本次 Draft 从固定模式切回推荐模式时清空已有 Overlay。                                                                                                             |
| [ProviderModelMetadataDialog.tsx](ProviderModelMetadataDialog.tsx)               | 新增模型时模型 ID 为空，如果沿用编辑态的上下文窗口自动聚焦，会让用户先落到默认数值字段。                                                                              |
| [ProviderModelMetadataDialogActions.tsx](ProviderModelMetadataDialogActions.tsx) | 实现或公开接口：ModelConfigRestoreButton、ModelConfigDraftFeedback、ModelSmartConfigSwitch、ProviderModelMetadataDialogActions。                                      |
| [ProviderModelMetadataFields.tsx](ProviderModelMetadataFields.tsx)               | 外层按钮负责完整点击与键盘语义；指示框不可再嵌一个可聚焦控件。                                                                                                        |
| [ProviderModelModalityOptions.tsx](ProviderModelModalityOptions.tsx)             | PDF 已经是正式的模型输入事实和可执行附件能力，旧列表漏掉它后用户无法修正该事实。                                                                                      |
| [ProviderModelReasoningLevelEditor.tsx](ProviderModelReasoningLevelEditor.tsx)   | 打开后原样失焦不是用户覆盖；否则仅查看档位就会把整组写成个人配置。                                                                                                    |
| [ProviderModelSettingsGroups.tsx](ProviderModelSettingsGroups.tsx)               | 实现或公开接口：ModelSettingsGroup、ProviderModelReasoningSettings。                                                                                                  |
| [ProviderStatusIndicator.tsx](ProviderStatusIndicator.tsx)                       | 只做展示映射，不能在 UI 再检查 Key、权益或模型成员。                                                                                                                  |
| [ProviderTemplatePicker.tsx](ProviderTemplatePicker.tsx)                         | Template 创建失败过去只写日志，用户留在选择页却看不到任何结果。                                                                                                       |
| [quotaModelDisplayName.ts](quotaModelDisplayName.ts)                             | 实现或公开接口：formatQuotaModelDisplayName。                                                                                                                         |
| [README.md](README.md)                                                           | 本目录用途、子目录与逐文件说明。                                                                                                                                      |
| [SectionLayout.tsx](SectionLayout.tsx)                                           | 实现或公开接口：shouldShowModelProviderRefreshLoading、ModelProviderSectionLayout。                                                                                   |
| [SortableProviderModelList.tsx](SortableProviderModelList.tsx)                   | 拖动状态沿用了普通行的可见底部分隔线，浮起后看起来像带下划线。                                                                                                        |
| [StartPlanBalanceCard.tsx](StartPlanBalanceCard.tsx)                             | Today's balance 后端已经按产品优先级返回 balances。                                                                                                                   |
| [StartPlanCard.tsx](StartPlanCard.tsx)                                           | 体验套餐卡片必须由远端 startPlanPreview.entitlements 驱动；                                                                                                           |
| [StartPlanQuotaStatusCard.tsx](StartPlanQuotaStatusCard.tsx)                     | 实现或公开接口：StartPlanQuotaStatusCard。                                                                                                                            |
| [StatusCards.tsx](StatusCards.tsx)                                               | 实现或公开接口：ModelProviderLoadingCard、PresetProviderPlaceholderCard、CodingPlanStatusPanel、hasStartPlanEntitlementQuota。                                        |
| [useCodingPlanEntitlements.ts](useCodingPlanEntitlements.ts)                     | Team 查询身份还包含 product/org/project。只使用 Registry 静态 Access                                                                                                  |
| [useCodingPlanProducts.ts](useCodingPlanProducts.ts)                             | 未登录/未连接时禁止打 paid batch-preview，但仍要展示静态套餐。                                                                                                        |
| [useEnterpriseCodingPlanProducts.ts](useEnterpriseCodingPlanProducts.ts)         | 静态目录控制购买横幅，不能用实时 pricing 补造目录中缺失的商品。                                                                                                       |
| [useIdleTrigger.ts](useIdleTrigger.ts)                                           | \* Provider 文本保存与 Model Config Resolution 共用的“停止输入后执行”调度器。                                                                                         |
| [useModelConfigResolution.ts](useModelConfigResolution.ts)                       | 旧恢复请求的错误也必须服从身份/编辑代次，不能覆盖用户后来的字段反馈。                                                                                                 |
| [useModelProviderNavigation.ts](useModelProviderNavigation.ts)                   | \* 当前账号明确有权益的 Provider。缺省等价于尚无账号权益；生产设置页始终显式传入。                                                                                    |
| [useOptimisticReorder.ts](useOptimisticReorder.ts)                               | 切换 Environment/Service Owner 时，即使 Provider 成员完全相同，也不能继续                                                                                             |
| [useProviderModelDraft.ts](useProviderModelDraft.ts)                             | 添加和编辑共享推荐生命周期；业务入口仅保留初始化、权限与各自的保存事务。                                                                                              |
| [useStartPlanPreview.ts](useStartPlanPreview.ts)                                 | Start Plan preview 和套餐列表共用 client/configs。                                                                                                                    |
| [utils.tsx](utils.tsx)                                                           | 品牌主入口沿用 Start 导航 ID，但不能因此显示体验套餐图标。                                                                                                            |

<!-- qingqi-directory-index:end -->
