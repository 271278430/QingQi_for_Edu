# runtime-task

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 runtime task 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                                       |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| [index.ts](index.ts)                                           | index 的实现文件。                                                                             |
| [notification-policy.ts](notification-policy.ts)               | 实现或公开接口：runtimeTaskTypeOf、shouldSuppressSealedSubagentBashNotification。              |
| [notification.ts](notification.ts)                             | \* workflow run 的渐进产物（`report(item)`），completed / failed / cancelled 一律携带。        |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                               |
| [registry.ts](registry.ts)                                     | local_dynamic_workflow 与 local_workflow 刻意分开：后者是 legacy `Workflow` 工具（不可取消）， |
| [workflow-blocked-reminder.ts](workflow-blocked-reminder.ts)   | 「run 还欠着决定、主代理闲着」的提醒钟                                                         |
| [workflow-notification-copy.ts](workflow-notification-copy.ts) | workflow run 的 run 中通知与 provider 停下文案表                                               |

<!-- qingqi-directory-index:end -->
