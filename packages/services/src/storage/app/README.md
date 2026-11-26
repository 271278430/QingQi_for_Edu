# app

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 app 实现源码。

### 文件

| 文件                                   | 简要说明                                                                                    |
| -------------------------------------- | ------------------------------------------------------------------------------------------- |
| [ports.ts](ports.ts)                   | \* app 层端口：storageService 只依赖这些接口，IO 由 adapters 实现并在 desktop host 注入。   |
| [README.md](README.md)                 | 本目录用途、子目录与逐文件说明。                                                            |
| [scanJob.ts](scanJob.ts)               | \* 单次扫描 job：持有 AbortController，把 runner 的进度节流成 ≥ throttleMs 一次的快照事件， |
| [storageService.ts](storageService.ts) | \* IStorageService 实现：扫描 job、最近快照、清理的唯一 owner。                             |

<!-- qingqi-directory-index:end -->
