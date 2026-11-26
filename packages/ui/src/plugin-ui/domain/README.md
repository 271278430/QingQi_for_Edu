# domain

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 domain 实现源码。

### 文件

| 文件                                                                 | 简要说明                                                                                                 |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [buildPluginUiHostCapabilities.ts](buildPluginUiHostCapabilities.ts) | 宿主实例真实可用的交互；缺省项对应的能力不声明，插件据此降级。                                           |
| [buildPluginUiHostContext.ts](buildPluginUiHostContext.ts)           | 容器宽度（px）；未知时 0。                                                                               |
| [pluginDisplayName.ts](pluginDisplayName.ts)                         | \* 插件 id 形如 `<name>@<marketplace>`；对用户只显示 name 部分。纯函数，供来源标签与确认框共用。         |
| [pluginUiDownloadFile.ts](pluginUiDownloadFile.ts)                   | \* ui/download-file 的纯规则——每项归一成 `{ name, mimeType, source }`，                                  |
| [pluginUiFollowUp.ts](pluginUiFollowUp.ts)                           | `ui/message` 的 structuredContent 序列化后允许的最大 UTF-8 字节数（与工具结果同一上限）。                |
| [pluginUiImageBlocks.ts](pluginUiImageBlocks.ts)                     | 一张已校验的图片块：base64 正文（无 data: 前缀）、mimeType 与解码后字节数。                              |
| [pluginUiInstancePolicy.ts](pluginUiInstancePolicy.ts)               | ：最近几个回合的插件卡片默认展开，更早的按默认收进折叠区。                                               |
| [pluginUiLogicalScope.ts](pluginUiLogicalScope.ts)                   | 只有显式共享身份可合并；权限声明不同的普通 widget 不共用页面。                                           |
| [pluginUiModelContext.ts](pluginUiModelContext.ts)                   | \* 插件 UI 经 `ui/update-model-context` 附加的下一轮模型上下文。                                         |
| [pluginUiRowPolicy.ts](pluginUiRowPolicy.ts)                         | 渲染层提供的按 toolCallId 的裁决：推导结果 + 用户手动固定 / 收起。                                       |
| [pluginUiStyleVariables.ts](pluginUiStyleVariables.ts)               | \* ZCode 主题 token（DESIGN.md / docs/design/zcode-tokens.md）→ MCP Apps 标准样式变量                    |
| [pluginUiToolFeed.ts](pluginUiToolFeed.ts)                           | 内联卡片与侧栏共用的 legacy ChatToolCall 子集（toolCallRowAdapter 输出）。                               |
| [README.md](README.md)                                               | 本目录用途、子目录与逐文件说明。                                                                         |
| [readPluginUiPresentation.ts](readPluginUiPresentation.ts)           | \* 从 ToolCallRow 的 legacy raw.display 读出插件 UI 呈现信息。display.ui 由 agent 投影、经 strict schema |

<!-- qingqi-directory-index:end -->
