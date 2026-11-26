# workspace-mcp-trust

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 workspace mcp trust 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                     |
| ------------------------------------------ | -------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 真实调用必须来自用户对当前行的显式审核动作。                                                 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                     |
| [contract.test.ts](contract.test.ts)       | 契约测试只 import contract 与 module，不知道实现是谁；同一份测试应同时跑真实现与跨进程代理。 |
| [contract.ts](contract.ts)                 | 只读当前声明及持久授权；不连接 MCP。                                                         |
| [index.ts](index.ts)                       | 同一 Host 的用户存储是唯一授权 owner；项目 storage.dir 不能选择信任文件。                    |
| [module.ts](module.ts)                     | \* workspace-mcp-trust 模块清单（architecture-governance managed 模块）。                    |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                             |

<!-- qingqi-directory-index:end -->
