# side-pane-full-view

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 side pane full view 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                          |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| [anchorPreference.ts](anchorPreference.ts)                         | 浮窗吸附位置是全局偏好（spec：docs/ui/side-pane-full-view.md），不随对话切换。                    |
| [contract.example.ts](contract.example.ts)                         | \* side-pane-full-view 标准调用示例：壳层只通过 controller 发命令，显隐全部从 fullView 只读派生。 |
| [CONTRACT.md](CONTRACT.md)                                         | 模块职责、公共接口、依赖方向和状态约定。                                                          |
| [contract.ts](contract.ts)                                         | side-pane-full-view 模块契约（spec：docs/ui/side-pane-full-view.md）。                            |
| [ConversationHost.tsx](ConversationHost.tsx)                       | Side Pane 完整视图的对话宿主（spec：docs/ui/side-pane-full-view.md）。                            |
| [conversationPanePresentation.ts](conversationPanePresentation.ts) | 对话 pane 的展示形态（spec：docs/ui/side-pane-full-view.md）。                                    |
| [ConversationTab.tsx](ConversationTab.tsx)                         | 完整视图下 tab 栏里固定在第一位的对话 tab；Radix value 用保留值，不进入面板 tab registry。        |
| [index.ts](index.ts)                                               | side-pane-full-view 模块公开入口（spec：docs/ui/side-pane-full-view.md）。                        |
| [model.ts](model.ts)                                               | Side Pane 完整视图的纯模型：状态类型与浮窗几何。spec：docs/ui/side-pane-full-view.md              |
| [module.ts](module.ts)                                             | \* side-pane-full-view 模块清单（architecture-governance managed 模块）。                         |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                  |
| [ToggleButton.tsx](ToggleButton.tsx)                               | Side Pane 右上角「进入 / 退出完整视图」按钮（spec：docs/ui/side-pane-full-view.md）。             |
| [useSidePaneFullView.ts](useSidePaneFullView.ts)                   | \* 完整视图状态的唯一 owner（spec：docs/ui/side-pane-full-view.md）。                             |

<!-- qingqi-directory-index:end -->
