# mcp-apps

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 mcp apps 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                             |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| [appTools.ts](appTools.ts)                 | \* App-Provided Tools（MCP Apps 规范「App-Provided Tools」）：页面在 `ui/initialize` 声明 `tools` 能力后，           |
| [content.ts](content.ts)                   | 把 content 块里的 text 拼成一段纯文本；非 text 块跳过。                                                              |
| [contract.example.ts](contract.example.ts) | 一个带 UI 资源的工具 `_meta` 归一化后应得到的描述。                                                                  |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                             |
| [contract.ts](contract.ts)                 | \* MCP Apps 协议契约：agent、host、renderer 与 main 共用的常量、工具 UI 元数据类型、沙箱句柄与登记载荷。             |
| [hostContract.ts](hostContract.ts)         | \* MCP Apps 宿主侧契约的第二半：ui/download-file 项、tool-input / tool-result 载荷、宿主提供的 titleBar 与样式变量。 |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                                   |
| [instance.ts](instance.ts)                 | Agent 签发的内存凭证；Main 的 initId 只用于端口握手。                                                                |
| [module.ts](module.ts)                     | \* mcp-apps-protocol 模块清单（architecture-governance managed 模块）。                                              |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                                     |
| [resourceMime.ts](resourceMime.ts)         | \* 页面发起的 `resources/read`（`mcp/uiReadResource`）单次结果总大小上限，以及 mimeType 白名单。                     |
| [sampling.ts](sampling.ts)                 | 重复四字符分组会在 MiB 级图片上耗尽 V8 正则栈；平坦字符检查保持线性。                                                |
| [schemas.ts](schemas.ts)                   | \* 以下 schema 是 mcp-apps-protocol 的运行时校验面：只覆盖 ZCode 自己的投影 / 元数据形状。                           |
| [toolMeta.ts](toolMeta.ts)                 | \* 工具可见性与 UI 呈现解耦。只读 `_meta.ui.visibility`，缺省 `["model", "app"]`；                                   |

<!-- qingqi-directory-index:end -->
