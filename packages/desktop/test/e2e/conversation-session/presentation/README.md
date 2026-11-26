# presentation

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 presentation 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                                                   | 简要说明                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| [conversation-session-agent-step-message-scope.test.ts](conversation-session-agent-step-message-scope.test.ts)                                         | conversation-session-agent-step-message-scope.test 的实现文件。                                           |
| [conversation-session-assistant-block-order.test.ts](conversation-session-assistant-block-order.test.ts)                                               | I76：一次响应里交错的思考、文字和工具按流顺序保存，并按请求规则回放。                                     |
| [conversation-session-assistant-preview-cards.test.ts](conversation-session-assistant-preview-cards.test.ts)                                           | 与 getFileManagerLabel 按平台取文案一致；E2E 进程与 Electron 同机，process.platform 等价于 UA 判断。      |
| [conversation-session-image-preview-edit.test.ts](conversation-session-image-preview-edit.test.ts)                                                     | 新版标注栏按需展开；保存按钮只在有标注后出现在图形下方，因此这里只保留 11-02 工具栏修订的“无橡皮擦”断言。 |
| [conversation-session-markdown-preview-selection.test.ts](conversation-session-markdown-preview-selection.test.ts)                                     | 修复原因：文件树行 test id 含绝对路径；Windows 反斜杠在 CSS 属性值里是转义符，                            |
| [conversation-session-markdown-table-enhanced-scroll.test.ts](conversation-session-markdown-table-enhanced-scroll.test.ts)                             | conversation-session-markdown-table-enhanced-scroll.test 的实现文件。                                     |
| [conversation-session-markdown-table-layout.test.ts](conversation-session-markdown-table-layout.test.ts)                                               | conversation-session-markdown-table-layout.test 的实现文件。                                              |
| [conversation-session-message-image-gallery.test.ts](conversation-session-message-image-gallery.test.ts)                                               | 断言失败会跳过用例末尾的关闭，残留独立图片会污染后续组内导航和下载。                                      |
| [conversation-session-message-link-menu.test.ts](conversation-session-message-link-menu.test.ts)                                                       | 桌面窗口最小宽度为 480px；窄屏视觉验收需临时放宽，结束后恢复窗口约束。                                    |
| [conversation-session-output-limit-continue-markdown-boundaries.test.ts](conversation-session-output-limit-continue-markdown-boundaries.test.ts)       | conversation-session-output-limit-continue-markdown-boundaries.test 的实现文件。                          |
| [conversation-session-output-limit-continue-markdown-content-types.test.ts](conversation-session-output-limit-continue-markdown-content-types.test.ts) | 原因：全局新建使用独立 cwd，无法读取项目中的相对图片和文件 fixture。                                      |
| [conversation-session-output-limit-continue-markdown-protocols.test.ts](conversation-session-output-limit-continue-markdown-protocols.test.ts)         | 原因：本地 Markdown 图片播种在项目目录，全局草稿的独立 cwd 不能读取这些相对路径。                         |
| [conversation-session-output-limit-continue-ui.test.ts](conversation-session-output-limit-continue-ui.test.ts)                                         | conversation-session-output-limit-continue-ui.test 的实现文件。                                           |
| [conversation-session-preview-image-actions.test.ts](conversation-session-preview-image-actions.test.ts)                                               | 单像素 APNG/BMP/ICO 使用真实格式字节，防止只改文件名的假夹具掩盖格式问题。                                |
| [conversation-session-purpose-section-drag.test.ts](conversation-session-purpose-section-drag.test.ts)                                                 | 正式回放曾在此刷新后进入欢迎页；保留配置事实，不能用重载或重试掩盖启动异常。                              |
| [conversation-session-selection-comments.test.ts](conversation-session-selection-comments.test.ts)                                                     | 第一轮回答里表格之前的正文，用来验证“仅原文”注释（不写评论直接回车）。                                    |
| [conversation-session-status-panel-inline-layout.test.ts](conversation-session-status-panel-inline-layout.test.ts)                                     | conversation-session-status-panel-inline-layout.test 的实现文件。                                         |
| [conversation-session-streaming-word-reveal.test.ts](conversation-session-streaming-word-reveal.test.ts)                                               | fixture 里各段的片段，用来确认完成态文本完整。                                                            |
| [conversation-session-switch-stability.test.ts](conversation-session-switch-stability.test.ts)                                                         | conversation-session-switch-stability.test 的实现文件。                                                   |
| [conversation-session-v4-scroll.test.ts](conversation-session-v4-scroll.test.ts)                                                                       | M5④ 门禁：长会话虚拟滚动（timeline 动态测高 + 底部锚定 + 回到底部）。                                     |
| [conversation-session-v4-turn-navigator.test.ts](conversation-session-v4-turn-navigator.test.ts)                                                       | conversation-session-v4-turn-navigator.test 的实现文件。                                                  |
| [conversation-session-v4-video-preview.test.ts](conversation-session-v4-video-preview.test.ts)                                                         | VI06 + VI07 门禁：媒体卡片、共享 gallery、本地路径/分片预览、失败重开与 edit 原始索引。                   |
| [README.md](README.md)                                                                                                                                 | 本目录用途、子目录与逐文件说明。                                                                          |

<!-- qingqi-directory-index:end -->
