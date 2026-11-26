# adapters

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 adapters 外部能力与平台适配。

### 文件

| 文件                                                               | 简要说明                                                                                          |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| [payloadRequester.ts](payloadRequester.ts)                         | Bugfix: 多个请求同时撞上 relay suspect 窗口时必须共用一次恢复。                                   |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                  |
| [relayMessage.ts](relayMessage.ts)                                 | 实现或公开接口：readWebSocketData、webSocketDataByteLength、parseRelayMessage、createFailure。    |
| [webRemoteControlDeviceClient.ts](webRemoteControlDeviceClient.ts) | 列表只是当前账号的在线快照；不缓存 JWT、设备元数据或失败响应正文。                                |
| [webRemoteControlDeviceInfo.ts](webRemoteControlDeviceInfo.ts)     | 实现或公开接口：collectWebRemoteControlMobileDeviceInfo。                                         |
| [webRemoteControlHttpSignal.ts](webRemoteControlHttpSignal.ts)     | 一次 HTTP 请求的取消资源；调用方须在回调内完成正文读取。                                          |
| [webRemoteControlThemeSeed.ts](webRemoteControlThemeSeed.ts)       | Bugfix: 手机远控首次打开原来只用 Web 默认主题，无法继承扫码时桌面端主题。                         |
| [webRemoteControlTransport.ts](webRemoteControlTransport.ts)       | 打散窗口与电脑共用，受桌面 3 秒手机断连宽限约束；规则见 WebRemoteControlV2RetryPolicy.nextDelay。 |
| [webRemoteControlV2Token.ts](webRemoteControlV2Token.ts)           | 一次性 token 不缓存；401 交给入口恢复登录，网络故障交给 transport 退避。                          |

<!-- qingqi-directory-index:end -->
