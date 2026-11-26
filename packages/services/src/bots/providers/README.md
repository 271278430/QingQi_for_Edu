# providers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 providers 实现源码。

### 文件

| 文件                                                 | 简要说明                                                                                                                   |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| [feishuAppRegistration.ts](feishuAppRegistration.ts) | Bugfix: 对齐 @larksuiteoapi/node-sdk registerApp：一键创建应用总是先从 Feishu accounts issuer                              |
| [feishuGroupMessages.ts](feishuGroupMessages.ts)     | 接收事件用 bot，历史接口用 app；此前混用导致真实机器人事件在入口被丢弃。                                                   |
| [feishuProvider.ts](feishuProvider.ts)               | SDK 自动重连耗尽后的终态；旧测试替身可不提供。                                                                             |
| [groupInputReaction.ts](groupInputReaction.ts)       | 接收确认可能晚于开始/结束事件；单消息串行并禁止状态回退，避免覆盖终态。                                                    |
| [groupMemberDirectory.ts](groupMemberDirectory.ts)   | 缺少权限时短暂缓存失败，避免每条群消息重复查询；不暴露不完整的分页结果。                                                   |
| [providerRequest.ts](providerRequest.ts)             | 修复原因：收到响应头不代表请求完成。必须在同一个 AbortSignal 和 deadline 下                                                |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                                                           |
| [telegramProvider.ts](telegramProvider.ts)           | 实现或公开接口：createTelegramBotProvider。                                                                                |
| [types.ts](types.ts)                                 | 实现或公开接口：BotTypingTarget、BotProviderDownloadedAttachment、BotStreamingReplyCardBlock、BotStreamingReplyCardState。 |
| [webhookProvider.ts](webhookProvider.ts)             | 实现或公开接口：createWebhookBotProvider。                                                                                 |
| [weixinProvider.ts](weixinProvider.ts)               | 微信 iLink CDN 返回 AES-128-ECB + PKCS7 padding 的密文字节；直接保存会得到不可识别的 data 文件。                           |
| [weixinRegistration.ts](weixinRegistration.ts)       | 实现或公开接口：beginWeixinRegistration、pollWeixinRegistration。                                                          |

<!-- qingqi-directory-index:end -->
