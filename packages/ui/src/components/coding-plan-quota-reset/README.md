# coding-plan-quota-reset

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 coding plan quota reset 界面组件。

### 文件

| 文件                                                                                 | 简要说明                                                                                       |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| [buildCodingPlanQuotaResetDialogConfig.ts](buildCodingPlanQuotaResetDialogConfig.ts) | Bugfix：这里曾额外用「额度剩余 100% 则重置无收益」门控隐藏整行。但核销会把剩余额度             |
| [CodingPlanQuotaResetAction.tsx](CodingPlanQuotaResetAction.tsx)                     | 自动/运营完成时由 Composer 触发器在 hover 展开面板后要求补播撒花的 used_at；手动重置为 null。  |
| [CodingPlanQuotaResetDialog.tsx](CodingPlanQuotaResetDialog.tsx)                     | 确认页的「重置」与列表行的「重置」位置相近，连点会穿透；切到确认页后的这段时间内忽略确认点击。 |
| [CodingPlanQuotaResetOpportunity.tsx](CodingPlanQuotaResetOpportunity.tsx)           | 弹框在 dialog 分支内常驻挂载，机会数从多降到单/零都不会提前卸载成功动画中的 Dialog；           |
| [CodingPlanQuotaResetStatus.tsx](CodingPlanQuotaResetStatus.tsx)                     | \* 自动重置提示内容（纯展示），供 composer 额度入口的受控 tooltip 使用：                       |
| [README.md](README.md)                                                               | 本目录用途、子目录与逐文件说明。                                                               |

<!-- qingqi-directory-index:end -->
