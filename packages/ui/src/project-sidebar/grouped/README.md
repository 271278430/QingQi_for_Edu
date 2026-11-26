# grouped

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 grouped 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                   |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| [colors.tsx](colors.tsx)                                           | colors 的React 组件。                                                                      |
| [draft-task-row.tsx](draft-task-row.tsx)                           | 实现或公开接口：GroupedDraftTaskRow。                                                      |
| [drag.ts](drag.ts)                                                 | 恢复自分组删除前的碰撞、落点与动画实现；不包含旧数据服务。                                 |
| [group-drag-overlay.tsx](group-drag-overlay.tsx)                   | cron 在存储层使用 `cron` 占位名；拖拽浮层曾绕过普通 header 的本地化逻辑，                  |
| [group-item.tsx](group-item.tsx)                                   | 实现或公开接口：GroupItem。                                                                |
| [group-title.ts](group-title.ts)                                   | 系统分组标题按语言环境本地化展示，忽略 DB 里存的固定占位标题（'cron' / 'off-peak'）。      |
| [ids.ts](ids.ts)                                                   | ids 的实现文件。                                                                           |
| [model.ts](model.ts)                                               | 旧组件只消费展示树；任务事实与组织结构仍来自当前唯一 owner。                               |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                           |
| [shared.tsx](shared.tsx)                                           | shared 的React 组件。                                                                      |
| [sticky-group-header-slot.tsx](sticky-group-header-slot.tsx)       | 实现或公开接口：StickyGroupHeaderSlot。                                                    |
| [sticky-group-header.tsx](sticky-group-header.tsx)                 | 系统分组（cron / 闲时）标题按语言环境本地化展示，与 GroupItem 保持一致。                   |
| [task-context-menu-content.tsx](task-context-menu-content.tsx)     | 归档专属的禁用原因（运行中任务）；其余操作不受影响。                                       |
| [task-item.tsx](task-item.tsx)                                     | 实现或公开接口：EmptyGroupDropZone、GroupedTaskItem。                                      |
| [task-row.tsx](task-row.tsx)                                       | 实现或公开接口：GroupedTaskRow。                                                           |
| [types.ts](types.ts)                                               | 行是纵向列：首行（标题 + 右侧元信息）固定 28px，其下可挂工作流运行行，所以外层只定 min-h。 |
| [useGroupedDrag.ts](useGroupedDrag.ts)                             | 任务活动不能重建 sensor options，否则拖拽 Context 会唤醒全部未变化行。                     |
| [view.ts](view.ts)                                                 | view 的实现文件。                                                                          |
| [virtualized-group-task-list.tsx](virtualized-group-task-list.tsx) | group 展开动画刚开始时，祖先容器可能还没被内容撑到 scrollHeight > clientHeight。           |
| [virtualized-scroll.ts](virtualized-scroll.ts)                     | group 虚拟列表在外层滚动容器中途重新挂载时，react-virtual                                  |
| [virtualized-top-level-list.tsx](virtualized-top-level-list.tsx)   | 折叠/展开时顶层行高度会先变、滚动高度后变；只认“当前已可滚”                                |

<!-- qingqi-directory-index:end -->
