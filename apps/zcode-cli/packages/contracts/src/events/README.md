# events

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/contracts 基础工程中的 events 实现源码。

### 文件

| 文件                                                                 | 简要说明                                                                                         |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [event-reducer-helpers.ts](event-reducer-helpers.ts)                 | Event Reducer Helpers - focused projection transforms                                            |
| [event-reducer.ts](event-reducer.ts)                                 | Event Reducer - State projection from events                                                     |
| [in-memory-session-event-store.ts](in-memory-session-event-store.ts) | 默认 `turn-window`；`unbounded` 供回滚与对照测试。也可注入自定义策略工厂（按 session 创建）。    |
| [index.ts](index.ts)                                                 | Events - session event types and semantics                                                       |
| [README.md](README.md)                                               | 本目录用途、子目录与逐文件说明。                                                                 |
| [session-event-retention.ts](session-event-retention.ts)             | 它们仍经 event store 分配 seq 并交给 live sink，但 turn 结束并被下一 turn 取代后即可从内存淘汰： |
| [session.events.ts](session.events.ts)                               | Session Events - All event types for the agent loop                                              |
| [stream-recovery.events.ts](stream-recovery.events.ts)               | \* stream recovery 作废半截 assistant 输出时写在 transcript 上的标记。                           |

<!-- qingqi-directory-index:end -->
