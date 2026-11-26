# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 src 实现源码。

### 子目录

| 目录                                        | 存放内容                                              |
| ------------------------------------------- | ----------------------------------------------------- |
| [local-ttft/](local-ttft/README.md)         | @zcode/desktop 基础工程中的 local ttft 实现源码。     |
| [plugin-sandbox/](plugin-sandbox/README.md) | @zcode/desktop 基础工程中的 plugin sandbox 实现源码。 |

### 文件

| 文件                                                                       | 简要说明                                                                                                                                                                    |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [armsBrowserBootstrap.ts](armsBrowserBootstrap.ts)                         | renderer 入口兜底（主路径在 preload 已 init，避免 module 脚本晚于 load）                                                                                                    |
| [databaseStartupAdmission.ts](databaseStartupAdmission.ts)                 | 页面只做同代准入；ready(A) 不能与端口(B) 拼成一次完成事实。                                                                                                                 |
| [desktopBrowserPlatformBridge.ts](desktopBrowserPlatformBridge.ts)         | Rebase 集成：browser bridge 若继续内联在 renderer 入口，会让入口越过 max-lines 门禁。                                                                                       |
| [desktopPlatform.ts](desktopPlatform.ts)                                   | Source 自动重连会替换 logical session；统一由 preload bridge 转发换代事件。                                                                                                 |
| [main.tsx](main.tsx)                                                       | T4:renderer bundle 开始执行。同时从 loadURL query 解析 main 注入的 T0-T3。                                                                                                  |
| [performanceTimelineCleanup.ts](performanceTimelineCleanup.ts)             | React 19.2 的 development build 会把组件渲染写入 Performance timeline。                                                                                                     |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                                                                                                            |
| [remoteWorkspaceServicePortBridge.ts](remoteWorkspaceServicePortBridge.ts) | 实现或公开接口：RemoteWorkspaceServicePortRegistration、parseRemoteWorkspaceServicePortMessage、parseRemoteWorkspaceServicePortReleasedMessage、notifyRemoteWorkspaceServic |
| [remoteWorkspaceSessionServices.ts](remoteWorkspaceSessionServices.ts)     | \* 高速卡与闲时任务只在本地生效（2026-10-21 产品决定），远程 workspace 一律不得路由到远端。                                                                                 |
| [resource-manager.tsx](resource-manager.tsx)                               | 资源管理器不创建主窗口的 Zustand store，text-ui-\* 无法自动获得持久化基准。                                                                                                 |
| [sourceSettingsServicePortBridge.ts](sourceSettingsServicePortBridge.ts)   | 实现或公开接口：handleSourceSettingsServicePortMessage。                                                                                                                    |
| [userActionTraceBootstrap.ts](userActionTraceBootstrap.ts)                 | 实现或公开接口：initializeDesktopUserActionTrace。                                                                                                                          |

<!-- qingqi-directory-index:end -->
