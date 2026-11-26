# app-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 app control 实现源码。

### 文件

| 文件                                       | 简要说明                                                        |
| ------------------------------------------ | --------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：appControlListExample。                         |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                        |
| [contract.ts](contract.ts)                 | 由 CLI tool runtime 注入；Host 仍需用活跃连接及根会话事实核对。 |
| [index.ts](index.ts)                       | index 的实现文件。                                              |
| [module.ts](module.ts)                     | 实现或公开接口：appControlProtocolModule。                      |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                |

<!-- qingqi-directory-index:end -->
