# provider-builtin-tool-compat

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 provider builtin tool compat 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                 |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| [compat.ts](compat.ts)                     | Provider 内置工具（GLM 的 analyze_image / webReader 等）的 Anthropic 线协议兼容。                        |
| [contract.example.ts](contract.example.ts) | \* provider-builtin-tool-compat 标准调用示例：在 SSE transform 里逐帧交给 rewriter，流结束时补发缓冲帧。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                 |
| [contract.ts](contract.ts)                 | \* Provider 内置工具线协议兼容的公开入口（docs/design/v2/model/anthropic-stream-compat.md                |
| [module.ts](module.ts)                     | \* provider-builtin-tool-compat 模块清单（architecture-governance managed 模块）。                       |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                         |

<!-- qingqi-directory-index:end -->
