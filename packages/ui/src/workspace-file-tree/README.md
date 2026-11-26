# workspace-file-tree

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 workspace file tree 实现源码。

### 文件

| 文件                                                                         | 简要说明                                                                                                                                                                    |
| ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [constants.ts](constants.ts)                                                 | 实现或公开接口：WORKSPACE*FILE_TREE_VIRTUAL_ROW_HEIGHT_PX、WORKSPACE_FILE_TREE_WATCH_DEBOUNCE_MS、WORKSPACE_FILE_TREE_WATCH_REFRESH_CONCURRENCY、WORKSPACE_FILE_TREE_WATCH* |
| [gitStatus.ts](gitStatus.ts)                                                 | 实现或公开接口：WorkspaceFileTreeGitStatusState、loadWorkspaceFileTreeGitStatus。                                                                                           |
| [helpers.ts](helpers.ts)                                                     | \* 本机系统文件管理器在 main 侧对应的编辑器 id：finder / explorer 收到文件路径时                                                                                            |
| [hierarchyGuides.ts](hierarchyGuides.ts)                                     | 实现或公开接口：getWorkspaceFileTreeHierarchyGuideStyle。                                                                                                                   |
| [model.ts](model.ts)                                                         | 修复：文件树之前把 Git 改动统一压成 M/U，导致 staged added/deleted/renamed                                                                                                  |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                                                                                                            |
| [refreshDirectories.ts](refreshDirectories.ts)                               | 实现或公开接口：getWorkspaceFileTreeRefreshDirectoryPaths。                                                                                                                 |
| [searchRows.ts](searchRows.ts)                                               | 搜索结果来自全 workspace 索引，目录可能未在懒加载树里展开过；显示相对路径能避免多个同名 Java 类看起来无法区分。                                                             |
| [statusStyles.ts](statusStyles.ts)                                           | 修复：目录文字颜色之前硬编码优先使用 untracked，和 descendant 圆点的                                                                                                        |
| [types.ts](types.ts)                                                         | 用户偏好：单击本地 .html 文件时进内置浏览器，而不是源码预览                                                                                                                 |
| [useInstalledFileTreeEditors.ts](useInstalledFileTreeEditors.ts)             | 实现或公开接口：useInstalledFileTreeEditors。                                                                                                                               |
| [useWorkspaceFileSearchIndex.ts](useWorkspaceFileSearchIndex.ts)             | packed 直存（Host 返回列式字符串）：树渲染用 useMemo unpack，搜索态直透 worker。                                                                                            |
| [useWorkspaceFileTreeData.ts](useWorkspaceFileTreeData.ts)                   | 实现或公开接口：useWorkspaceFileTreeData。                                                                                                                                  |
| [useWorkspaceFileTreeRowDragState.ts](useWorkspaceFileTreeRowDragState.ts)   | Electron/浏览器在拖拽离开窗口时不一定向源行派发 dragend。                                                                                                                   |
| [useWorkspaceFileTreeRows.ts](useWorkspaceFileTreeRows.ts)                   | 实现或公开接口：useWorkspaceFileTreeRows。                                                                                                                                  |
| [useWorkspaceFileTreeStickyFolders.ts](useWorkspaceFileTreeStickyFolders.ts) | 每一层 sticky 行都会把下一层触发线向下推 28px；如果所有层级                                                                                                                 |
| [useWorkspaceFileTreeWatchers.ts](useWorkspaceFileTreeWatchers.ts)           | 实现或公开接口：useWorkspaceFileTreeWatchers。                                                                                                                              |
| [WorkspaceFileTree.tsx](WorkspaceFileTree.tsx)                               | HTML 单击打开方式是本机界面偏好；远端 workspace 下也读本机设置。                                                                                                            |
| [WorkspaceFileTreeList.tsx](WorkspaceFileTreeList.tsx)                       | 修复原因：sticky 与虚拟列表是滚动容器内的兄弟节点，列表原行仍会从 sticky 下方经过。                                                                                         |
| [WorkspaceFileTreeNotice.tsx](WorkspaceFileTreeNotice.tsx)                   | 实现或公开接口：WorkspaceFileTreeNotice。                                                                                                                                   |
| [WorkspaceFileTreeRowName.tsx](WorkspaceFileTreeRowName.tsx)                 | 实现或公开接口：WorkspaceFileTreeRowName。                                                                                                                                  |
| [WorkspaceFileTreeRowView.tsx](WorkspaceFileTreeRowView.tsx)                 | 实现或公开接口：WorkspaceFileTreeRowView。                                                                                                                                  |
| [WorkspaceFileTreeStickyFolders.tsx](WorkspaceFileTreeStickyFolders.tsx)     | 实现或公开接口：WorkspaceFileTreeStickyFolders。                                                                                                                            |

<!-- qingqi-directory-index:end -->
