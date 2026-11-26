# usage-stats

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 usage stats 实现源码。

### 文件

| 文件                                                                   | 简要说明                                                                                                                             |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| [appUsageChartPalette.ts](appUsageChartPalette.ts)                     | 实现或公开接口：APP_USAGE_MODEL_CHART_COLORS、getAppUsageModelChartColor。                                                           |
| [AppUsageDailyModelTrendChart.tsx](AppUsageDailyModelTrendChart.tsx)   | XAxis 首尾刻度以绘图区边界为中心向两侧延伸，原 8px margin 小于日期文本半宽，                                                         |
| [appUsageModelPieChartViewModel.ts](appUsageModelPieChartViewModel.ts) | 实现或公开接口：AppUsageModelPieSlice、buildAppUsageModelPieChartViewModel。                                                         |
| [AppUsageModelUsagePieChart.tsx](AppUsageModelUsagePieChart.tsx)       | Recharts 会镜像 data/config props 到内部 store；稳定饼图数据可避免设置页刷新时重复派发。                                             |
| [AppUsagePanel.tsx](AppUsagePanel.tsx)                                 | Recharts 会在模块初始化阶段触发 decimal.js-light 的 LN10 校验，                                                                      |
| [CodingPlanUsageBarChart.tsx](CodingPlanUsageBarChart.tsx)             | 实现或公开接口：CodingPlanBarChartSeries、calculateCodingPlanBarChartMaxValue、CodingPlanUsageBarChart。                             |
| [codingPlanUsageChartSeries.ts](codingPlanUsageChartSeries.ts)         | 实现或公开接口：buildCodingPlanModelLineChartSeries、buildCodingPlanToolLineChartSeries、buildCodingPlanUsageDetailLineChartSeries。 |
| [CodingPlanUsageLineChart.tsx](CodingPlanUsageLineChart.tsx)           | XAxis 首尾刻度以绘图区边界为中心向两侧延伸，左右安全区太小会裁掉                                                                     |
| [CodingPlanUsagePanel.tsx](CodingPlanUsagePanel.tsx)                   | Usage stats 独有的完整重置时刻格式；其它紧凑入口继续按各自规则展示。                                                                 |
| [README.md](README.md)                                                 | 本目录用途、子目录与逐文件说明。                                                                                                     |
| [UsageChartLoadBoundary.tsx](UsageChartLoadBoundary.tsx)               | 实现或公开接口：UsageChartLoadBoundary。                                                                                             |
| [UsageHeatmap.tsx](UsageHeatmap.tsx)                                   | oxlint-disable max-lines -- 热力图在同一文件内维护每日、每周、累计三种展示计算，拆分会割裂共享列模型。                               |
| [UsageHeatmapCells.tsx](UsageHeatmapCells.tsx)                         | 实现或公开接口：TokenActivityMode、HeatmapDisplayCell、HeatmapDisplayColumn、HeatmapColumn。                                         |
| [UsageStatsErrorNotice.tsx](UsageStatsErrorNotice.tsx)                 | 团队套餐业务错误（如"您当前暂无有效的团队套餐授权记录…"）含"授权"字样，                                                              |
| [usageStatsUiParts.tsx](usageStatsUiParts.tsx)                         | 通用紧凑格式会把中文单位直接贴在数字后；摘要卡片与相邻的时长、天数指标统一保留单位间距。                                             |

<!-- qingqi-directory-index:end -->
