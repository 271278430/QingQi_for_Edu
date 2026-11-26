# workspace-file-search

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 workspace file search 实现源码。

### 文件

| 文件                                                                       | 简要说明                                                                       |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [fetchWorkspaceFileEntries.ts](fetchWorkspaceFileEntries.ts)               | \* 分块拉取 workspace 文件索引的列式 packed 字符串。                           |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                               |
| [useWorkspaceFileSearchFilter.ts](useWorkspaceFileSearchFilter.ts)         | 按 query 过滤并映射回的原始 entry 列表（有序）。                               |
| [workspaceFileEntriesCodec.ts](workspaceFileEntriesCodec.ts)               | 实现已上移 @zcode/shared/workspaceFileEntriesCodec（services/Host 侧也要使用， |
| [workspaceFileSearch.ts](workspaceFileSearch.ts)                           | workspaceFileSearch 的实现文件。                                               |
| [workspaceFileSearchFilter.worker.ts](workspaceFileSearchFilter.worker.ts) | \* 工作区文件搜索过滤 Worker：持有全量候选，收 query 在后台线程打分+top-K，    |
| [workspaceFileSearchFilterBackend.ts](workspaceFileSearchFilterBackend.ts) | \* 工作区文件搜索过滤后端抽象：候选打分+top-K 排序的执行位置。                 |

<!-- qingqi-directory-index:end -->
