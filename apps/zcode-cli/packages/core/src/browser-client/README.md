# browser-client

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 browser client 实现源码。

### 文件

| 文件                                 | 简要说明                                                                                  |
| ------------------------------------ | ----------------------------------------------------------------------------------------- |
| [documentation.ts](documentation.ts) | Browser Use MCP 已是每次调用 fresh kernel；fallback 不能继续诱导模型采用 global binding。 |
| [facade.ts](facade.ts)               | 视口坐标点（cua 坐标路 / drag / elementInfo 用；与 CDP Input 同坐标系）。                 |
| [index.ts](index.ts)                 | 实现或公开接口：setupBrowserRuntime。                                                     |
| [manifest.ts](manifest.ts)           | open() 是默认导航入口（同站采用 + 激活 + 原地跳转）；不声明会被 hideUnknown               |
| [playwright.ts](playwright.ts)       | 实现或公开接口：TextMatcher、LoadState、WaitUntil、WaitForState。                         |
| [README.md](README.md)               | 本目录用途、子目录与逐文件说明。                                                          |
| [result.ts](result.ts)               | 实现或公开接口：BrowserCommandError、base64ToBytes、expectOk、expectPayload。             |
| [selection.ts](selection.ts)         | \* open(url) 的 tab 采用匹配：在 agent-owned tabs 里挑最值得原地跳转的一个。              |

<!-- qingqi-directory-index:end -->
