# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/tui 基础工程中的 src 实现源码。

### 子目录

| 目录                      | 存放内容                                 |
| ------------------------- | ---------------------------------------- |
| [theme/](theme/README.md) | @zcode/tui 基础工程中的 theme 实现源码。 |

### 文件

| 文件                                                               | 简要说明                                                                                                                               |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| [app-approval-panel.tsx](app-approval-panel.tsx)                   | \* 审批区：请求不属于当前主会话时（例如 CreateSession 建的后台会话），在面板上方标明来源。                                             |
| [app-approval.ts](app-approval.ts)                                 | 实现或公开接口：decisionsForApproval、handleApprovalKey、approvalDecisionLabel、isOfficialCuaProjectApproval。                         |
| [app-clipboard-image.ts](app-clipboard-image.ts)                   | 实现或公开接口：useClipboardImagePaste。                                                                                               |
| [app-compact-timeline.ts](app-compact-timeline.ts)                 | 实现或公开接口：compactCommandFromText、isCompactSlashCommand、createLocalCompactTimelineMessage、compactTimelineMessageFromPayload。  |
| [app-components.tsx](app-components.tsx)                           | Fixed one-row heights let wrapped text draw over later commands in narrow terminals.                                                   |
| [app-copy.ts](app-copy.ts)                                         | 实现或公开接口：SelectionCopyResult、createSelectionCopyHandler、hasCopyableSelectionText、selectionCopyStatus。                       |
| [app-effort-command.ts](app-effort-command.ts)                     | 实现或公开接口：useEffortCommandController。                                                                                           |
| [app-effort-suggestion-panel.tsx](app-effort-suggestion-panel.tsx) | 实现或公开接口：EffortSuggestionPanel。                                                                                                |
| [app-empty-transcript.tsx](app-empty-transcript.tsx)               | 实现或公开接口：ZCODE_LOGO_LINES、EmptyTranscriptLogo。                                                                                |
| [app-event-data.ts](app-event-data.ts)                             | 实现或公开接口：validContextUsage、contextWindowFromPayload、usageFromPayload、cacheStatsFromPayload。                                 |
| [app-events.ts](app-events.ts)                                     | 实现或公开接口：applySessionEventToState。                                                                                             |
| [app-file-mention-panel.tsx](app-file-mention-panel.tsx)           | 实现或公开接口：FileMentionPanel。                                                                                                     |
| [app-file-mentions.ts](app-file-mentions.ts)                       | 实现或公开接口：FILE_MENTION_VISIBLE_COUNT、ActiveFileMention、FileMentionState、useFileMentionController。                            |
| [app-input-history.ts](app-input-history.ts)                       | 实现或公开接口：useInputHistory。                                                                                                      |
| [app-input-pane.tsx](app-input-pane.tsx)                           | OpenTUI destroys the previous EditorView during keyed remounts; keep                                                                   |
| [app-input-status.tsx](app-input-status.tsx)                       | 实现或公开接口：InputActiveStatus、InputComposerStatus、inputActiveStatusRow、inputComposerStatusRow。                                 |
| [app-input.ts](app-input.ts)                                       | 实现或公开接口：filterSlashCommands、reconcileSlashSelection、selectedSlashCommand、visibleSlashCommandWindow。                        |
| [app-keyboard-helpers.ts](app-keyboard-helpers.ts)                 | model streaming output still leaves the composer editable; blocking                                                                    |
| [app-keyboard-suggestions.ts](app-keyboard-suggestions.ts)         | 实现或公开接口：handleSuggestionNavigationKey。                                                                                        |
| [app-keyboard.ts](app-keyboard.ts)                                 | 实现或公开接口：useTuiKeyboardControls。                                                                                               |
| [app-locale.ts](app-locale.ts)                                     | 实现或公开接口：DEFAULT_TUI_COPY。                                                                                                     |
| [app-markdown-theme.ts](app-markdown-theme.ts)                     | 实现或公开接口：markdownSyntaxRules、createMarkdownSyntaxStyle。                                                                       |
| [app-markdown.tsx](app-markdown.tsx)                               | 实现或公开接口：detectMarkdownRenderMode、MarkdownText。                                                                               |
| [app-mcp-status.ts](app-mcp-status.ts)                             | 实现或公开接口：useMcpSidebarStatus。                                                                                                  |
| [app-mode-command.ts](app-mode-command.ts)                         | 实现或公开接口：modeCommandQuery、filterModeOptions、selectedModeOption、useModeCommandController。                                    |
| [app-mode-suggestion-panel.tsx](app-mode-suggestion-panel.tsx)     | 实现或公开接口：ModeSuggestionPanel、visibleModeOptionWindow。                                                                         |
| [app-mode.ts](app-mode.ts)                                         | Keyboard handlers fire-and-forget this promise, so reflect the local mode                                                              |
| [app-model-command.ts](app-model-command.ts)                       | Opening from an empty catalog must admit selection when the fresh catalog arrives.                                                     |
| [app-model-ref.ts](app-model-ref.ts)                               | Display only; model commands carry ref directly instead of parsing this value.                                                         |
| [app-model-streaming.ts](app-model-streaming.ts)                   | provider tool-input deltas are JSON arguments for a future tool call, not assistant text.                                              |
| [app-model-suggestion-panel.tsx](app-model-suggestion-panel.tsx)   | 实现或公开接口：ModelSuggestionPanel。                                                                                                 |
| [app-model.ts](app-model.ts)                                       | 实现或公开接口：Message、TranscriptPart、TimelineMessage、TuiTextFormat。                                                              |
| [app-modified-files.ts](app-modified-files.ts)                     | 实现或公开接口：ModifiedFileStat、modifiedFileStatsFromToolResultPayload、applyModifiedFileStats。                                     |
| [app-motion.tsx](app-motion.tsx)                                   | 实现或公开接口：SHIMMER_SWEEP_PERIOD_MS、SPINNER_FRAME_INTERVAL_MS、SPINNER_WIDTH、ShimmerText。                                       |
| [app-network-events.ts](app-network-events.ts)                     | 实现或公开接口：applyNetworkRequestEvent、applyModelNetworkEvent。                                                                     |
| [app-permission.ts](app-permission.ts)                             | \* CreateWorkflow 的确认 gate 在 CLI 侧自动放行。                                                                                      |
| [app-question-panel.tsx](app-question-panel.tsx)                   | 实现或公开接口：QuestionPanel。                                                                                                        |
| [app-question-state.ts](app-question-state.ts)                     | 实现或公开接口：createQuestionPromptState、handleQuestionKey。                                                                         |
| [app-queued-inputs.tsx](app-queued-inputs.tsx)                     | 实现或公开接口：QueuedInputPanel、upsertQueuedInput、removeQueuedInputs。                                                              |
| [app-result.ts](app-result.ts)                                     | 实现或公开接口：useTuiApplyResult。                                                                                                    |
| [app-selection-keyboard.ts](app-selection-keyboard.ts)             | selectedIndex is global within the filtered rows, so the rendered                                                                      |
| [app-selection-panel.tsx](app-selection-panel.tsx)                 | 实现或公开接口：SelectionPanel。                                                                                                       |
| [app-selection-state.ts](app-selection-state.ts)                   | 实现或公开接口：createSelectionState。                                                                                                 |
| [app-session-event-handler.ts](app-session-event-handler.ts)       | \* 已应用事件 id 的记忆窗。                                                                                                            |
| [app-shiki-diff-view.tsx](app-shiki-diff-view.tsx)                 | 实现或公开接口：ShikiDiffView、diffViewForWidth、buildDiffRows、buildSplitDiffRows。                                                   |
| [app-shiki-highlighter.ts](app-shiki-highlighter.ts)               | 实现或公开接口：ShikiHighlightSegment、inferShikiLanguage、highlightShikiCodeLines、resetShikiHighlighterForTest。                     |
| [app-sidebar-api.tsx](app-sidebar-api.tsx)                         | 实现或公开接口：ApiSection。                                                                                                           |
| [app-sidebar-keyboard.ts](app-sidebar-keyboard.ts)                 | 实现或公开接口：handleSidebarShortcutKey。                                                                                             |
| [app-sidebar-layout.ts](app-sidebar-layout.ts)                     | 实现或公开接口：SIDEBAR_WIDTH、SIDEBAR_HORIZONTAL_PADDING_COLUMNS、SIDEBAR_CONTENT_WIDTH、SIDEBAR_OVERLAY_BACKGROUND。                 |
| [app-sidebar-mcp.tsx](app-sidebar-mcp.tsx)                         | 实现或公开接口：McpSection。                                                                                                           |
| [app-sidebar-modified-files.tsx](app-sidebar-modified-files.tsx)   | 实现或公开接口：ModifiedFilesSection。                                                                                                 |
| [app-sidebar-section-header.tsx](app-sidebar-section-header.tsx)   | 实现或公开接口：SidebarSectionHeader。                                                                                                 |
| [app-sidebar-shortcut.ts](app-sidebar-shortcut.ts)                 | 实现或公开接口：SIDEBAR_LEADER_HINT、SIDEBAR_HIDDEN_STATUS、SIDEBAR_SHOWN_STATUS、SIDEBAR_APIS_COLLAPSED_STATUS。                      |
| [app-sidebar-subagents.tsx](app-sidebar-subagents.tsx)             | 实现或公开接口：SubagentsSection。                                                                                                     |
| [app-sidebar.tsx](app-sidebar.tsx)                                 | 实现或公开接口：Sidebar。                                                                                                              |
| [app-startup.tsx](app-startup.tsx)                                 | 实现或公开接口：TuiStartupScreen。                                                                                                     |
| [app-subagent-events.ts](app-subagent-events.ts)                   | Directory refreshes follow lifecycle boundaries, never individual tokens.                                                              |
| [app-subagent-transcript.ts](app-subagent-transcript.ts)           | Completed replies already exist in persisted history. Replaying historical                                                             |
| [app-subagent-view.tsx](app-subagent-view.tsx)                     | 实现或公开接口：SubagentView。                                                                                                         |
| [app-subagents.ts](app-subagents.ts)                               | An event can invalidate the directory after the loop exits but before                                                                  |
| [app-submit-controller.ts](app-submit-controller.ts)               | 实现或公开接口：useSubmitValue。                                                                                                       |
| [app-submit-resolver.ts](app-submit-resolver.ts)                   | 实现或公开接口：resolveComposerSubmittedText。                                                                                         |
| [app-submit.ts](app-submit.ts)                                     | resume 回放以前只保留 content/role，导致已持久化的 reasoning/tool                                                                      |
| [app-terminal-width.ts](app-terminal-width.ts)                     | 实现或公开接口：truncateDisplay、wordWrappedLineCount、displayWidth。                                                                  |
| [app-theme-sync.ts](app-theme-sync.ts)                             | 实现或公开接口：useTuiThemeSync。                                                                                                      |
| [app-thought-components.tsx](app-thought-components.tsx)           | 实现或公开接口：ThoughtTranscriptPartView、ThoughtTranscriptPartFrame、thoughtPlaceholderLabel。                                       |
| [app-tool-components.tsx](app-tool-components.tsx)                 | tool rows should align with assistant text; child detail rows carry their own indent.                                                  |
| [app-tool-diff-display.ts](app-tool-diff-display.ts)               | 窄屏只保留一列行号，避免旧/新双行号把正文挤出可读区域。                                                                                |
| [app-tool-path-display.ts](app-tool-path-display.ts)               | 实现或公开接口：formatToolFilePath。                                                                                                   |
| [app-tool-transcript.ts](app-tool-transcript.ts)                   | 实现或公开接口：applyToolTranscriptEvent、summarizeToolInput、buildToolTranscriptProjection。                                          |
| [app-transcript-components.tsx](app-transcript-components.tsx)     | speaker labels were visually noisy; only user prompts carry row chrome.                                                                |
| [app-transcript-errors.ts](app-transcript-errors.ts)               | runtime error events often arrive before the rejected prompt promise;                                                                  |
| [app-transcript-stream.ts](app-transcript-stream.ts)               | 实现或公开接口：appendStreamingTextDelta、markStreamingMessageComplete、finalizeStreamProjectedMessages、appendStreamingThoughtDelta。 |
| [app-turn-complete.ts](app-turn-complete.ts)                       | turn_complete 的处理：用量/缓存统计 + 结果兜底。                                                                                       |
| [app-view.tsx](app-view.tsx)                                       | 实现或公开接口：AppView、ComposerInputArea。                                                                                           |
| [app-workflow-card.tsx](app-workflow-card.tsx)                     | CreateWorkflow 的实时工具卡。                                                                                                          |
| [app-workflow-controller.ts](app-workflow-controller.ts)           | dwf 运行态镜像的 TUI 控制器（与 useSidebarController / useInputHistory 同一 hook 惯例）。                                              |
| [app-workflow-events.ts](app-workflow-events.ts)                   | 会话事件 → workflowRuns 镜像的桥（app-events.ts 的 dwf case 只调这一个函数）。                                                         |
| [app-workflow-mirror.ts](app-workflow-mirror.ts)                   | TUI 侧的 workflowRuns 镜像                                                                                                             |
| [app-workflow-seed.ts](app-workflow-seed.ts)                       | 冷启动 / 恢复会话时的镜像回放、补种与 interrupted notice。                                                                             |
| [app.tsx](app.tsx)                                                 | Startup sentinels are diagnostics, not user-visible transcript messages.                                                               |
| [index.ts](index.ts)                                               | index 的实现文件。                                                                                                                     |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                                                       |
| [state.ts](state.ts)                                               | 实现或公开接口：normalizePromptInput、describeSessionEvent、asRecord、stringField。                                                    |
| [tui.tsx](tui.tsx)                                                 | Session replacement can raise SIGPIPE while closing MCP pipes. OpenTUI's                                                               |
| [types.ts](types.ts)                                               | Model picker commands retain the reference separately from their display text.                                                         |

<!-- qingqi-directory-index:end -->
