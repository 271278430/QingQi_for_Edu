# browser-use

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 browser use 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                                                                    |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [backend.ts](backend.ts)                   | \* Browser backend family。Playwright 是 Tab 上的能力层，不是 backend。                                                                                     |
| [command-metadata.ts](command-metadata.ts) | 内置自由尺寸与 Agent viewport API 共用同一组 CSS px 安全边界。                                                                                              |
| [commands.ts](commands.ts)                 | 键盘修饰键；CDP dispatchMouse/KeyEvent 的 modifiers 位掩码由 executor 映射。                                                                                |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                                                                          |
| [nodeReplBroker.ts](nodeReplBroker.ts)     | 实现或公开接口：NODE_REPL_BROWSER_BROKER_SOCKET_ENV、NODE_REPL_BROWSER_BROKER_TOKEN_ENV、nodeReplBrowserBrokerRequestSchema、NodeReplBrowserBrokerRequest。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                                                                            |
| [result.ts](result.ts)                     | \* 受控 tab 摘要（list 命令返回）：agent 用 tabId 寻址某个具体 tab（含 human 开的 tab）。                                                                   |
| [snapshot.ts](snapshot.ts)                 | \* 单个可交互元素的快照条目，以 role、name、ref 提供定位信息，避免转储整页 DOM。                                                                            |

<!-- qingqi-directory-index:end -->
