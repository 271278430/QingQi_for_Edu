# marketing-touch

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 marketing touch 界面组件。

### 文件

| 文件                                                                         | 简要说明                                                                                      |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [MarketingBanner.tsx](MarketingBanner.tsx)                                   | 原 bg-card 让关闭/loading 带上常驻底色；两种状态都保持透明。                                  |
| [MarketingDialogs.tsx](MarketingDialogs.tsx)                                 | 实现或公开接口：MarketingDialogs。                                                            |
| [MarketingFailureDialog.tsx](MarketingFailureDialog.tsx)                     | 实现或公开接口：MarketingFailureDialog。                                                      |
| [marketingPopupAdapter.ts](marketingPopupAdapter.ts)                         | 实现或公开接口：canOpenMarketingPopup、marketingLabel、adaptMarketingPopup。                  |
| [marketingResources.ts](marketingResources.ts)                               | 实现或公开接口：prepareMarketingImage、PreparedMarketingHero、prepareMarketingHero。          |
| [marketingTouchController.ts](marketingTouchController.ts)                   | 导出以便 controller 类型（经 MarketingTouchContext）可被 .d.ts 命名引用。                     |
| [marketingTouchPoller.ts](marketingTouchPoller.ts)                           | 唯一串行调度器；用户触发在途刷新合并为一次后续查询。                                          |
| [MarketingTouchProvider.tsx](MarketingTouchProvider.tsx)                     | 导出给左下角活动仲裁层（SidebarBottomActivity）读取 Banner 可见性；控制器仍是唯一 owner。     |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                              |
| [useMarketingBannerVisible.ts](useMarketingBannerVisible.ts)                 | controller 缺席时用 noop 订阅、快照恒为 false，与 GlobalNoticeSurface 的 null-safe 写法一致。 |
| [useMarketingTaskCompletionRefresh.ts](useMarketingTaskCompletionRefresh.ts) | 仅观察任务完成边沿；活动查询仍由窗口唯一 poller 调度。                                        |

<!-- qingqi-directory-index:end -->
