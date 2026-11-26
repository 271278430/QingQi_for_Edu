# model

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 model 实现源码。

### 子目录

| 目录                                                                    | 存放内容                                                             |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------- |
| [endpoint-routing-edition/](endpoint-routing-edition/README.md)         | @zcode/adapters 基础工程中的 endpoint routing edition 实现源码。     |
| [provider-builtin-tool-compat/](provider-builtin-tool-compat/README.md) | @zcode/adapters 基础工程中的 provider builtin tool compat 实现源码。 |
| [request-security-edition/](request-security-edition/README.md)         | @zcode/adapters 基础工程中的 request security edition 实现源码。     |

### 文件

| 文件                                                                         | 简要说明                                                                                                                                                    |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [account-request-retry.ts](account-request-retry.ts)                         | 实现或公开接口：AccountRequestRetry、isProjectTokenRejection。                                                                                              |
| [anthropic-reasoning-metadata.ts](anthropic-reasoning-metadata.ts)           | 把“没有 signature”直接等同于“不兼容”会让同模型历史里的                                                                                                      |
| [anthropic-request-metadata.ts](anthropic-request-metadata.ts)               | 实现或公开接口：createAnthropicRequestMetadataUserId、resolveAnthropicRequestMetadataUserId、redactAnthropicRequestMetadata。                               |
| [anthropic-stream-compat.ts](anthropic-stream-compat.ts)                     | 修复原因：AI SDK 会在发请求前合并连续的 user message；Memory selector 的                                                                                    |
| [empty-completion-retry.ts](empty-completion-retry.ts)                       | 实现或公开接口：EMPTY_COMPLETION_MAX_RETRIES、EMPTY_COMPLETION_MESSAGE、createEmptyCompletionFailure、canRetryEmptyCompletion。                             |
| [errors.ts](errors.ts)                                                       | AI SDK model adapter errors                                                                                                                                 |
| [failure-ai-sdk-provider-error.ts](failure-ai-sdk-provider-error.ts)         | \* 只读取 AI SDK 已解析并暴露的错误对象；未知业务码继续交给既有通用分类链路。                                                                               |
| [failure-classifier.ts](failure-classifier.ts)                               | 分类链路能读取 AI SDK parsed error，但观测链路只认识 ProviderBusinessError，                                                                                |
| [failure-inspection.ts](failure-inspection.ts)                               | AI SDK/stream chunk 可能把 ProviderBusinessError 包在 cause 里；                                                                                            |
| [failure-provider-business-codes.ts](failure-provider-business-codes.ts)     | 部分 OpenAI-compatible provider 会把可恢复的上游网络故障包装成业务码。                                                                                      |
| [failure-tls.ts](failure-tls.ts)                                             | AI SDK adapter 可能只转发外层错误，丢失 Node TLS cause.code；                                                                                               |
| [index.ts](index.ts)                                                         | Model adapters backed by the Vercel AI SDK                                                                                                                  |
| [media-transform-policy.ts](media-transform-policy.ts)                       | Provider 格式重构与 PDF 支持发生冲突时，旧正则解析和新实现的                                                                                                |
| [model-execution.ts](model-execution.ts)                                     | Vercel AI SDK model execution                                                                                                                               |
| [model-option-map-fetch.ts](model-option-map-fetch.ts)                       | Option Map 是 reasoning/max-output 的唯一请求字段权威。若 SDK 改成非文本 Body 却静默                                                                        |
| [model-request-headers.ts](model-request-headers.ts)                         | 会话能力标签（docs/design/v2/model/session-features-header.md）。                                                                                           |
| [model.ts](model.ts)                                                         | 实现或公开接口：ModelExecutionRequest、ModelExecutor、CreateModelOptions、createModel。                                                                     |
| [off-peak-request-auth.ts](off-peak-request-auth.ts)                         | 派发快照只固定票据与登录作用域；短期 PAT 必须在每个 HTTP attempt 向原 owner 解析。                                                                          |
| [official-coding-plan-gateway.ts](official-coding-plan-gateway.ts)           | 静态实现只提供 URL 决策；Host 清理、请求与响应透传由公共 fetch wrapper 负责。                                                                               |
| [offpeak-retry.ts](offpeak-retry.ts)                                         | off-peak 排队协议只对显式声明 off-peak-queue 的请求生效。                                                                                                   |
| [openai-responses-json-compat.ts](openai-responses-json-compat.ts)           | 部分 Responses-compatible 服务在非流式 compact 响应里省略                                                                                                   |
| [opencode-session.ts](opencode-session.ts)                                   | 实现或公开接口：isOpenCodeGoBaseUrl。                                                                                                                       |
| [provider-endpoint-routing-fetch.ts](provider-endpoint-routing-fetch.ts)     | 配置接口只接受账号 owner 返回的 ID，禁止从模型 PAT 或手工 Key 推导。                                                                                        |
| [provider-endpoint-routing-options.ts](provider-endpoint-routing-options.ts) | 由 bootstrap 注入的运行环境；实现不得修改 Provider 的持久化配置。                                                                                           |
| [provider-finish-business-error.ts](provider-finish-business-error.ts)       | AI SDK 的 error chunk 常带普通 Error.message（如 rate limited），没有业务码；                                                                               |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                                                                                            |
| [reasoning-history-normalization.ts](reasoning-history-normalization.ts)     | 签名拒绝重试日志里 provider 报错原文的最大字符数：留下定位原因所需的内容，不把整段响应体写进日志。                                                          |
| [request-admission.ts](request-admission.ts)                                 | \* runner 在每次尝试**发出前** `admitAttempt`，拿到票据后才发请求；尝试结束（成功、失败、抛出、消费者                                                       |
| [request-observations.ts](request-observations.ts)                           | 实现或公开接口：RequestObservationStore、readRequestObservationId。                                                                                         |
| [request-security.ts](request-security.ts)                                   | 进程只共享可采用资源，每个模型执行器仍持有独立的请求状态。                                                                                                  |
| [retry-budget.ts](retry-budget.ts)                                           | \* 「无上限」**只**放宽瞬态失败的放弃条件：runner 的 attempt 循环、失败后「还能不能再试」两处闸门；                                                         |
| [retry-policy.ts](retry-policy.ts)                                           | maxAttempts includes the first request; env/config names expose retry count.                                                                                |
| [runner-attribution.ts](runner-attribution.ts)                               | \* runner-status.ts 顶到 oxlint max-lines 上限（400 行），把「请求归因 header」一族                                                                         |
| [runner-debug-redaction.ts](runner-debug-redaction.ts)                       | 内部 dataUrl、AI SDK image/file 与 provider wire 的媒体键名不同，                                                                                           |
| [runner-debug.ts](runner-debug.ts)                                           | 生产环境 rollout 目录最多保留的 model-io 会话文件数。超出删最旧。                                                                                           |
| [runner-diagnostics.ts](runner-diagnostics.ts)                               | 空文本可能携带有效的 reasoning 签名，不能当作空超窗丢弃。                                                                                                   |
| [runner-generate.ts](runner-generate.ts)                                     | 重试预算档位：workflow actor 的请求带 unbounded，                                                                                                           |
| [runner-network-headers.ts](runner-network-headers.ts)                       | 实现或公开接口：sanitizeModelNetworkHeaders。                                                                                                               |
| [runner-normalization.ts](runner-normalization.ts)                           | \* 非流式结果按 AI SDK `result.content` 的顺序给 reasoning、text、tool-call 编号                                                                            |
| [runner-options.ts](runner-options.ts)                                       | zcode-plan 业务码常只出现在 finish chunk 的 response.body，流式路径需显式开启。                                                                             |
| [runner-record.ts](runner-record.ts)                                         | 实现或公开接口：asRecord、isRecord、stringProperty、numberProperty。                                                                                        |
| [runner-retry.ts](runner-retry.ts)                                           | Retry-After 之上追加的抖动：最多 retry-after 的 20%，且不超过 5 秒。                                                                                        |
| [runner-runtime-headers.ts](runner-runtime-headers.ts)                       | 只信任 Host 的结构化分类；旧文案也可能来自无效配置，不能按文本扩大重试。                                                                                    |
| [runner-runtime.ts](runner-runtime.ts)                                       | Start Plan 的账号鉴权材料按 attempt 刷新；adapter 内部 retry 也是真实模型请求，                                                                             |
| [runner-status.ts](runner-status.ts)                                         | 请求归因 header 一族住在 runner-attribution.ts（max-lines 拆分）；公开面仍从本文件导出，                                                                    |
| [runner-stream.ts](runner-stream.ts)                                         | runner-stream 的实现文件。                                                                                                                                  |
| [runner-telemetry.ts](runner-telemetry.ts)                                   | model status 虽然记录了原始异常类型和阶段，但终态 ErrorPayload 曾丢失这些事实；                                                                             |
| [runner.ts](runner.ts)                                                       | Vercel AI SDK model runner                                                                                                                                  |
| [stream-idle-timeout.ts](stream-idle-timeout.ts)                             | 实现或公开接口：MODEL_STREAM_IDLE_TIMEOUT_RETRY_INCREMENT_MS、resolveModelStreamIdleTimeoutMs、isModelStreamIdleTimeoutError、createLinkedAbortController。 |
| [stream-retry-boundary.ts](stream-retry-boundary.ts)                         | Note: these events are buffered, not yielded, until a committed stream boundary appears.                                                                    |
| [streaming-tool-call-assembler.ts](streaming-tool-call-assembler.ts)         | 已经进入流式 input 生命周期时，final call 不能替代缺失的                                                                                                    |
| [strict-tool-schema.ts](strict-tool-schema.ts)                               | Anthropic strict 工具 schema：资格判定 + 子集折叠                                                                                                           |
| [system-message-compat.ts](system-message-compat.ts)                         | 部分旧式 OpenAI-compatible chat template 只接受一个开头 system。                                                                                            |
| [tool-call-validation.ts](tool-call-validation.ts)                           | client-executed 的空名调用仍可用原 id 闭合。在 Adapter                                                                                                      |
| [tool-input-normalization.ts](tool-input-normalization.ts)                   | 上游会先把合法 JSON 字面量 "null" 解析成原生 null；                                                                                                         |
| [tool-result-media-projection.ts](tool-result-media-projection.ts)           | 根因：openai kind 使用 Responses API；按宽泛的 OpenAI-like 家族判断会把它                                                                                   |
| [tool-search.ts](tool-search.ts)                                             | 模型请求能力只由协议与接入方式决定；core 投影据此选择请求形态。                                                                                             |
| [tool-transform.ts](tool-transform.ts)                                       | Vercel AI SDK tool transforms                                                                                                                               |
| [transform.ts](transform.ts)                                                 | Vercel AI SDK protocol transforms                                                                                                                           |
| [workflow-model-failure-policy.ts](workflow-model-failure-policy.ts)         | \* workflow 内的模型侧错误策略表。                                                                                                                          |

<!-- qingqi-directory-index:end -->
