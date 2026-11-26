# schedule

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 schedule 测试场景。

### 文件

| 文件                                                                                       | 简要说明                                                                             |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| [automations-create-manage.test.ts](automations-create-manage.test.ts)                     | \* 定时任务「表单创建 → 编辑 → 暂停/恢复 → 删除」端到端。                            |
| [automations-custom-monthly-interval.test.ts](automations-custom-monthly-interval.test.ts) | 新建态默认不带日程；必须从“添加日程”进入 Custom，不能依赖编辑态才存在的频率 Select。 |
| [automations-custom-yearly-schedule.test.ts](automations-custom-yearly-schedule.test.ts)   | \* 定时任务「自定义 → 年」内联月/日选择器端到端。                                    |
| [README.md](README.md)                                                                     | 本目录用途、子目录与逐文件说明。                                                     |

<!-- qingqi-directory-index:end -->
