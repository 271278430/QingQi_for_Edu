# subagent

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 subagent 实现源码。

### 文件

| 文件                                                       | 简要说明                                                                                     |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| [background-stall.ts](background-stall.ts)                 | \* 后台 subagent 长时间无进展的发现与报告（apps/zcode-cli/docs/design/v2/tool/07-subagent.md |
| [borrowed-mcp-port.ts](borrowed-mcp-port.ts)               | child 借用 parent adapter，不拥有 MCP 连接生命周期。                                         |
| [completion-notification.ts](completion-notification.ts)   | 结构化 error 的上限，与 workflow 行的 error 相同。                                           |
| [computer-use-policy.ts](computer-use-policy.ts)           | Parent MCP 尚无启动快照时，只能依赖已认证 server 的 namespace；一旦收到                      |
| [context-builder.ts](context-builder.ts)                   | 逐段标记会耗尽缓存断点额度，导致对话末尾标记被丢弃；正文合并时保留各段自带的换行。           |
| [coordinator-response.ts](coordinator-response.ts)         | void 会接受 async callback；undefined 才能让类型系统守住同步入队 ack。                       |
| [definitions.ts](definitions.ts)                           | 同步读取已发布的内存快照；加载、覆盖和移除由提供方负责。                                     |
| [explore-tools.ts](explore-tools.ts)                       | 对齐文件搜索型子 agent 的工具面。direct branch 会暴露 Glob/Grep；                            |
| [explore.ts](explore.ts)                                   | Explore Subagent Definition                                                                  |
| [general-purpose.ts](general-purpose.ts)                   | General Purpose Subagent Definition                                                          |
| [index.ts](index.ts)                                       | Subagent exports                                                                             |
| [interaction-origin.ts](interaction-origin.ts)             | 实现或公开接口：SubagentInteractionOriginContext、buildSubagentInteractionOrigin。           |
| [listing.ts](listing.ts)                                   | 历史写入/恢复边界已校验并复制 delta；本轮新增 delta 由收集器生成。                           |
| [mcp-config.ts](mcp-config.ts)                             | 内联声明来自 Agent 文档，不能伪造 Host 来源绕过工作区 MCP 信任；具名引用保留权威来源。       |
| [message-steering.ts](message-steering.ts)                 | 只交付 message，summary 只用于 UI 预览。                                                     |
| [persistent-memory-prompt.ts](persistent-memory-prompt.ts) | 实现或公开接口：buildPersistentAgentMemoryPrompt。                                           |
| [persistent-memory.ts](persistent-memory.ts)               | 不存在或不可读的 MEMORY.md 都使用基线的 empty index 文案。                                   |
| [profile.ts](profile.ts)                                   | 用户/项目 profile 可以同名覆盖内置 Explore，不能只按名称套用内置行为。                       |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                             |
| [runner.ts](runner.ts)                                     | Subagent Runner                                                                              |
| [runtime-task-registry.ts](runtime-task-registry.ts)       | runtime-task-registry 的实现文件。                                                           |
| [system-prompt.ts](system-prompt.ts)                       | 子代理 system 在 agent 正文和 Notes 之间的一段：启动方消息只指导工作，不代表用户授权。       |
| [tool-event-mirror.ts](tool-event-mirror.ts)               | Subagent Tool Event Mirror                                                                   |
| [tool-policy.ts](tool-policy.ts)                           | 子 agent 没有独立的 plan approval 恢复面，暴露 plan tools 会让                               |

<!-- qingqi-directory-index:end -->
