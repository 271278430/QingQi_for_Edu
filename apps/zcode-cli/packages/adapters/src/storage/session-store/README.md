# session-store

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 session store 实现源码。

### 子目录

| 目录                                    | 存放内容                                             |
| --------------------------------------- | ---------------------------------------------------- |
| [migrations/](migrations/README.md)     | @zcode/adapters 基础工程中的 migrations 数据库迁移。 |
| [repositories/](repositories/README.md) | @zcode/adapters 基础工程中的 repositories 实现源码。 |

### 文件

| 文件                                               | 简要说明                                                                                                                             |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| [codecs.ts](codecs.ts)                             | 迁移无法确定身份时可能留下 null；回滚后也可能缺字段。不能让配置残缺阻断整条消息的协议读取。                                          |
| [errors.ts](errors.ts)                             | 实现或公开接口：SqliteSessionMigrationErrorKind、SqliteSessionMigrationErrorOptions、SqliteSessionMigrationError。                   |
| [json.ts](json.ts)                                 | 实现或公开接口：encodeJson、decodeJson。                                                                                             |
| [migration-runner.ts](migration-runner.ts)         | 实现或公开接口：DEFAULT_SQLITE_STARTUP_LOCK_TIMEOUT_MS、SqliteMigrationPhase、SqliteMigrationProgress、AsyncSqliteMigrationOptions。 |
| [migrations.ts](migrations.ts)                     | 实现或公开接口：SQLITE_MIGRATIONS。                                                                                                  |
| [options.ts](options.ts)                           | 仅供事务原子性测试；生产调用不得设置。                                                                                               |
| [paths.ts](paths.ts)                               | 实现或公开接口：getDefaultSessionDbPath。                                                                                            |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                                                     |
| [rows.ts](rows.ts)                                 | 实现或公开接口：SessionRow、MessageRow、PartRow、SessionEntryRow。                                                                   |
| [schema.baseline.sql](schema.baseline.sql)         | schema.baseline 模块的资源或工程文件。                                                                                               |
| [sqlite-session-store.ts](sqlite-session-store.ts) | 端口留在领域包 @zcode/dynamic-workflow，这里只做类型引用：adapters 运行时不依赖它。                                                  |

<!-- qingqi-directory-index:end -->
