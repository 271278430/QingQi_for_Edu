# managed-worktrees

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 managed worktrees 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                                |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                         | 示例：启动创建后，成功时只得到创建记录 ID；进度从 Host 推送的创建记录读取。                             |
| [CONTRACT.md](CONTRACT.md)                                         | 模块职责、公共接口、依赖方向和状态约定。                                                                |
| [contract.ts](contract.ts)                                         | 受管 worktree UI 模块对服务层的唯一类型入口（docs/git/worktree.md §3）。                                |
| [ForkDestinationMenu.tsx](ForkDestinationMenu.tsx)                 | assistant 行的"分叉"目的地菜单（docs/git/worktree.md §3.6）：在当前目录（或当前 worktree）分叉          |
| [index.ts](index.ts)                                               | index 的实现文件。                                                                                      |
| [managedWorktreeContexts.ts](managedWorktreeContexts.ts)           | worktree 相关的 SessionPane → 行组件通道（docs/git/worktree.md §3.6）。                                 |
| [ManagedWorktreeCreatingRows.tsx](ManagedWorktreeCreatingRows.tsx) | 侧栏项目下"正在创建 worktree"的任务行（docs/git/worktree.md §3.3）。                                    |
| [ManagedWorktreeCreationView.tsx](ManagedWorktreeCreationView.tsx) | 发送后、会话创建前的展示（docs/git/worktree.md §3.3、§3.5）：用户消息 + 进度卡片 + 失败操作。           |
| [managedWorktreeErrors.ts](managedWorktreeErrors.ts)               | worktree 相关错误的本地化：只按结构化 code 选择文案，不解析 git 原始报错文本。                          |
| [module.ts](module.ts)                                             | 实现或公开接口：moduleDefinition。                                                                      |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                        |
| [useManagedWorktreeCreations.ts](useManagedWorktreeCreations.ts)   | worktree 创建记录的订阅（docs/git/worktree.md §6.2）。记录只在 Host 内存中，是创建阶段的                |
| [useTaskWorktreePlacement.ts](useTaskWorktreePlacement.ts)         | 会话的 cwd 与所在受管 worktree（docs/git/worktree.md §2.1、§3.7、§3.12）。                              |
| [useWorktreeSupport.ts](useWorktreeSupport.ts)                     | worktree 入口（composer 复选框、"在新 worktree 中分叉"）的可见性与可用性（docs/git/worktree.md §3.1）。 |
| [WorktreeComposerControls.tsx](WorktreeComposerControls.tsx)       | 新建任务 composer 头部的 worktree 复选框与分支选择（docs/git/worktree.md §3.2）。                       |
| [WorktreeCreatedMarker.tsx](WorktreeCreatedMarker.tsx)             | 会话历史中的"已创建 worktree"（docs/git/worktree.md §6.6.4）：由 CLI 写入历史，                         |
| [worktreeLabel.ts](worktreeLabel.ts)                               | worktree 显示名 `<仓库名> · <bucket>`（docs/git/worktree.md §3.7），只由任务的 worktree 根目录          |
| [WorktreeOutputBlock.tsx](WorktreeOutputBlock.tsx)                 | worktree 创建的 git 输出与"已创建 worktree"历史项共用的展示块（docs/git/worktree.md §3.3）。            |

<!-- qingqi-directory-index:end -->
