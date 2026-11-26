# plugin-sandbox

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 plugin sandbox 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                                                       |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| [alias.ts](alias.ts)                                               | \* 注入到插件 HTML 顶部的 `window.zcode` / `window.openai` 别名（以 IIFE 打包为 out/plugin-sandbox/plugin-sandbox-alias.js）。 |
| [aliasApi.ts](aliasApi.ts)                                         | `window.zcode` / `window.openai` 的公开形状；实现在 aliasRuntime / openaiAlias，两边只依赖这里。                               |
| [aliasRuntime.ts](aliasRuntime.ts)                                 | \* 插件 iframe 内 `window.zcode` / `window.openai` 别名的运行时：官方 ext-apps `App` 上的薄封装，协议、握手、                  |
| [desktopPluginSandboxPlatform.ts](desktopPluginSandboxPlatform.ts) | \* 桌面 renderer 的插件沙箱平台端口：原生操作委托 preload 命名空间，那条 JSON-RPC 端口从 preload 经                            |
| [genUi.ts](genUi.ts)                                               | 旧 SDK 临时改写 html 高度来测量，测量自身会触发溢出布局；这里仅读取实际内容。                                                  |
| [genUiTweakRuntime.d.ts](genUiTweakRuntime.d.ts)                   | 类型边界由 Gen UI 消息 schema 校验；函数体保留上游 JavaScript。                                                                |
| [genUiTweakRuntime.js](genUiTweakRuntime.js)                       | oxlint-disable max-lines -- Keep parameter binding and registration lifecycle in one runtime.                                  |
| [main.ts](main.ts)                                                 | \* 受信 relay shell 的 DOM 接线：监听 preload 转交的 init 帧，创建插件 iframe，                                                |
| [openaiAlias.ts](openaiAlias.ts)                                   | 全部转调同一 `window.zcode` 实例；globals 变化时由 alias.ts 派发 `openai:set_globals`（detail.globals 与本对象同源）。         |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                                               |
| [relay.ts](relay.ts)                                               | \* 受信 relay shell 的纯逻辑：不解析、不缓冲协议消息，只在宿主 MessagePort 与插件 iframe 之间原样转发 JSON-RPC。               |

<!-- qingqi-directory-index:end -->
