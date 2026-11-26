# components

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 components 界面组件。

### 文件

| 文件                                                             | 简要说明                                                                                        |
| ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| [PluginUiCard.tsx](PluginUiCard.tsx)                             | 侧栏模式撑满容器；内联模式按 height 固定。                                                      |
| [PluginUiFollowUpDialogHost.tsx](PluginUiFollowUpDialogHost.tsx) | \* 无用户手势时插件代发消息的确认框。prompt 可编辑；挂在 RootShell，与 ConfirmDialogHost 并列。 |
| [PluginUiLauncherItems.tsx](PluginUiLauncherItems.tsx)           | 所属 pane 的有效 session，包含已就绪的草稿预热。                                                |
| [PluginUiSidePane.tsx](PluginUiSidePane.tsx)                     | 纯侧栏视图：不读取会话、lease、projection 或 workspace store。                                  |
| [PluginUiToolCallBlock.tsx](PluginUiToolCallBlock.tsx)           | 纯工具卡片视图：平台能力、结果与侧栏归属都由适配器提供。                                        |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                                |

<!-- qingqi-directory-index:end -->
