# channel-reply

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 channel reply 实现源码。

### 文件

| 文件                                       | 简要说明                                                                        |
| ------------------------------------------ | ------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 只登记既有 ToolEntry；实际发送仍通过公共工具执行链。                            |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                        |
| [contract.ts](contract.ts)                 | 采用原工具入口；执行输入绑定、发送、取消和错误继续由 handler 与 Host 端口负责。 |
| [module.ts](module.ts)                     | \* channel-reply-tool 模块清单（architecture-governance managed 模块）。        |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                |

<!-- qingqi-directory-index:end -->
