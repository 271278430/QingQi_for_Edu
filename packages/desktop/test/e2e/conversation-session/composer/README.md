# composer

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 composer 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                             | 简要说明                                                                               |
| ---------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [conversation-session-composer-compression.test.ts](conversation-session-composer-compression.test.ts)           | Think 已合并到模型按钮；绿条在该按钮内，不再有独立 Think 控件。                        |
| [conversation-session-composer-draft-switching.test.ts](conversation-session-composer-draft-switching.test.ts)   | 本例验证同一项目内的 session/草稿附件；任务入口的换目录由 PD01/02 单独断言。           |
| [conversation-session-composer-prefix-routing.test.ts](conversation-session-composer-prefix-routing.test.ts)     | 文件及候选夹具归属于项目；全局新建会切到未归类 cwd，无法读取这里的文件。               |
| [conversation-session-composer-recent-mode.test.ts](conversation-session-composer-recent-mode.test.ts)           | ZCT-2098314627607224320：首发迁移 Root 后，再新建任务必须继承最近接纳的权限。          |
| [conversation-session-draft-create-singleflight.test.ts](conversation-session-draft-create-singleflight.test.ts) | 先进入已完成任务，再从真实新任务入口进入新草稿，避免采用前置草稿的预热。               |
| [conversation-session-file-mention-host-search.test.ts](conversation-session-file-mention-host-search.test.ts)   | 冷启动可能先连接到过渡窗口；切到产品窗口后，再退出隔离用户目录的首次引导。             |
| [conversation-session-first-send.test.ts](conversation-session-first-send.test.ts)                               | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。                    |
| [conversation-session-mention-selection.test.ts](conversation-session-mention-selection.test.ts)                 | E2E_MENTION_SELECTION：仅编辑草稿；不发送 prompt，不需要 synthetic provider 响应。     |
| [conversation-session-plus-menu.test.ts](conversation-session-plus-menu.test.ts)                                 | E2E_PLUS_MENU：只编辑草稿，不发送 prompt；空 provider fixture 是有意的合同。           |
| [conversation-session-v4-composer-toolbar.test.ts](conversation-session-v4-composer-toolbar.test.ts)             | M5 门禁：composer 工具条（模型选择器 / 思考深度 / 模式 / slash 候选面板）。            |
| [conversation-session-v4-input-control.test.ts](conversation-session-v4-input-control.test.ts)                   | v4 输入控制条收口：autoDrain / followupMode 不再作为 composer 局部按钮暴露。           |
| [conversation-session-v4-mention.test.ts](conversation-session-v4-mention.test.ts)                               | S01 / S05 / S08 门禁：composer 聚合入口、兼容触发器与 Session Skill catalog 生命周期。 |
| [README.md](README.md)                                                                                           | 本目录用途、子目录与逐文件说明。                                                       |

<!-- qingqi-directory-index:end -->
