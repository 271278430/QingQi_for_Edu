# project-sidebar

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 project sidebar 实现源码。

### 子目录

| 目录                          | 存放内容                                  |
| ----------------------------- | ----------------------------------------- |
| [grouped/](grouped/README.md) | @zcode/ui 基础工程中的 grouped 实现源码。 |

### 文件

| 文件                                                                                   | 简要说明                                                                                                       |
| -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [archive-view.ts](archive-view.ts)                                                     | cwd 可属于多个虚拟项目，不能再用目录叶名和路径合并归档。                                                       |
| [ArchiveGroupCard.tsx](ArchiveGroupCard.tsx)                                           | 实现或公开接口：ArchiveGroupCard。                                                                             |
| [ArchiveManagement.tsx](ArchiveManagement.tsx)                                         | 实现或公开接口：ArchiveManagement。                                                                            |
| [ChatRemoteFolderSelection.tsx](ChatRemoteFolderSelection.tsx)                         | 聊天切换只在显式目录确认后解析项目；其他创建/设备管理入口不使用此流程。                                        |
| [ComposerSubmissionPendingContext.ts](ComposerSubmissionPendingContext.ts)             | 菜单持有切换意图；输入框只投影当前草稿是否允许提交，不保存第二份草稿。                                         |
| [contract.example.ts](contract.example.ts)                                             | 先校验/确认再提交；不制造本地归属副本。                                                                        |
| [CONTRACT.md](CONTRACT.md)                                                             | 模块职责、公共接口、依赖方向和状态约定。                                                                       |
| [contract.ts](contract.ts)                                                             | 与上一组操作之间画分隔线；首项忽略。                                                                           |
| [grouped-expansion.ts](grouped-expansion.ts)                                           | Bugfix: 受限浏览器或 SSR 测试里 storage 可能不可写，折叠状态写入失败不能阻断侧栏交互。                         |
| [grouped-view.ts](grouped-view.ts)                                                     | 任务存在性只来自 Host 树；分组结构保留不可见成员，投影不能反向删写。                                           |
| [HomeOnlyWorkspaceRows.tsx](HomeOnlyWorkspaceRows.tsx)                                 | home-only 首页的工作区入口：可 bridge 的行打开工作区，其余行交给桌面已有重连 owner。                           |
| [index.tsx](index.tsx)                                                                 | 实现或公开接口：ProjectSidebar。                                                                               |
| [ManagedWorktreesDialog.tsx](ManagedWorktreesDialog.tsx)                               | 项目菜单 → Worktrees 管理弹窗（docs/git/worktree.md §3.6、§3.7、§3.8）。                                       |
| [module.ts](module.ts)                                                                 | \* project-sidebar 模块清单（architecture-governance managed 模块）。                                          |
| [OfflineRemoteProjectRows.tsx](OfflineRemoteProjectRows.tsx)                           | 四种任务视图共用项目占位，不在这里保存或展示离线任务缓存。                                                     |
| [project-file-navigation.ts](project-file-navigation.ts)                               | 文件读取目标只取用户选中的 root；不能用同路径的当前 tab 猜远端身份。                                           |
| [project-management-view.ts](project-management-view.ts)                               | 空项目创建后的宽限期：刚建的项目还没来得及开会话，不算不再使用。                                               |
| [project-tree-reader.ts](project-tree-reader.ts)                                       | Host 入口列表是可见集合的权威；网络结果不能恢复已移除的成员实例。                                              |
| [ProjectComposerMenu.tsx](ProjectComposerMenu.tsx)                                     | 是否显示项目 chip 的快捷脱离按钮；默认跟随非项目工作区选择能力。                                               |
| [ProjectCreation.tsx](ProjectCreation.tsx)                                             | Root 的动作 controller 没有装配 projection；设备全集必须直接订阅同一个 Source 服务。                           |
| [ProjectDirectoryProvider.tsx](ProjectDirectoryProvider.tsx)                           | 角标基线锚定 renderer 进程生命周期而不是组件生命周期：owner 可能因 services 切换                               |
| [ProjectEditor.tsx](ProjectEditor.tsx)                                                 | SelectItem 的 ItemText 默认按内容收缩；撑满整行后状态才能靠右，长名称截断时不挤掉状态。                        |
| [ProjectFolderIcon.tsx](ProjectFolderIcon.tsx)                                         | 沿用 Folders 的后层轮廓，前层增加打开的折页，保持相同画布、线宽和主题颜色。                                    |
| [ProjectFolderTrustDialog.tsx](ProjectFolderTrustDialog.tsx)                           | 聊天固定目录创建时展示本次名称；恢复沿用已确认项目的名称。                                                     |
| [ProjectIdentityHoverCard.tsx](ProjectIdentityHoverCard.tsx)                           | \* 项目模型迁移曾漏接详情；项目入口只读项目及其可选 Host，悬停结束即关闭，不保存点击锁定状态。                 |
| [ProjectManagement.tsx](ProjectManagement.tsx)                                         | 选择只是 UI 草稿：生效集合 = 草稿 ∩ 当前可见且可移除的行，树刷新后自然收敛，不另做同步。                       |
| [ProjectManagementRow.tsx](ProjectManagementRow.tsx)                                   | 表格列只在宽屏出现；窄屏把设备、会话和最近活动折成一行元信息。                                                 |
| [ProjectNode.tsx](ProjectNode.tsx)                                                     | Escape 或在其他区域松手时，源节点才收到 dragend；目标也要清除临时高亮。                                        |
| [ProjectNodeContent.tsx](ProjectNodeContent.tsx)                                       | 修复原因：memo 内容的内联默认对象/数组会在每次渲染时新建引用，触发引用稳定性门禁。                             |
| [projectOrder.ts](projectOrder.ts)                                                     | 控制端显示偏好不写远端 position；暂时不可见的入口保留原位置。                                                  |
| [ProjectRemovalDialog.tsx](ProjectRemovalDialog.tsx)                                   | undefined = 本批无本机候选；"measuring" = 正在计算；null = 测量失败或无数据，隐藏选项。                        |
| [ProjectSections.tsx](ProjectSections.tsx)                                             | 原因：任务分区遗漏项目内列表的左侧留白，导致整行背景和文字贴左；统一内缩 8px。                                 |
| [ProjectSidebarListHeader.tsx](ProjectSidebarListHeader.tsx)                           | 列表头部独立于导航和滚动内容，搜索与视图仍使用现有 owner。                                                     |
| [ProjectSidebarNavigation.tsx](ProjectSidebarNavigation.tsx)                           | 顶部导航只展示 Shell 的选中状态，路由仍由 Shell 唯一持有。                                                     |
| [ProjectSidebarNode.tsx](ProjectSidebarNode.tsx)                                       | 仅本机桌面且 Host 提供受管 worktree 服务时传入（docs/git/worktree.md §3.6）。                                  |
| [ProjectTaskListContext.ts](ProjectTaskListContext.ts)                                 | 列表展示配置只来自侧栏 owner；不承载 Host 行集合或会话运行态。                                                 |
| [ProjectTaskRows.tsx](ProjectTaskRows.tsx)                                             | 原因：每行订阅完整 activeTaskId 会让同工作区所有行随选择更新；只订阅自身选中态。                               |
| [PurposeSections.tsx](PurposeSections.tsx)                                             | 原因：横向拖动会撑宽 overflow-y:auto 的侧栏并触发水平自动滚动；在碰撞计算前固定纵轴。                          |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                                                                               |
| [remote-navigation.ts](remote-navigation.ts)                                           | \* 同一设备在途的未指定目录连接。Host 把这类 connect 按设备采用为同一 logical session，                        |
| [remote-project-connection.ts](remote-project-connection.ts)                           | 最近目录不是新建请求；连接前固定已有入口，避免连接完成后误入创建器。                                           |
| [RemoteConnectionProgressSection.tsx](RemoteConnectionProgressSection.tsx)             | 与 Host 侧 resolveProjectHostService 相同的解析；URL Server 直连不属于 Source 管理域。                         |
| [RemoteConversationDisconnected.tsx](RemoteConversationDisconnected.tsx)               | 冷态不读取远端数据；草稿只读既有持久化，离线页面没有提交或排队处理器。                                         |
| [RemoteHostSection.tsx](RemoteHostSection.tsx)                                         | 实现或公开接口：remoteHostLabel。                                                                              |
| [RemoteProjectList.tsx](RemoteProjectList.tsx)                                         | 原因：返回草稿或成员换代后，旧选择不得再登记入口或关闭新的流程。                                               |
| [RemoteProjectMenu.tsx](RemoteProjectMenu.tsx)                                         | 实现或公开接口：RemoteProjectMenu。                                                                            |
| [RemoteProjectPicker.tsx](RemoteProjectPicker.tsx)                                     | 旧连接/项目入口继续保留新建能力；创建表单只采用列表，避免两个草稿 owner。                                      |
| [RemovedProjects.tsx](RemovedProjects.tsx)                                             | 只列本机软删除项目；远程入口移除后不保留，重新添加走远程项目选择器。                                           |
| [SortableProjects.tsx](SortableProjects.tsx)                                           | Bug 根因：内联 options 会让 useSensor 每次目录更新都重建 activators/listeners，                                |
| [task-mutation.ts](task-mutation.ts)                                                   | 已查看事件读取唯一 owner 的 marker；不借用 UI 行缓存，也不跨 Source 使用本机服务。                             |
| [TaskGroupedView.tsx](TaskGroupedView.tsx)                                             | 恢复删除前的组件与手势（fd2f4f38a4a^1）；仅将旧事实缓存/applyOrder 改接当前 owner。                            |
| [TaskGroupTaskMenu.tsx](TaskGroupTaskMenu.tsx)                                         | 实现或公开接口：TaskGroupTaskMenu。                                                                            |
| [timelineDates.ts](timelineDates.ts)                                                   | 日期段按本地日历计算；夏令时的一天可能为 23/25 小时，不能直接用毫秒差取整。                                    |
| [useAppControlNavigation.ts](useAppControlNavigation.ts)                               | 桌面只登记既有导航 owner；手机共享目录/事件不会因此接收桌面导航。                                              |
| [useArchiveManagement.ts](useArchiveManagement.ts)                                     | 固定确认时的身份集合；搜索变化、新归档和重复点击不能扩充已经确认的批次。                                       |
| [useHomeOnlyWorkspaces.ts](useHomeOnlyWorkspaces.ts)                                   | \* home-only 没有项目契约，工作区行只投影桌面 listWorkspaces 与推送；不轮询，也不另存连接状态。                |
| [useManagedWorktrees.ts](useManagedWorktrees.ts)                                       | 受管 worktree 管理弹窗的数据 hook（docs/git/worktree.md §3.6）。                                               |
| [useProjectConnectionDiagnostics.ts](useProjectConnectionDiagnostics.ts)               | \* 只合并 Host 投影与旧 workspace 的连接错误；连接进度由详情直接读连接管理服务的操作日志。                     |
| [useProjectDirectoryServices.ts](useProjectDirectoryServices.ts)                       | 目录查询沿用项目的 Host 路由，手机无需桌面专用 attachment，也不借当前 tab 的文件服务。                         |
| [useProjectFileTree.ts](useProjectFileTree.ts)                                         | Bug 原因：代际只在最后挡住文件面板，被取代的旧请求在等重连结束后仍会连接设备并 bind，                          |
| [useProjectManagement.ts](useProjectManagement.ts)                                     | 本批成功移除的项；远程入口在移除前抓取，撤销时按原 projectId / roots / membership 重新登记。                   |
| [useProjectPinIntent.ts](useProjectPinIntent.ts)                                       | 只保存命令及刷新期间的 UI 意图；不缓存 task，也不建立已接受命令队列。                                          |
| [useProjectRemoteSync.tsx](useProjectRemoteSync.tsx)                                   | \* 侧栏远端项目菜单的同步项：打开数据同步弹窗，定位到该项目所在设备与所选分类，MCP 按该项目做 workspace 映射。 |
| [useProjectSidebarPreferences.ts](useProjectSidebarPreferences.ts)                     | 浏览器禁用存储时仍保持当前窗口偏好，不影响 Host 命令。                                                         |
| [useProjectTaskActions.ts](useProjectTaskActions.ts)                                   | UI 命令适配：采用原 Host 入口，成功后仅处理本窗口展示，不保存会话事实。                                        |
| [useProjectTaskNavigation.ts](useProjectTaskNavigation.ts)                             | 打开任务才绑定 workspace；列表 mutation 不借导航创建 scope。                                                   |
| [useProjectTree.ts](useProjectTree.ts)                                                 | 成功 host 集合只在内容变化时才发布新引用，与 availability 的防抖口径一致。                                     |
| [useProjectUnreadSignals.ts](useProjectUnreadSignals.ts)                               | 前台完成补记记录：written=已补写，marker=补写回包的未读版本（自动清除的 CAS 凭据）。                           |
| [useRemoteProjectConnectionPresentation.ts](useRemoteProjectConnectionPresentation.ts) | 实现或公开接口：useRemoteProjectConnectionPresentation。                                                       |
| [useRemoteWorkspaceConnectionGate.ts](useRemoteWorkspaceConnectionGate.ts)             | \* 把 Root 的 reconnectingRemoteWorkspaceKeys 变成可等待的门：key 离开集合即放行。                             |
| [useSavedWorkflowProjectOptions.ts](useSavedWorkflowProjectOptions.ts)                 | 实现或公开接口：useSavedWorkflowProjectOptions。                                                               |
| [useTaskGroups.ts](useTaskGroups.ts)                                                   | 控制端唯一订阅；三个筛选视图和所有任务菜单共享同一份已接受结构。                                               |
| [useWebRemoteControlRendererActions.ts](useWebRemoteControlRendererActions.ts)         | 只用桌面 scratch workspace 的目录创建能力（~/ZCodeProject/<name>）。                                           |
| [view-preference.ts](view-preference.ts)                                               | 原因：重构换了偏好 key；忽略旧 organizeBy 会让原本选分组的用户升级后跳回项目。                                 |
| [view.ts](view.ts)                                                                     | 活动态只覆盖已有行的 UI sidecar；Controller 快照不能替代项目树的行集合和事实。                                 |
| [WorkspaceDragOverlay.tsx](WorkspaceDragOverlay.tsx)                                   | 实现或公开接口：WorkspaceDragOverlay。                                                                         |

<!-- qingqi-directory-index:end -->
