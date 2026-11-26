# nodes

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 nodes 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                        |
| -------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [mentionIconDom.ts](mentionIconDom.ts)                   | PromptMentionNode.ts 承载 Lexical 节点行为 + 全部分类图标 DOM 数据，            |
| [promptMentionDecoration.ts](promptMentionDecoration.ts) | CSS 中相对 URL 会按样式表路径解析；统一按文档 baseURI 解析，和原 img.src 一致。 |
| [PromptMentionNode.ts](PromptMentionNode.ts)             | 根因：TextNode 的 firstChild 链必须通向展示文字，不能被图标截断。               |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                |

<!-- qingqi-directory-index:end -->
