# mcp

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 mcp 实现源码。

### 文件

| 文件                                             | 简要说明                                                                                              |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| [app-tools.ts](app-tools.ts)                     | MCP Apps App-Provided Tools → core 工具条目。条目只描述「模型怎么看见、审批怎么走、结果怎么进模型」； |
| [image-normalization.ts](image-normalization.ts) | 帧像素契约（integrity gate + inline 上限）的唯一定义在 producer；宿主经                               |
| [index.ts](index.ts)                             | MCP tool bridge - projects MCP descriptors into core tool entries                                     |
| [name.ts](name.ts)                               | 模型可见的 MCP 工具名都以 `mcp__` 开头。                                                              |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                                      |

<!-- qingqi-directory-index:end -->
