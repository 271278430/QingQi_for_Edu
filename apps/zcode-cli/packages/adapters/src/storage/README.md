# storage

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 storage 实现源码。

### 子目录

| 目录                                                | 存放内容                                                   |
| --------------------------------------------------- | ---------------------------------------------------------- |
| [session-data-files/](session-data-files/README.md) | @zcode/adapters 基础工程中的 session data files 实现源码。 |
| [session-store/](session-store/README.md)           | @zcode/adapters 基础工程中的 session store 实现源码。      |

### 文件

| 文件                                                           | 简要说明                                                                                                              |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [fs-fault-injection.ts](fs-fault-injection.ts)                 | 实现或公开接口：ZCODE_E2E_FS_FAULTS_ENV、ZCODE_E2E_FS_FAULTS_ALLOW_ENV、StorageFsFaultOperation、StorageFsFaultRule。 |
| [index.ts](index.ts)                                           | Storage adapters - EventStore, ArtifactStore, MemoryStore implementations                                             |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                                      |
| [session-store.ts](session-store.ts)                           | run 内省查询的类型住在 adapters 而不是 contracts：它们说的是 **journal 行**的词汇                                     |
| [session-target.ts](session-target.ts)                         | SQLite session target helpers                                                                                         |
| [workspace-hook-trust-store.ts](workspace-hook-trust-store.ts) | 进程启动时间的比较容差：ps/proc 的秒级精度 + 调度延迟，2s 足以覆盖且不放过采用。                                      |

<!-- qingqi-directory-index:end -->
