# V4 会话架构：当前状态与文档导航

更新日期：2026-07-15

V4 conversation 主链路已经落地：CLI 维护 canonical facts、command inbox 和 product projection；
Host/relay 转发连接与 topic；renderer/web 订阅 projection、发送 command，并只保留局部 UI 状态。

本目录混合了两类文档：

- 当前规格：schema、恢复、fault、sessions-index 等仍约束现行代码；
- 实施轨迹：phasing、review、deletion/parity 记录迁移依据，正文中的 legacy 路径、行数和“待实现”
  只代表当时状态。

产品语义优先读 [Conversation Product Protocol](../conversation-product-protocol.md)，系统总览优先读
[ZCode Protocol](../zcode-protocol.md) 与 [Message Flow](../architecture/message-flow.md)。

## 当前拓扑

```text
Electron / Web / mobile remote
  |-- SessionPane + read-only projection stores
  |-- command(commandId, clientId, baseRevision, payload)
  `-- local draft / scroll / focus / optimistic overlay
          |
          | @zcode/rpc MessagePort / remote attachment
          v
Host connection scope
  |-- trusted clientMode / connectionId
  |-- owned topic subscription routing
  |-- runtime generation / stale subscription cleanup
  `-- no conversation reducer or second queue
          |
          | @zcode/shared/zcode-protocol-v4 over stdio
          v
ZCode CLI
  |-- transcript + session metadata + goal facts
  |-- V4 command inbox / durable input admission
  |-- ProductProjection + SessionsIndexProjection
  |-- topic publisher: snapshot / delta / seq / logEpoch
  `-- runtime config, queue, interaction and active/background work
```

手机 `/remote` 通过 shared-host attachment 连接桌面已存在、承载目标 workspace scope 的 Local/Remote Host。relay 和
desktop main 只做鉴权、配对、心跳与 frame/app payload 透传，不拥有 session、queue、snapshot 或
projection。

## 当前不变量

- conversation UI 按 projection rows 渲染，不从 flat message 数组重新推导 turn、timeline、endedness
  或 action availability。
- command 使用 `commandId` 幂等身份和可选 `baseRevision`；ACK 与后续 projection 分工明确。
- 每个 attachment/subscription 有独立 ownership、generation、seq 和 recovery；下行帧只投递 owner port。
- desktop 是 continuous online delivery；mobile remote 是 replayable recovery。两端共享 CLI 事实，
  但 recovery frame 不能扩散到桌面 online 主链路。
- snapshot 原子替换；delta 必须连续；gap/epoch 变化触发 resync，恢复在途时不能让迟到 online 帧覆盖。
- session queue 和 interaction pending state 位于 CLI；Host、relay、renderer 不建立第二份 accepted queue。
- identity/cache/topic 隔离使用 `workspaceIdentity?.trim() || workspacePath`；路径执行仍使用
  `workspacePath`，远程链路还要携带 `remoteSessionId`。
- `tasks-index` 拥有持久 task 行集合以及 pin/archive/group/unread 等组织态；`sessions-index` 只拥有
  列表活性与实时详情摘要，客户端以 task row 为左表做字段级 join。

## 当前代码入口

| 层                 | 入口                                                                                                        |
| ------------------ | ----------------------------------------------------------------------------------------------------------- |
| V4 schema          | `packages/shared/src/zcode-protocol-v4/`                                                                    |
| UI transport/store | `packages/ui/src/v4/agentConversationTransport.ts`、`conversationProjectionStore.ts`、`sessionDataLayer.ts` |
| UI pane/commands   | `packages/ui/src/v4/SessionPane.tsx`、`ConversationComposer.tsx`                                            |
| Host/service route | `packages/services/src/zcode-agent/zcodeAgentConnectionScope.ts`、`zcodeAgentService.ts`                    |
| CLI gateway        | `apps/zcode-cli/packages/bootstrap/src/zcode-protocol-v4/v4-gateway.ts`                                     |
| CLI projection     | `product-projection.ts`、`sessions-index-projection.ts`                                                     |
| CLI commands       | `apps/zcode-cli/packages/bootstrap/src/zcode-protocol-v4/commands/`                                         |

## 文档索引

| 文档                                                                   | 当前角色                                    |
| ---------------------------------------------------------------------- | ------------------------------------------- |
| [01-topology.md](./01-topology.md)                                     | 拓扑和职责设计；结合当前总览读取            |
| [02-projection.md](./02-projection.md)                                 | projection 设计与裁决依据                   |
| [03-commands.md](./03-commands.md)                                     | command/ACK/inbox 规格与未完成项            |
| [04-sync-and-recovery.md](./04-sync-and-recovery.md)                   | topic 订阅、seq、snapshot、recovery 约束    |
| [05-transport-and-backpressure.md](./05-transport-and-backpressure.md) | transport/wire/backpressure 规格            |
| [06-ui.md](./06-ui.md)                                                 | V4 UI 设计和实施轨迹                        |
| [07-persistence.md](./07-persistence.md)                               | canonical facts、投影重建和迁移             |
| [08-phasing.md](./08-phasing.md)                                       | 历史分期与清理轨迹，不是当前进度表          |
| [09-protocol-schema.md](./09-protocol-schema.md)                       | 早期 schema 设计；字段冲突时让位于代码与 10 |
| [10-protocol-spec.md](./10-protocol-spec.md)                           | V4 字段级主规格                             |
| [11-deletion-plan.md](./11-deletion-plan.md)                           | 历史删除执行清单                            |
| [12-fault-catalog.md](./12-fault-catalog.md)                           | fault/reason code 词表                      |
| [13-golden-test-mapping.md](./13-golden-test-mapping.md)               | case 到 reducer/protocol/WDIO 证据映射      |
| [14-sessions-index.md](./14-sessions-index.md)                         | sessions-index 当前规格和实现入口           |
| [design-review.md](./design-review.md)                                 | 迁移前代码审计与风险轨迹                    |
| [review-meeting-brief.md](./review-meeting-brief.md)                   | 评审历史输入，不是现状摘要                  |

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

v4 refactor 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                           | 简要说明                                                               |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| [01-topology.md](01-topology.md)                                               | 进程拓扑：连接隔离与 CLI 权威事实：说明文档。                          |
| [02-projection.md](02-projection.md)                                           | Conversation Product Projection 当前实现：说明文档。                   |
| [03-commands.md](03-commands.md)                                               | V4 Command 模型当前规格：说明文档。                                    |
| [04-sync-and-recovery.md](04-sync-and-recovery.md)                             | 订阅与恢复：连接级 resync 是唯一恢复路径：说明文档。                   |
| [05-transport-and-backpressure.md](05-transport-and-backpressure.md)           | 传输与背压：subscriber 隔离、1 MiB 物理帧与原子 resync：说明文档。     |
| [06-ui.md](06-ui.md)                                                           | UI 重写：只读投影渲染 + 多 session 分屏（实施设计）：说明文档。        |
| [07-persistence.md](07-persistence.md)                                         | V4 持久化与冷恢复当前规格：说明文档。                                  |
| [08-phasing.md](08-phasing.md)                                                 | 分期落地与清理：说明文档。                                             |
| [09-protocol-schema.md](09-protocol-schema.md)                                 | Protocol Schema：V4 对话核心闭环：说明文档。                           |
| [10-protocol-spec.md](10-protocol-spec.md)                                     | ZCode Protocol v4：字段级规范：说明文档。                              |
| [11-deletion-plan.md](11-deletion-plan.md)                                     | 删除与采用清单（历史执行记录）：说明文档。                             |
| [12-fault-catalog.md](12-fault-catalog.md)                                     | Fault Catalog：`fault.*` 协议错误枚举（G-12）：说明文档。              |
| [13-golden-test-mapping.md](13-golden-test-mapping.md)                         | Case Catalog → 黄金测试映射（M0 素材）：说明文档。                     |
| [14-sessions-index.md](14-sessions-index.md)                                   | sessions-index topic 当前规格：说明文档。                              |
| [15-timeline-resolver-design-review.md](15-timeline-resolver-design-review.md) | Timeline Resolver Design — 架构/逻辑 Review：说明文档。                |
| [15-timeline-resolver-design.md](15-timeline-resolver-design.md)               | Conversation Timeline Resolver Design：说明文档。                      |
| [16-timeline-authority-plan.md](16-timeline-authority-plan.md)                 | Timeline Authority 实施计划：说明文档。                                |
| [17-cold-resume-runtime-activation.md](17-cold-resume-runtime-activation.md)   | V4 冷恢复：Runtime 激活与 Legacy Snapshot 解耦：说明文档。             |
| [18-resume-race-audit-plan.md](18-resume-race-audit-plan.md)                   | V4 Resume / Activation 竞态审计与测试计划：说明文档。                  |
| [design-review.md](design-review.md)                                           | V4 重构设计 Review：对照现有代码与历史 bugfix 的交叉验证：说明文档。   |
| [m5-composer-parity.md](m5-composer-parity.md)                                 | M5 Composer Parity — 输入框全量对齐老版 · 能力审计对账：说明文档。     |
| [m5-composer-restore.md](m5-composer-restore.md)                               | M5：v4 会话 composer 还原（输入区能力收口）：说明文档。                |
| [m6-model-selection-parity.md](m6-model-selection-parity.md)                   | M6 Model-Selection Parity — 输入框「选模型」逻辑补齐规划：说明文档。   |
| [m6-p1-runtime-model-resolution.md](m6-p1-runtime-model-resolution.md)         | M6 Phase 1 — CLI provider/凭据解析（runtimeModel）历史设计：说明文档。 |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                       |
| [review-meeting-brief.md](review-meeting-brief.md)                             | V4 重构评审稿：Conversation 状态同步与多端协议收敛：说明文档。         |
| [v4-chat-layout-parity.md](v4-chat-layout-parity.md)                           | V4 Chat Layout Parity：说明文档。                                      |
| [v4-goal-command-parity-plan.md](v4-goal-command-parity-plan.md)               | V4 Goal Command Parity Plan：说明文档。                                |

<!-- qingqi-directory-index:end -->
