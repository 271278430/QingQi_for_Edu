# remote

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 remote 实现源码。

### 文件

| 文件                                                                           | 简要说明                                                                                                                |
| ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                                                                        |
| [remoteWorkspaceController.ts](remoteWorkspaceController.ts)                   | 旧回调也不能绕过项目创建，拒绝前不产生连接或目录副作用。                                                                |
| [remoteWorkspaceProjection.ts](remoteWorkspaceProjection.ts)                   | 旧侧栏 Source 分组（lib/workspaceSourceGroups.ts）随 Group 视图下线；这是其中唯一仍被                                   |
| [SourceServerBoundaryDialogContent.tsx](SourceServerBoundaryDialogContent.tsx) | 中文自然折行会留下孤立尾字，保留文案中的语义换行；英文随可用宽度均衡折行。                                              |
| [useRemoteWorkspaceController.tsx](useRemoteWorkspaceController.tsx)           | 实现或公开接口：RemoteWorkspaceControllerProvider、useRemoteWorkspaceController、useOptionalRemoteWorkspaceController。 |

<!-- qingqi-directory-index:end -->
