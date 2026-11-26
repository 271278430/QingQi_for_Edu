# ai-elements

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 ai elements 界面组件。

### 文件

| 文件                                                       | 简要说明                                                                                               |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [agent.tsx](agent.tsx)                                     | \* Derived from vercel/ai-elements (packages/elements/src/agent.tsx).                                  |
| [artifact.tsx](artifact.tsx)                               | \* Derived from vercel/ai-elements (packages/elements/src/artifact.tsx).                               |
| [attachments.tsx](attachments.tsx)                         | \* Derived from vercel/ai-elements (packages/elements/src/attachments.tsx).                            |
| [audio-player.tsx](audio-player.tsx)                       | 实现或公开接口：AudioPlayerProps、AudioPlayer、AudioPlayerElementProps、AudioPlayerElement。           |
| [canvas.tsx](canvas.tsx)                                   | 实现或公开接口：Canvas。                                                                               |
| [chain-of-thought.tsx](chain-of-thought.tsx)               | 实现或公开接口：ChainOfThoughtProps、ChainOfThought、ChainOfThoughtHeaderProps、ChainOfThoughtHeader。 |
| [chat-loading.tsx](chat-loading.tsx)                       | 球面密度独立于 Z 点阵，避免调整字形间距时意外改变球体；动画几何只生成一次。                            |
| [checkpoint.tsx](checkpoint.tsx)                           | \* Derived from vercel/ai-elements (packages/elements/src/checkpoint.tsx).                             |
| [code-block.tsx](code-block.tsx)                           | \* Derived from vercel/ai-elements (packages/elements/src/code-block.tsx).                             |
| [commit.tsx](commit.tsx)                                   | \* Derived from vercel/ai-elements (packages/elements/src/commit.tsx).                                 |
| [confirmation.tsx](confirmation.tsx)                       | \* Derived from vercel/ai-elements (packages/elements/src/confirmation.tsx).                           |
| [connection.tsx](connection.tsx)                           | \* Derived from vercel/ai-elements (packages/elements/src/connection.tsx).                             |
| [context.tsx](context.tsx)                                 | \* Derived from vercel/ai-elements (packages/elements/src/context.tsx).                                |
| [controls.tsx](controls.tsx)                               | \* Derived from vercel/ai-elements (packages/elements/src/controls.tsx).                               |
| [conversation.tsx](conversation.tsx)                       | \* Derived from vercel/ai-elements (packages/elements/src/conversation.tsx).                           |
| [diagram-preview-dialog.tsx](diagram-preview-dialog.tsx)   | Mermaid 输出的 SVG 常见为 width="100%" + max-width=viewBox 宽度。                                      |
| [edge.tsx](edge.tsx)                                       | \* Derived from vercel/ai-elements (packages/elements/src/edge.tsx).                                   |
| [environment-variables.tsx](environment-variables.tsx)     | Default noop for context default value                                                                 |
| [file-tree.tsx](file-tree.tsx)                             | Default noop for context default value                                                                 |
| [image-preview-dialog.tsx](image-preview-dialog.tsx)       | 媒体 gallery 切离 video 时旧播放器可能继续解码或发声；显式暂停，                                       |
| [image-thumbnail-gallery.tsx](image-thumbnail-gallery.tsx) | 实现或公开接口：imageThumbnailTriggerClassName、imageThumbnailClassName、ImageThumbnailGallery。       |
| [image.tsx](image.tsx)                                     | \* Derived from vercel/ai-elements (packages/elements/src/image.tsx).                                  |
| [inline-citation.tsx](inline-citation.tsx)                 | 实现或公开接口：InlineCitationProps、InlineCitation、InlineCitationTextProps、InlineCitationText。     |
| [jsx-preview.tsx](jsx-preview.tsx)                         | Bugfix: react-jsx-parser 的声明在 NodeNext + verbatimModuleSyntax 下会被推成模块对象，                 |
| [markdown-blockquote.tsx](markdown-blockquote.tsx)         | 实现或公开接口：MarkdownBlockquoteProps、MarkdownBlockquote。                                          |
| [markdown-image.tsx](markdown-image.tsx)                   | \* Streamdown 会在 rehype 前按空行拆块。仅移除连续纯图片行之间的空行，让同组图片进入                   |
| [markdown-list.tsx](markdown-list.tsx)                     | 有序列表编号到两位/三位时，list-outside 会把 marker 向父容器外侧扩展；                                 |
| [markdown-table.tsx](markdown-table.tsx)                   | assistant markdown 属于不可信输入，CSV 被 Excel/Numbers/LibreOffice                                    |
| [mermaid-block.tsx](mermaid-block.tsx)                     | \* 应用主题（store 耦合剥离）：由调用方从上层状态传入。                                                |
| [message.tsx](message.tsx)                                 | \* Derived from vercel/ai-elements (packages/elements/src/message.tsx).                                |
| [mic-selector.tsx](mic-selector.tsx)                       | 实现或公开接口：useAudioDevices、MicSelectorProps、MicSelector、MicSelectorTriggerProps。              |
| [model-selector.tsx](model-selector.tsx)                   | oxlint-disable-next-l                                                                                  |
| [node.tsx](node.tsx)                                       | \* Derived from vercel/ai-elements (packages/elements/src/node.tsx).                                   |
| [open-in-chat.tsx](open-in-chat.tsx)                       | 实现或公开接口：OpenInProps、OpenIn、OpenInContentProps、OpenInContent。                               |
| [package-info.tsx](package-info.tsx)                       | 实现或公开接口：PackageInfoHeaderProps、PackageInfoHeader、PackageInfoNameProps、PackageInfoName。     |
| [panel.tsx](panel.tsx)                                     | \* Derived from vercel/ai-elements (packages/elements/src/panel.tsx).                                  |
| [persona.tsx](persona.tsx)                                 | \* Derived from vercel/ai-elements (packages/elements/src/persona.tsx).                                |
| [plan.tsx](plan.tsx)                                       | \* Derived from vercel/ai-elements (packages/elements/src/plan.tsx).                                   |
| [prompt-input-actions.tsx](prompt-input-actions.tsx)       | \* Derived from vercel/ai-elements (packages/elements/src/prompt-input.tsx).                           |
| [prompt-input-buttons.tsx](prompt-input-buttons.tsx)       | \* Derived from vercel/ai-elements (packages/elements/src/prompt-input.tsx).                           |
| [prompt-input-primitives.tsx](prompt-input-primitives.tsx) | \* Derived from vercel/ai-elements (packages/elements/src/prompt-input.tsx).                           |
| [prompt-input-textarea.tsx](prompt-input-textarea.tsx)     | \* Derived from vercel/ai-elements (packages/elements/src/prompt-input.tsx).                           |
| [prompt-input.tsx](prompt-input.tsx)                       | \* Derived from vercel/ai-elements (packages/elements/src/prompt-input.tsx).                           |
| [queue.tsx](queue.tsx)                                     | \* Derived from vercel/ai-elements (packages/elements/src/queue.tsx).                                  |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                                       |
| [reasoning.tsx](reasoning.tsx)                             | \* Derived from vercel/ai-elements (packages/elements/src/reasoning.tsx).                              |
| [sandbox.tsx](sandbox.tsx)                                 | \* Derived from vercel/ai-elements (packages/elements/src/sandbox.tsx).                                |
| [schema-display.tsx](schema-display.tsx)                   | Highlight path parameters                                                                              |
| [shimmer.tsx](shimmer.tsx)                                 | \* Derived from vercel/ai-elements (packages/elements/src/shimmer.tsx).                                |
| [snippet.tsx](snippet.tsx)                                 | \* Derived from vercel/ai-elements (packages/elements/src/snippet.tsx).                                |
| [sources.tsx](sources.tsx)                                 | \* Derived from vercel/ai-elements (packages/elements/src/sources.tsx).                                |
| [speech-input.tsx](speech-input.tsx)                       | \* Callback for when audio is recorded using MediaRecorder fallback.                                   |
| [stack-trace.tsx](stack-trace.tsx)                         | Regex patterns for parsing stack traces                                                                |
| [streamdown-controls.ts](streamdown-controls.ts)           | 交互调整：表格本身已经能在消息流里完整浏览，再保留 fullscreen 入口会把阅读路径打断。                   |
| [suggestion.tsx](suggestion.tsx)                           | \* Derived from vercel/ai-elements (packages/elements/src/suggestion.tsx).                             |
| [task.tsx](task.tsx)                                       | \* Derived from vercel/ai-elements (packages/elements/src/task.tsx).                                   |
| [terminal.tsx](terminal.tsx)                               | \* Derived from vercel/ai-elements (packages/elements/src/terminal.tsx).                               |
| [test-results.tsx](test-results.tsx)                       | \* Derived from vercel/ai-elements (packages/elements/src/test-results.tsx).                           |
| [tool.tsx](tool.tsx)                                       | \* Derived from vercel/ai-elements (packages/elements/src/tool.tsx).                                   |
| [toolbar.tsx](toolbar.tsx)                                 | \* Derived from vercel/ai-elements (packages/elements/src/toolbar.tsx).                                |
| [transcription.tsx](transcription.tsx)                     | 实现或公开接口：TranscriptionProps、Transcription、TranscriptionSegmentProps、TranscriptionSegment。   |
| [voice-selector.tsx](voice-selector.tsx)                   | 实现或公开接口：useVoiceSelector、VoiceSelectorProps、VoiceSelector、VoiceSelectorTriggerProps。       |
| [web-preview.tsx](web-preview.tsx)                         | Sync input value with context URL when it changes externally (derived state pattern)                   |

<!-- qingqi-directory-index:end -->
