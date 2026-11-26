# chat-input-toolbar

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 chat input toolbar 实现源码。

### 文件

| 文件                                                                                 | 简要说明                                                                                                                                      |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| [ChatCodingPlanMcpUsageMeter.tsx](ChatCodingPlanMcpUsageMeter.tsx)                   | MCP 不必无条件占据独立横行，只有一两张主额度时会浪费网格空位；                                                                                |
| [ChatModeSwitchControl.tsx](ChatModeSwitchControl.tsx)                               | 触发器看起来像空白长按钮。窄态同步隐藏箭头并收成正方形，宽态恢复完整信息。                                                                    |
| [CodingPlanContextUsage.tsx](CodingPlanContextUsage.tsx)                             | Composer 触发器 hover 展开面板后要求补播撒花的自动完成 used_at,按重置类型定位到对应额度条。                                                   |
| [codingPlanQuotaResetAutoPlay.ts](codingPlanQuotaResetAutoPlay.ts)                   | \* 把异步 reservation 和组件展示边界串起来。                                                                                                  |
| [codingPlanResetOpportunityBadge.ts](codingPlanResetOpportunityBadge.ts)             | Bugfix：徽标曾在额度剩余 100% 时隐藏（重置无收益）。但核销会把剩余改写成 100%，                                                               |
| [CodingPlanUsageHeaderAction.tsx](CodingPlanUsageHeaderAction.tsx)                   | 实现或公开接口：CodingPlanUsageHeaderAction。                                                                                                 |
| [CodingPlanUsageNotice.tsx](CodingPlanUsageNotice.tsx)                               | 实现或公开接口：CodingPlanUsageNotice。                                                                                                       |
| [composer-thought-slider.css](composer-thought-slider.css)                           | 参考图中的白色滑块在两套主题下保持一致，轨道与档位圆点继续使用语义主题色。                                                                    |
| [ComposerEffortHeading.tsx](ComposerEffortHeading.tsx)                               | 实现或公开接口：ComposerEffortHeading。                                                                                                       |
| [ComposerModelMenu.tsx](ComposerModelMenu.tsx)                                       | 固定种子避免重渲染重新随机，让最高档气泡错峰流动而不影响模型选择状态。                                                                        |
| [ComposerProviderMenu.tsx](ComposerProviderMenu.tsx)                                 | 合并菜单曾只渲染名称而丢失接入标识；主行和子菜单采用同一目录字段。                                                                            |
| [ComposerTriggerTransition.tsx](ComposerTriggerTransition.tsx)                       | 实现或公开接口：ComposerTriggerTransition。                                                                                                   |
| [contextPanelAction.ts](contextPanelAction.ts)                                       | HoverCard 内按钮点击不会像外部 hover leave 一样自动关闭面板。                                                                                 |
| [contextQuotaMeterGrid.ts](contextQuotaMeterGrid.ts)                                 | Start/Coding 额度来自服务端快照，实际可能是 1/2/3 条；官方 MCP                                                                                |
| [contextQuotaResetOpportunityReminder.tsx](contextQuotaResetOpportunityReminder.tsx) | 会话切换会重新挂载 composer；已读状态必须归当前 renderer 窗口所有，                                                                           |
| [contextUsage.tsx](contextUsage.tsx)                                                 | 实现或公开接口：formatContextUsageTokenCount、formatContextUsageSummary、formatContextCacheHitRateLabel、buildContextUsageBreakdownSegments。 |
| [display-help.ts](display-help.ts)                                                   | 审批框与输入框共用权限颜色，浅色/深色主题由语义 token 决定。                                                                                  |
| [display.tsx](display.tsx)                                                           | Radix Select 在受控值与子项注册竞争时可能发出空值等未渲染值；直接上抛会把                                                                     |
| [modelSelection.ts](modelSelection.ts)                                               | 实现或公开接口：shouldShowManageModelsAction、resolveModelSelectTriggerDisplay。                                                              |
| [README.md](README.md)                                                               | 本目录用途、子目录与逐文件说明。                                                                                                              |
| [RollingToolbarLabel.tsx](RollingToolbarLabel.tsx)                                   | 实现或公开接口：RollingToolbarLabel。                                                                                                         |
| [StartPlanContextBalance.tsx](StartPlanContextBalance.tsx)                           | hover 打开 context 面板时发起的静默 access 刷新（与 Coding Plan 段 onAccess 语义一致）。                                                      |
| [ThoughtLevelCycleControl.tsx](ThoughtLevelCycleControl.tsx)                         | 聊天输入框由统一布局 owner 收起文字，其他调用方保留原断点规则。                                                                               |
| [thoughtLevelLabels.ts](thoughtLevelLabels.ts)                                       | 纯展示词表：工作流分享页不可经工具栏组件引入 Desktop 状态和服务。                                                                             |
| [thoughtLevelOptions.ts](thoughtLevelOptions.ts)                                     | 配置已声明档位顺序；名称别名只用于展示，不能改变菜单或快捷键顺序。                                                                            |

<!-- qingqi-directory-index:end -->
