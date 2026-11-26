# components

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 components 界面组件。

### 文件

| 文件                                                                   | 简要说明                                                                                                       |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [ComposerStatusSlot.tsx](ComposerStatusSlot.tsx)                       | \* composer.status 插槽：输入框工具栏、上下文用量圆环左边。                                                    |
| [extensionIcons.ts](extensionIcons.ts)                                 | \* 扩展可用的 Lucide 图标白名单（DESIGN.md「Extension slots」）。清单里写图标名；                              |
| [ExtensionLauncherSection.tsx](ExtensionLauncherSection.tsx)           | \* 启动页「扩展」分区（docs/plugins/extension-host.md §6、§16.1）。不依赖会话。                                |
| [ExtensionLogsPane.tsx](ExtensionLogsPane.tsx)                         | 级别只用语义色的文字与行底色表达，文字本身可读（DESIGN.md「Color Usage Rules」）。                             |
| [ExtensionMentionOptionContent.tsx](ExtensionMentionOptionContent.tsx) | 插件 composer.mention 候选行：白名单图标 + 标题 + 说明，与 skills 行同一密度（DESIGN.md「Extension slots」）。 |
| [ExtensionPermissionsSection.tsx](ExtensionPermissionsSection.tsx)     | 八个写动作在「最近操作」里的动作名（§17.8）；其余能力显示能力 id。                                             |
| [ExtensionViewPane.tsx](ExtensionViewPane.tsx)                         | \* 扩展视图标签页（docs/plugins/extension-host.md §8）。挂载时创建实例、卸载时关闭；                           |
| [NavPrimarySlot.tsx](NavPrimarySlot.tsx)                               | 未读数超过它时显示「99+」。                                                                                    |
| [README.md](README.md)                                                 | 本目录用途、子目录与逐文件说明。                                                                               |

<!-- qingqi-directory-index:end -->
