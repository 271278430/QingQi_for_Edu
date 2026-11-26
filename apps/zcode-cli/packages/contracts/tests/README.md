# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/contracts 基础工程中的 tests 验收与回归场景。

### 文件

| 文件                                                                           | 简要说明                                                                                                             |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| [amend-workflow.test.ts](amend-workflow.test.ts)                               | docs/dynamic-workflow/launch.md「The `AmendWorkflow` tool」：模型面只有 run_id 必填，其余字段省略                    |
| [ask-user-question.test.ts](ask-user-question.test.ts)                         | ask-user-question.test 的实现文件。                                                                                  |
| [automation.test.ts](automation.test.ts)                                       | 向后兼容：delayMinutes 是新增的相对时间能力，绝不能变成必填让旧调用方                                                |
| [compact.test.ts](compact.test.ts)                                             | compact.test 的实现文件。                                                                                            |
| [create-workflow.test.ts](create-workflow.test.ts)                             | 坏脚本路径完全不变：handler 直接回诊断，不启动、不建 run，因此两个新字段缺席。                                       |
| [custom-commands.test.ts](custom-commands.test.ts)                             | 行内块后面的原文另起一行，代码块的结束标记才成立。                                                                   |
| [dynamic-workflow-run-progress.test.ts](dynamic-workflow-run-progress.test.ts) | 进度投影的契约面：一条引擎 RunEvent → 一条 dynamic_workflow_run_progress 会话事件。                                  |
| [edit.test.ts](edit.test.ts)                                                   | edit.test 的实现文件。                                                                                               |
| [event-reducer-session-status.test.ts](event-reducer-session-status.test.ts)   | event-reducer-session-status.test 的实现文件。                                                                       |
| [event-reducer.test.ts](event-reducer.test.ts)                                 | Event Reducer Tests                                                                                                  |
| [fill-workflow-hole.test.ts](fill-workflow-hole.test.ts)                       | docs/dynamic-workflow/launch.md「The `FillWorkflowHole` tool」：模型面是 run_id + hole_id + 恰好一个                 |
| [get-workflow-run.test.ts](get-workflow-run.test.ts)                           | snake_case 随 TaskOutput 的 task_id：两个工具在模型眼里是同一族的 run/task 键。                                      |
| [git-bash-path.test.ts](git-bash-path.test.ts)                                 | git-bash-path.test 的实现文件。                                                                                      |
| [grep.test.ts](grep.test.ts)                                                   | grep.test 的实现文件。                                                                                               |
| [in-memory-session-event-store.test.ts](in-memory-session-event-store.test.ts) | turn 1 的 3 条 delta 已淘汰，其余全部保留；顺序仍按 seq。                                                            |
| [list-models.test.ts](list-models.test.ts)                                     | docs/dynamic-workflow/launch.md：dwf 选型的发现面。只读、无入参、输出的每一行都能逐字                                |
| [list-workflow-runs.test.ts](list-workflow-runs.test.ts)                       | 用户裁决（spec 的「`ListWorkflowRuns` 输出」行）：limit 是**钳制**而不是拒绝。一次只读                               |
| [local-date.test.ts](local-date.test.ts)                                       | local-date.test 的实现文件。                                                                                         |
| [model-image-media.test.ts](model-image-media.test.ts)                         | model-image-media.test 的实现文件。                                                                                  |
| [model-invocation-context.test.ts](model-invocation-context.test.ts)           | model-invocation-context.test 的实现文件。                                                                           |
| [model-media-policy.test.ts](model-media-policy.test.ts)                       | model-media-policy.test 的实现文件。                                                                                 |
| [model-request-admission.test.ts](model-request-admission.test.ts)             | docs/dynamic-workflow/concurrency.md「One ticket per request attempt」：准入端口是 runtime-only 请求字段；票据同时是 |
| [model-retry-budget.test.ts](model-retry-budget.test.ts)                       | docs/dynamic-workflow/concurrency.md「Unbounded retries for workflow traffic」：重试预算档位是 runtime-only 字段；   |
| [model-schema-contract.test.ts](model-schema-contract.test.ts)                 | model-schema-contract.test 的实现文件。                                                                              |
| [model-selection.test.ts](model-selection.test.ts)                             | model-selection.test 的实现文件。                                                                                    |
| [model-usage.test.ts](model-usage.test.ts)                                     | model-usage.test 的实现文件。                                                                                        |
| [off-peak.test.ts](off-peak.test.ts)                                           | off-peak.test 的实现文件。                                                                                           |
| [public-egress-ip.test.ts](public-egress-ip.test.ts)                           | public-egress-ip.test 的实现文件。                                                                                   |
| [read-pdf.test.ts](read-pdf.test.ts)                                           | read-pdf.test 的实现文件。                                                                                           |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                                                                     |
| [respond-to-coordinator.test.ts](respond-to-coordinator.test.ts)               | respond-to-coordinator.test 的实现文件。                                                                             |
| [resume-workflow-run.test.ts](resume-workflow-run.test.ts)                     | 成功输出只有一个形状：run 恢复后在后台飞行，携勿轮询引导。失败走 ToolHandlerFailure                                  |
| [rewind.test.ts](rewind.test.ts)                                               | rewind.test 的实现文件。                                                                                             |
| [session-event-retention.test.ts](session-event-retention.test.ts)             | session-event-retention.test 的实现文件。                                                                            |
| [submit-result.test.ts](submit-result.test.ts)                                 | 声明的输入有意通用：具体 per-ask schema 在 ask epilogue 里，不进工具声明。                                           |
| [target.test.ts](target.test.ts)                                               | target.test 的实现文件。                                                                                             |
| [task-output.test.ts](task-output.test.ts)                                     | task-output.test 的实现文件。                                                                                        |
| [telemetry.test.ts](telemetry.test.ts)                                         | telemetry.test 的实现文件。                                                                                          |
| [tool-execution-telemetry.test.ts](tool-execution-telemetry.test.ts)           | tool-execution-telemetry.test 的实现文件。                                                                           |
| [tool-json-schema.test.ts](tool-json-schema.test.ts)                           | input_schema 的固定字节：key 顺序也计入 tools 缓存前缀。                                                             |
| [tool-result-metadata.test.ts](tool-result-metadata.test.ts)                   | tool-result-metadata.test 的实现文件。                                                                               |
| [workflow-scheduler-state.test.ts](workflow-scheduler-state.test.ts)           | 实现或公开接口：meta。                                                                                               |
| [workflow-settings.test.ts](workflow-settings.test.ts)                         | docs/dynamic-workflow/launch.md「Adjusting the settings in the window」                                              |
| [workspace-hook-trust.test.ts](workspace-hook-trust.test.ts)                   | onError 进声明摘要（shared/workspace-hook-digest.ts），改了要重新信任。                                              |
| [workspace-mutating-tool-call.test.ts](workspace-mutating-tool-call.test.ts)   | 「第一笔写入」的判定（apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Amend-resume」）：          |

<!-- qingqi-directory-index:end -->
