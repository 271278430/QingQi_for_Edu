# repositories

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 repositories 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                                                                                     |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| [debug.ts](debug.ts)                                           | 实现或公开接口：debugMigrationIds、debugCounts。                                                                                             |
| [dwf-journal-artifacts.ts](dwf-journal-artifacts.ts)           | \* 用户面**产物**的两条宿主读面。                                                                                                            |
| [dwf-journal-codecs.ts](dwf-journal-codecs.ts)                 | _ dwf\__ journal 表的行 ↔ 记录映射。                                                                                                         |
| [dwf-journal-fields.ts](dwf-journal-fields.ts)                 | \* 看板只取字段的读（docs/execution-engine.md「Reading the journal」）：按 spec 点名的字段路径，                                             |
| [dwf-journal-introspection.ts](dwf-journal-introspection.ts)   | \* dwf-journal.ts 顶到 oxlint max-lines 上限（400 行），把宿主侧 \*\*run 内省读面                                                            |
| [dwf-journal-pages.ts](dwf-journal-pages.ts)                   | \* dwf_event 上按条数**与字节**两道界分页的读（docs/execution-engine.md「Reading the journal」）：                                           |
| [dwf-journal-reads.ts](dwf-journal-reads.ts)                   | \* `JournalStorePort` 读面的 SQL（docs/execution-engine.md「Reading the journal」）：kinds / types                                           |
| [dwf-journal.ts](dwf-journal.ts)                               | _ `JournalStorePort` 的 SQLite 实现（dwf\__ 表）。                                                                                           |
| [input-history.ts](input-history.ts)                           | 实现或公开接口：recordInputHistory、recallPreviousInputHistory。                                                                             |
| [local-settings.ts](local-settings.ts)                         | 实现或公开接口：getProjectPermission、saveProjectPermission、getProjectPermissionMode、saveProjectPermissionMode。                           |
| [messages.ts](messages.ts)                                     | 只补回旧版快照字段，不合并整个 JSON：递归 merge 会让已清空的 metadata/options 残留。                                                         |
| [permission-full-access.ts](permission-full-access.ts)         | SQLite adapter 的同步事务中不 await，取消检查和提交之间没有异步重入窗口。                                                                    |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                                                             |
| [script-workflow-activities.ts](script-workflow-activities.ts) | 实现或公开接口：createScriptWorkflowActivity、updateScriptWorkflowActivity、findCachedScriptWorkflowActivity、listScriptWorkflowActivities。 |
| [script-workflow-codecs.ts](script-workflow-codecs.ts)         | 实现或公开接口：WorkflowDefinitionRow、WorkflowRunRow、WorkflowActivityRow、WorkflowEventRow。                                               |
| [script-workflow-runs.ts](script-workflow-runs.ts)             | 实现或公开接口：upsertScriptWorkflowDefinition、createScriptWorkflowRun、updateScriptWorkflowRun、getScriptWorkflowRun。                     |
| [session-entries.ts](session-entries.ts)                       | 旧版读取 data 的平铺身份；新版 port 仍传逻辑 Selection，包装只属于存储 adapter。                                                             |
| [session-inputs.ts](session-inputs.ts)                         | session_input 账本仓库。                                                                                                                     |
| [sessions.ts](sessions.ts)                                     | Bug 根因：先读整行再 await 会用旧快照覆盖并发标题、权限和结果；只更新本次输入拥有的列。                                                      |
| [todos.ts](todos.ts)                                           | 实现或公开接口：readTodos、updateTodos。                                                                                                     |
| [usage.ts](usage.ts)                                           | 用量事实永久保留；查询时间范围只负责筛选，写入时不能清理历史统计。                                                                           |

<!-- qingqi-directory-index:end -->
