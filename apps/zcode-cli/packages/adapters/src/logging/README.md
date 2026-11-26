# logging

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 logging 实现源码。

### 文件

| 文件                         | 简要说明                                                                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| [index.ts](index.ts)         | Node logging adapter - JSONL file and optional stderr sink                                                                |
| [README.md](README.md)       | 本目录用途、子目录与逐文件说明。                                                                                          |
| [retention.ts](retention.ts) | 实现或公开接口：LOG_RETENTION_DAYS、LOG_CLEANUP_STARTUP_DELAY_MS、LogRetentionCleanupOptions、LogRetentionCleanupResult。 |
| [serialize.ts](serialize.ts) | 实现或公开接口：SerializedLogError、SerializableLogEntry、DefaultLogRedactor、stripReservedContext。                      |

<!-- qingqi-directory-index:end -->
