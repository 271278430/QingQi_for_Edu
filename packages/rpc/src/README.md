# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/rpc 基础工程中的 src 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                     |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| [buffer.ts](buffer.ts)                                             | \* Layer 0.5: 跨平台 Buffer 抽象                                                             |
| [channelClient.ts](channelClient.ts)                               | Promise 请求和事件监听共用 handlers，但只有前者需要在连接终结时 reject。                     |
| [channels.shared.ts](channels.shared.ts)                           | 实现或公开接口：IChannel、IServerChannel、enum。                                             |
| [channels.ts](channels.ts)                                         | channels 的实现文件。                                                                        |
| [channelServer.ts](channelServer.ts)                               | 修复原因：同一 protocol 上还有反向 ChannelClient，对方发来的响应也会到这里；原来先解码消息体 |
| [delayedChannel.ts](delayedChannel.ts)                             | 实现或公开接口：getDelayedChannel。                                                          |
| [foundation.ts](foundation.ts)                                     | \* Layer 0: 基础设施                                                                         |
| [index.ts](index.ts)                                               | \* IPC Framework —— 统一导出                                                                 |
| [ipc.ts](ipc.ts)                                                   | \* Layer 4: 连接管理 —— IPCServer 和 IPCClient                                               |
| [logging-middleware.ts](logging-middleware.ts)                     | \* 装饰 ChannelServer / ChannelClient，在不侵入核心逻辑的前提下                              |
| [network-telemetry-middleware.ts](network-telemetry-middleware.ts) | \* RPC 调用网络遥测：记录 channel.command 级成功率与耗时，供桌面主进程聚合上报 ARMS。        |
| [persistent-protocol.ts](persistent-protocol.ts)                   | \* PersistentProtocol —— 可靠性层（从 protocol.ts 拆出，避免单文件超限）。                   |
| [protocol.ts](protocol.ts)                                         | \* Layer 2: 传输协议抽象                                                                     |
| [proxy-channel.ts](proxy-channel.ts)                               | \* Layer 5: ProxyChannel —— 服务自动代理（杀手锏）                                           |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                             |
| [remote.ts](remote.ts)                                             | \* Layer 6: Remote 远程连接抽象                                                              |
| [serialization.ts](serialization.ts)                               | \* Layer 1: 二进制序列化                                                                     |

<!-- qingqi-directory-index:end -->
