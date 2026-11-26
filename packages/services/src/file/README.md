# file

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 file 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                                                             |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| [file.ts](file.ts)                                             | 无命中补扫：绕过尚未过期的文件索引。                                                                                 |
| [fileService.ts](fileService.ts)                               | 实现或公开接口：isSkippableWorkspaceFileListError、FileExistenceCache、CreateFileServiceOptions、createFileService。 |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                                     |
| [workspaceFileIgnore.ts](workspaceFileIgnore.ts)               | \* workspace 文件搜索忽略的单一真相源。                                                                              |
| [workspaceFileMentionFilter.ts](workspaceFileMentionFilter.ts) | \* `.zcodeignore` 规则加载成功时为 true：目录排除的单一真相源是规则文件，                                            |
| [workspaceFileSearch.ts](workspaceFileSearch.ts)               | 分批解码已有 packed 索引，防止把 Renderer 的长任务简单搬到共享 Host。                                                |

<!-- qingqi-directory-index:end -->
