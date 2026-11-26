# memory

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 memory 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                              |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [index.ts](index.ts)                                     | index 的实现文件。                                                                    |
| [memory.ts](memory.ts)                                   | 已由 MemoryService 校验并限制在本地 Project Memory 根目录内的实际路径。               |
| [memoryService.ts](memoryService.ts)                     | 只校验 workspace 子目录时，projectsRoot symlink 会让 list/read 跟随到本地数据目录外。 |
| [projectMemoryStableRead.ts](projectMemoryStableRead.ts) | 路径检查后再 readFile(path) 会重新解析路径，可能跟随并发替换的链接读取外部文件。      |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
