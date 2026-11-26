# delivery

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 delivery 测试场景。

### 文件

| 文件                                                                               | 简要说明                                                                                |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [bot-automation-result-delivery.test.ts](bot-automation-result-delivery.test.ts)   | Host 只有在 watcher 已经进入 task service 后才允许继续 sendPrompt；快速终态不会漏回推。 |
| [bot-large-attachment.test.ts](bot-large-attachment.test.ts)                       | bot-large-attachment.test 的实现文件。                                                  |
| [bot-private-redelivery.test.ts](bot-private-redelivery.test.ts)                   | Telegram/微信的 Typing 每 4 秒续发一次；观察窗口超过一个周期才能证明已经停止。          |
| [bot-private-task-sync.test.ts](bot-private-task-sync.test.ts)                     | 微信首次入站只激活，随后才形成 task。                                                   |
| [feishu-delivery-error.test.ts](feishu-delivery-error.test.ts)                     | 合成飞书业务拒绝；验证客户端错误链路，不冒充真实租户复现。                              |
| [feishu-streaming-card-lifecycle.test.ts](feishu-streaming-card-lifecycle.test.ts) | feishu-streaming-card-lifecycle.test 的实现文件。                                       |
| [README.md](README.md)                                                             | 本目录用途、子目录与逐文件说明。                                                        |

<!-- qingqi-directory-index:end -->
