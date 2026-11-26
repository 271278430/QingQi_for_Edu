# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/session-control 基础工程中的 src 实现源码。

### 子目录

| 目录                                  | 存放内容                                                   |
| ------------------------------------- | ---------------------------------------------------------- |
| [application/](application/README.md) | @zcode/session-control 基础工程中的 application 实现源码。 |
| [contract/](contract/README.md)       | @zcode/session-control 基础工程中的 contract 实现源码。    |
| [domain/](domain/README.md)           | @zcode/session-control 基础工程中的 domain 实现源码。      |
| [testing/](testing/README.md)         | @zcode/session-control 基础工程中的 testing 实现源码。     |

### 文件

| 文件                                       | 简要说明                                                                                            |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：sendAndObserve。                                                                    |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                            |
| [contract.test.ts](contract.test.ts)       | 扩展新建会话时的权限模式（docs/plugins/extension-host.md §17.12）只进端口；模型的工具 schema 不变。 |
| [contract.ts](contract.ts)                 | contract 的实现文件。                                                                               |
| [module.ts](module.ts)                     | 实现或公开接口：sessionControlModule。                                                              |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                    |

<!-- qingqi-directory-index:end -->
