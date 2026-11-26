# branching

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 branching 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                               | 简要说明                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| [conversation-session-fork-cold-start-membership.test.ts](conversation-session-fork-cold-start-membership.test.ts) | Bug 根因：fork child 的 conversation hydration 会把 pane 恢复出来，但旧 gateway                             |
| [conversation-session-fork-merged-assistant.test.ts](conversation-session-fork-merged-assistant.test.ts)           | 修复原因：这个正式 case 专门复现一条可见 assistant 由多条 raw                                               |
| [conversation-session-fork-rollback-isolation.test.ts](conversation-session-fork-rollback-isolation.test.ts)       | 等旧 Electron/Host/Agent 全部退出，再通过真实 store 制造交错；不直接改 CLI 数据库行。                       |
| [conversation-session-fork-side-pane-empty-state.test.ts](conversation-session-fork-side-pane-empty-state.test.ts) | 默认空 scope 现在有一个 new-tab 启动页；父辅助 tab 仍必须被 scope 隔离。                                    |
| [conversation-session-selection-side-chat.test.ts](conversation-session-selection-side-chat.test.ts)               | 用例断言中文辅助 tab 标题；首帧跟随系统语言，必须先固定语言再创建 child。                                   |
| [conversation-session-side-chat-escape.test.ts](conversation-session-side-chat-escape.test.ts)                     | 面板开关的 Tooltip 会消费 Esc；移开指针并失焦，验证无浮层的页面空白焦点。                                   |
| [conversation-session-side-chat-reminder.test.ts](conversation-session-side-chat-reminder.test.ts)                 | 本地 endpoint 也通过真实模型能力判定启用 MCS，避免正式回归依赖在线 capture。                                |
| [conversation-session-side-pane-full-view.test.ts](conversation-session-side-pane-full-view.test.ts)               | spec：docs/ui/side-pane-full-view.md；用例：docs/testing/side-pane-tabs-e2e-case-catalog.md（SPFV-007/008） |
| [conversation-session-side-pane-late-close.test.ts](conversation-session-side-pane-late-close.test.ts)             | 登录返回可能恢复另一草稿；显式回到原任务，避免将 scope 隐藏误判为标签丢失。                                 |
| [conversation-session-side-slash-arguments.test.ts](conversation-session-side-slash-arguments.test.ts)             | idle + /side：参数成为 child 的第一条普通 user message，不落入父 timeline。                                 |
| [conversation-session-v4-fork-edit-branch.test.ts](conversation-session-v4-fork-edit-branch.test.ts)               | catalog E09（forkUsesEditedActiveBranch）验收（case catalog 战役）。                                        |
| [conversation-session-v4-fork.test.ts](conversation-session-v4-fork.test.ts)                                       | M4 门禁：forkAssistant（catalog E 组）。                                                                    |
| [README.md](README.md)                                                                                             | 本目录用途、子目录与逐文件说明。                                                                            |

<!-- qingqi-directory-index:end -->
