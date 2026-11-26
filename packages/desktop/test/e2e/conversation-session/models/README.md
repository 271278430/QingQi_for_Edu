# models

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 models 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                                                         | 简要说明                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| [conversation-session-active-model-context.test.ts](conversation-session-active-model-context.test.ts)                                                       | 模型身份是历史公告：换模型时追加一条，之前的公告留在历史                              |
| [conversation-session-claude-anthropic-reasoning-budget.test.ts](conversation-session-claude-anthropic-reasoning-budget.test.ts)                             | conversation-session-claude-anthropic-reasoning-budget.test 的实现文件。              |
| [conversation-session-composer-provider-identity.test.ts](conversation-session-composer-provider-identity.test.ts)                                           | rolling 动画短暂保留旧标签；等待实际展示收敛，避免读取退场节点。                      |
| [conversation-session-deepseek-v4-reasoning-request-shape.test.ts](conversation-session-deepseek-v4-reasoning-request-shape.test.ts)                         | 当前 main 的 custom provider 表单只保存 model ID；DeepSeek V4 档位由 Agent            |
| [conversation-session-draft-model-switch-first-send.test.ts](conversation-session-draft-model-switch-first-send.test.ts)                                     | 已接纳的执行模型仍是 secondary；此后只修改 Composer，不能提前改写 Session。           |
| [conversation-session-glm52-reasoning-request-shape.test.ts](conversation-session-glm52-reasoning-request-shape.test.ts)                                     | conversation-session-glm52-reasoning-request-shape.test 的实现文件。                  |
| [conversation-session-gpt-openai-compatible-reasoning-effort.test.ts](conversation-session-gpt-openai-compatible-reasoning-effort.test.ts)                   | conversation-session-gpt-openai-compatible-reasoning-effort.test 的实现文件。         |
| [conversation-session-model-availability-fallback.test.ts](conversation-session-model-availability-fallback.test.ts)                                         | 回放使用 Messages 协议，不能用默认 Chat Completions 种子请求另一条路由。              |
| [conversation-session-model-config.test.ts](conversation-session-model-config.test.ts)                                                                       | conversation-session-model-config.test 的实现文件。                                   |
| [conversation-session-model-output-token-budget.test.ts](conversation-session-model-output-token-budget.test.ts)                                             | conversation-session-model-output-token-budget.test 的实现文件。                      |
| [conversation-session-model-output-token-preflight-smoke.test.ts](conversation-session-model-output-token-preflight-smoke.test.ts)                           | conversation-session-model-output-token-preflight-smoke.test 的实现文件。             |
| [conversation-session-model-output-token-preflight.test.ts](conversation-session-model-output-token-preflight.test.ts)                                       | provider usage anchor 已覆盖上一轮 assistant；suffix 估算本轮 user 的 85,328 tokens， |
| [conversation-session-model-provider-add-send.test.ts](conversation-session-model-provider-add-send.test.ts)                                                 | Template 的模型成员 ID 与通用 replay Provider 不同，不能借用 UPSTREAM_MODEL。         |
| [conversation-session-model-provider-effective-selection.test.ts](conversation-session-model-provider-effective-selection.test.ts)                           | 冷启动的默认 workspace 尚未经过项目草稿导航，先从真实项目入口建立作用域。             |
| [conversation-session-model-provider-list-filtering.test.ts](conversation-session-model-provider-list-filtering.test.ts)                                     | conversation-session-model-provider-list-filtering.test 的实现文件。                  |
| [conversation-session-model-provider-plan-surface.test.ts](conversation-session-model-provider-plan-surface.test.ts)                                         | \* 定时任务的模型选择是 task-local 记录，不能因为聊天默认计划改变而被重写。           |
| [conversation-session-model-provider-regression-gaps.test.ts](conversation-session-model-provider-regression-gaps.test.ts)                                   | \* 目录里没有被既有正式用例完整覆盖的组合。                                           |
| [conversation-session-model-provider-restart-recovery.test.ts](conversation-session-model-provider-restart-recovery.test.ts)                                 | Bug 根因：运行中的 Host 会在退出时落盘内存里的连接选择；若 fixture 预先               |
| [conversation-session-model-provider-session-isolation.test.ts](conversation-session-model-provider-session-isolation.test.ts)                               | conversation-session-model-provider-session-isolation.test 的实现文件。               |
| [conversation-session-model-provider-settings-transition.test.ts](conversation-session-model-provider-settings-transition.test.ts)                           | conversation-session-model-provider-settings-transition.test 的实现文件。             |
| [conversation-session-model-provider-turbo-recovery.test.ts](conversation-session-model-provider-turbo-recovery.test.ts)                                     | conversation-session-model-provider-turbo-recovery.test 的实现文件。                  |
| [conversation-session-model-provider-turbo-switch.test.ts](conversation-session-model-provider-turbo-switch.test.ts)                                         | Bug 根因：V4 草稿跨模型切换以 toolbar projection 为显示真值，不再把乐观               |
| [conversation-session-model-switch-auto-compact.test.ts](conversation-session-model-switch-auto-compact.test.ts)                                             | 当前 planner 保留最近一轮；两轮历史才有可压缩分区，不能将 noop 算作覆盖。             |
| [conversation-session-model-switch-compact.test.ts](conversation-session-model-switch-compact.test.ts)                                                       | 原因：旧 case 的单轮短文本可能合法 noop，旧 non-stream/operationId 也不属于 V4。      |
| [conversation-session-model-switch-image-strip.test.ts](conversation-session-model-switch-image-strip.test.ts)                                               | 修复原因：WDIO wrapper 会在进入 test body 前读取 Mocha Runnable timeout；             |
| [conversation-session-model-switch-queue.test.ts](conversation-session-model-switch-queue.test.ts)                                                           | 修复原因：标题生成也会短暂进入 streaming；必须等真正的 main request                   |
| [conversation-session-model-switch-restore-repro.test.ts](conversation-session-model-switch-restore-repro.test.ts)                                           | conversation-session-model-switch-restore-repro.test 的实现文件。                     |
| [conversation-session-model-trajectory-viewer.test.ts](conversation-session-model-trajectory-viewer.test.ts)                                                 | TRJ02：错误投影和工具元数据必须从真实 host 文件读取链路进入 UI。                      |
| [conversation-session-model-unavailable-reselect.test.ts](conversation-session-model-unavailable-reselect.test.ts)                                           | 场景：会话常驻模型所属 Provider 从 Registry 下架（对应体验套餐到期 / 切账号）。       |
| [conversation-session-new-session-inherits-model.test.ts](conversation-session-new-session-inherits-model.test.ts)                                           | Recent 按项目/任务范围隔离；前后两次都从全局新任务入口建立同一范围。                  |
| [conversation-session-openai-compatible-thinking-toggle-request-shape.test.ts](conversation-session-openai-compatible-thinking-toggle-request-shape.test.ts) | 表单不保存 reasoning metadata；首发先验证 Agent resolver 的 enabled 默认请求，        |
| [conversation-session-openrouter-model-id-colon.test.ts](conversation-session-openrouter-model-id-colon.test.ts)                                             | 修复原因：产品要求切换到新模型后由用户显式选择思考档位，未选时发送键保持禁用；        |
| [conversation-session-opus47-anthropic-adaptive-reasoning.test.ts](conversation-session-opus47-anthropic-adaptive-reasoning.test.ts)                         | conversation-session-opus47-anthropic-adaptive-reasoning.test 的实现文件。            |
| [conversation-session-provider-registry-prewarm.test.ts](conversation-session-provider-registry-prewarm.test.ts)                                             | 冷恢复 helper 恢复默认项目；选择必须写入同一项目的草稿，不能混用全局草稿目录。        |
| [conversation-session-readstate-model-isolation.test.ts](conversation-session-readstate-model-isolation.test.ts)                                             | conversation-session-readstate-model-isolation.test 的实现文件。                      |
| [conversation-session-running-model-switch-usage.test.ts](conversation-session-running-model-switch-usage.test.ts)                                           | Node 内置 SQLite 当前只提供同步只读接口；E2E 每次只读一行并立即关闭句柄。             |
| [conversation-session-same-model-draft-provider-identity.test.ts](conversation-session-same-model-draft-provider-identity.test.ts)                           | conversation-session-same-model-draft-provider-identity.test 的实现文件。             |
| [conversation-session-same-model-provider-identity.test.ts](conversation-session-same-model-provider-identity.test.ts)                                       | 目标模型可能默认 max；请求 high 的断言必须由真实 UI 选择建立前置条件。                |
| [conversation-session-thought-level-cold-resume.test.ts](conversation-session-thought-level-cold-resume.test.ts)                                             | 个人 Provider 不能依赖旧内建 GLM metadata 补齐；明确声明被验证的合法档位和 wire map。 |
| [conversation-session-thought-level-session-isolation.test.ts](conversation-session-thought-level-session-isolation.test.ts)                                 | 修复原因：formal admission 禁止依赖整套 legacy conversation-session helper；          |
| [conversation-session-v4-model-switch.test.ts](conversation-session-v4-model-switch.test.ts)                                                                 | M4 门禁：switchModelConfig（v4 控制条模型配置表单）。                                 |
| [conversation-session-worker-effective-selection.test.ts](conversation-session-worker-effective-selection.test.ts)                                           | 读取真正 adapter 写出的 model-io，不用 helper 返回值冒充 child 请求。                 |
| [README.md](README.md)                                                                                                                                       | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
