# app

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 app 实现源码。

### 文件

| 文件                                                                     | 简要说明                                                                                                    |
| ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| [pluginUiAppTools.ts](pluginUiAppTools.ts)                               | tools/list 翻页上限：够取满 50 个工具，防页面返回无穷游标。                                                 |
| [pluginUiBackgroundRetention.ts](pluginUiBackgroundRetention.ts)         | 只管理显式声明的 MCP 页面；不接管共享容量或 Gen UI 的五分钟回收。                                           |
| [pluginUiDisclosureStore.ts](pluginUiDisclosureStore.ts)                 | \* 用户对插件卡片的手动固定 / 收起（renderer 视图态，不持久化）。                                           |
| [pluginUiFollowUpDialogStore.ts](pluginUiFollowUpDialogStore.ts)         | \* 无用户手势的 sendFollowUpMessage 需要用户确认（可编辑 prompt）。                                         |
| [pluginUiHostAppHandlers.ts](pluginUiHostAppHandlers.ts)                 | \* 页面发起的规范请求 / 通知接到官方 AppBridge：`ui/request-display-mode`、`tools/call`、`ui/open-link`、   |
| [pluginUiHostBridge.ts](pluginUiHostBridge.ts)                           | 官方 SDK 请求 handler 的上下文子集：中止信号在 `ctx.mcpReq.signal`。                                        |
| [pluginUiHostController.ts](pluginUiHostController.ts)                   | initialized 已到：可以直接 send*；之前的 notify* 不排队——initialized 时按 getToolFeed 读最新值。            |
| [pluginUiHostControllerContract.ts](pluginUiHostControllerContract.ts)   | \* 宿主侧编排：prepareSandbox → 拿句柄挂 webview → 等 initId 匹配的端口 → `AppBridge(null)` 接 Transport →  |
| [pluginUiHostTeardown.ts](pluginUiHostTeardown.ts)                       | \* 实例卸载的收尾顺序：已握手的实例先给页面 `ui/resource-teardown` 的清理窗口（回包或超时），再关桥与端口、 |
| [pluginUiInstanceStore.ts](pluginUiInstanceStore.ts)                     | \* 每个会话最近一次由时间线推导出的逻辑 UI 裁决（renderer 内存）。时间线在 effect 里写入，                  |
| [pluginUiInteractionPorts.ts](pluginUiInteractionPorts.ts)               | 宿主实例注入的交互回调；缺省时对应请求回 -32601（能力声明与回调一一对应）。                                 |
| [pluginUiPageManager.ts](pluginUiPageManager.ts)                         | 窗口级页面 owner。视图只持锚点租约，切位置不会销毁 controller 或活页面。                                    |
| [pluginUiResourceNotificationBus.ts](pluginUiResourceNotificationBus.ts) | \* server 资源通知的路由表（renderer 内存）。                                                               |
| [pluginUiResourceSubscriptions.ts](pluginUiResourceSubscriptions.ts)     | \* 一个沙箱实例发起的 MCP 资源请求（read / list / templates / subscribe / unsubscribe）接到官方 AppBridge： |
| [pluginUiSampling.ts](pluginUiSampling.ts)                               | 先注册取消与 busy，再发请求，确保取消先于 Agent 接纳也能留下终态。                                          |
| [pluginUiSurfaceFeedStore.ts](pluginUiSurfaceFeedStore.ts)               | \* 面板投喂快照的 owner（renderer 内存，不持久化）。键为 `buildPluginUiSurfaceKey(target, surfaceScope)`，  |
| [pluginUiSurfaceStore.ts](pluginUiSurfaceStore.ts)                       | \* 同一作用域同时只保留一个活 sandbox。                                                                     |
| [pluginUiWidgetStateStore.ts](pluginUiWidgetStateStore.ts)               | \* 插件页面 widgetState 的唯一 owner。                                                                      |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                            |

<!-- qingqi-directory-index:end -->
