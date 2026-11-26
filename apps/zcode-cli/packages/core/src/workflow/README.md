# workflow

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 workflow 实现源码。

### 子目录

| 目录                              | 存放内容                                      |
| --------------------------------- | --------------------------------------------- |
| [expert/](expert/README.md)       | @zcode/core 基础工程中的 expert 实现源码。    |
| [scheduler/](scheduler/README.md) | @zcode/core 基础工程中的 scheduler 实现源码。 |

### 文件

| 文件                           | 简要说明                                                                                                                                                               |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [definition.ts](definition.ts) | 实现或公开接口：BUILT_IN_EXPERT_WORKFLOW_KIND、BUILT_IN_EXPERT_WORKFLOW_DEFINITION_ID、BUILT_IN_EXPERT_WORKFLOW_DEFINITION_VERSION、DEFAULT_EXPERT_WORKFLOW_STRATEGY。 |
| [expert.ts](expert.ts)         | expert 的实现文件。                                                                                                                                                    |
| [lifecycle.ts](lifecycle.ts)   | 实现或公开接口：WorkflowGraphNodeChange、WorkflowSnapshotLifecycleResult、ReconcileWorkflowSnapshotForResumeOptions、CancelWorkflowSnapshotOptions。                   |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                                                                                                                                       |
| [scheduler.ts](scheduler.ts)   | 实现或公开接口：WorkflowGraphScheduler。                                                                                                                               |

<!-- qingqi-directory-index:end -->
