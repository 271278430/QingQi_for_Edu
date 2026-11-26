# terminal

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 terminal 实现源码。

### 文件

| 文件                                                                     | 简要说明                                                                                   |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                           |
| [sidePaneTerminalSessionRegistry.ts](sidePaneTerminalSessionRegistry.ts) | sidePaneTerminalSessionRegistry —— side pane terminal 跨 workspace 会话保活的模块级单例。  |
| [terminalComposedInputFallback.ts](terminalComposedInputFallback.ts)     | 手机 229 输入由原生 input 事件提交，避免与 xterm 的定时 textarea 读取竞争。                |
| [terminalDataTransform.ts](terminalDataTransform.ts)                     | Windows PowerShell/PSReadLine 重绘当前输入行时，会用 ANSI 40m 给尾随空白 cell 补黑色背景。 |
| [terminalLinks.ts](terminalLinks.ts)                                     | 实现或公开接口：findHttpLinksInTerminalText、getHttpLinksForTerminalBufferLine。           |
| [terminalPanelState.ts](terminalPanelState.ts)                           | 把 nextIndex 作为只增不减的派生状态保存，会让关闭编号 2 后再新建错误地得到 3。             |
| [TerminalSession.tsx](TerminalSession.tsx)                               | \* 跨组件生命周期的会话采用 key（仅 side pane terminal 用）。                              |
| [TerminalTabTrigger.tsx](TerminalTabTrigger.tsx)                         | 实现或公开接口：TerminalTabTrigger。                                                       |
| [terminalTheme.ts](terminalTheme.ts)                                     | \* xterm 的 `css.toColor` 不认 `color-mix()`、`var()`、现代 `rgb(r g b / a)` 新语法。      |

<!-- qingqi-directory-index:end -->
