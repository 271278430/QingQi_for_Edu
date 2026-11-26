# official-command-endpoint

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 official command endpoint 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                               |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | \* cli-official-command-endpoint 标准调用：agent 入口创建一个端点，每个 session 的执行端口用它包一层。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                               |
| [contract.ts](contract.ts)                 | \* cli-official-command-endpoint 对外契约（ZCode Sites 技术方案 5.8）。                                |
| [endpoint.ts](endpoint.ts)                 | 官方插件命令进程的本地代理端点（ZCode Sites 技术方案 5.8）。                                           |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                     |
| [module.ts](module.ts)                     | \* cli-official-command-endpoint 模块清单（architecture-governance managed 模块）。                    |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                       |

<!-- qingqi-directory-index:end -->
