# onboarding

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 onboarding 实现源码。

### 子目录

| 目录                        | 存放内容                                 |
| --------------------------- | ---------------------------------------- |
| [assets/](assets/README.md) | @zcode/ui 基础工程中的 assets 静态资源。 |

### 文件

| 文件                                                                       | 简要说明                                                                                                                        |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| [OccupationOnboarding.tsx](OccupationOnboarding.tsx)                       | 追加本地引导记录（userId 由 host 补全）；channel 缺失挂起时 5 秒超时按写失败处理。                                              |
| [OccupationOnboardingVisual.tsx](OccupationOnboardingVisual.tsx)           | 系统版本在会话内固定；采用主界面的版本查询和圆角规则，未知版本沿用其保守值。                                                    |
| [occupationOptions.ts](occupationOptions.ts)                               | 步骤 2 模式选择用的图标：coding / office。                                                                                      |
| [OnboardingAgentsFileStep.tsx](OnboardingAgentsFileStep.tsx)               | 实现或公开接口：OnboardingAgentsFileStep。                                                                                      |
| [OnboardingDialog.tsx](OnboardingDialog.tsx)                               | "plugins-import",                                                                                                               |
| [OnboardingDialogParts.tsx](OnboardingDialogParts.tsx)                     | \\                                                                                                                              | "plugins-import" |
| [OnboardingFlowParts.tsx](OnboardingFlowParts.tsx)                         | 实现或公开接口：OnboardingWorkspaceCandidate、FinishExecutionState、createInitialFinishExecutionState、OnboardingSessionsStep。 |
| [OnboardingHeader.tsx](OnboardingHeader.tsx)                               | 实现或公开接口：OnboardingHeader。                                                                                              |
| [onboardingLogoSweep.css](onboardingLogoSweep.css)                         | 掩膜只保留 1px 描边，旋转光场不影响品牌图标本体。                                                                               |
| [OnboardingMeshBackground.tsx](OnboardingMeshBackground.tsx)               | 装饰背景拥有自己的渲染生命周期，不订阅或修改业务状态。                                                                          |
| [onboardingMeshRenderer.ts](onboardingMeshRenderer.ts)                     | 独立实现的柔和灰阶流场，不包含第三方付费预设代码。                                                                              |
| [OnboardingModeSelector.tsx](OnboardingModeSelector.tsx)                   | 引导第二步的 UI 模式选择；从 OccupationOnboarding 抽出以控制文件行数。                                                          |
| [OnboardingOccupationGrid.tsx](OnboardingOccupationGrid.tsx)               | 职业显示文案（i18n 已格式化）。                                                                                                 |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                                                                |
| [useOnboardingAgentsFileMigration.ts](useOnboardingAgentsFileMigration.ts) | 实现或公开接口：OnboardingAgentsFileMigrationState、useOnboardingAgentsFileMigration。                                          |
| [useOnboardingMigration.ts](useOnboardingMigration.ts)                     | 实现或公开接口：shouldAutoScanOnboardingSessions、useOnboardingMigration。                                                      |
| [useOnboardingTelemetry.ts](useOnboardingTelemetry.ts)                     | 业务选择仍由引导组件持有；这里只记录本次真实展示范围和上报去重。                                                                |
| [useOnboardingTrigger.ts](useOnboardingTrigger.ts)                         | \* 引导触发判定：当前用户在本地记录里没有条目时 needsOnboarding=true（null 表示异步                                             |

<!-- qingqi-directory-index:end -->
