# expert

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 expert 实现源码。

### 子目录

| 目录                          | 存放内容                                    |
| ----------------------------- | ------------------------------------------- |
| [parsers/](parsers/README.md) | @zcode/core 基础工程中的 parsers 实现源码。 |

### 文件

| 文件                                     | 简要说明                                                                                                                                       |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| [critic-loop.ts](critic-loop.ts)         | 实现或公开接口：runFinalCriticLoop。                                                                                                           |
| [failures.ts](failures.ts)               | 实现或公开接口：latestWorkflowActivity、workflowFailureFromError、workflowRecoveryActions。                                                    |
| [formatters.ts](formatters.ts)           | 实现或公开接口：formatExpertWorkflowStatus、formatExpertWorkflowCompletion。                                                                   |
| [graph-artifacts.ts](graph-artifacts.ts) | 实现或公开接口：seedGraphFromPhaseArtifact、updateNodePromptsFromPhaseArtifact。                                                               |
| [ids.ts](ids.ts)                         | 实现或公开接口：phaseNodeId、edgeId、executableNodeIdsForPhase、safeArtifactName。                                                             |
| [phase-runner.ts](phase-runner.ts)       | 实现或公开接口：runPhase。                                                                                                                     |
| [prompts.ts](prompts.ts)                 | 实现或公开接口：buildPhasePrompt、buildScheduledNodePrompt、buildScheduledPhaseSummary、buildReport。                                          |
| [README.md](README.md)                   | 本目录用途、子目录与逐文件说明。                                                                                                               |
| [retry-state.ts](retry-state.ts)         | 实现或公开接口：prepareSnapshotForRetry。                                                                                                      |
| [run-loop.ts](run-loop.ts)               | 实现或公开接口：continueRun。                                                                                                                  |
| [runtime-context.ts](runtime-context.ts) | 实现或公开接口：ExpertWorkflowRuntimeContext、lifecyclePayload、compactWorkflowPayload、dedupeWorkflowNodeChanges。                            |
| [runtime.ts](runtime.ts)                 | 实现或公开接口：ExpertWorkflowRuntime。                                                                                                        |
| [scheduled-phase.ts](scheduled-phase.ts) | 实现或公开接口：runScheduledPhase。                                                                                                            |
| [types.ts](types.ts)                     | 实现或公开接口：ExpertWorkflowAgentRunInput、ExpertWorkflowChildSessionStartedEvent、ExpertWorkflowAgentRunResult、ExpertWorkflowAgentRunner。 |

<!-- qingqi-directory-index:end -->
