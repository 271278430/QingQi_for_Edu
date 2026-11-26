# prompt-editor

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 prompt editor 实现源码。

### 文件

| 文件                                                       | 简要说明                                                                                 |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [ChatPromptActionMenu.tsx](ChatPromptActionMenu.tsx)       | \* 「添加」分区里紧随附件之后的命令快捷项，选中即插入与 `/` 面板相同的命令标签。         |
| [ChatPromptEditor.tsx](ChatPromptEditor.tsx)               | 输入展示壳：纯 props 组件、无 store/协议依赖；mention 面板通过 enableMentionPanel 透传。 |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                         |
| [useComposerToolbarFit.ts](useComposerToolbarFit.ts)       | \* 仅拥有 DOM 布局投影；权限、Plan 和 CUA 业务状态仍由原有 hooks 管理。                  |
| [usePromptEditorDragState.ts](usePromptEditorDragState.ts) | 取消 OS 文件拖拽或把 file tree 拖拽拖出窗口时，Electron/浏览器不一定派发 drop/dragend。  |

<!-- qingqi-directory-index:end -->
