# tool-result-settlement

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 tool result settlement 实现源码。

### 文件

| 文件                                       | 简要说明                                                                      |
| ------------------------------------------ | ----------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 把原 Runtime 与整批结果交回同一结算方法，不复制历史或再执行工具。             |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                      |
| [contract.ts](contract.ts)                 | 整批结果先进入 Runtime 历史，再等待既有持久化；沿用原调用方、错误和取消语义。 |
| [module.ts](module.ts)                     | \* tool-result-settlement 模块清单（architecture-governance managed 模块）。  |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                              |

<!-- qingqi-directory-index:end -->
