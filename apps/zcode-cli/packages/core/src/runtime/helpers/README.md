# helpers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 helpers 实现源码。

### 文件

| 文件                                                                               | 简要说明                                                                                                                                                 |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [agent-listing.ts](agent-listing.ts)                                               | 持久化成功后才提交到权威历史，失败不能让后续请求误判为已通知。                                                                                           |
| [attachment-artifacts.ts](attachment-artifacts.ts)                                 | 内存媒体仍可供当前请求使用时吞掉写入失败，会落下冷恢复无法重建的成功历史。                                                                               |
| [attachment-data-url.ts](attachment-data-url.ts)                                   | base64 正文对应的原始字节数（无需解码）。                                                                                                                |
| [attachment-image.ts](attachment-image.ts)                                         | 实现或公开接口：prepareImageDataUrl、inferImageMimeFromPath。                                                                                            |
| [attachment-media-resolver.ts](attachment-media-resolver.ts)                       | 实现或公开接口：resolveInlineMediaAttachment、resolveLocalMediaAttachment。                                                                              |
| [attachment-path-reference.ts](attachment-path-reference.ts)                       | 原说明只存在于 contentBlock 时，冷恢复会丢失降级原因和读取提示，改变模型历史前缀。                                                                       |
| [attachment-pdf.ts](attachment-pdf.ts)                                             | 实现或公开接口：PDF_INPUT_MAX_BYTES、parseInlinePdfDataUrl、isPdfBytes。                                                                                 |
| [attachment-placeholder.ts](attachment-placeholder.ts)                             | 无效 media data URL 虽已降级为占位文本，过去仍会通过 file part 的 url                                                                                    |
| [attachment-video.ts](attachment-video.ts)                                         | video 附件共用的 mime 推断与大小校验。                                                                                                                   |
| [attachments.ts](attachments.ts)                                                   | \* 附件 → TurnStarted 事件的轻量展示元信息（TurnAttachmentMeta）。                                                                                       |
| [child-client-ports.ts](child-client-ports.ts)                                     | child runtime 的「对外交互」端口派生（唯一出口）                                                                                                         |
| [commands.ts](commands.ts)                                                         | 实现或公开接口：parseCompactCommand、parseRewindCommand。                                                                                                |
| [compact-media.ts](compact-media.ts)                                               | video 与 image/document 同语义：retry 媒体瘦身漏掉 video 会让大体积 base64                                                                               |
| [compact-post-reminders.ts](compact-post-reminders.ts)                             | compaction 附件：补回的文件内容或引用提示，按选择顺序。                                                                                                  |
| [compact-preservation.ts](compact-preservation.ts)                                 | 原因：runtime 与数据库的 user/attachment 数量不是一一对应，尤其 synthetic                                                                                |
| [compact-selection.ts](compact-selection.ts)                                       | 实现或公开接口：CompactEntrySelection、selectCompactEntries、selectCompactEntriesAfterPromptTooLong、selectCompactEntriesForInitialPromptTooLong。       |
| [compact.ts](compact.ts)                                                           | compact 后只保留 metadata 标记的 prefix，避免用户 literal <system-reminder> 被文本规则误留。                                                             |
| [context-usage-breakdown.ts](context-usage-breakdown.ts)                           | \* context_usage_snapshot 调试日志里每个粗类别的贡献者。                                                                                                 |
| [conversation-quotes.ts](conversation-quotes.ts)                                   | 引用只在模型边界转为材料，不能混入 canonical 用户正文或解析成控制命令。                                                                                  |
| [conversation.ts](conversation.ts)                                                 | \* 隐藏提醒记录：公告、批次提示、中断标记等只给模型看的 system_reminder 记录。它是模型上下文，                                                           |
| [data.ts](data.ts)                                                                 | 实现或公开接口：isRuntimeDiffHunk、isPlainRecord、objectKeys、stringProperty。                                                                           |
| [gen-ui-output.test.ts](gen-ui-output.test.ts)                                     | 目录随环境公告发送；Desktop 段只声明支持 Gen UI，不含按会话变化的路径。                                                                                  |
| [gen-ui-output.ts](gen-ui-output.ts)                                               | \* 会话的 Gen UI 输出目录；fork 时传子会话 id，取子会话自己的目录。                                                                                      |
| [index.ts](index.ts)                                                               | index 的实现文件。                                                                                                                                       |
| [media-attachment-path.ts](media-attachment-path.ts)                               | inline 只表示 provider-ready 媒体，不保证存在可重建的 durable artifact。                                                                                 |
| [media-budget.ts](media-budget.ts)                                                 | 独立的视频预算无法约束请求总量；所有媒体统一按编码后的体积计入 40MiB，                                                                                   |
| [media-capability.ts](media-capability.ts)                                         | 实现或公开接口：MediaCapabilityProjection、projectMessagesForInputFormat、logMediaCapabilityProjection。                                                 |
| [media-observability.ts](media-observability.ts)                                   | 实现或公开接口：logResolvedTurnAttachments、logModelRequestMediaSummary。                                                                                |
| [model-anomaly.ts](model-anomaly.ts)                                               | 实现或公开接口：detectRepeatedToolCallWarnings、detectToolCallBudgetWarning、buildRepeatedToolCallReminderBody、buildToolCallBudgetReminderBody。        |
| [model-errors.ts](model-errors.ts)                                                 | GLM（MaaS）输出侧安全审核用非标准的 sensitive 终止流；AI SDK 只认 content-filter。                                                                       |
| [model-tool-call-validation.ts](model-tool-call-validation.ts)                     | Adapter 后仍可能存在自定义 Model 实现；runtime admission 必须与                                                                                          |
| [official-cua-media.ts](official-cua-media.ts)                                     | 实现或公开接口：OFFICIAL_CUA_RASTER_UNAVAILABLE_TEXT、officialCuaImageRefIndexesForUnavailableMedia、officialCuaRasterUnavailableBlock。                 |
| [permission-broker.ts](permission-broker.ts)                                       | 实现或公开接口：isResolvablePermissionBroker、isInspectablePermissionBroker。                                                                            |
| [permission-grant-resume.ts](permission-grant-resume.ts)                           | 授权 receipt 在恢复时仅提供辅助标记；格式损坏不能阻断历史及执行状态恢复。                                                                                |
| [persisted-remote-session-path-repair.ts](persisted-remote-session-path-repair.ts) | \* 旧版把 workspaceIdentity 当成 cwd，或追加到真实 workspacePath 后落库。                                                                                |
| [plan-file-continuity.ts](plan-file-continuity.ts)                                 | 实现或公开接口：resolveApprovedPlanFilePath、writeApprovedPlanFile、readApprovedPlanFileReferenceEntry、formatPlanFileReference。                        |
| [project-memory-agent.ts](project-memory-agent.ts)                                 | Extraction 继承产生该工作的 Turn Model。                                                                                                                 |
| [project-memory-dream.ts](project-memory-dream.ts)                                 | 当前产品链路不自动触发 Dream；保留可等待的 handler，待 project transcript 隔离方案确定后再接线。                                                         |
| [project-memory-extraction.ts](project-memory-extraction.ts)                       | 原因：headless 只关闭自动 Extraction，必须在读取快照或访问文件前返回，避免后台副作用。                                                                   |
| [project-memory-recall.ts](project-memory-recall.ts)                               | Selector 必须得到严格 JSON Schema；禁止因能力不足另选一个隐式 Provider/Model。                                                                           |
| [project-memory.ts](project-memory.ts)                                             | 受管 worktree 会话与源仓库共用项目记忆（docs/git/worktree.md §6.6.3）。                                                                                  |
| [project.ts](project.ts)                                                           | 实现或公开接口：titleFromInput、slugify、projectIdFromDirectory。                                                                                        |
| [prompt-snapshot.ts](prompt-snapshot.ts)                                           | 主会话 prompt 快照（docs/design/v2/loop/prompt-snapshot.md）                                                                                             |
| [provider-business-error.ts](provider-business-error.ts)                           | 实现或公开接口：findProviderBusinessFailureInMetadata、createCoreErrorFromProviderBusinessLike。                                                         |
| [provider-entry-origins.ts](provider-entry-origins.ts)                             | 空闲整批相邻两条通知块之间的分隔。                                                                                                                       |
| [provider-mid-conversation-system.ts](provider-mid-conversation-system.ts)         | 没有合法锚点时整组降级为一条 user reminder，只包一次。                                                                                                   |
| [provider-request-messages.ts](provider-request-messages.ts)                       | 仅用于内部归属；runtime metadata 不会进入 `messages`。                                                                                                   |
| [README.md](README.md)                                                             | 本目录用途、子目录与逐文件说明。                                                                                                                         |
| [rewind.ts](rewind.ts)                                                             | 实现或公开接口：WORKSPACE_CHECKPOINT_CONTENT_TYPE、getFileMutationCheckpointCandidate、stringifyWorkspaceCheckpointArtifact、selectCheckpointForRewind。 |
| [runtime-provider-request-messages.ts](runtime-provider-request-messages.ts)       | 本次请求是否走 MCS 的唯一判断：provider 投影与 system prompt 的 Harness 文案共用。                                                                       |
| [runtime-reminders.ts](runtime-reminders.ts)                                       | 实现或公开接口：RUNTIME_MODE_REMINDER_CONFIG、TODO_REMINDER_CONFIG、buildSilentTurnReminderBody、TodoReminderTurnCounts。                                |
| [runtime-tools.ts](runtime-tools.ts)                                               | submit_result 只在注入了 workflowSubmitPort 的 workflow actor 会话注册。以端口存在为门，                                                                 |
| [steering.ts](steering.ts)                                                         | copy by value + provenance：child 用新 local id 排序/渲染                                                                                                |
| [streaming-tool-ledger.ts](streaming-tool-ledger.ts)                               | 实现或公开接口：createStreamingToolAttemptId、createStreamRecoveryAnchorId、emitStreamingToolLedgerUpdate、emitStreamRecoveryAnchor。                    |
| [subagent-interaction-broker.ts](subagent-interaction-broker.ts)                   | 修复原因：子 agent 的 permission / AskUserQuestion / ExitPlanMode 都需要父 task 的 UI 响应；                                                             |
| [subagent-selection.ts](subagent-selection.ts)                                     | 显式 profile 是待解析意图；继承与内部 override 已有执行归属，不重新对应账号。                                                                            |
| [tool-allowlist.ts](tool-allowlist.ts)                                             | \* workflow child 运行时额外不注册的工具。                                                                                                               |
| [tool-result-media-persistence.ts](tool-result-media-persistence.ts)               | 已完成工具的媒体属于结果收尾；继承本轮 Stop 信号会中断保存并丢失冷恢复内容。                                                                             |
| [tool-result.ts](tool-result.ts)                                                   | \* 一批工具结果交给模型的 entries：每个结果一条 tool result，之后是这批的附件。                                                                          |
| [total-tokens-budget.ts](total-tokens-budget.ts)                                   | \* 每个 runtime 一份的预算计数（主会话、每个子 agent 各一份）。只在内存，resume 时重新开始。                                                             |
| [turn-errors.ts](turn-errors.ts)                                                   | 宿主用此窄入口中止 turn，同时要求 core 持久化 TurnError 而不是用户取消。                                                                                 |
| [turn-file-changes.ts](turn-file-changes.ts)                                       | 实现或公开接口：recordTurnFileChange、buildTurnFileChangeSummary。                                                                                       |

<!-- qingqi-directory-index:end -->
