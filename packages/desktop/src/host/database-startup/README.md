# database-startup

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 database startup 实现源码。

### 文件

| 文件                                                             | 简要说明                                                                                       |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                       | 宿主构造 Worker 输入；文件路径保持原值，真实打开与迁移只发生在 Worker。                        |
| [CONTRACT.md](CONTRACT.md)                                       | 模块职责、公共接口、依赖方向和状态约定。                                                       |
| [contract.ts](contract.ts)                                       | 实现或公开接口：tasksStorageWorkerDataSchema、workerMessageSchema、TasksStorageWorkerMessage。 |
| [hostDatabaseStartup.ts](hostDatabaseStartup.ts)                 | 历史项目 ENOTDIR/无权限不是数据库失败；与普通 Agent 使用同一 cwd 选择规则。                    |
| [module.ts](module.ts)                                           | \* host-database-startup 模块清单（architecture-governance managed 模块）。                    |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                               |
| [storagePreparationProcesses.ts](storagePreparationProcesses.ts) | 在 Host 所属 Worker 运行同一 CLI bundle 的存储入口；Host 退出不会留下持锁孤儿进程。            |
| [tasksStorageWorker.ts](tasksStorageWorker.ts)                   | Worker 必须携带旧设置完成项目迁移，否则后续 Host 只能看到已记账的空项目种子。                  |

<!-- qingqi-directory-index:end -->
