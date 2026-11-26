# packaging

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server-cli 基础工程中的 packaging 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                      |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| [nodeDistMirror.ts](nodeDistMirror.ts)             | \* Node dist 下载源的唯一解析点（本包内）。                                                   |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                              |
| [remoteAssetRelease.ts](remoteAssetRelease.ts)     | Bug 原因：新一代构建在 collect 前失败时，旧 descriptor 仍可让开发连接成功消费上一代 archive。 |
| [stage.ts](stage.ts)                               | tsup 产物目录（server-cli.js / server-core.js）                                               |
| [stageArchives.ts](stageArchives.ts)               | Bug 原因：Windows runner 的 PATH 可能优先命中 Git Bash GNU tar，且系统没有                    |
| [stageCli.ts](stageCli.ts)                         | DOM fetch 的 ReadableStream 与 node:stream/web 的同名类型在 @types/node 下不兼容，            |
| [stageDependencies.ts](stageDependencies.ts)       | 提取 bundle 的顶层裸模块引用，并过滤 Node 内置模块。                                          |
| [stageRemoteAssetsCli.ts](stageRemoteAssetsCli.ts) | Bug 原因：Windows 上 pnpm 只以 .cmd/.ps1 shim 存在，Node 不经 shell 无法解析，                |
| [tarCommand.ts](tarCommand.ts)                     | Windows：Git Bash 可能把 GNU tar 前置到 PATH——它会把归档参数里的 `C:` 当远程主机、            |

<!-- qingqi-directory-index:end -->
