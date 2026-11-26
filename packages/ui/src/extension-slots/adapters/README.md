# adapters

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 adapters 外部能力与平台适配。

### 文件

| 文件                                                         | 简要说明                                                                                                    |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| [extensionViewPage.ts](extensionViewPage.ts)                 | 扩展视图页面（docs/plugins/extension-host.md §8）：采用 MCP App 的页面层（沙箱 webview、端口 transport、    |
| [extensionViewsContext.ts](extensionViewsContext.ts)         | 打开扩展视图标签的入口：由 App 层的 ExtensionViewsProvider 提供（它持有侧栏标签的 owner 回调）。            |
| [ExtensionViewsProvider.tsx](ExtensionViewsProvider.tsx)     | \* 扩展视图的打开入口（docs/plugins/extension-host.md §8）。侧栏标签的 owner 是 App 层的面板状态，          |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                            |
| [useComposerMentionSlot.ts](useComposerMentionSlot.ts)       | 每个条目最近一次发出的查询。键 = 作用域 + query。                                                           |
| [useExtensionGrants.ts](useExtensionGrants.ts)               | 扩展授权的 Renderer 入口（docs/plugins/extension-host.md §17.7）：授权状态的最近一份、授权对话框、撤销、    |
| [useExtensionLogs.ts](useExtensionLogs.ts)                   | 没有扩展门面（Web、手机远控）时用的空 store：hook 照常调用，结果为空。                                      |
| [useExtensionMentionGroups.ts](useExtensionMentionGroups.ts) | \* `@` 面板的插件分组（docs/plugins/extension-host.md §16.6），给 mentions/MentionPlugin 当一个候选来源：   |
| [useExtensionSlots.ts](useExtensionSlots.ts)                 | 没有扩展门面（Web、手机远控）时用的空 store：hooks 照常调用，结果为空。                                     |
| [useExtensionWorkbench.ts](useExtensionWorkbench.ts)         | \* 对话窗格登记自己的屏幕会话（docs/plugins/extension-host.md §3.4、§9）：会话、草稿、焦点或草稿所选模型    |
| [useFileViewerRouter.ts](useFileViewerRouter.ts)             | 冲突日志的去重键：每份静态表（rev）对同一组插件只记一次。                                                   |
| [useNavPrimarySlot.ts](useNavPrimarySlot.ts)                 | \* nav.primary 的渲染模型（docs/plugins/extension-host.md §16.4）：没有扩展门面（Web、手机远控）时为 null。 |
| [useOpenSlotSurface.ts](useOpenSlotSurface.ts)               | \* 插槽的 surface target：打开插件的 MCP App 页面（docs/plugins/extension-host.md §16.3）。                 |

<!-- qingqi-directory-index:end -->
