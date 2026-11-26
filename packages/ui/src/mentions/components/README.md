# components

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 components 界面组件。

### 文件

| 文件                                                               | 简要说明                                                                         |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| [ContextMentionOptionContent.tsx](ContextMentionOptionContent.tsx) | 这里只给 file/directory 传 kind，让 fileDisplay 继续按文件和文件夹图标渲染；     |
| [MentionPanel.tsx](MentionPanel.tsx)                               | 禁选态（如同名 Plugin 冲突 fail closed）：可见但不可点击，键盘导航由上层跳过。   |
| [PluginMentionOptionContent.tsx](PluginMentionOptionContent.tsx)   | 实现或公开接口：PluginMentionOptionContent。                                     |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                 |
| [scrollMask.ts](scrollMask.ts)                                     | Thinking 与工具分组共用：容器拥有跟随状态，内容/容器变高时只在用户未离底时跟随。 |

<!-- qingqi-directory-index:end -->
