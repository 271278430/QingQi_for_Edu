# repo

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 repo 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                        |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| [gitCheckpointHelpers.ts](gitCheckpointHelpers.ts) | 实现或公开接口：toAbsolutePath、getWorkspacePathspec、getCheckpointRefName、parseNameStatus。   |
| [gitCheckpointRepo.ts](gitCheckpointRepo.ts)       | 所有 checkpoint 操作都必须建立在“当前 workspace 对应一个真实 Git 仓库”这个前提上。              |
| [gitCheckpointStore.ts](gitCheckpointStore.ts)     | 一个 workspace 的检查点目录；项目数据删除按同一规则定位，不能另算 hash。                        |
| [gitCliHelpers.ts](gitCliHelpers.ts)               | 分支切换是否被阻塞，最终以 Git 原生命令的真实报错为准。                                         |
| [gitCliRepo.ts](gitCliRepo.ts)                     | 完整 diff 的任一侧读取失败后若被补成空字符串，UI 会把“不可读”误判成                             |
| [gitCliTypes.ts](gitCliTypes.ts)                   | 实现或公开接口：GitLineStat、GitStatusEntry、GitBranchComparisonChange、GitResolvedRepository。 |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                |

<!-- qingqi-directory-index:end -->
