# components

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 components 界面组件。

### 子目录

| 目录                                                          | 存放内容                                                  |
| ------------------------------------------------------------- | --------------------------------------------------------- |
| [ai-elements/](ai-elements/README.md)                         | @zcode/ui 基础工程中的 ai elements 界面组件。             |
| [cloud-content-dialog/](cloud-content-dialog/README.md)       | @zcode/ui 基础工程中的 cloud content dialog 界面组件。    |
| [coding-plan-quota-reset/](coding-plan-quota-reset/README.md) | @zcode/ui 基础工程中的 coding plan quota reset 界面组件。 |
| [icons/](icons/README.md)                                     | @zcode/ui 基础工程中的 icons 图标。                       |
| [lib/](lib/README.md)                                         | @zcode/ui 基础工程中的 lib 界面组件。                     |
| [manual-claim-plan/](manual-claim-plan/README.md)             | @zcode/ui 基础工程中的 manual claim plan 界面组件。       |
| [marketing-touch/](marketing-touch/README.md)                 | @zcode/ui 基础工程中的 marketing touch 界面组件。         |
| [mobile-ui/](mobile-ui/README.md)                             | @zcode/ui 基础工程中的 mobile ui 界面组件。               |
| [ui/](ui/README.md)                                           | @zcode/ui 基础工程中的 ui 界面组件。                      |
| [workflow-graph/](workflow-graph/README.md)                   | @zcode/ui 基础工程中的 workflow graph 界面组件。          |
| [workflow-run-line/](workflow-run-line/README.md)             | @zcode/ui 基础工程中的 workflow run line 界面组件。       |
| [workflow-timeline/](workflow-timeline/README.md)             | @zcode/ui 基础工程中的 workflow timeline 界面组件。       |

### 文件

| 文件                                                           | 简要说明                                                                                 |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [ClientSceneLucideIcon.tsx](ClientSceneLucideIcon.tsx)         | 按 Client Scenes 下发的 Lucide canonical 名称加载图标，未知名称保留调用方语义回退。      |
| [EmbeddedWebsiteHeader.tsx](EmbeddedWebsiteHeader.tsx)         | 实现或公开接口：EmbeddedWebsiteHeader。                                                  |
| [ModelInputCapabilityBadge.tsx](ModelInputCapabilityBadge.tsx) | 实现或公开接口：MODEL_INPUT_CAPABILITY_BADGE_CLASS_NAME、ModelInputCapabilityBadge。     |
| [PluginIcon.tsx](PluginIcon.tsx)                               | Plugin 原始图标；支持官方内置图标与 HTTPS，缺失或失败时使用调用方兜底，默认回退 Blocks。 |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                         |
| [TaskTitleOverflowText.tsx](TaskTitleOverflowText.tsx)         | 原生 title 提示框会在 hover 走马灯时遮挡正在滚动的任务名称。                             |

<!-- qingqi-directory-index:end -->
