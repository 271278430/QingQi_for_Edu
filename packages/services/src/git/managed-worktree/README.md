# managed-worktree

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 managed worktree 实现源码。

### 文件

| 文件                                       | 简要说明                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 示例：Host 编排在删除前先完成任务占用检查，再调用 git 层删除，并把结构化错误交给 UI。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                              |
| [contract.ts](contract.ts)                 | git 输出与进度行，按到达顺序回调（写入创建记录，§6.2）。                              |
| [gitWorktreeRepo.ts](gitWorktreeRepo.ts)   | 受管 worktree 的 Git 操作（docs/git/worktree.md §3.4、§6.3、§6.5）。                  |
| [index.ts](index.ts)                       | index 的实现文件。                                                                    |
| [module.ts](module.ts)                     | 实现或公开接口：moduleDefinition。                                                    |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
