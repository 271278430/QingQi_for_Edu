# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/client 基础工程中的 src 实现源码。

### 文件

| 文件                                                                                                   | 简要说明                                                                                                                          |
| ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| [globals.d.ts](globals.d.ts)                                                                           | \* window.zcode 类型定义 —— 仅包含需要 main 进程参与的平台操作                                                                    |
| [index.ts](index.ts)                                                                                   | index 的实现文件。                                                                                                                |
| [logger.ts](logger.ts)                                                                                 | \* Renderer 端日志工具                                                                                                            |
| [messageport.ts](messageport.ts)                                                                       | 生产构建下 renderer 连接日志不输出，避免窗口启动和重连路径产生同步 console 成本。                                                 |
| [README.md](README.md)                                                                                 | 本目录用途、子目录与逐文件说明。                                                                                                  |
| [remoteServiceAccess.ts](remoteServiceAccess.ts)                                                       | \* RemoteServiceAccess — 通过 ChannelClient 自动创建类型安全的服务代理                                                            |
| [rendererLoggingEnv.ts](rendererLoggingEnv.ts)                                                         | 实现或公开接口：isRendererProductionBuild。                                                                                       |
| [webRemoteControlAcknowledgedRelayBatchQueue.ts](webRemoteControlAcknowledgedRelayBatchQueue.ts)       | 内部有界性测试观察点；不从 @zcode/client public entry 导出。                                                                      |
| [webRemoteControlAcknowledgedRelayDeadline.ts](webRemoteControlAcknowledgedRelayDeadline.ts)           | 实现或公开接口：AcknowledgedRelayDeadlineState、AcknowledgedRelayDeadline。                                                       |
| [webRemoteControlAcknowledgedRelayProtocol.ts](webRemoteControlAcknowledgedRelayProtocol.ts)           | 实现或公开接口：createAcknowledgedWebRemoteControlRelayProtocol。                                                                 |
| [webRemoteControlAcknowledgedRelayProtocolTypes.ts](webRemoteControlAcknowledgedRelayProtocolTypes.ts) | 原 8 MiB 按 Base64/JSON 外壳计量，合法的 16 MiB RPC 在发送前就会被误拒并触发重建。                                                |
| [webRemoteControlRelayPayloadSerializer.ts](webRemoteControlRelayPayloadSerializer.ts)                 | \* 为同一个 immutable app payload 固定唯一 final relay JSON。                                                                     |
| [webRemoteControlRelayProtocol.ts](webRemoteControlRelayProtocol.ts)                                   | 实现或公开接口：WebRemoteControlRelayProtocolOptions、WebRemoteControlRelayProtocolAdapter、createWebRemoteControlRelayProtocol。 |
| [websocket.ts](websocket.ts)                                                                           | bridge 只释放传输时，旧 RPC 会永久等待，发送前已 claim 的草稿也无法进入失败恢复。                                                 |

<!-- qingqi-directory-index:end -->
