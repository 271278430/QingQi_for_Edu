# composer

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 composer 实现源码。

### 文件

| 文件                                                                             | 简要说明                                                                                                         |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [attachmentUpload.ts](attachmentUpload.ts)                                       | 附件命令面（UI 侧）：ZCodePromptAttachment（composer 序列化产物）→ AttachmentRef                                 |
| [CodeCommentAttachmentChip.tsx](CodeCommentAttachmentChip.tsx)                   | 实现或公开接口：CodeCommentAttachmentChip。                                                                      |
| [codeCommentPreviewSync.ts](codeCommentPreviewSync.ts)                           | 实现或公开接口：removeCodeCommentPreview。                                                                       |
| [composerAutoFocus.ts](composerAutoFocus.ts)                                     | \* composer 自动聚焦决策（纯函数，脱离 React/DOM 便于单测）。                                                    |
| [composerDraftRevision.ts](composerDraftRevision.ts)                             | 推荐 Prompt 的延迟可信解析需要知道用户是否在等待期间编辑了 Composer。                                            |
| [composerDraftStore.ts](composerDraftStore.ts)                                   | composer parity：v4 composer 的 per-session 草稿持久化（新做，轻量 localStorage）。                              |
| [composerDraftWorkspaceTransfer.ts](composerDraftWorkspaceTransfer.ts)           | 读取编辑器当前值，避免把尚未到持久化时点的文字丢在旧工作区。                                                     |
| [composerPromptContexts.ts](composerPromptContexts.ts)                           | 插件 UI 经 ui/update-model-context 附加；缺省视为空。                                                            |
| [composerSubmissionConfig.ts](composerSubmissionConfig.ts)                       | 在点击提交的瞬间，把 Composer 意图冻结成本次 Submission 的执行配置。                                             |
| [composerSubmissionSettlement.ts](composerSubmissionSettlement.ts)               | Bug 根因（R3A-B-07）：ACK 丢失时远端 ChannelClient dispose 会先 reject 在途 sendText，                           |
| [configPickerState.ts](configPickerState.ts)                                     | 实现或公开接口：V4ComposerConfigPicker、resolveV4ComposerConfigPickerState。                                     |
| [ContextAttachmentPill.tsx](ContextAttachmentPill.tsx)                           | \* 上下文附件共享同一个 pill 与详情浮层外壳，避免各类型复制布局和交互样式。                                      |
| [ConversationBackgroundWorkTrigger.tsx](ConversationBackgroundWorkTrigger.tsx)   | workflow run 单独计数，不并入 bashCount。totalCount 汇总三类后台工作，                                           |
| [conversationDropTarget.ts](conversationDropTarget.ts)                           | \* ConversationComposer 暴露给外层对话表面的文件 drop 接口。                                                     |
| [ConversationSelectionReferenceChip.tsx](ConversationSelectionReferenceChip.tsx) | \* 注释 chip：输入框与历史消息共用。每条注释只算一条（有无评论都一样），                                         |
| [draftWorkspaceDefaults.ts](draftWorkspaceDefaults.ts)                           | 工具条只展示 Composer 的下一次提交选择；Session 不是存活编辑器的补值来源。                                       |
| [ElementMentionSyncPlugin.tsx](ElementMentionSyncPlugin.tsx)                     | 设计模式点选的元素在输入框正文里是元素 token（docs/browser-use/2026-11-03-browser-design-mode-spec.md 第四节）， |
| [escapeStop.ts](escapeStop.ts)                                                   | composer parity：Esc → stop 的忽略判定（纯函数，无宿主依赖）。                                                   |
| [followupModeSettings.ts](followupModeSettings.ts)                               | queue 模式的修饰键发送曾被解释成 guide；“立即发送”实际是队列既有的抢占语义。                                     |
| [modelTriggerDisplay.ts](modelTriggerDisplay.ts)                                 | 切换记录必须保留当时的套餐身份，不能从当前连接或可用模型目录反推历史套餐。                                       |
| [newTaskDraft.ts](newTaskDraft.ts)                                               | 普通新任务与首次分享导入共用初始化；保留 Recent 原意图，由公共 View 解析有效选择。                               |
| [onlineModelFallback.ts](onlineModelFallback.ts)                                 | \* 只确认当前目标 Session 的在线 fallback 已经落到权威投影。                                                     |
| [PptxElementReferenceChip.tsx](PptxElementReferenceChip.tsx)                     | 实现或公开接口：PptxElementReferenceChip。                                                                       |
| [README.md](README.md)                                                           | 本目录用途、子目录与逐文件说明。                                                                                 |
| [sessionConfigTaskCache.ts](sessionConfigTaskCache.ts)                           | \* 把 v4 session 权威配置叠到 workspace 完整目录，供 task → draft 继承使用。                                     |
| [toolbarShortcuts.ts](toolbarShortcuts.ts)                                       | \* V4 composer 工具条键盘热键（composer parity）。                                                               |
| [useCodeCommentContexts.ts](useCodeCommentContexts.ts)                           | 按 composer 草稿 scope 缓存未发送的代码评论：切任务或进入/退出 composer 编辑态后切回，                           |
| [useComposerAttachments.ts](useComposerAttachments.ts)                           | \* 换代重传的兜底上限。dev 实测同一 workspace 可达 runtimeGeneration=4（3 次换代），                             |
| [useConversationSelectionReferences.ts](useConversationSelectionReferences.ts)   | 当前会话的权威 rows；提供时，rewind 删除来源行的带评论注释会被同步移除。                                         |
| [useDraftConfigControl.ts](useDraftConfigControl.ts)                             | 当前编辑由 Composer 持有；进入已有 Session 从当前快照恢复权限/Plan，在线只响应新变化。                           |
| [useDraftModelReadinessGate.ts](useDraftModelReadinessGate.ts)                   | 只有 readiness 已确认或检查本身不可用时，才允许进入 workspace prepare/prewarm。                                  |
| [useDraftRuntimeRebuildGate.ts](useDraftRuntimeRebuildGate.ts)                   | \* 重建窗口上限。实测 agent start→ready 约 550-650ms，createSession 再数百 ms，5s 有充分余量。                   |
| [useDraftSessionPrewarm.ts](useDraftSessionPrewarm.ts)                           | 草稿态 v4 draft session 预热。                                                                                   |
| [useOpenPptxElementReference.ts](useOpenPptxElementReference.ts)                 | 实现或公开接口：useOpenPptxElementReference。                                                                    |
| [usePptxElementReferences.ts](usePptxElementReferences.ts)                       | 按 composer 草稿 scope 缓存未发送的 PPTX 元素引用；切任务或进入/退出编辑态后切回原样恢复。                       |
| [usePrimaryFollowupModifier.ts](usePrimaryFollowupModifier.ts)                   | \* 分屏和多窗口内容树可能同时挂载多个 Composer。修饰键是 window 事实，                                           |
| [useWebElementContexts.ts](useWebElementContexts.ts)                             | 用户在输入框里删掉（会通知浏览器取消选中）                                                                       |
| [V4ComposerCuaEntry.tsx](V4ComposerCuaEntry.tsx)                                 | \* CUA 输入框常驻入口按钮。                                                                                      |
| [V4ComposerModeControls.tsx](V4ComposerModeControls.tsx)                         | Plan 是独立勾选项，三种权限仍为单选；只编辑草稿，不向 Runtime 发切换命令。                                       |
| [V4ComposerToolbar.tsx](V4ComposerToolbar.tsx)                                   | \* V4 composer 工具条。                                                                                          |
| [WebElementContextAttachmentChip.tsx](WebElementContextAttachmentChip.tsx)       | 实现或公开接口：WebElementContextAttachmentChip。                                                                |

<!-- qingqi-directory-index:end -->
