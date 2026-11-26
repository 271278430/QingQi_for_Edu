# materialization

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 materialization 实现源码。

### 文件

| 文件                                       | 简要说明                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：measureWireExample。                                                  |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                              |
| [contract.test.ts](contract.test.ts)       | contract.test 的实现文件。                                                            |
| [contract.ts](contract.ts)                 | 只能传尚未发布的候选，不得传 publisher 当前权威投影。                                 |
| [index.ts](index.ts)                       | 无状态的 conversation 投影视图与候选重放；状态仍由 publisher/ProductProjection 持有。 |
| [module.ts](module.ts)                     | 实现或公开接口：conversationMaterializationModule。                                   |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
