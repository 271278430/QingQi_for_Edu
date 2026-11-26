# browser-use

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 browser use 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                                           | 简要说明                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [conversation-session-browser-use-agent-element-picker.test.ts](conversation-session-browser-use-agent-element-picker.test.ts)                 | 人类 tab 的「选择元素」统一成设计点选后，原来的元素 chip 选择器只剩 Agent 的 Browser Use tab 在用（!3548 SG-01） |
| [conversation-session-browser-use-iab-multitab-lifecycle.test.ts](conversation-session-browser-use-iab-multitab-lifecycle.test.ts)             | 修复回归：finalize({ keep: [A] }) 是 lifecycle 标记，不是关闭白名单。                                            |
| [conversation-session-browser-use-keypress-host-isolation.test.ts](conversation-session-browser-use-keypress-host-isolation.test.ts)           | BU-E2E-028（docs/browser-use/2026-07-12-browser-use-runtime-semantics-spec.md §2.2）：                           |
| [conversation-session-browser-use-subagent-boundary.test.ts](conversation-session-browser-use-subagent-boundary.test.ts)                       | child 开的 Tab 归当前对话：面板直接展示它，而不是挂成看不见的孤儿 shell。                                        |
| [conversation-session-browser-zoom-coordinates.test.ts](conversation-session-browser-zoom-coordinates.test.ts)                                 | BU-E2E-020：只回放模型选择，实际输入和截图必须走产品的 Node REPL -> guest 链路。                                 |
| [conversation-session-node-repl-stateless-browser-multisession.test.ts](conversation-session-node-repl-stateless-browser-multisession.test.ts) | 修复原因：Windows 不会把 process.title 写回 WMI 命令行，Node REPL 子进程在那里只表现为                           |
| [README.md](README.md)                                                                                                                         | 本目录用途、子目录与逐文件说明。                                                                                 |

<!-- qingqi-directory-index:end -->
