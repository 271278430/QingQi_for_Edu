# managed-worktree-tasks

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 managed worktree tasks 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                         |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 示例：管理弹窗读取项目的受管 worktree，并在没有任务占用时删除第一个。                            |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                         |
| [contract.ts](contract.ts)                 | 任务所属 workspace（项目主目录）。                                                               |
| [index.ts](index.ts)                       | index 的实现文件。                                                                               |
| [module.ts](module.ts)                     | 实现或公开接口：moduleDefinition。                                                               |
| [ports.ts](ports.ts)                       | 受管 worktree 服务的注入端口（docs/git/worktree.md §5、§6）：git、任务行、会话命令、终端查询、   |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                 |
| [removal-gate.ts](removal-gate.ts)         | 受管 worktree 的删除租约与会话操作闸门（docs/git/worktree.md §8.3）。                            |
| [removal.ts](removal.ts)                   | 受管 worktree 的删除（docs/git/worktree.md §8.3）：删除租约、检查顺序与 CLI 卸载会话集中在这里。 |
| [service.ts](service.ts)                   | 受管 worktree 的编排（docs/git/worktree.md §3.3–§3.6、§3.11、§8）。                              |

<!-- qingqi-directory-index:end -->
