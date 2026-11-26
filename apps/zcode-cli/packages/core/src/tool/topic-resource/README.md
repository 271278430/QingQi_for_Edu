# topic-resource

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 topic resource 实现源码。

### 文件

| 文件                                       | 简要说明                                                                               |
| ------------------------------------------ | -------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 只在注入 topicResourcePort 的运行时登记；资源索引对象原样作为输入。                    |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                               |
| [contract.ts](contract.ts)                 | 会话工具设计 0.8：原 ReadSessionContext(topic, attachment) 的唯一后继，只读取当前会话  |
| [module.ts](module.ts)                     | \* topic-resource-tool 模块清单（architecture-governance managed 模块）。              |
| [reader.ts](reader.ts)                     | 只读当前会话：授权来自最近一条带 botGroupSource 的可信用户输入，不接受模型自报的会话。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                       |

<!-- qingqi-directory-index:end -->
