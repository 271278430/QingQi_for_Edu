# subagents

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 subagents 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                                     | 简要说明                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [conversation-session-built-in-subagent-model-overrides.test.ts](conversation-session-built-in-subagent-model-overrides.test.ts)         | Bug 根因：child 与 parent 档位相同时，忽略 profile 并错误继承 parent 的回归也会通过。              |
| [conversation-session-explore-permission-delegate.test.ts](conversation-session-explore-permission-delegate.test.ts)                     | 修复原因：内置 Explore 曾固定以 yolo 运行，只靠 prompt 约束只读，提示注入后模型可经                |
| [conversation-session-subagent-catalog-refresh.test.ts](conversation-session-subagent-catalog-refresh.test.ts)                           | 原因：本用例的回放 Provider 只声明 high/max；保留两个不同合法档位验证配置更新与隔离。              |
| [conversation-session-subagent-compact-delivery.test.ts](conversation-session-subagent-compact-delivery.test.ts)                         | conversation-session-subagent-compact-delivery.test 的实现文件。                                   |
| [conversation-session-subagent-context-boundaries.test.ts](conversation-session-subagent-context-boundaries.test.ts)                     | 原因：本用例的回放 Provider 只声明 high/max；保留两个不同合法档位验证配置更新与隔离。              |
| [conversation-session-subagent-cross-host.test.ts](conversation-session-subagent-cross-host.test.ts)                                     | 原因：本用例的回放 Provider 只声明 high/max；保留两个不同合法档位验证配置更新与隔离。              |
| [conversation-session-subagent-interaction-delegate.test.ts](conversation-session-subagent-interaction-delegate.test.ts)                 | 单条失败时先释放 child broker，避免仍在等待的 interaction 污染下一条 case。                        |
| [conversation-session-subagent-model-boundary.test.ts](conversation-session-subagent-model-boundary.test.ts)                             | 本 case 的回放响应是 Messages 协议；默认 Chat Completions 种子会请求错误路由并返回夹具 500。       |
| [conversation-session-subagent-multi-workspace.test.ts](conversation-session-subagent-multi-workspace.test.ts)                           | 原因：本用例的回放 Provider 只声明 high/max；保留两个不同合法档位验证配置更新与隔离。              |
| [conversation-session-subagent-parallel-projection.test.ts](conversation-session-subagent-parallel-projection.test.ts)                   | Bug 原因：旧链路在 SubagentSpawned 后另查 session/subagents；第 7 个 child                         |
| [conversation-session-subagent-profile-fields.test.ts](conversation-session-subagent-profile-fields.test.ts)                             | 原因：本用例的回放 Provider 只声明 high/max；保留两个不同合法档位验证配置更新与隔离。              |
| [conversation-session-subagent-prompt-assembly.test.ts](conversation-session-subagent-prompt-assembly.test.ts)                           | conversation-session-subagent-prompt-assembly.test 的实现文件。                                    |
| [conversation-session-subagent-provider-registry-cold-start.test.ts](conversation-session-subagent-provider-registry-cold-start.test.ts) | conversation-session-subagent-provider-registry-cold-start.test 的实现文件。                       |
| [conversation-session-subagent-provider-retry-status.test.ts](conversation-session-subagent-provider-retry-status.test.ts)               | Bug 原因：完成 token 曾同时出现在 user prompt 与 provider reply，聚合 timeline                     |
| [conversation-session-subagent-respond-to-coordinator.test.ts](conversation-session-subagent-respond-to-coordinator.test.ts)             | Bug 原因：工具执行失败已经统一使用通用生命周期文案；旧断言仍期待 TaskOutput / RespondToCoordinator |
| [conversation-session-subagent-runtime-catalog-reasoning.test.ts](conversation-session-subagent-runtime-catalog-reasoning.test.ts)       | 选择器值是 `custom:provider:model`；落盘的 Markdown 用 provider/model，保存后按落盘格式断言。      |
| [conversation-session-subagent-runtime-refresh.test.ts](conversation-session-subagent-runtime-refresh.test.ts)                           | 原因：本用例的回放 Provider 只声明 high/max；保留两个不同合法档位验证配置更新与隔离。              |
| [conversation-session-subagent-side-tabs.test.ts](conversation-session-subagent-side-tabs.test.ts)                                       | 先观察运行中 tab 的去重，再释放上游流，避免依赖固定 sleep 的抢时序。                               |
| [conversation-session-subagent-sidebar-isolation.test.ts](conversation-session-subagent-sidebar-isolation.test.ts)                       | 真正重启 CLI 清空 detached publisher；打开历史详情必须恢复原身份。                                 |
| [conversation-session-subagent-team-scope.test.ts](conversation-session-subagent-team-scope.test.ts)                                     | Team child 缺少 organization/project 时，在 child provider 请求之前失败，父会话仍可继续。          |
| [README.md](README.md)                                                                                                                   | 本目录用途、子目录与逐文件说明。                                                                   |

<!-- qingqi-directory-index:end -->
