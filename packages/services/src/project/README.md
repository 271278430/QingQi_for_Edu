# project

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 project 实现源码。

### 子目录

| 目录                    | 存放内容                                     |
| ----------------------- | -------------------------------------------- |
| [data/](data/README.md) | @zcode/services 基础工程中的 data 实现源码。 |

### 文件

| 文件                                               | 简要说明                                                                                         |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [autoArchiveScheduler.ts](autoArchiveScheduler.ts) | \* 扫描只读一次设置 + 一次索引小查询，代价可忽略；5 分钟让刚超期或刚失去保护的任务               |
| [contract.example.ts](contract.example.ts)         | 实现或公开接口：projectExample、openFolderExample。                                              |
| [CONTRACT.md](CONTRACT.md)                         | 模块职责、公共接口、依赖方向和状态约定。                                                         |
| [contract.ts](contract.ts)                         | 当前 Host 的权威项目服务；远端通过现有 attachment 的服务代理调用。                               |
| [index.ts](index.ts)                               | Bug 原因（ZCT-2113660144497782784）：目录的 stat 可能永久不返回（例如 macOS 等待文件夹访问授权、 |
| [legacy-single-root.ts](legacy-single-root.ts)     | 旧 Server 的只读边界；实际 RPC 的选择由连接装配器完成。                                          |
| [module.ts](module.ts)                             | \* project 模块清单（architecture-governance managed 模块）。                                    |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                 |

<!-- qingqi-directory-index:end -->
