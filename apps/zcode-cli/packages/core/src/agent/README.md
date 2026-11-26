# agent

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 agent 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                                           |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [agent-listing-metadata.ts](agent-listing-metadata.ts)         | 持久化目录增量；恢复只信结构化数据，不从自然语言正文推断已通知类型。                               |
| [compact-session.ts](compact-session.ts)                       | summary 之前的请求前公告与 summary 同一事务写在其之前，由 compaction part 声明后放回。             |
| [file-part-hydration.ts](file-part-hydration.ts)               | 这是已发给模型的说明，不是文件内容；直接恢复原文，不重新读取或推测降级原因。                       |
| [index.ts](index.ts)                                           | index 的实现文件。                                                                                 |
| [loaded-skills.ts](loaded-skills.ts)                           | 「这段历史里加载过某个技能吗」（docs/dynamic-workflow/authoring.md「The authoring surface」）      |
| [message-history-usage.ts](message-history-usage.ts)           | 历史 TokenUsageInfo 会把缺失的 provider outputTokens 归一化成 0。                                  |
| [message-history.ts](message-history.ts)                       | Message History - Maintains conversation context across turns                                      |
| [read-file-state-hydrator.ts](read-file-state-hydrator.ts)     | \* resume 传 true：恢复出的记录带 restoredFromSession，compaction 补回按读取时间排序。             |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                   |
| [runtime-input-presentation.ts](runtime-input-presentation.ts) | 新标记决定真实输入身份，不能让 coordinator 继承 guide 的 real_user。                               |
| [session-history-hydrator.ts](session-history-hydrator.ts)     | Session History Hydration - rebuild provider-visible context                                       |
| [tool-part-order.ts](tool-part-order.ts)                       | 提前执行失败或断流恢复会另建 part；同一声明只恢复最后新建的记录，旧 part 迟到更新不影响选择。      |
| [tool-search-hydration.ts](tool-search-hydration.ts)           | 实现或公开接口：hydrateToolSearchContent、hydrateCompactDiscovery、hydrateToolSearchAnnouncement。 |
| [turn-machine.ts](turn-machine.ts)                             | Turn Machine - State machine for turn lifecycle                                                    |
| [turn-state.ts](turn-state.ts)                                 | Turn State - Turn state machine types                                                              |

<!-- qingqi-directory-index:end -->
