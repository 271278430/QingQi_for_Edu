# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

运行层的公开契约、能力实现和 Python/Node 通信入口。

### 文件

| 文件                                       | 简要说明                                                |
| ------------------------------------------ | ------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：example。                               |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                |
| [contract.ts](contract.ts)                 | 实现或公开接口：TOOL_NAMES、ToolName、Frame、ToolSpec。 |
| [index.ts](index.ts)                       | 基于ZCode注册工具、调度、权限、MCP与Skills运行能力。    |
| [memory.ts](memory.ts)                     | 按授权范围、去重与读取预算筛选学习记忆。                |
| [model-options.ts](model-options.ts)       | 调用ZCode受限CEL编译器映射模型参数。                    |
| [module.ts](module.ts)                     | 实现或公开接口：moduleId。                              |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                        |
| [server.ts](server.ts)                     | Python与Node运行层之间的请求、结果和错误通信入口。      |

<!-- qingqi-directory-index:end -->
