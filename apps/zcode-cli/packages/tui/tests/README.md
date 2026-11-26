# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/tui 基础工程中的 tests 验收与回归场景。

### 文件

| 文件                                                                         | 简要说明                                                                                    |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [ctrl-c-exit-guard.test.ts](ctrl-c-exit-guard.test.ts)                       | ctrl-c-exit-guard.test 的实现文件。                                                         |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                            |
| [tui-app.test.ts](tui-app.test.ts)                                           | tui-app.test 的实现文件。                                                                   |
| [tui-approval-panel.test.ts](tui-approval-panel.test.ts)                     | tui-approval-panel.test 的实现文件。                                                        |
| [tui-background-approval.test.ts](tui-background-approval.test.ts)           | 回归：独立 TUI 的审批入口在挂载期间一直有效（会话工具设计 0.5）。                           |
| [tui-ctrl-c-draft.test.ts](tui-ctrl-c-draft.test.ts)                         | tui-ctrl-c-draft.test 的实现文件。                                                          |
| [tui-effort-suggestions.test.ts](tui-effort-suggestions.test.ts)             | tui-effort-suggestions.test 的实现文件。                                                    |
| [tui-events.test.ts](tui-events.test.ts)                                     | tui-events.test 的实现文件。                                                                |
| [tui-file-mentions.test.ts](tui-file-mentions.test.ts)                       | tui-file-mentions.test 的实现文件。                                                         |
| [tui-focus.test.ts](tui-focus.test.ts)                                       | tui-focus.test 的实现文件。                                                                 |
| [tui-image-paste.test.ts](tui-image-paste.test.ts)                           | tui-image-paste.test 的实现文件。                                                           |
| [tui-input-sync.test.ts](tui-input-sync.test.ts)                             | tui-input-sync.test 的实现文件。                                                            |
| [tui-input.test.ts](tui-input.test.ts)                                       | tui-input.test 的实现文件。                                                                 |
| [tui-main-session-effects.test.ts](tui-main-session-effects.test.ts)         | WP-F 效果级回归：actor/子会话的原始事件绝不进主转写（user directive 2026-08-23）。          |
| [tui-main-session-filter.test.ts](tui-main-session-filter.test.ts)           | 主会话闸门（WP-F，user directive 2026-08-23）。                                             |
| [tui-markdown.test.ts](tui-markdown.test.ts)                                 | tui-markdown.test 的实现文件。                                                              |
| [tui-mode-suggestions.test.ts](tui-mode-suggestions.test.ts)                 | tui-mode-suggestions.test 的实现文件。                                                      |
| [tui-model-suggestions.test.ts](tui-model-suggestions.test.ts)               | 模型选项改为协议 Model Option（ref + label），别名（main/lite）已移除；                     |
| [tui-question-state.test.ts](tui-question-state.test.ts)                     | tui-question-state.test 的实现文件。                                                        |
| [tui-selection-panel.test.ts](tui-selection-panel.test.ts)                   | tui-selection-panel.test 的实现文件。                                                       |
| [tui-sidebar-render.test.ts](tui-sidebar-render.test.ts)                     | Todos 改为可折叠区块，标题与 API 等区块一样带展开标记。                                     |
| [tui-sidebar.test.ts](tui-sidebar.test.ts)                                   | tui-sidebar.test 的实现文件。                                                               |
| [tui-slash-suggestions.test.ts](tui-slash-suggestions.test.ts)               | tui-slash-suggestions.test 的实现文件。                                                     |
| [tui-theme.test.ts](tui-theme.test.ts)                                       | tui-theme.test 的实现文件。                                                                 |
| [tui-thought.test.ts](tui-thought.test.ts)                                   | tui-thought.test 的实现文件。                                                               |
| [tui-tool-transcript.test.ts](tui-tool-transcript.test.ts)                   | tui-tool-transcript.test 的实现文件。                                                       |
| [tui-turn-complete-fallback.test.ts](tui-turn-complete-fallback.test.ts)     | turn_complete 的 response 兜底：通知驱动的回合没有 applyResult，流式又可能一个字都没画      |
| [tui-workflow-approval-bypass.test.ts](tui-workflow-approval-bypass.test.ts) | CreateWorkflow 的确认 gate 旁路（docs/dynamic-workflow/launch.md「The approval bypass」）。 |
| [tui-workflow-card.test.ts](tui-workflow-card.test.ts)                       | ── 镜像：共享 reducer 驱动 + React 引用回传 ──                                              |
| [tui-workflow-expansion-key.test.ts](tui-workflow-expansion-key.test.ts)     | `+` / `-` 是可打印字符且 composer 默认持焦：这组测试钉住"绝不吃掉正常输入"的三层闸门        |
| [tui.unit.test.ts](tui.unit.test.ts)                                         | 登录提示改为“没有可用模型”，引导用 /model 查看模型或 /login 连接账号。                      |

<!-- qingqi-directory-index:end -->
