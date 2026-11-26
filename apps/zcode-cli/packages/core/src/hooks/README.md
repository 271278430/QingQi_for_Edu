# hooks

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 hooks 生命周期与操作入口。

### 文件

| 文件                                                                       | 简要说明                                                                                                       |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [configured-runner-callback.ts](configured-runner-callback.ts)             | 实现或公开接口：createConfiguredHookCallback。                                                                 |
| [configured-runner-input.ts](configured-runner-input.ts)                   | 这里只补无损 alias，继续保留 ZCode camelCase 字段作为内部主契约。                                              |
| [configured-runner.ts](configured-runner.ts)                               | 实现或公开接口：createConfiguredHookRunner。                                                                   |
| [display-metadata.ts](display-metadata.ts)                                 | 实现或公开接口：createHookExecutionDescriptor、sanitizeHookDisplayText。                                       |
| [index.ts](index.ts)                                                       | index 的实现文件。                                                                                             |
| [output.ts](output.ts)                                                     | 实现或公开接口：processHookOutput、mergeHookRunResult、matchesHookMatcher。                                    |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                                               |
| [runner-helpers.ts](runner-helpers.ts)                                     | 安全 gate 自身异常时不能继续创建进程或后台任务。                                                               |
| [runner.ts](runner.ts)                                                     | skipLifecycle 的 hook 不发事件，不能计入客户端等待完成的 hookCount。                                           |
| [session-mailbox.ts](session-mailbox.ts)                                   | 实现或公开接口：createSessionMailboxHookRegistrations。                                                        |
| [types.ts](types.ts)                                                       | \* 配置 Hook 的执行器可以附带 stderr 等诊断；这些信息只进入生命周期事件，                                      |
| [workspace-hook-policy.ts](workspace-hook-policy.ts)                       | 实现或公开接口：WorkspaceHookPolicyChange、WorkspaceHookPolicyProvider、InMemoryWorkspaceHookPolicyProvider。  |
| [workspace-hook-review-flow.ts](workspace-hook-review-flow.ts)             | Runtime-owned review generation registry. It contains no persistence or UI behavior.                           |
| [workspace-hook-runtime-admission.ts](workspace-hook-runtime-admission.ts) | Compatibility assertion for callers that hold a bundle target. Runtime registrations omit it.                  |
| [workspace-hook-telemetry.ts](workspace-hook-telemetry.ts)                 | revoke 需要专门观测：排查「撤销后面板失效」时，必须能从日志判断                                                |
| [workspace-hook-trust-coordinator.ts](workspace-hook-trust-coordinator.ts) | \* 非抛错版资格判定：controller 的 respond 在 mutation 前用它返回精确 reasonCode                               |
| [workspace-hook-trust-domain.ts](workspace-hook-trust-domain.ts)           | workspace-hook-trust-domain 的实现文件。                                                                       |
| [workspace-hook-trust-evaluation.ts](workspace-hook-trust-evaluation.ts)   | 实现或公开接口：evaluateWorkspaceHookEntry、trustKey。                                                         |
| [workspace-hook-trust-records.ts](workspace-hook-trust-records.ts)         | 实现或公开接口：createWorkspaceHookTrustRecords。                                                              |
| [workspace-hook-trust-types.ts](workspace-hook-trust-types.ts)             | 实现或公开接口：WorkspaceHookTrustStoreStatus、WorkspaceHookTrustStoreState、WorkspaceHookSnapshotEvaluation。 |

<!-- qingqi-directory-index:end -->
