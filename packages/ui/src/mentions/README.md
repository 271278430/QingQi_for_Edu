# mentions

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 mentions 实现源码。

### 子目录

| 目录                                | 存放内容                                     |
| ----------------------------------- | -------------------------------------------- |
| [components/](components/README.md) | @zcode/ui 基础工程中的 components 界面组件。 |
| [nodes/](nodes/README.md)           | @zcode/ui 基础工程中的 nodes 实现源码。      |
| [providers/](providers/README.md)   | @zcode/ui 基础工程中的 providers 实现源码。  |

### 文件

| 文件                                                   | 简要说明                                                                                                 |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| [activePromptInputToken.ts](activePromptInputToken.ts) | ArrowLeft/ArrowRight 只改变 selection，token 文本并未改变。                                              |
| [mentionChip.ts](mentionChip.ts)                       | inline-flex token 用 align-middle 会按父文本基线 + x-height 对齐，不是和行盒视觉中心对齐。               |
| [mentionHelpers.ts](mentionHelpers.ts)                 | 实现或公开接口：getCurrentTextNodeSelection。                                                            |
| [mentionMarkdown.ts](mentionMarkdown.ts)               | Streamdown/rehype-harden 会把 `foo/bar.ts` 这种裸路径当成自定义协议 `foo:`，                             |
| [mentionPanelRouting.ts](mentionPanelRouting.ts)       | \* 输入触发器只负责发现入口，不改变候选选中后的 canonical mention。                                      |
| [MentionPlugin.tsx](MentionPlugin.tsx)                 | 已有 Session 的 id；null/undefined = 新建草稿。决定 Plugins 分组的 catalog authority。                   |
| [mentionSearch.ts](mentionSearch.ts)                   | \* Safety-net cap for virtualized display. Large enough to never feel                                    |
| [mentionTypes.ts](mentionTypes.ts)                     | 插件 composer.mention 条目给的候选项（docs/plugins/extension-host.md §16.6）：序列化为 insertText 原文。 |
| [PromptClipboardPlugin.tsx](PromptClipboardPlugin.tsx) | 根因：返回 false 会继续进入 PlainTextPlugin 的默认 CUT，写入失败仍可能删除选区。                         |
| [promptMentionLabel.ts](promptMentionLabel.ts)         | 旧草稿快照里可能把完整 markdown 链接写进 mention node 的 text 字段。                                     |
| [promptSerialization.ts](promptSerialization.ts)       | 编辑器文本用于光标；业务输出显式读取 canonical，不能覆写 TextNode 文本语义。                             |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                                         |

<!-- qingqi-directory-index:end -->
