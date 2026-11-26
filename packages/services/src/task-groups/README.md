# task-groups

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 task groups 实现源码。

### 文件

| 文件                                       | 简要说明                                                                          |
| ------------------------------------------ | --------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：createGroupExample。                                              |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                          |
| [contract.ts](contract.ts)                 | 来源不匹配表示另一客户端已整理，不能用旧 UI 覆盖。                                |
| [index.ts](index.ts)                       | 实现或公开接口：createTaskGroupService。                                          |
| [migration-v6.ts](migration-v6.ts)         | 冻结 0006 的只增 SQL；后续结构调整必须追加迁移，不能跟随运行 Repo 修改 checksum。 |
| [module.ts](module.ts)                     | \* task-groups 模块清单（architecture-governance managed 模块）。                 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                  |
| [repository.ts](repository.ts)             | 采用旧表的控制端组织仓库；同步 SQLite 事务内没有 await，不跨进程改写任务事实。    |

<!-- qingqi-directory-index:end -->
