# v2

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

zcode-cli 基础工程中的 v2 设计与维护文档。

### 子目录

| 目录                          | 存放内容                                        |
| ----------------------------- | ----------------------------------------------- |
| [compact/](compact/README.md) | zcode-cli 基础工程中的 compact 设计与维护文档。 |
| [loop/](loop/README.md)       | zcode-cli 基础工程中的 loop 设计与维护文档。    |
| [memory/](memory/README.md)   | zcode-cli 基础工程中的 memory 设计与维护文档。  |
| [model/](model/README.md)     | zcode-cli 基础工程中的 model 设计与维护文档。   |
| [rewind/](rewind/README.md)   | zcode-cli 基础工程中的 rewind 设计与维护文档。  |
| [tool/](tool/README.md)       | zcode-cli 基础工程中的 tool 设计与维护文档。    |

### 文件

| 文件                                                                           | 简要说明                                                                       |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| [architecture.md](architecture.md)                                             | ZCode CLI 架构设计 v2：说明文档。                                              |
| [auth-login.md](auth-login.md)                                                 | Auth Login：说明文档。                                                         |
| [btw-side-question.md](btw-side-question.md)                                   | `/btw` Side Question：说明文档。                                               |
| [commands.md](commands.md)                                                     | Command Center：说明文档。                                                     |
| [conversation-input-source.md](conversation-input-source.md)                   | 会话输入来源（ConversationInputSource）：说明文档。                            |
| [core-adapters-boundary-plan.md](core-adapters-boundary-plan.md)               | Core / Adapters Boundary Refactor Plan：说明文档。                             |
| [count-lint.md](count-lint.md)                                                 | Count Lint Script：说明文档。                                                  |
| [custom-commands.md](custom-commands.md)                                       | Custom Commands：说明文档。                                                    |
| [debug-execution-gantt.md](debug-execution-gantt.md)                           | Debug Execution Gantt：说明文档。                                              |
| [debug-observability.md](debug-observability.md)                               | Debug Observability App：说明文档。                                            |
| [expert-workflow-todo.md](expert-workflow-todo.md)                             | Expert Workflow TODO：说明文档。                                               |
| [expert-workflow.md](expert-workflow.md)                                       | Expert Workflow Runtime：说明文档。                                            |
| [extension-discovery-priority.md](extension-discovery-priority.md)             | Extension Discovery Priority：说明文档。                                       |
| [hooks.md](hooks.md)                                                           | ZCode CLI Hooks 设计 v2：说明文档。                                            |
| [i18n.md](i18n.md)                                                             | i18n Runtime：说明文档。                                                       |
| [ink-tui-renderer.md](ink-tui-renderer.md)                                     | Ink TUI Renderer：说明文档。                                                   |
| [input-history.md](input-history.md)                                           | Input History：说明文档。                                                      |
| [live-session-updates.md](live-session-updates.md)                             | Live Session Updates：说明文档。                                               |
| [local-setting-migrations.md](local-setting-migrations.md)                     | Local Settings And SQLite Migrations：说明文档。                               |
| [logging.md](logging.md)                                                       | Logging and Trace：说明文档。                                                  |
| [mcp-node-fallback.md](mcp-node-fallback.md)                                   | MCP Stdio Node Fallback (Electron Node)：说明文档。                            |
| [mcp.md](mcp.md)                                                               | MCP Minimal Integration：说明文档。                                            |
| [message-attachments.md](message-attachments.md)                               | 消息附件与多模态输入：说明文档。                                               |
| [multi-workspace.md](multi-workspace.md)                                       | Multi-Workspace / `--add-dir` 设计草案 v2：说明文档。                          |
| [network-capture-debug.md](network-capture-debug.md)                           | Debug Network Capture：说明文档。                                              |
| [official-command-endpoint.md](official-command-endpoint.md)                   | Official Command Endpoint：说明文档。                                          |
| [permission-broker.md](permission-broker.md)                                   | Permission Broker 设计 v2：说明文档。                                          |
| [permission-responder-race.md](permission-responder-race.md)                   | PermissionRequest Hook 与审批交互竞速（Permission Responder Race）：说明文档。 |
| [plugin-compat.md](plugin-compat.md)                                           | Claude Plugin Compatibility：说明文档。                                        |
| [pre-commit-quality-gate.md](pre-commit-quality-gate.md)                       | Pre-commit Quality Gate：说明文档。                                            |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                               |
| [rewind-compact.md](rewind-compact.md)                                         | Rewind 与 Compact 协同设计 v2：说明文档。                                      |
| [runtime-refactor.md](runtime-refactor.md)                                     | Runtime Refactor：说明文档。                                                   |
| [sea-cross-target-packaging.md](sea-cross-target-packaging.md)                 | SEA Cross-Target Packaging：说明文档。                                         |
| [sea-smb-upload.md](sea-smb-upload.md)                                         | SEA SMB Upload：说明文档。                                                     |
| [session-event-store-retention.md](session-event-store-retention.md)           | Session Event Store 保留策略（内存 event store 的 turn 窗口淘汰）：说明文档。  |
| [session-eventlog.example.jsonl](session-eventlog.example.jsonl)               | session-eventlog.example 模块的资源或工程文件。                                |
| [session-idle-deactivation.md](session-idle-deactivation.md)                   | Session Resident Pool（app-server 进程内混合常驻池）：说明文档。               |
| [session-persistence.md](session-persistence.md)                               | Session Persistence：说明文档。                                                |
| [session-runtime-lifecycle.md](session-runtime-lifecycle.md)                   | Session runtime 生命周期：说明文档。                                           |
| [session-target.md](session-target.md)                                         | Session Goal：说明文档。                                                       |
| [session-title-generation.md](session-title-generation.md)                     | Session Title Generation：说明文档。                                           |
| [skill-command-enable-override.md](skill-command-enable-override.md)           | Skill / Command 可用性覆盖（config.json）：说明文档。                          |
| [skill.md](skill.md)                                                           | Skill Integration Plan：说明文档。                                             |
| [streaming-runtime-plan.md](streaming-runtime-plan.md)                         | Streaming Runtime Production Plan：说明文档。                                  |
| [tui-ask-user-question.md](tui-ask-user-question.md)                           | AskUserQuestion TUI 规划：说明文档。                                           |
| [tui-borderless-layout.md](tui-borderless-layout.md)                           | TUI Borderless Layout：说明文档。                                              |
| [tui-copy-registry.md](tui-copy-registry.md)                                   | TUI Copy Registry：说明文档。                                                  |
| [tui-file-mentions.md](tui-file-mentions.md)                                   | TUI File Mentions：说明文档。                                                  |
| [tui-idle-logo-animation.md](tui-idle-logo-animation.md)                       | TUI Empty Transcript Logo：说明文档。                                          |
| [tui-image-paste.md](tui-image-paste.md)                                       | TUI Image Paste：说明文档。                                                    |
| [tui-input-active-status.md](tui-input-active-status.md)                       | TUI Input Active Status：说明文档。                                            |
| [tui-input-session-panel.md](tui-input-session-panel.md)                       | TUI Input Session Panel：说明文档。                                            |
| [tui-markdown-rendering.md](tui-markdown-rendering.md)                         | TUI Markdown Rendering：说明文档。                                             |
| [tui-mode-switching.md](tui-mode-switching.md)                                 | TUI Mode Switching：说明文档。                                                 |
| [tui-model-selection.md](tui-model-selection.md)                               | TUI Model Selection：说明文档。                                                |
| [tui-mouse-scrollback.md](tui-mouse-scrollback.md)                             | TUI Transcript Scrollback：说明文档。                                          |
| [tui-multiline-input.md](tui-multiline-input.md)                               | TUI Multiline Input：说明文档。                                                |
| [tui-network-status-panel.md](tui-network-status-panel.md)                     | TUI Network Status Projection：说明文档。                                      |
| [tui-opentui-sea-packaging.md](tui-opentui-sea-packaging.md)                   | OpenTUI Node Runtime In SEA：说明文档。                                        |
| [tui-responsive-sidebar.md](tui-responsive-sidebar.md)                         | TUI Responsive Sidebar：说明文档。                                             |
| [tui-selection-copy.md](tui-selection-copy.md)                                 | TUI Selection Copy：说明文档。                                                 |
| [tui-selection-list.md](tui-selection-list.md)                                 | TUI Selection List：说明文档。                                                 |
| [tui-sidebar-production-chrome.md](tui-sidebar-production-chrome.md)           | TUI Sidebar Production Chrome：说明文档。                                      |
| [tui-sidebar-session-modified-files.md](tui-sidebar-session-modified-files.md) | TUI Sidebar Session Modified Files：说明文档。                                 |
| [tui-sidebar-workspace.md](tui-sidebar-workspace.md)                           | TUI Sidebar Workspace：说明文档。                                              |
| [tui-slash-command-suggestions.md](tui-slash-command-suggestions.md)           | TUI Slash Command Suggestions：说明文档。                                      |
| [tui-theme.md](tui-theme.md)                                                   | TUI Theme：说明文档。                                                          |
| [tui-thought-placeholder.md](tui-thought-placeholder.md)                       | TUI Thought Placeholder：说明文档。                                            |
| [tui-todo-display.md](tui-todo-display.md)                                     | TUI Todo Display：说明文档。                                                   |
| [tui-tool-call-detail-blocks.md](tui-tool-call-detail-blocks.md)               | TUI Tool Call Detail Blocks：说明文档。                                        |
| [tui-transcript-message-rows.md](tui-transcript-message-rows.md)               | TUI Transcript Message Rows：说明文档。                                        |
| [tui-turn-elapsed.md](tui-turn-elapsed.md)                                     | TUI Turn Elapsed Indicator：说明文档。                                         |
| [turn-cancellation.md](turn-cancellation.md)                                   | Turn Cancellation：说明文档。                                                  |
| [usage-observability.md](usage-observability.md)                               | Usage Observability：说明文档。                                                |
| [visualize-reference-format.md](visualize-reference-format.md)                 | Visualize 回复引用格式：说明文档。                                             |
| [workflow-expert-runtime-split.md](workflow-expert-runtime-split.md)           | Expert Workflow Runtime Split：说明文档。                                      |
| [workflow-failure-recovery.md](workflow-failure-recovery.md)                   | Workflow Failure Recovery：说明文档。                                          |
| [workflow-script.md](workflow-script.md)                                       | Script Workflow Runtime：说明文档。                                            |
| [workflow-session-linking.md](workflow-session-linking.md)                     | Workflow Session Linking：说明文档。                                           |
| [zcode-protocol-agent-server.md](zcode-protocol-agent-server.md)               | ZCode Protocol Agent Server：说明文档。                                        |

<!-- qingqi-directory-index:end -->
