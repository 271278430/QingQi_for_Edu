# provider-builtin-tool-compat

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 provider builtin tool compat 验收与回归场景。

### 文件

| 文件                                             | 简要说明                                                                                 |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| [contract.test.ts](contract.test.ts)             | SSE 端到端（经 anthropic-stream-compat 与 AI SDK）见 model-execution.test.ts。           |
| [mcp-format.test.ts](mcp-format.test.ts)         | 新格式：服务端直接下发 mcp_tool_use / mcp_tool_result，结果摘要在结果之后。              |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                         |
| [stream-test-helpers.ts](stream-test-helpers.ts) | provider-builtin-tool-compat 契约用例共用的帧构造：逐帧喂给改写器，返回下游看到的 JSON。 |

<!-- qingqi-directory-index:end -->
