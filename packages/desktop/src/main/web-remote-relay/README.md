# web-remote-relay

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 web remote relay 实现源码。

### 文件

| 文件                                                                   | 简要说明                                                                                 |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                             | 实现或公开接口：restoreRegisteredDevice。                                                |
| [CONTRACT.md](CONTRACT.md)                                             | 模块职责、公共接口、依赖方向和状态约定。                                                 |
| [contract.ts](contract.ts)                                             | schema 不认识的 payload；由上层决定是否回 unsupported-action，transport 不理解业务语义。 |
| [index.ts](index.ts)                                                   | 手机日志通道：实时落盘、拉取编排与导出。                                                 |
| [mobileLogPull.ts](mobileLogPull.ts)                                   | 桌面主动拉取手机日志（mobile-log-pull-request/response）的会话编排：                     |
| [mobileLogPullExport.ts](mobileLogPullExport.ts)                       | 「拉取手机日志」：向已配对手机发 mobile-log-pull-request，分片逐片写入                   |
| [mobileLogSink.ts](mobileLogSink.ts)                                   | 手机实时日志（mobile-log 推送帧）的桌面落盘：按「设备目录 / 日期\_会话 文件」分文件，    |
| [mobilePushConnection.ts](mobilePushConnection.ts)                     | 每次上报前从本机设置读取；enabled 是用户的 offline push 开关。                           |
| [module.ts](module.ts)                                                 | 依赖与 architecture-policy.yaml 同步；新增文件必须属于此 managed 边界。                  |
| [README.md](README.md)                                                 | 本目录用途、子目录与逐文件说明。                                                         |
| [webRemoteControlActionRequests.ts](webRemoteControlActionRequests.ts) | \* 手机动作请求 → 应答 payload。只做协议翻译，执行交给 Renderer；                        |
| [webRemoteControlDeviceStorage.ts](webRemoteControlDeviceStorage.ts)   | 实现或公开接口：createWebRemoteControlDeviceStorage。                                    |
| [webRemoteControlRendererAction.ts](webRemoteControlRendererAction.ts) | \* 把手机动作转给目标窗口 Renderer 执行。                                                |
| [webRemoteControlTransport.ts](webRemoteControlTransport.ts)           | 首次注册和失效后的重注册共用连接尝试，网络失败均由此处退避，不能在 manager 裸 await。    |
| [webRemoteControlV2Http.ts](webRemoteControlV2Http.ts)                 | \* Main 直接 Node fetch；不使用会触发全局登出的 services HTTP 客户端。                   |

<!-- qingqi-directory-index:end -->
