# session-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 session control 实现源码。

### 文件

| 文件                                       | 简要说明                                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：bindAppSessionControl。                                              |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                             |
| [contract.test.ts](contract.test.ts)       | contract.test 的实现文件。                                                           |
| [contract.ts](contract.ts)                 | 模型工具是会话类调用方：上下文总带根会话。                                           |
| [index.ts](index.ts)                       | 这里只转发模型工具（会话类调用方）；客户端类调用方只由 App Host 构造，不会经过 CLI。 |
| [module.ts](module.ts)                     | 实现或公开接口：appSessionControlClientModule。                                      |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                     |

<!-- qingqi-directory-index:end -->
