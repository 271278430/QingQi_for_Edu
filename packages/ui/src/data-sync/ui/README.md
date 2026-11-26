# ui

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 ui 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                                            |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [DataSyncDialog.tsx](DataSyncDialog.tsx)                       | 模型提供商是只读分类，不是 IDataSyncCategoryService：不参与勾选与「推送全部」，单独渲染。           |
| [DataSyncDialogContainer.tsx](DataSyncDialogContainer.tsx)     | 设备行与入口共用：名称与「传输方式 · 地址」取自管理快照的同一份展示输入。                           |
| [DataSyncDialogFooter.tsx](DataSyncDialogFooter.tsx)           | 模型提供商只读：没有推送按钮，也不参与「推送全部」。                                                |
| [DataSyncDialogProvider.tsx](DataSyncDialogProvider.tsx)       | 窗口级挂载：页面切换不能卸载推送 owner；最小化只改变显示状态。                                      |
| [DataSyncEntry.tsx](DataSyncEntry.tsx)                         | 旧入口能定位的分类：技能、MCP、插件。                                                               |
| [DataSyncMinimizedProgress.tsx](DataSyncMinimizedProgress.tsx) | 非模态状态条始终挂在窗口根部，不受设置页滚动容器或页面卸载影响。                                    |
| [DataSyncProvidersPanel.tsx](DataSyncProvidersPanel.tsx)       | 模型提供商分类页（只读）：说明、最近一次自动同步的结果、失败时的「重试」，以及本机提供商列表。      |
| [DataSyncSection.tsx](DataSyncSection.tsx)                     | 打开已有的全局连接向导（Root 注入）；返回 false 表示向导正忙、未接受本次意图。                      |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                    |
| [settingsEntry.ts](settingsEntry.ts)                           | \* 技能、MCP、插件设置页的「远端上下文」：当前目标是已连接的 SSH / WSL / Docker 远程 workspace 时， |

<!-- qingqi-directory-index:end -->
