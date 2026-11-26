# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                                                     | 简要说明                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [conversation-session-r3-bot-private-client-id.test.ts](conversation-session-r3-bot-private-client-id.test.ts)                           | Bot 私聊输入的命令信封 clientId 是 `bot:<botId>:<chatId>:<userId>`（formatBotInputClientId）。私聊过去用 |
| [conversation-session-r3-live-bigmodel-team.test.ts](conversation-session-r3-live-bigmodel-team.test.ts)                                 | 原小写 API 名称无法匹配当前菜单与运行记录使用的规范 Model ID。                                           |
| [conversation-session-r3-live-zapi.test.ts](conversation-session-r3-live-zapi.test.ts)                                                   | 用户输入含相同标记；必须在 assistant 正文中等待，并容许模型插入空白。                                    |
| [conversation-session-remote-command-authority-race.test.ts](conversation-session-remote-command-authority-race.test.ts)                 | 保留写端使 Core 的 open 能完成而 read 继续等待；因此可从 Core fd 证明请求确实在途。                      |
| [conversation-session-remote-memory-settings.test.ts](conversation-session-remote-memory-settings.test.ts)                               | 与现有 Scope 用例相同：已打开时不再次切换，Radix 只发送一次 pointerdown 打开。                           |
| [conversation-session-remote-settings-safeguards.test.ts](conversation-session-remote-settings-safeguards.test.ts)                       | 前项截图停在窄屏设置页，项目侧栏处于响应式隐藏态；独立操作场景恢复桌面视口。                             |
| [conversation-session-ssh-remote-account-isolation.test.ts](conversation-session-ssh-remote-account-isolation.test.ts)                   | 两账号同路径场景要求双方能遍历目录；镜像 home 的默认权限会先触发另一个权限场景。                         |
| [conversation-session-ssh-remote-project-conversation-scope.test.ts](conversation-session-ssh-remote-project-conversation-scope.test.ts) | 项目创建已打开所属 Source 的草稿；全局新建会改为本地未分类任务。                                         |
| [conversation-session-ssh-remote-resource-settings.test.ts](conversation-session-ssh-remote-resource-settings.test.ts)                   | conversation-session-ssh-remote-resource-settings.test 的实现文件。                                      |
| [conversation-session-ssh-remote-share-authority.test.ts](conversation-session-ssh-remote-share-authority.test.ts)                       | 合成身份仅发送到本 case 的 loopback API；记录只保存 actor 标签，不保存凭据值。                           |
| [conversation-session-ssh-remote-wizard-credentials.test.ts](conversation-session-ssh-remote-wizard-credentials.test.ts)                 | 用标题栏的关闭按钮（屏幕阅读器名称为“关闭”）关闭向导，与用户点击 × 的路径一致。                          |
| [README.md](README.md)                                                                                                                   | 本目录用途、子目录与逐文件说明。                                                                         |

<!-- qingqi-directory-index:end -->
