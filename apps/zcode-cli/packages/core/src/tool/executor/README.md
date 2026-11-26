# executor

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 executor 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                                         |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| [appAuthorization.test.ts](appAuthorization.test.ts)               | appAuthorization.test 的实现文件。                                                                               |
| [approval-gate.ts](approval-gate.ts)                               | \* 在权限服务已判定 ask 之后调用工具自报的 `prepareApproval`，并把它的答复与工具声明的                           |
| [background-task-output.ts](background-task-output.ts)             | 后台 Agent 的 child session 身份若只留在 Agent output / runtime                                                  |
| [background-task-registry.ts](background-task-registry.ts)         | workflow run 的快照沿用 WorkflowTaskSnapshot 的形状但把 output 放宽成 unknown（产物由脚本                        |
| [background-tasks.ts](background-tasks.ts)                         | ⚠ 两个 artifact：上面那个是脚本的**顶层返回值**（引擎内部的 `RunSettlement.artifact`，进                         |
| [bash-result-display.ts](bash-result-display.ts)                   | 原因：模型 envelope 会再次缩短正文且隐藏 Bash 的截断事实；Desktop 必须使用                                       |
| [batch-runner.ts](batch-runner.ts)                                 | const TOOL_SKIPPED_AFTER_BLOCKING_FAILURE =                                                                      |
| [call-runner.ts](call-runner.ts)                                   | 历史只保存一份原始目标参数；执行/Hook 可修改的对象在执行入口独立复制。                                           |
| [create-workflow-display.ts](create-workflow-display.ts)           | \* CreateWorkflow 的结果卡 display 构造。从 result-display.ts 拆出（400 行纪律）：                               |
| [display-text.ts](display-text.ts)                                 | \* display 文本的字节限长助手。从 result-display.ts 拆出：观察类工作流 display 的构造                            |
| [errors.ts](errors.ts)                                             | 工具补充给模型的说明，接在模型可见原文之后；不改 `error.message`。                                               |
| [events.ts](events.ts)                                             | 解析后的副作用能力（与权限判定同源）：订阅者据此在工具动手前知道「要写了」。                                     |
| [hook-flow.ts](hook-flow.ts)                                       | 实现或公开接口：runPreToolUseHooks、runPermissionRequestHooks、runPostToolUseHooks、runPostToolUseFailureHooks。 |
| [impl.ts](impl.ts)                                                 | 一个 runtime 一个执行器，序号在同一 assistant 内可比；删除、清空读取状态不影响它。                               |
| [memory-file-permission.ts](memory-file-permission.ts)             | alwaysAsk 是工具自报的"任何情况都要问"，这里不能把它放行掉。今天走不到这条分支                                   |
| [model-status-sink.ts](model-status-sink.ts)                       | \* 工具内部模型请求的默认状态出口。                                                                              |
| [permission-capability.ts](permission-capability.ts)               | capability group is provenance, not a runtime/model-controlled override.                                         |
| [permission-flow.ts](permission-flow.ts)                           | \* 只判断 Read 是否被模式或权限规则直接拒绝，不跑 hook、不弹确认、不发事件；规则只加载一次。                     |
| [permission-input-adjustments.ts](permission-input-adjustments.ts) | 确认窗里的入参调整：授权之后、handler 之前的那一步                                                               |
| [permission-input-recheck.ts](permission-input-recheck.ts)         | 与首次判权同一份上下文（mode、bashShellSelection、cwd 快照），由 executor 构造并透传。                           |
| [permission-input.ts](permission-input.ts)                         | 审批只读快照；先冻结再下钻，避免可信 Hook 返回循环引用时无限递归。                                               |
| [permission-request.ts](permission-request.ts)                     | 同一个请求生命周期；user-once 和重判后的请求只关闭 Hook 应答方，不另起审批流水线。                               |
| [permission-responder-race.ts](permission-responder-race.ts)       | PermissionRequest hook 链与交互 broker 的并发竞速。                                                              |
| [permission-response.ts](permission-response.ts)                   | 确认窗里的调整中实际生效的那部分（applyInputAdjustments 的 applied）。                                           |
| [permission-rules-persistence.ts](permission-rules-persistence.ts) | 权限规则的读取、持久化与授权后的落定（从 permission-flow.ts 拆出）。                                             |
| [permission-rules.ts](permission-rules.ts)                         | 实现或公开接口：applyPermissionUpdates。                                                                         |
| [permission-suggestions.ts](permission-suggestions.ts)             | 实现或公开接口：buildDefaultPermissionUpdates。                                                                  |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                                 |
| [result-content-projection.ts](result-content-projection.ts)       | 引用既是 schema 加载协议也是发现状态，不能按展示文本截断或转成 artifact。                                        |
| [result-display.ts](result-display.ts)                             | 拆到 create-workflow-display.ts 后保持既有导出面（handlers/create-workflow.ts 仍从这里 import）。                |
| [result-serialization.ts](result-serialization.ts)                 | Bash 空输出也需要通用占位，避免模型把静默成功误读成缺失工具结果。                                                |
| [telemetry.ts](telemetry.ts)                                       | 业务执行器会在所有正常返回分支按事实收口；这里只负责连 ToolCallStarted/Error                                     |
| [timeout.ts](timeout.ts)                                           | \* 可暂停的工具 deadline。                                                                                       |
| [turn-control.ts](turn-control.ts)                                 | 创建上限是需要用户手动释放名额的产品边界，不是 Agent 可恢复错误。                                                |
| [types.ts](types.ts)                                               | 后台跟踪的真实完成链（含终态写入）属于 runtime，不能随工具返回丢失。                                             |
| [utils.ts](utils.ts)                                               | 实现或公开接口：isRecord、summarizeInput、previewHookValue。                                                     |
| [validation.ts](validation.ts)                                     | 模型原始参数的首次 schema 失败需要把具体问题回传给模型；Hook 或权限                                              |
| [workflow-artifact.ts](workflow-artifact.ts)                       | \* workflow run 产物的序列化规则，被 core 内的两处共用：完成通知的 `<result>`（background-tasks.ts）             |
| [workflow-observation-display.ts](workflow-observation-display.ts) | \* 工作流工具的结果卡 display 构造：观察类五件套（GetWorkflowRun / ListWorkflowRuns                              |
| [workflow-published-artifacts.ts](workflow-published-artifacts.ts) | \* workflow run 的**用户面产物**在模型面的一行投影，被三处共用：                                                 |

<!-- qingqi-directory-index:end -->
