# queue

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 queue 测试场景。

### 文件

| 文件                                                                                                               | 简要说明                                                                                |
| ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| [conversation-session-auto-drain.test.ts](conversation-session-auto-drain.test.ts)                                 | 先确认主请求已输出正文，避免标题生成的短暂 running 被误当成可入队的首轮。               |
| [conversation-session-prewarming-queue.test.ts](conversation-session-prewarming-queue.test.ts)                     | conversation-session-prewarming-queue.test 的实现文件。                                 |
| [conversation-session-queue-edit-freeze-mobile.test.ts](conversation-session-queue-edit-freeze-mobile.test.ts)     | B09j/B09l/B09m 排队消息冻结编辑的多端边界（docs/ui/composer-edit-mode.md）。            |
| [conversation-session-queue-edit-freeze.test.ts](conversation-session-queue-edit-freeze.test.ts)                   | B09h/B09i/B09k/B09o/B09p 排队消息冻结编辑（docs/ui/composer-edit-mode.md）。            |
| [conversation-session-queue-operations.test.ts](conversation-session-queue-operations.test.ts)                     | 编辑时队列项原位冻结（docs/ui/composer-edit-mode.md），composer 载入原文。              |
| [conversation-session-queued-command-restart.test.ts](conversation-session-queued-command-restart.test.ts)         | queue projection 正常会及时清除 renderer ingress ledger；这里重建的是线上可能出现的     |
| [conversation-session-running-queue.test.ts](conversation-session-running-queue.test.ts)                           | 原因：M04/M05 当前合同是 compact 维护项入 FIFO，旧用例仍要求拒绝。                      |
| [conversation-session-running-send-now.test.ts](conversation-session-running-send-now.test.ts)                     | 必须等当前轮产生 text-only assistant；更早轮次的文字不能作为这次抢占的锚点。            |
| [conversation-session-stop-held-queue.test.ts](conversation-session-stop-held-queue.test.ts)                       | running 投影早于首个模型 delta；先等真实回答，避免把首发取消当作流中断。                |
| [conversation-session-turn-error-queue-preserved.test.ts](conversation-session-turn-error-queue-preserved.test.ts) | N05 / NQ：普通主 turn 报错时，已 accepted 的 future queue 不得被清空。                  |
| [conversation-session-v4-auto-drain-running-fork.test.ts](conversation-session-v4-auto-drain-running-fork.test.ts) | PV4-03/PV4-08 pending：Q0 running 时先把 Q1/Q2 入 CLI FIFO；Q1 auto-drain               |
| [conversation-session-v4-queue-drain.test.ts](conversation-session-v4-queue-drain.test.ts)                         | catalog C02（queueAutoDrain）+ queuedPromptMessagePreserved 验收（case catalog 战役）。 |
| [conversation-session-v4-queue.test.ts](conversation-session-v4-queue.test.ts)                                     | M4 门禁：queue 单项管理 + B09 冻结编辑（docs/ui/composer-edit-mode.md）。               |
| [conversation-session-v4-sendnow.test.ts](conversation-session-v4-sendnow.test.ts)                                 | M4 门禁：sendQueuedNow（catalog B 组）。                                                |
| [conversation-session-v4-stop-queue.test.ts](conversation-session-v4-stop-queue.test.ts)                           | catalog B02/B04（stopKeepsQueueAndDisablesAutoDrain）+ B06（暂停队列发送确认）          |
| [README.md](README.md)                                                                                             | 本目录用途、子目录与逐文件说明。                                                        |

<!-- qingqi-directory-index:end -->
