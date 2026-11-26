# app

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 app 实现源码。

### 文件

| 文件                                                                                   | 简要说明                                                                                          |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                                                                  |
| [webRemoteControlBridgeRecovery.ts](webRemoteControlBridgeRecovery.ts)                 | 失效通知可随心跳重送；只有 raw adapter 的首次状态转换能启动恢复。                                 |
| [webRemoteControlEntry.ts](webRemoteControlEntry.ts)                                   | BigModel 使用 authCode；必须先进入既有回调校验，不能落回未登录门禁。                              |
| [webRemoteControlKnownDevices.ts](webRemoteControlKnownDevices.ts)                     | 键名沿用旧版“设备名”缓存，旧的 [mid, name] 条目可直接读出。                                       |
| [webRemoteControlLifecycle.ts](webRemoteControlLifecycle.ts)                           | Bugfix: 浏览器首屏加载也可能触发 pageshow，旧逻辑会在 terminal 仍处于 connecting 时强制 recover， |
| [webRemoteControlRoute.ts](webRemoteControlRoute.ts)                                   | \* 页面路由与资源目录分离：OSS 多版本发布用 `/remote/v4/<version>/` 作为 Vite base，              |
| [webRemoteControlTaskRead.ts](webRemoteControlTaskRead.ts)                             | \* 手机任务首页的 unreadAt 来自 desktop 快照，不保证存在于当前 Root 的 query cache。              |
| [webRemoteControlTaskView.ts](webRemoteControlTaskView.ts)                             | 只保留 Reporter 的当前投影供传输恢复重申；任务已读仍由桌面唯一 writer 提交。                      |
| [webRemoteControlVersion.ts](webRemoteControlVersion.ts)                               | 只读取响应；依赖当前连接的副作用由 onAccepted 同步提交。                                          |
| [webRemoteControlWorkspaceBridgeSession.ts](webRemoteControlWorkspaceBridgeSession.ts) | 能力校验未完成时新 bridge 仍是 pending；只重放 active 会让丢帧请求一直等到降级。                  |

<!-- qingqi-directory-index:end -->
