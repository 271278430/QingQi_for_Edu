# task-management

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 task management 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                                           | 简要说明                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [conversation-session-active-task-metadata.test.ts](conversation-session-active-task-metadata.test.ts)                                         | 2026-09-15 裁决：自动归档纯按最后活动时间，置顶与运行中除外；未读、error 不再保护旧任务。 |
| [conversation-session-archive-management.test.ts](conversation-session-archive-management.test.ts)                                             | 上一组高度动画会移动下一组的点击位置，等布局稳定再继续逐组操作。                          |
| [conversation-session-archived-task-closes-side-pane-tabs.test.ts](conversation-session-archived-task-closes-side-pane-tabs.test.ts)           | conversation-session-archived-task-closes-side-pane-tabs.test 的实现文件。                |
| [conversation-session-auto-archived-task-closes-side-pane-tabs.test.ts](conversation-session-auto-archived-task-closes-side-pane-tabs.test.ts) | 自动归档只看 CLI 最后活动时间；把它拨到保留期之外，再开启设置触发 Host 补扫。             |
| [conversation-session-delete-all-archived-tasks.test.ts](conversation-session-delete-all-archived-tasks.test.ts)                               | 修复原因：直接运行 wdio 时默认 HOME 是 `.e2e-home`（无 runId 后缀），旧守卫只认           |
| [conversation-session-deleted-task-restart.test.ts](conversation-session-deleted-task-restart.test.ts)                                         | 提示中也有回答 marker；旧屏障在真实回答前归档并关闭 runtime，导致标题旁路报错。           |
| [conversation-session-guarded-batch-delete.test.ts](conversation-session-guarded-batch-delete.test.ts)                                         | DCA-V1-19/20/23/24：仅覆盖 POSIX/Git Bash 桌面拒绝，Windows 原生语义另有 oracle。         |
| [conversation-session-guarded.test.ts](conversation-session-guarded.test.ts)                                                                   | DCA-V1-01/05/07/09..15：真实桌面 broker → handler → provider result。                     |
| [conversation-session-open-existing-only.test.ts](conversation-session-open-existing-only.test.ts)                                             | conversation-session-open-existing-only.test 的实现文件。                                 |
| [conversation-session-sidebar-activity-refresh.test.ts](conversation-session-sidebar-activity-refresh.test.ts)                                 | 已看到实际输出和持久行后才计数；测试不依赖可选的自动标题 sidecar。                        |
| [conversation-session-sidebar-selection-rendering.test.ts](conversation-session-sidebar-selection-rendering.test.ts)                           | 生产 bundle 会压缩函数名；按生产组件的独有 props 形状识别内容层，不依赖函数名。           |
| [conversation-session-sidebar-show-more-typography.test.ts](conversation-session-sidebar-show-more-typography.test.ts)                         | 合成 Host 索引仅用于样式和分页，不恢复任务或请求模型；node:sqlite 仅提供同步 API。        |
| [conversation-session-sidebar-stop-status-race.test.ts](conversation-session-sidebar-stop-status-race.test.ts)                                 | 旧 membership 聚合器已退役，旧 gate 不再被产品调用。只暂挂当前目录 RPC，                  |
| [conversation-session-sidebar-unread-clear.test.ts](conversation-session-sidebar-unread-clear.test.ts)                                         | pending case 独立跑时 app data 每次重建；显式选择 replay provider，避免仅有配置但         |
| [conversation-session-sidebar-width-stability.test.ts](conversation-session-sidebar-width-stability.test.ts)                                   | 合成索引仅准备分页/长标题布局，不恢复这些任务，也不请求模型。                             |
| [conversation-session-task-created-project-row.test.ts](conversation-session-task-created-project-row.test.ts)                                 | Bug 根因：只依赖 active optimistic overlay 会掩盖旧 task-row cache。                      |
| [conversation-session-task-groups.test.ts](conversation-session-task-groups.test.ts)                                                           | 颜色菜单在 Portal 中退场；只等列表动画会让指针按在尚未卸载的菜单上。                      |
| [conversation-session-task-index-row-authority.test.ts](conversation-session-task-index-row-authority.test.ts)                                 | Bug 根因：tasks-index 里的历史 running 只是一份持久 meta；没有 sessions-index             |
| [conversation-session-task-title-marquee.test.ts](conversation-session-task-title-marquee.test.ts)                                             | Bug 根因：重复 mouseenter 会先取消上一条 case 留下的动画，再经过 1 秒                     |
| [conversation-session-title-generation-timeout.test.ts](conversation-session-title-generation-timeout.test.ts)                                 | 运行录像已显示标题更新；旧 taskListCache 在 V4 中不再持有该任务，改查真实 Header 与侧栏。 |
| [conversation-session-v4-delete.test.ts](conversation-session-v4-delete.test.ts)                                                               | 通过侧栏现有入口操作，验证真实标题投影或归档后的永久删除。                                |
| [conversation-session-v4-rename.test.ts](conversation-session-v4-rename.test.ts)                                                               | 通过侧栏现有入口操作，验证真实标题投影或归档后的永久删除。                                |
| [conversation-session-v4-session-action-locks.test.ts](conversation-session-v4-session-action-locks.test.ts)                                   | O22 / PV4-14（fork 部分）：fork 与文件撤销的 session 锁只由 availability 下发             |
| [conversation-session-v4-sidebar.test.ts](conversation-session-v4-sidebar.test.ts)                                                             | 通过侧栏现有入口操作，验证真实标题投影或归档后的永久删除。                                |
| [README.md](README.md)                                                                                                                         | 本目录用途、子目录与逐文件说明。                                                          |

<!-- qingqi-directory-index:end -->
