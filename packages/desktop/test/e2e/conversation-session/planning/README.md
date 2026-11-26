# planning

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 planning 测试场景。

### 文件

| 文件                                                                                                                                 | 简要说明                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| [conversation-session-independent-plan-draft.test.ts](conversation-session-independent-plan-draft.test.ts)                           | 新用户可能先进入职业引导；只处理已确认可见的引导，不吞掉其他初始化失败。         |
| [conversation-session-plan-approval-feedback-user-message.test.ts](conversation-session-plan-approval-feedback-user-message.test.ts) | EnterPlanMode 是隐藏的控制工具；用真实结果证明进入计划模式。                     |
| [conversation-session-plan-approval-primary-submit.test.ts](conversation-session-plan-approval-primary-submit.test.ts)               | Bug 根因：formal case 仍从 legacy store 读 session/运行态，                      |
| [conversation-session-plan-directory-order.test.ts](conversation-session-plan-directory-order.test.ts)                               | V4 隐藏内部 EnterPlanMode 行；真实工具结果已回到下一次模型请求才证明模式已进入。 |
| [conversation-session-plan-file-compact-continuity.test.ts](conversation-session-plan-file-compact-continuity.test.ts)               | EnterPlanMode 是隐藏的控制工具；用真实结果证明进入计划模式。                     |
| [conversation-session-plan-mode-capabilities.test.ts](conversation-session-plan-mode-capabilities.test.ts)                           | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。              |
| [conversation-session-plan-mode-mcp-permission.test.ts](conversation-session-plan-mode-mcp-permission.test.ts)                       | 用户级 MCP 只在会话启动时加载，必须在 prepare 创建会话前写入。                   |
| [conversation-session-plan-session-switch-restore.test.ts](conversation-session-plan-session-switch-restore.test.ts)                 | EnterPlanMode 是隐藏的控制工具；用真实结果证明进入计划模式。                     |
| [conversation-session-v4-plan-shortcut.test.ts](conversation-session-v4-plan-shortcut.test.ts)                                       | 计划模式列表操作：真实 Tab / Enter / 点击只修改 Composer，发送采用标准 Plan。    |
| [README.md](README.md)                                                                                                               | 本目录用途、子目录与逐文件说明。                                                 |

<!-- qingqi-directory-index:end -->
