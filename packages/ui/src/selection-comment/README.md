# selection-comment

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 selection comment 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                         |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| [annotationActions.ts](annotationActions.ts)                       | 撤销窗口：删除后 6 秒内可撤销，其余编号自动补位、撤销后恢复。                                    |
| [AnnotationNumber.tsx](AnnotationNumber.tsx)                       | \* 注释编号气泡。正文标记、composer 注释列表与编辑浮层共用，保证三处同一条注释长得一样：         |
| [contract.example.ts](contract.example.ts)                         | 标准调用：点“注释”时冻结选区位置与原文，保存时把评论（可为空）写回同一条注释。                   |
| [CONTRACT.md](CONTRACT.md)                                         | 模块职责、公共接口、依赖方向和状态约定。                                                         |
| [contract.ts](contract.ts)                                         | \* 选区批注输入浮层的输入契约，以实际组件为唯一类型源。                                          |
| [ConversationAnnotationMarks.tsx](ConversationAnnotationMarks.tsx) | 时间线消息层（relative、随内容滚动）；标记挂在这里就不用跟着 scroll 事件重算位置。               |
| [index.ts](index.ts)                                               | index 的实现文件。                                                                               |
| [module.ts](module.ts)                                             | \* selection-comment 模块清单（architecture-governance managed 模块）。                          |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                 |
| [SelectionCommentEditor.tsx](SelectionCommentEditor.tsx)           | \* 选区“注释”输入浮层，新增与编辑共用。它独立于 useTextSelection：聚焦输入框会折叠正文选区并触发 |
| [textAnchor.ts](textAnchor.ts)                                     | \* 选区文字锚点：把一段 DOM Range 记成“来源行 → 第几个可选区域 → 字符偏移”，                     |
| [useSelectionCommentSupport.ts](useSelectionCommentSupport.ts)     | 选区“批注”入口只对声明 conversationQuoteComment 的 CLI 开放：旧 CLI 会静默剥掉引用上的           |

<!-- qingqi-directory-index:end -->
