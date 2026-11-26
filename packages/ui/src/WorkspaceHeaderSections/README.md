# WorkspaceHeaderSections

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 WorkspaceHeaderSections 实现源码。

### 文件

| 文件                                                                 | 简要说明                                                                                                                              |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| [README.md](README.md)                                               | 本目录用途、子目录与逐文件说明。                                                                                                      |
| [shared.ts](shared.ts)                                               | 实现或公开接口：WorkspaceHeaderState、WorkspaceHeaderVariant、WorkspaceHeaderReloadSessionOptions、WorkspaceHeaderTitleSectionProps。 |
| [WorkspaceContextPath.tsx](WorkspaceContextPath.tsx)                 | 路径缩写必须使用当前 workspace 的主机信息，不能把本机 home 套到远程路径上。                                                           |
| [workspaceContextPathFormat.ts](workspaceContextPathFormat.ts)       | 实现或公开接口：formatWorkspaceContextPath。                                                                                          |
| [WorkspaceHeaderActionSection.tsx](WorkspaceHeaderActionSection.tsx) | Windows header 内容区有 p-2，普通工具栏按钮 hover 只覆盖 32px 高度。                                                                  |
| [WorkspaceLastActivity.tsx](WorkspaceLastActivity.tsx)               | 实现或公开接口：WorkspaceLastActivity。                                                                                               |

<!-- qingqi-directory-index:end -->
