# recall

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 recall 实现源码。

### 文件

| 文件                       | 简要说明                                                                                                                       |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| [content.ts](content.ts)   | 实现或公开接口：readRecalledMemories、formatRelevantMemoryAttachment。                                                         |
| [index.ts](index.ts)       | 实现或公开接口：MEMORY_RECALL_SESSION_CHARACTER_LIMIT、createMemoryRecallState、canStartMemoryRecall、recordRecalledMemories。 |
| [manifest.ts](manifest.ts) | 单个失效的文件 symlink 与单个无法读取的事实文件一样，不影响其他 manifest 项。                                                  |
| [README.md](README.md)     | 本目录用途、子目录与逐文件说明。                                                                                               |
| [selector.ts](selector.ts) | 修复原因：显式 real_user 已经是非 meta 的事实来源，文本前缀只用于兼容缺少 metadata 的旧历史。                                  |
| [types.ts](types.ts)       | 实现或公开接口：MEMORY_RECALL_TYPES、MemoryRecallType、MemoryManifestEntry、MemorySelectorResult。                             |

<!-- qingqi-directory-index:end -->
