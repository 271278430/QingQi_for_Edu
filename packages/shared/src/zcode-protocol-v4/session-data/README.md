# session-data

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 session data 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                        |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* protocol-session-data 标准调用示例：Host 为一个项目测量、删除数据时发出的载荷与 CLI 的回包。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                        |
| [contract.ts](contract.ts)                 | 项目数据彻底删除（docs/superpowers/specs/2026-10-24-project-management.md「彻底删除数据」）。   |
| [index.ts](index.ts)                       | index 的实现文件。                                                                              |
| [module.ts](module.ts)                     | \* protocol-session-data 模块清单（architecture-governance managed 模块）。                     |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                |

<!-- qingqi-directory-index:end -->
