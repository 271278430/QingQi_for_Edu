# workflow-entrypoints

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 workflow entrypoints 实现源码。

### 文件

| 文件                                       | 简要说明                                                                        |
| ------------------------------------------ | ------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 只注册既有入口；调用仍进入公共调度、参数校验及审批链。                          |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                        |
| [contract.ts](contract.ts)                 | 采用原 ToolEntry 与执行器契约，不包装 handler 或复制工具配置。                  |
| [module.ts](module.ts)                     | \* workflow-tool-entrypoints 模块清单（architecture-governance managed 模块）。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                |

<!-- qingqi-directory-index:end -->
