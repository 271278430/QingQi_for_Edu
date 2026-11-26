# project-storage

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 project storage 实现源码。

### 子目录

| 目录                                              | 存放内容                                                  |
| ------------------------------------------------- | --------------------------------------------------------- |
| [default-workspace/](default-workspace/README.md) | @zcode/services 基础工程中的 default workspace 实现源码。 |
| [migration-order/](migration-order/README.md)     | @zcode/services 基础工程中的 migration order 实现源码。   |
| [purge/](purge/README.md)                         | @zcode/services 基础工程中的 purge 实现源码。             |

### 文件

| 文件                                             | 简要说明                                                                                            |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)       | \* project-storage 标准调用示例：agent 靠模仿写代码，这里放的就是该模仿的那份。                     |
| [CONTRACT.md](CONTRACT.md)                       | 模块职责、公共接口、依赖方向和状态约定。                                                            |
| [contract.ts](contract.ts)                       | 可信持库 Server 身份；不受客户端请求或旧 canonical route 影响。                                     |
| [index.ts](index.ts)                             | 彻底删除项目数据的行操作；与 repository() 同一 Host 范围（规格见 purge/contract.ts）。              |
| [legacy-tasks.ts](legacy-tasks.ts)               | 同一 workspace 的持久化父事实优先于目录匹配；父引用缺失时不能退回目录猜测。                         |
| [migrate-projects.ts](migrate-projects.ts)       | Bug 原因：历史任务目录不代表用户仍保留该工作区，扫描 tasks 会复活已移除的项目入口。                 |
| [module.ts](module.ts)                           | \* project-storage 模块清单（architecture-governance managed 模块）。                               |
| [project-repository.ts](project-repository.ts)   | \* worktree 任务的放置：workspace 是项目，cwd 位于受管 worktree 内（docs/git/worktree.md §6.6.1）。 |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                                    |
| [remote-policy.ts](remote-policy.ts)             | 远端限制必须依据持库宿主，不能让请求中的 hostId 或 addMissingRoot 绕过。                            |
| [repository-contract.ts](repository-contract.ts) | 所属 Host 异步探测的只读投影，不写入项目数据库或远端入口缓存；旧 Server 可省略。                    |
| [schema.baseline.sql](schema.baseline.sql)       | schema.baseline 模块的资源或工程文件。                                                              |
| [schema.ts](schema.ts)                           | 远端项目删除态缓存；在线刷新写入，离线回退读取，避免已删项目以缓存行复现。                          |
| [startup-entry.ts](startup-entry.ts)             | startup-entry 的实现文件。                                                                          |
| [startup.ts](startup.ts)                         | 与既有 Repo 一致：避免构建器把 node:sqlite 改写成不存在的 npm sqlite 包。                           |

<!-- qingqi-directory-index:end -->
