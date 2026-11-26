# sqlite-migrations

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 sqlite migrations 实现源码。

### 文件

| 文件                                       | 简要说明                                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------ |
| [backup-volumes.ts](backup-volumes.ts)     | 仅在首选卷不可用时探测已挂载卷；不挂载设备，也不扫描用户内容。                       |
| [backup.ts](backup.ts)                     | 新库没有待保护的历史表；不为每个内存测试或首次安装制造空备份。                       |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：exampleSqliteMigrations。                                            |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                             |
| [contract.ts](contract.ts)                 | 历史 SQL 是 checksum 输入，发布后不可修改；apply 只供带数据回填的迁移使用。          |
| [index.ts](index.ts)                       | 实现或公开接口：sqliteMigrations。                                                   |
| [legacy.ts](legacy.ts)                     | 调用方持有库级事务；Agent 与 Source 使用同一应用原语，避免相同 ID 的 checksum 漂移。 |
| [module.ts](module.ts)                     | \* sqlite-migrations 模块清单（architecture-governance managed 模块）。              |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                     |
| [restore.ts](restore.ts)                   | 校验与复制共用备份库读快照，避免两次读取之间文件被修改；不在 JS 保留整表。           |
| [runner.ts](runner.ts)                     | 合并上游迁移时曾漏填清单，运行成功却没有备份；必须在任何 SQL 写入前拒绝。            |
| [table-snapshot.ts](table-snapshot.ts)     | 校验时可同时复制一行；原库快照和备份连接的事务由调用方持有。                         |

<!-- qingqi-directory-index:end -->
