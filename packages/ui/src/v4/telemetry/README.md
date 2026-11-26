# telemetry

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 telemetry 实现源码。

### 子目录

| 目录                                | 存放内容                                     |
| ----------------------------------- | -------------------------------------------- |
| [local-ttft/](local-ttft/README.md) | @zcode/ui 基础工程中的 local ttft 实现源码。 |

### 文件

| 文件                                                                               | 简要说明                                                                                                 |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| [conversationPromptTelemetry.ts](conversationPromptTelemetry.ts)                   | 修复原因：V4 config 把 provider/model 拆开保存，直接上报 model 会丢失旧 UI                               |
| [ConversationTelemetryAttachment.tsx](ConversationTelemetryAttachment.tsx)         | service generation 换代时，零引用旧 supervisor 立即销毁；仍被 pane 使用的旧代标 stale，                  |
| [conversationTelemetryParityE2E.ts](conversationTelemetryParityE2E.ts)             | 实现或公开接口：ConversationTelemetryParityScenarioResult、installConversationTelemetryParityE2EBridge。 |
| [conversationTelemetrySupervisor.ts](conversationTelemetrySupervisor.ts)           | 实现或公开接口：ConversationTelemetrySupervisor。                                                        |
| [README.md](README.md)                                                             | 本目录用途、子目录与逐文件说明。                                                                         |
| [useSessionOpenArmsTelemetry.ts](useSessionOpenArmsTelemetry.ts)                   | Bug 原因：warm/keep-warm 都采用已有 projection store，state 中的 timing 属于上一次                       |
| [useSessionSubscriptionErrorTelemetry.ts](useSessionSubscriptionErrorTelemetry.ts) | Bug 原因：recovery fail-closed 会把纯 reasonCode 直接写入 lastError，旧逻辑只识别                        |

<!-- qingqi-directory-index:end -->
