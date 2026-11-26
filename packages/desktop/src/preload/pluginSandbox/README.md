# pluginSandbox

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pluginSandbox 实现源码。

### 文件

| 文件                                 | 简要说明                                                                                           |
| ------------------------------------ | -------------------------------------------------------------------------------------------------- |
| [hostBridge.ts](hostBridge.ts)       | \* 插件 UI 沙箱：独立命名空间，不进 window.zcode。只暴露明确的沙箱操作；                           |
| [index.ts](index.ts)                 | \* 插件 UI 沙箱 guest 的 preload。只做一件事：把 main 送来的那条 MessagePort 经 window.postMessage |
| [README.md](README.md)               | 本目录用途、子目录与逐文件说明。                                                                   |
| [retainedMoves.ts](retainedMoves.ts) | 在 Electron 注册 webview 前于主世界执行；函数不能捕获 preload 的闭包。                             |

<!-- qingqi-directory-index:end -->
