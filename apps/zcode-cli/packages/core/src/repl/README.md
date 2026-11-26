# repl

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 repl 实现源码。

### 文件

| 文件                                                         | 简要说明                                                                                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| [browser-turn-state.ts](browser-turn-state.ts)               | 实现或公开接口：BrowserTurnScreenshotCandidate、recordBrowserTurnPageActivity、recordBrowserTurnToolResult、consumeBrowserTurnState。 |
| [executors.ts](executors.ts)                                 | \* ReplExecutor —— 「执行 + 跨调用持久」策略接缝（A-ready）。                                                                         |
| [instrument.ts](instrument.ts)                               | \* REPL 代码 instrument 纯函数集（路线 B：顶层绑定跨调用持久）。                                                                      |
| [node-repl-runtime-helpers.ts](node-repl-runtime-helpers.ts) | screenshot() 返回 Uint8Array；JSON.stringify 会把每个字节展开成数字键，                                                               |
| [node-repl-session.ts](node-repl-session.ts)                 | REPL 收集的图片（nodeRepl.emitImage）。                                                                                               |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                                                      |

<!-- qingqi-directory-index:end -->
