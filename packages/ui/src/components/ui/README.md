# ui

原始目录说明见 [UPSTREAM_README.md](UPSTREAM_README.md)，原文和版权完整保留。

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 ui 界面组件。

### 文件

| 文件                                                                                 | 简要说明                                                                                                                                                            |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [accordion.tsx](accordion.tsx)                                                       | accordion 的React 组件。                                                                                                                                            |
| [alert-dialog.tsx](alert-dialog.tsx)                                                 | Linux 旧标题栏避让会留下未遮罩的顶部亮条；确认弹窗也应覆盖完整窗口。                                                                                                |
| [alert.tsx](alert.tsx)                                                               | alert 的React 组件。                                                                                                                                                |
| [avatar.tsx](avatar.tsx)                                                             | avatar 的React 组件。                                                                                                                                               |
| [badge.tsx](badge.tsx)                                                               | badge 的React 组件。                                                                                                                                                |
| [button-group.tsx](button-group.tsx)                                                 | button-group 的React 组件。                                                                                                                                         |
| [button.tsx](button.tsx)                                                             | 大会话窗口 resize trace 显示基础按钮的 transition-all 会批量启动                                                                                                    |
| [card.tsx](card.tsx)                                                                 | card 的React 组件。                                                                                                                                                 |
| [carousel.tsx](carousel.tsx)                                                         | carousel 的React 组件。                                                                                                                                             |
| [chart.tsx](chart.tsx)                                                               | Format: { THEME_NAME: CSS_SELECTOR }                                                                                                                                |
| [checkbox.tsx](checkbox.tsx)                                                         | checkbox 的React 组件。                                                                                                                                             |
| [code-viewer.tsx](code-viewer.tsx)                                                   | \* 需要点名的行号（1 起，与 `firstLineNumber` 同一坐标）：只把这些行的**行号**染成警示色，                                                                          |
| [collapsible.tsx](collapsible.tsx)                                                   | collapsible 的React 组件。                                                                                                                                          |
| [command.tsx](command.tsx)                                                           | cmdk 键盘上下键只会切换 data-                                                                                                                                       |
| [context-menu.tsx](context-menu.tsx)                                                 | 圆角规范迁移：旧菜单沿用 xl/lg，统一为独立外壳 lg、内部选项 md；子菜单重新起算。                                                                                    |
| [dialog.tsx](dialog.tsx)                                                             | Linux 旧标题栏避让让模态遮罩从 48px 以下开始，窗口顶部仍保持高亮且 tooltip 可见。                                                                                   |
| [diff-viewer.tsx](diff-viewer.tsx)                                                   | 完整 diff 运行在 @pierre/diffs Shadow DOM 中，不会自动继承外层 font-mono class。                                                                                    |
| [dropdown-menu.tsx](dropdown-menu.tsx)                                               | 圆角规范迁移：旧菜单沿用 xl/lg，统一为独立外壳 lg、内部选项 md；子菜单重新起算。                                                                                    |
| [flip-metric-value.tsx](flip-metric-value.tsx)                                       | 数字槽以前用 baseline + 负偏移，冒号和 K/M 单位走静态 inline，                                                                                                      |
| [floating-particles.tsx](floating-particles.tsx)                                     | 高亮 index 按 seeded startLeft 选取，横向覆盖约 8%–92%，避免亮点集中在同一区域。                                                                                    |
| [GlmMonochromeIcon.tsx](GlmMonochromeIcon.tsx)                                       | 线框化版本会破坏原始 logo 的识别度，视觉上也偏轻。                                                                                                                  |
| [highlighted-lightweight-diff-preview.tsx](highlighted-lightweight-diff-preview.tsx) | 实现或公开接口：getHighlightedLightweightDiffLine、buildHighlightedLightweightDiffCode、HighlightedLightweightDiffPreviewProps、HighlightedLightweightDiffPreview。 |
| [hover-card.tsx](hover-card.tsx)                                                     | 自定义锚点时 Portal 与内容必须共享 Root 的 scope，才能读取同一浮层的开关与定位上下文。                                                                              |
| [input-group.tsx](input-group.tsx)                                                   | input-group 的React 组件。                                                                                                                                          |
| [input.tsx](input.tsx)                                                               | input 的React 组件。                                                                                                                                                |
| [kbd.tsx](kbd.tsx)                                                                   | 每个按键保留独立键帽，采用全应用快捷键提示的样式与平台字体。                                                                                                        |
| [label.tsx](label.tsx)                                                               | label 的React 组件。                                                                                                                                                |
| [lightweight-diff-preview.tsx](lightweight-diff-preview.tsx)                         | 实现或公开接口：LightweightDiffLineKind、LightweightDiffLineParts、LightweightDiffPreviewProps、getLightweightDiffLineParts。                                       |
| [pdf-viewer.tsx](pdf-viewer.tsx)                                                     | 与 service 层 readFileRange 的默认分段大小对齐，一次 range 请求对应一次 RPC 调用。                                                                                  |
| [popover.tsx](popover.tsx)                                                           | Popover 与 tooltip 同为 z-50 时，后挂载的辅助提示会覆盖正在操作的浮层。                                                                                             |
| [pptx-preview-viewer.tsx](pptx-preview-viewer.tsx)                                   | 实现或公开接口：PptxPreviewViewerLabels、PptxPreviewViewer。                                                                                                        |
| [pptx-selection-action-bar.tsx](pptx-selection-action-bar.tsx)                       | \* PPTX 元素选择的应用层操作条。                                                                                                                                    |
| [progress.tsx](progress.tsx)                                                         | 实现或公开接口：ProgressSegment。                                                                                                                                   |
| [radio-group.tsx](radio-group.tsx)                                                   | radio-group 的React 组件。                                                                                                                                          |
| [README.md](README.md)                                                               | 本目录用途、子目录与逐文件说明。                                                                                                                                    |
| [resizable.tsx](resizable.tsx)                                                       | ResizablePanelGroup                                                                                                                                                 |
| [scroll-area.tsx](scroll-area.tsx)                                                   | scroll-area 的React 组件。                                                                                                                                          |
| [scroll-fade-viewport.tsx](scroll-fade-viewport.tsx)                                 | Tailwind arbitrary value 里用下划线表示 calc 空格，避免生成无效的 calc(100%-24px)。                                                                                 |
| [select.tsx](select.tsx)                                                             | resize 大会话时 Select trigger 跟随基础控件批量重排，                                                                                                               |
| [separator.tsx](separator.tsx)                                                       | separator 的React 组件。                                                                                                                                            |
| [smooth-metric-value.tsx](smooth-metric-value.tsx)                                   | 实现或公开接口：SmoothMetricDisplayInput、normalizeSmoothMetricTarget、estimateSmoothMetricLinesPerSecond、resolveNextSmoothMetricDisplay。                         |
| [spinner.tsx](spinner.tsx)                                                           | spinner 的React 组件。                                                                                                                                              |
| [switch.tsx](switch.tsx)                                                             | switch 的React 组件。                                                                                                                                               |
| [tabs.tsx](tabs.tsx)                                                                 | tabs 的React 组件。                                                                                                                                                 |
| [textarea.tsx](textarea.tsx)                                                         | textarea 的React 组件。                                                                                                                                             |
| [toast.tsx](toast.tsx)                                                               | \* 不引入第三方库，用 React portal 渲染到 body，3 秒自动消失。                                                                                                      |
| [tooltip.tsx](tooltip.tsx)                                                           | Radix 的 skipDelayDuration=0 仍在下一轮 timer 才清除快速打开状态；                                                                                                  |
| [UPSTREAM_README.md](UPSTREAM_README.md)                                             | ZCode 或第三方资料的原始目录说明，保留原文和版权。                                                                                                                  |
| [usePdfZoomOverlay.ts](usePdfZoomOverlay.ts)                                         | 修饰键 + 滚轮的连续缩放灵敏度：兼容触控板高频小 delta 和鼠标滚轮大 delta。                                                                                          |
| [ZCodeAboutLogo.tsx](ZCodeAboutLogo.tsx)                                             | 实现或公开接口：ZCodeAboutLogo、ZCodeWordmarkLogo。                                                                                                                 |

<!-- qingqi-directory-index:end -->
