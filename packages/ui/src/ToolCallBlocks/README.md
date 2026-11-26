# ToolCallBlocks

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 ToolCallBlocks 实现源码。

### 子目录

| 目录                              | 存放内容                                    |
| --------------------------------- | ------------------------------------------- |
| [renderers/](renderers/README.md) | @zcode/ui 基础工程中的 renderers 实现源码。 |
| [session/](session/README.md)     | @zcode/ui 基础工程中的 session 实现源码。   |

### 文件

| 文件                                                           | 简要说明                                                                                                              |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [fileSummaries.ts](fileSummaries.ts)                           | ZCode agent 的 edit/write/apply_patch 工具会把真实 diff 放在                                                          |
| [fileSummaryHeuristics.ts](fileSummaryHeuristics.ts)           | TodoWrite/AskUserQuestion 这类固定工具名不能再靠字符串片段判断写文件。                                                |
| [fileSummaryTypes.ts](fileSummaryTypes.ts)                     | Bugfix：这里曾写成类型位置的内联动态 import 写法（在 typeof 后跟圆括号包模块名）。                                    |
| [presentationCapabilities.tsx](presentationCapabilities.tsx)   | 实现或公开接口：ToolPresentationCapabilities、ToolPresentationCapabilitiesProvider、useToolPresentationCapabilities。 |
| [QueuedSummaryContent.tsx](QueuedSummaryContent.tsx)           | #185：禁用动画时逐 token 在 effect 里复制 state，会在连续同步提交中积累嵌套更新。                                     |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                                      |
| [renderers.tsx](renderers.tsx)                                 | 完成态曾回退到工具类型名，导致子项仍显示 Write / Edit；采用已有过去式文案。                                           |
| [resolveRenderer.ts](resolveRenderer.ts)                       | 工具卡 renderer 注册表：tool identity → 具体 renderer 组件                                                            |
| [shared.tsx](shared.tsx)                                       | shared 的React 组件。                                                                                                 |
| [ToolCallBody.tsx](ToolCallBody.tsx)                           | 应用主题（store 耦合剥离）：透传给 markdown / 代码块渲染，缺省按 "system" 兜底。                                      |
| [ToolCallProgressIndicator.tsx](ToolCallProgressIndicator.tsx) | 从 legacy raw 读出投影的运行中进度（toolCallRowAdapter 透传 ToolCallRow.progress）。                                  |
| [ToolLayout.tsx](ToolLayout.tsx)                               | 内存诊断计数器：该表按 toolId 只增不减，先落日志。                                                                    |
| [ToolPresentation.tsx](ToolPresentation.tsx)                   | 无宿主依赖的工具装配：共享原 renderer；公开页面不构造服务、插件 runtime 或工作区。                                    |
| [toolResultDisplay.ts](toolResultDisplay.ts)                   | \* 工作流 display kind → 解析函数的查表（新增 kind 只改这一处）。每个条目用 shared 侧的                               |
| [ToolSnapshotFieldNotice.tsx](ToolSnapshotFieldNotice.tsx)     | 实现或公开接口：ToolSnapshotFieldNotice。                                                                             |
| [ToolSummaryRow.tsx](ToolSummaryRow.tsx)                       | 收起的未闭合组头采用已完成工具摘要，扫光表达分组仍在继续，不改写工具状态。                                            |

<!-- qingqi-directory-index:end -->
