# preload

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 preload 实现源码。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [pluginSandbox/](pluginSandbox/README.md) | @zcode/desktop 基础工程中的 pluginSandbox 实现源码。 |

### 文件

| 文件                                                                     | 简要说明                                                                                        |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| [browserVideoRecorder.ts](browserVideoRecorder.ts)                       | MessagePort 不能经 contextBridge 代理；专用 preload 只把 main 定向发送的 port 转交给            |
| [codingPlanWebview.ts](codingPlanWebview.ts)                             | Coding Plan 官网页 preload：                                                                    |
| [cuaPermissionPanel.ts](cuaPermissionPanel.ts)                           | \* CUA 权限拖拽浮窗的 preload。                                                                 |
| [embeddedBrowserDesignBridge.ts](embeddedBrowserDesignBridge.ts)         | 设计运行时页面 → 宿主的转发（docs/browser-use/2026-11-03-browser-design-mode-spec.md 第二节）。 |
| [embeddedBrowserJavaScriptDialog.ts](embeddedBrowserJavaScriptDialog.ts) | Main 不可用时退回 Chromium 原生 API，不能吞掉网页 Dialog。                                      |
| [embeddedBrowserWheel.ts](embeddedBrowserWheel.ts)                       | 将触控板、滚轮和 Shift+滚轮统一成宿主画布使用的 CSS pixel 二维 delta。                          |
| [index.ts](index.ts)                                                     | ARMS frame preload 闭包内的 send 不会随后序 ipcRenderer.send 补丁生效，须同步包装 Bridge.send   |
| [oauthCallbackBridge.ts](oauthCallbackBridge.ts)                         | preload 只负责桥接 OAuth 回调与主进程握手，不能把 renderer 回调异常继续外抛成未处理 rejection。 |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                |
| [resourceManager.ts](resourceManager.ts)                                 | \* 资源管理器窗口专用 preload —— 资源快照拉取 + 存储管理命令面。                                |
| [rewardsWebview.ts](rewardsWebview.ts)                                   | 普通网页和三方导航不能继承邀请页的 bridge；仅宿主批准的开发模式允许 localhost。                 |

<!-- qingqi-directory-index:end -->
