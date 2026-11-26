# runtime-subagents

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 runtime subagents 实现源码。

### 文件

| 文件                                       | 简要说明                                                                   |
| ------------------------------------------ | -------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：exampleSubagentConfiguration。                             |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                   |
| [contract.ts](contract.ts)                 | 文件 IO 由 loader 完成；本模块只解析注入文本，不读取磁盘或补充 Host 快照。 |
| [index.ts](index.ts)                       | 独立 CLI 的磁盘 loader 采用共享纯解析器，保留原文件配置来源。              |
| [module.ts](module.ts)                     | \* cli-subagent-config 模块清单（architecture-governance managed 模块）。  |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                           |

<!-- qingqi-directory-index:end -->
