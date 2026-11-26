# scheduler

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 scheduler 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                                                                                                  |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [collection-events.ts](collection-events.ts)   | 实现或公开接口：emitExpansionEvents、exhaustCollection。                                                                                                                  |
| [collection-planner.ts](collection-planner.ts) | 实现或公开接口：checkCollectionPlanners。                                                                                                                                 |
| [collection-runtime.ts](collection-runtime.ts) | 实现或公开接口：WorkflowCollectionPlannerRuntime。                                                                                                                        |
| [events.ts](events.ts)                         | 实现或公开接口：WorkflowSchedulerEventLog。                                                                                                                               |
| [graph.ts](graph.ts)                           | 实现或公开接口：readyExecutableNodes、orderedReadyExecutableNodes、blockedExecutableNodes、areExecutableNodesComplete。                                                   |
| [node-runner.ts](node-runner.ts)               | 实现或公开接口：WorkflowNodeRunnerRuntime、runWorkflowNode。                                                                                                              |
| [planner-expansion.ts](planner-expansion.ts)   | 实现或公开接口：applyPlannerExpansion。                                                                                                                                   |
| [prompts.ts](prompts.ts)                       | 实现或公开接口：buildDefaultNodePrompt、buildDefaultPlannerPrompt、safeArtifactName。                                                                                     |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                                                                                                          |
| [types.ts](types.ts)                           | 实现或公开接口：WorkflowGraphSchedulerActivityInput、WorkflowGraphSchedulerActivityResult、WorkflowGraphSchedulerChildSessionStartedEvent、WorkflowGraphSchedulerRunner。 |

<!-- qingqi-directory-index:end -->
