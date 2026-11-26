# session-data

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 session data 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                                              |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)     | \* cli-session-data 标准调用示例：一个不加载任何会话的最小宿主（管理面进程的情形）。                                  |
| [CONTRACT.md](CONTRACT.md)                     | 模块职责、公共接口、依赖方向和状态约定。                                                                              |
| [contract.test.ts](contract.test.ts)           | 执行面的行为测试在 packages/bootstrap/tests/session-data.test.ts（释放顺序、运行中保留、失败留行、幂等）。            |
| [contract.ts](contract.ts)                     | cli-session-data 对外契约：v4/storage/sessionData/\* 执行面依赖的窄宿主接口。                                         |
| [index.ts](index.ts)                           | 项目数据彻底删除的 CLI 执行面（v4/storage/sessionData/\*）。                                                          |
| [module.ts](module.ts)                         | \* cli-session-data 模块清单（architecture-governance managed 模块）。                                                |
| [permanent-deletion.ts](permanent-deletion.ts) | 实现或公开接口：SessionDeletionHost、previewSessionDeletionWith、executeSessionDeletionWith、previewSessionDeletion。 |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                                                      |

<!-- qingqi-directory-index:end -->
