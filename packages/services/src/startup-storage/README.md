# startup-storage

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 startup storage 实现源码。

### 文件

| 文件                                       | 简要说明                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：exampleStartupStorage。                                        |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                       |
| [contract.ts](contract.ts)                 | 采用已有 Agent executable resolver 的结果；协议命令前的 runtime 参数原样保留。 |
| [index.ts](index.ts)                       | 实现或公开接口：startupStorage。                                               |
| [module.ts](module.ts)                     | \* startup-storage 模块清单（architecture-governance managed 模块）。          |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                               |

<!-- qingqi-directory-index:end -->
