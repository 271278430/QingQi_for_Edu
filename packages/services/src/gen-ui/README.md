# gen-ui

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 gen ui 实现源码。

### 子目录

| 目录                            | 存放内容                                                   |
| ------------------------------- | ---------------------------------------------------------- |
| [adapters/](adapters/README.md) | @zcode/services 基础工程中的 adapters 外部能力与平台适配。 |
| [app/](app/README.md)           | @zcode/services 基础工程中的 app 实现源码。                |

### 文件

| 文件                                       | 简要说明                                                                                        |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：exampleGenUiPrepare。                                                           |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                        |
| [contract.ts](contract.ts)                 | readDocument runs on the executor Host. State and sandbox methods run on desktop base services. |
| [index.ts](index.ts)                       | index 的实现文件。                                                                              |
| [module.ts](module.ts)                     | 实现或公开接口：genUiServiceModule。                                                            |
| [node.ts](node.ts)                         | node 的实现文件。                                                                               |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                |

<!-- qingqi-directory-index:end -->
