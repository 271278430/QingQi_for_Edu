# workflow-timeline

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 workflow timeline 界面组件。

### 文件

| 文件                                                                     | 简要说明                                                                                                                     |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| [draft-scan.ts](draft-scan.ts)                                           | 脚本、分析器还没跑，卡上就先把**阶段线**画出来——只有站与淡墨轨道段，没有药丸、没有弧、没有                                   |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                                             |
| [roster-model.ts](roster-model.ts)                                       | \* 阶段名册：一站的参与者过了阈值，药丸列                                                                                    |
| [stage-lamps.ts](stage-lamps.ts)                                         | 顺序规则的两件（`isCurrentPhase` / `stationStatus`）原在 timeline-model.ts；dwf-recursive 与                                 |
| [station-observation.ts](station-observation.ts)                         | \* 一站观察到的东西（docs/dynamic-workflow/presentation.md「The timeline model」「Past six                                   |
| [subagent-model-label.ts](subagent-model-label.ts)                       | \* 子代理模型的**词**：run 上存的是规范串                                                                                    |
| [timeline-bands.ts](timeline-bands.ts)                                   | \* 分析器报的 `alongside` 是**节点事实**：进入这一阶段时，还没 join 的其他阶段的 strand 仍在跑。                             |
| [timeline-cache.ts](timeline-cache.ts)                                   | \* 一对 (graph, run) 只建一次时间线模型（docs/dynamic-workflow/presentation.md「The timeline                                 |
| [timeline-frames.ts](timeline-frames.ts)                                 | \* 补全的框（docs/dynamic-workflow/presentation.md「Holes on the timeline」的「Filled with phases」与                        |
| [timeline-geometry.ts](timeline-geometry.ts)                             | \* 横向时间线的几何常量。与设计画布逐字相同：                                                                                |
| [timeline-holes.ts](timeline-holes.ts)                                   | \* 留白在时间线模型上的派生（docs/dynamic-workflow/presentation.md「Holes on the timeline」）。                              |
| [timeline-ledge.ts](timeline-ledge.ts)                                   | \* 边檐的纯几何：一根轨道两端压缩。                                                                                          |
| [timeline-model.ts](timeline-model.ts)                                   | \* 一个纯函数把有界 display 与 `workflowRuns` 投影折成三样东西：站（阶段）、轨道段（相邻且                                   |
| [timeline-pill-activity.ts](timeline-pill-activity.ts)                   | 原在 timeline-model.ts；dwf-recursive 与 dwf-pipeline-display 合并后那个文件到了 430 行（oxlint                              |
| [timeline-summary.ts](timeline-summary.ts)                               | \* 卡片表头细节与页脚摘要行的文案素材。侧栏状态头的摘要行也读这里——同一个 run 在两个面上必须说同一句话。                     |
| [use-fill-growth.ts](use-fill-growth.ts)                                 | \* 补全的生长（docs/dynamic-workflow/presentation.md「Holes on the timeline」的「Growth」）：补全接进 run 时                 |
| [use-timeline-viewport.ts](use-timeline-viewport.ts)                     | \* 滚动视口的三个数（scrollLeft / clientWidth / scrollWidth）与「正在滚」标记。                                              |
| [use-typewriter.ts](use-typewriter.ts)                                   | \* 模型的脚本按块到达，扫描器看到的是跳变：一整个 `phase("implement")` 在一个 delta 里，有时                                 |
| [useWorkflowSettingsModelChoices.ts](useWorkflowSettingsModelChoices.ts) | 子代理模型的选择面：「配置」弹层与确认窗共用                                                                                 |
| [workflow-face-motion.ts](workflow-face-motion.ts)                       | 一张脸只有一个待执行计时器；DOM 动作不触发整个工作流的 React 重渲染。                                                        |
| [WorkflowAgentFace.tsx](WorkflowAgentFace.tsx)                           | \* 瓦片脸：应用图标的圆角方块去掉 Z、                                                                                        |
| [WorkflowAgentPill.tsx](WorkflowAgentPill.tsx)                           | 名字 + 右侧状态标记。卡片的站下与侧栏的行都是它——同一个特性只有一枚药丸。                                                    |
| [WorkflowArtifactIndex.tsx](WorkflowArtifactIndex.tsx)                   | \* 产物索引（侧板）：交付物行之后的**其余产物**，一件一行。                                                                  |
| [WorkflowArtifactPill.tsx](WorkflowArtifactPill.tsx)                     | \* 产物药丸：与子代理药丸同一套语法——                                                                                        |
| [WorkflowArtifactRow.tsx](WorkflowArtifactRow.tsx)                       | \* 交付物行（侧板）：run 的 primary 产物在完成卡与 run 侧板上的样子。                                                        |
| [WorkflowArtifactStrip.tsx](WorkflowArtifactStrip.tsx)                   | \* 产物条：一行产物药丸，至多三枚，                                                                                          |
| [WorkflowArtifactTile.tsx](WorkflowArtifactTile.tsx)                     | \* 产物瓦片：一件产物 = 预览区 + 说明行。                                                                                    |
| [workflowAskSettings.ts](workflowAskSettings.ts)                         | 确认窗里可调的两项 run 设置：纯规则                                                                                          |
| [WorkflowAskSettingsLines.tsx](WorkflowAskSettingsLines.tsx)             | 确认窗里的两项 run 设置（docs/dynamic-workflow/presentation.md「The confirmation window」）                                  |
| [WorkflowAskSettingsParts.tsx](WorkflowAskSettingsParts.tsx)             | 确认窗两句设置的零件（docs/dynamic-workflow/presentation.md「The confirmation window」）                                     |
| [WorkflowCardChrome.tsx](WorkflowCardChrome.tsx)                         | \* 不走 `ToolLayout`：它的摘要行是 `inline-flex self-start`，右对齐的状态簇放不进去。表头一行：                              |
| [WorkflowCompletionArtifacts.tsx](WorkflowCompletionArtifacts.tsx)       | 从 `WorkflowCompletionCard` 拆出来：卡本身要守 400 行的门。                                                                  |
| [WorkflowCompletionCard.tsx](WorkflowCompletionCard.tsx)                 | \* 完成卡：主代理消化一条 **completed** 工作流通知的那一轮，                                                                 |
| [WorkflowHoleParts.tsx](WorkflowHoleParts.tsx)                           | \* 留白的小零件（docs/dynamic-workflow/presentation.md「Holes on the timeline」），卡、侧板与工具行共用：                    |
| [WorkflowMarchLight.tsx](WorkflowMarchLight.tsx)                         | \* 行进边的光：控制流进入正在运行的站所走的那条边，                                                                          |
| [WorkflowMoreRow.tsx](WorkflowMoreRow.tsx)                               | \* 「还有 n 个」那一行：卡上名册站                                                                                           |
| [WorkflowRoll.tsx](WorkflowRoll.tsx)                                     | \* 门后的名单：侧板名册站里没被钉住                                                                                          |
| [WorkflowRosterParts.tsx](WorkflowRosterParts.tsx)                       | \* 阶段名册的两件小零件：计数行与量条。                                                                                      |
| [WorkflowRunDigest.tsx](WorkflowRunDigest.tsx)                           | 下方运行卡默认展开，无箭头但仍可收起；状态由标题表达。                                                                       |
| [workflowRunSave.ts](workflowRunSave.ts)                                 | 完成卡「保存 / 再次运行」的纯逻辑（docs/dynamic-workflow/transcript-and-notifications.md                                     |
| [workflowRunSettings.ts](workflowRunSettings.ts)                         | 弹层组件只管画与接线，这里是它的全部判断：哪些 run 能配、表单从哪儿起步、Apply 发什么、                                      |
| [WorkflowRunSettingsFields.tsx](WorkflowRunSettingsFields.tsx)           | 从 WorkflowRunSettingsPopover.tsx 拆出：那边管表单状态、命令与后果句，这里只画两个受控字段——                                 |
| [WorkflowRunSettingsPopover.tsx](WorkflowRunSettingsPopover.tsx)         | run 卡的 Configure 钮、详情页的 Configure 钮与详情页摘要行的模型段打开同一个弹层：两个字段、                                 |
| [WorkflowSaveFields.tsx](WorkflowSaveFields.tsx)                         | 「保存工作流」弹层里细线之下的那一半（docs/dynamic-workflow/transcript-and-notifications.md                                  |
| [WorkflowSavePopover.tsx](WorkflowSavePopover.tsx)                       | 完成卡「保存」弹层（docs/dynamic-workflow/transcript-and-notifications.md「The popover」）。                                 |
| [workflowSettingsChange.ts](workflowSettingsChange.ts)                   | 一次「配置」在两个面上留下记录：转写里 run 卡上方的一行「已调整设置 · 子代理改用 X · 最多 N 个                               |
| [WorkflowSettingsChangeRow.tsx](WorkflowSettingsChangeRow.tsx)           | 「配置」的一次修改在转写里留下一个控制轮：没有用户气泡，它的呈现是新 run 的卡，卡上方这一行说                                |
| [WorkflowStationMeta.tsx](WorkflowStationMeta.tsx)                       | 站头元数据（从 `WorkflowTimeline.tsx` 拆出以守 400 行）：`⟳ n` 轮次（只在循环上的站）与 `a/b` 步数分数（只在观察到节点后）。 |
| [WorkflowStreamChevrons.tsx](WorkflowStreamChevrons.tsx)                 | \* 流轨的 chevron（docs/dynamic-workflow/presentation.md「Stream rails」）：轨道在它可见跨度的正中断开                       |
| [WorkflowTimeline.tsx](WorkflowTimeline.tsx)                             | \* 横向时间线：一根轨道、站在轨道上、                                                                                        |
| [WorkflowTimelineArcs.tsx](WorkflowTimelineArcs.tsx)                     | \* 弧层：时间线唯一的一层 SVG，只画                                                                                          |
| [WorkflowTimelineFills.tsx](WorkflowTimelineFills.tsx)                   | 补全接进 run 之后框自己画一遍、头染警示色的时长（docs/dynamic-workflow/presentation.md「The stroke」）。                     |
| [WorkflowTimelineLedge.tsx](WorkflowTimelineLedge.tsx)                   | \* 边檐：折叠到视口一侧的站，画成一排同一枚 10px 灯（16px 一枚），之间是那条边的墨色小轨道段，                               |
| [WorkflowTimelineStation.tsx](WorkflowTimelineStation.tsx)               | \* 站头：名字 + 元数据，一枚没有背景的                                                                                       |
| [WorkflowTimelineTracks.tsx](WorkflowTimelineTracks.tsx)                 | \* 没有带的时间线里轨道段还是站头行里的一截 border（逐像素不动）。**有带**时整条轨道搬进弧那一层                             |
| [WorkflowTruncatedNotice.tsx](WorkflowTruncatedNotice.tsx)               | \* 「仅展示 {shown}/{total} 步的详情」（docs/dynamic-workflow/presentation.md「The run card」                                |

<!-- qingqi-directory-index:end -->
