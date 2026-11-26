# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode-dev/plugin-api 基础工程中的 src 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                 |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 插件作者的写法（docs/plugins/extension-host.md §17.9）：按包名导入四个入口，编译期拿到与宿主相同的类型。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                 |
| [contract.ts](contract.ts)                 | 只转出 extension-host-protocol 的类型，不手写第二份；没有运行时代码。                                    |
| [manifest.ts](manifest.ts)                 | manifest 的实现文件。                                                                                    |
| [module.ts](module.ts)                     | \* plugin-api 模块清单（architecture-governance managed 模块）。                                         |
| [protocol-v4.ts](protocol-v4.ts)           | 版本跟 v4 协议走（清单 protocols.rows）。                                                                |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                         |
| [sessions.ts](sessions.ts)                 | 会话动作：SessionActionInput<"createSession"> 等                                                         |

<!-- qingqi-directory-index:end -->
