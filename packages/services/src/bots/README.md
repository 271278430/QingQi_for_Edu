# bots

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 bots 实现源码。

### 子目录

| 目录                                                            | 存放内容                                                         |
| --------------------------------------------------------------- | ---------------------------------------------------------------- |
| [providers/](providers/README.md)                               | @zcode/services 基础工程中的 providers 实现源码。                |
| [topic-history-attachment/](topic-history-attachment/README.md) | @zcode/services 基础工程中的 topic history attachment 实现源码。 |

### 文件

| 文件                                                   | 简要说明                                                                                                 |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| [botConfigHelpers.ts](botConfigHelpers.ts)             | Bot 配置化后 allowedWorkspaces 是唯一 workspace 权限边界；空数组统一落成 "\*"。                          |
| [bots.ts](bots.ts)                                     | 与该次 sendPrompt.traceId 一致，避免排队期间污染其他轮次。                                               |
| [botsService.ts](botsService.ts)                       | 实现或公开接口：createBotsService。                                                                      |
| [channelMentionResolver.ts](channelMentionResolver.ts) | 名字只是查询条件；候选身份只能来自 Provider 目录与已授权原生节点。                                       |
| [channelReply.ts](channelReply.ts)                     | 输入来源不是发送授权：从任务唯一绑定中解析可信目标，禁止拿另一任务/旧授权兜底。                          |
| [channelRuntime.ts](channelRuntime.ts)                 | Bugfix: provider callback 以返回值表达可恢复的业务失败，不一定 reject。                                  |
| [commandOrder.ts](commandOrder.ts)                     | 实现或公开接口：BOT_MENU_COMMAND_ORDER。                                                                 |
| [commandParser.ts](commandParser.ts)                   | 实现或公开接口：parseBotCommand。                                                                        |
| [config.ts](config.ts)                                 | 回滚兼容：旧 App 对 Options 严格解析，旧文件仅作升级前快照，不得持续回写。                               |
| [feishuChannelRuntime.ts](feishuChannelRuntime.ts)     | Bugfix: runtime 停止或锁目录异常时，锁文件创建可能在进入连接 try 块前失败。                              |
| [groupAdminAttention.ts](groupAdminAttention.ts)       | 仅由服务明确识别的配置/连接错误升级，不能扫描模型输出猜测管理员待办。                                    |
| [groupDeliveryThrottle.ts](groupDeliveryThrottle.ts)   | 群消息共享发送额度；只预留发送时间，不保存或执行任务输入。                                               |
| [groupQueueCard.ts](groupQueueCard.ts)                 | 原实现只改表情；卡片也必须记录单向生命周期，迟到的 admission 不能覆盖终态。                              |
| [groupReply.ts](groupReply.ts)                         | 明确拒绝后的有限降级；话题不能误发到群主聊天，也不能重试同一失效锚点。                                   |
| [groupResultDelivery.ts](groupResultDelivery.ts)       | 只保存和发送已生成结果；不持有任务执行或输入队列。                                                       |
| [groupSessions.ts](groupSessions.ts)                   | 群身份不能用发送者代替，否则多人会串到私聊或各自创建任务。                                               |
| [messages.ts](messages.ts)                             | Bugfix: 这条错误由通用 provider callback 处理路径触发，微信/飞书失败时不能误显示 Telegram。              |
| [modelSelectionHelpers.ts](modelSelectionHelpers.ts)   | 实现或公开接口：resolveTaskModel、getNativeModelProviderId。                                             |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                                         |
| [replyFormatter.ts](replyFormatter.ts)                 | Telegram Markdown 的 inline code 需要转义反斜杠和反引号，否则路径/命令里的特殊字符会导致文本退回裸显示。 |
| [repo.ts](repo.ts)                                     | 回滚兼容：v3 已存在就只认 v3；损坏时暴露错误，绝不能恢复旧 Bot 或覆盖用户新修改。                        |
| [statusFormatting.ts](statusFormatting.ts)             | Bugfix: 第三方 /status 之前把运行时长塞进 Task 行；这里按 UI 的已工作时长语义单独输出 Worked。           |
| [storageMigration.ts](storageMigration.ts)             | 只在 v3 文件不存在时调用；不是当前 Bot Options 的兼容读取器。                                            |
| [taskStreamHub.ts](taskStreamHub.ts)                   | 同一任务只有一个实时源；接收目标自己串行消费，单个渠道失败不阻塞其他渠道。                               |
| [telegramChannelRuntime.ts](telegramChannelRuntime.ts) | Telegram 服务端长轮询最多等待 25 秒；客户端额外预留传输时间，但必须覆盖响应体读取，                      |
| [topicContinuation.ts](topicContinuation.ts)           | 必须等到指定 run 的权威终态；停止 RPC 返回不等于运行已经结束。                                           |
| [topicHistory.ts](topicHistory.ts)                     | 区分权限拒绝和临时网络错误，避免错误引导用户授权。                                                       |
| [topicHistoryAttachment.ts](topicHistoryAttachment.ts) | 历史正文只写一份附件；服务端归档用于权限和检查点，不再生成模型隐藏消息。                                 |
| [topicPreparationState.ts](topicPreparationState.ts)   | 仅保留未提交材料；对外投影不包含文件二进制，重试仍由入站授权链处理。                                     |
| [topicResource.ts](topicResource.ts)                   | 历史附件此前只有文字占位；下载必须从已接收输入反查身份，不能相信模型提供的群信息。                       |
| [weixinChannelRuntime.ts](weixinChannelRuntime.ts)     | Bugfix：每个窗口都有独立 host。微信锁 I/O 失败必须退避重试，不能让后台 Promise 退出。                    |
| [workspaceHelpers.ts](workspaceHelpers.ts)             | 实现或公开接口：getWorkspaceKey、getWorkspaceLabel、createWorkspaceRef、normalizeAllowedWorkspaces。     |

<!-- qingqi-directory-index:end -->
