# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 tests 验收与回归场景。

### 子目录

| 目录                                                                    | 存放内容                                                                   |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [fixtures/](fixtures/README.md)                                         | @zcode/adapters 基础工程中的 fixtures 测试夹具与样例。                     |
| [memory-diagnostics/](memory-diagnostics/README.md)                     | @zcode/adapters 基础工程中的 memory diagnostics 验收与回归场景。           |
| [provider-builtin-tool-compat/](provider-builtin-tool-compat/README.md) | @zcode/adapters 基础工程中的 provider builtin tool compat 验收与回归场景。 |

### 文件

| 文件                                                                                                   | 简要说明                                                                                                                |
| ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| [agent-listing-wire.test.ts](agent-listing-wire.test.ts)                                               | 首次与完整工具批次后的 listing 在 MCS 分支都为 system string，                                                          |
| [anthropic-effort-wire.test.ts](anthropic-effort-wire.test.ts)                                         | anthropic-effort-wire.test 的实现文件。                                                                                 |
| [anthropic-mid-conversation-system-wire.test.ts](anthropic-mid-conversation-system-wire.test.ts)       | anthropic-mid-conversation-system-wire.test 的实现文件。                                                                |
| [anthropic-request-metadata-wire.test.ts](anthropic-request-metadata-wire.test.ts)                     | Drain the provider stream until its expected wire-capture error.                                                        |
| [anthropic-request-metadata.test.ts](anthropic-request-metadata.test.ts)                               | anthropic-request-metadata.test 的实现文件。                                                                            |
| [async-migration-startup.test.ts](async-migration-startup.test.ts)                                     | 本 hotfix 不改迁移算法；状态通知不能让执行路径偏离账本对应的冻结原 SQL。                                                |
| [attachment-resume-wire.test.ts](attachment-resume-wire.test.ts)                                       | attachment-resume-wire.test 的实现文件。                                                                                |
| [auth.test.ts](auth.test.ts)                                                                           | auth.test 的实现文件。                                                                                                  |
| [bash-direct-execution.test.ts](bash-direct-execution.test.ts)                                         | bash-direct-execution.test 的实现文件。                                                                                 |
| [bash-file-output.test.ts](bash-file-output.test.ts)                                                   | bash-file-output.test 的实现文件。                                                                                      |
| [bash-output-preview.test.ts](bash-output-preview.test.ts)                                             | bash-output-preview.test 的实现文件。                                                                                   |
| [bash-process-stop.test.ts](bash-process-stop.test.ts)                                                 | bash-process-stop.test 的实现文件。                                                                                     |
| [bash-progress-poller.test.ts](bash-progress-poller.test.ts)                                           | bash-progress-poller.test 的实现文件。                                                                                  |
| [bash-resource-lifecycle.test.ts](bash-resource-lifecycle.test.ts)                                     | bash-resource-lifecycle.test 的实现文件。                                                                               |
| [bash-resource-telemetry.test.ts](bash-resource-telemetry.test.ts)                                     | bash-resource-telemetry.test 的实现文件。                                                                               |
| [bash-shutdown.test.ts](bash-shutdown.test.ts)                                                         | 不能在 Vitest worker 内验证保活：框架的 IPC/定时器会掩盖 Node 在 close 尚未完成时退出。                                 |
| [bash-startup-script.test.ts](bash-startup-script.test.ts)                                             | bash-startup-script.test 的实现文件。                                                                                   |
| [bash-tool-result-wire.test.ts](bash-tool-result-wire.test.ts)                                         | bash-tool-result-wire.test 的实现文件。                                                                                 |
| [browser.test.ts](browser.test.ts)                                                                     | browser.test 的实现文件。                                                                                               |
| [builtin-mcs-search-wire.test.ts](builtin-mcs-search-wire.test.ts)                                     | 本用例验证模型配置与 wire；安全端口注入离线透传，独立安全契约用例覆盖官方版本校验。                                     |
| [commands.test.ts](commands.test.ts)                                                                   | 仅保留未被禁用的命令；load 采用 discover 也应拒绝被禁用项                                                               |
| [config.test.ts](config.test.ts)                                                                       | config.test 的实现文件。                                                                                                |
| [connectivity-probe-wire.test.ts](connectivity-probe-wire.test.ts)                                     | 离线拦截所有请求，包含意外的鉴权/控制面请求；绝不回落真实账号网络。                                                     |
| [credential-access-lifecycle.test.ts](credential-access-lifecycle.test.ts)                             | 与 Host 的接收路径相同；超限回复不能被静默丢弃后挂起迁移。                                                              |
| [credential-recovery-fence.test.ts](credential-recovery-fence.test.ts)                                 | credential-recovery-fence.test 的实现文件。                                                                             |
| [credential-security-linux-fallback.test.ts](credential-security-linux-fallback.test.ts)               | 回退开关是进程级的：本文件独立运行（vitest 按文件隔离），模拟开启回退的 Linux Desktop Main。                            |
| [credential-security.test.ts](credential-security.test.ts)                                             | credential-security.test 的实现文件。                                                                                   |
| [dwf-journal-store.test.ts](dwf-journal-store.test.ts)                                                 | _ SQLite 版 JournalStorePort（dwf\__ 表）的测试。                                                                       |
| [embedded-search-prelude.test.ts](embedded-search-prelude.test.ts)                                     | embedded-search-prelude.test 的实现文件。                                                                               |
| [empty-reasoning-wire.test.ts](empty-reasoning-wire.test.ts)                                           | empty-reasoning-wire.test 的实现文件。                                                                                  |
| [empty-tool-name-projection.test.ts](empty-tool-name-projection.test.ts)                               | empty-tool-name-projection.test 的实现文件。                                                                            |
| [env-model-config.test.ts](env-model-config.test.ts)                                                   | env-model-config.test 的实现文件。                                                                                      |
| [exec.test.ts](exec.test.ts)                                                                           | exec.test 的实现文件。                                                                                                  |
| [failure-classifier.test.ts](failure-classifier.test.ts)                                               | failure-classifier.test 的实现文件。                                                                                    |
| [frozen-migration-startup.test.ts](frozen-migration-startup.test.ts)                                   | frozen-migration-startup.test 的实现文件。                                                                              |
| [fs-context.test.ts](fs-context.test.ts)                                                               | Bugfix: 这些测试可能从仓库根或 apps/zcode-cli 子工程启动；fixture 路径必须绑定到当前测试文件位置。                      |
| [fs-text-encoding.test.ts](fs-text-encoding.test.ts)                                                   | Bug 根因：旧实现将样本末尾的半个字符当成完整文件错误，导致拒读或误判为 legacy 编码。                                    |
| [git-snapshot-hardening.test.ts](git-snapshot-hardening.test.ts)                                       | 用真实 git 验证加固确实生效：仓库配置里的 fsmonitor 不再被 ZCode 自己执行，                                             |
| [git-snapshot.test.ts](git-snapshot.test.ts)                                                           | 没有 git 退出码的失败：timeout 被 kill、signal 取消、git 无法启动。                                                     |
| [goal-verifier-model-options.test.ts](goal-verifier-model-options.test.ts)                             | 捕获真实 Model 合并、校验之后的参数，而非仅观察 Factory 输入。                                                          |
| [http-cancellation.test.ts](http-cancellation.test.ts)                                                 | 固定 TLS 私钥会进入公开源码；临时生成测试密钥，仍走真实 HTTPS 与自定义 CA 验证。                                        |
| [http-response-status.test.ts](http-response-status.test.ts)                                           | 上游状态码不在 WHATWG `Response` 能表示的范围里时（docs/design/v2/model/http-proxy.md「行为」）。                       |
| [http.test.ts](http.test.ts)                                                                           | http.test 的实现文件。                                                                                                  |
| [image.test.ts](image.test.ts)                                                                         | image.test 的实现文件。                                                                                                 |
| [logging.test.ts](logging.test.ts)                                                                     | logging.test 的实现文件。                                                                                               |
| [markdown-frontmatter.test.ts](markdown-frontmatter.test.ts)                                           | Bugfix 回归：市场详情技能描述此前只剩一个 `>`。                                                                         |
| [marketplace-listing.test.ts](marketplace-listing.test.ts)                                             | 商店信息（Store Listing）与 featured 策展名单的解析测试：                                                               |
| [mcp-config-protocol-version.test.ts](mcp-config-protocol-version.test.ts)                             | mcp-config-protocol-version.test 的实现文件。                                                                           |
| [mcp-connection-pool.test.ts](mcp-connection-pool.test.ts)                                             | mcp-connection-pool.test 的实现文件。                                                                                   |
| [mcp-network.test.ts](mcp-network.test.ts)                                                             | mcp-network.test 的实现文件。                                                                                           |
| [mcp-node-fallback.test.ts](mcp-node-fallback.test.ts)                                                 | 测试机没有 Electron：用当前 Node 冒充“Electron 可执行文件”。shim 只关心它能执行 JS，                                    |
| [mcp-oauth-callback.test.ts](mcp-oauth-callback.test.ts)                                               | Bug 回归：陌生 state（并发事务、浏览器里残留的旧授权 URL）过去会 reject 本事务的                                        |
| [mcp-oauth-cross-process.e2e.test.ts](mcp-oauth-cross-process.e2e.test.ts)                             | \* 跨进程端到端验证:线上事故的竞态发生在多个真实 CLI 进程之间,同进程测试无法复现                                        |
| [mcp-oauth-lease.test.ts](mcp-oauth-lease.test.ts)                                                     | 起一个真实的长驻子进程，只为拿到一个确定存活、随后可被杀死的 PID。                                                      |
| [mcp-oauth-refresh.test.ts](mcp-oauth-refresh.test.ts)                                                 | 卡住 token 响应，直到 release() 被调用。用于构造 barrier。                                                              |
| [mcp-oauth.e2e.test.ts](mcp-oauth.e2e.test.ts)                                                         | mcp-oauth.e2e.test 的实现文件。                                                                                         |
| [mcp-official-auth-integration.test.ts](mcp-official-auth-integration.test.ts)                         | fake 官方 Plugin + fake Streamable HTTP MCP 的端到端验证。                                                              |
| [mcp-official-auth-stdio-meta.test.ts](mcp-official-auth-stdio-meta.test.ts)                           | OMCP-S01~S06 —— stdio 官方 MCP 的身份头随所有出站请求与通知的 `_meta` 下发                                              |
| [mcp-official-auth.test.ts](mcp-official-auth.test.ts)                                                 | 官方 MCP 逐请求动态身份头注入与失败分类。                                                                               |
| [mcp-process-lifecycle.test.ts](mcp-process-lifecycle.test.ts)                                         | mcp-process-lifecycle.test 的实现文件。                                                                                 |
| [mcp-resource-telemetry.test.ts](mcp-resource-telemetry.test.ts)                                       | mcp-resource-telemetry.test 的实现文件。                                                                                |
| [mcp-stdio-transport.test.ts](mcp-stdio-transport.test.ts)                                             | mcp-stdio-transport.test 的实现文件。                                                                                   |
| [mcp-telemetry-source.test.ts](mcp-telemetry-source.test.ts)                                           | mcp-telemetry-source.test 的实现文件。                                                                                  |
| [mcp-telemetry.test.ts](mcp-telemetry.test.ts)                                                         | mcp-telemetry.test 的实现文件。                                                                                         |
| [mcp-version-negotiation.test.ts](mcp-version-negotiation.test.ts)                                     | 飞书项目 MCP 的真实响应形状：对未知方法（server/discover probe）回 HTTP 200 +                                           |
| [mcp.test.ts](mcp.test.ts)                                                                             | \* 把 Phase 1 建连做成认证失败，并接管 Phase 2 的 `auth()`：调用 provider 的                                            |
| [memory-provider-body.test.ts](memory-provider-body.test.ts)                                           | memory-provider-body.test 的实现文件。                                                                                  |
| [mfjs-properties-wire.test.ts](mfjs-properties-wire.test.ts)                                           | 只抓出站载荷，明确终止；不消耗账号额度，也不伪造成功模型结果。                                                          |
| [migration-crash-recovery.test.ts](migration-crash-recovery.test.ts)                                   | migration-crash-recovery.test 的实现文件。                                                                              |
| [model-execution.test.ts](model-execution.test.ts)                                                     | model-execution.test 的实现文件。                                                                                       |
| [model-option-map-fetch.test.ts](model-option-map-fetch.test.ts)                                       | model-option-map-fetch.test 的实现文件。                                                                                |
| [model-output-tokens-wire.test.ts](model-output-tokens-wire.test.ts)                                   | 恢复 v0.16.6 的 wire 验收：通过真实 SDK 序列化检查相邻 user 合并后的准确文案和次数。                                    |
| [model-query-source-wire.test.ts](model-query-source-wire.test.ts)                                     | HEAD 实测：SDK 流式与非流式的大小写冲突结果不同，本功能只收口 query-source。                                            |
| [model-request-headers.test.ts](model-request-headers.test.ts)                                         | model-request-headers.test 的实现文件。                                                                                 |
| [model-request-security.test.ts](model-request-security.test.ts)                                       | model-request-security.test 的实现文件。                                                                                |
| [model-session-features-wire.test.ts](model-session-features-wire.test.ts)                             | 规格：docs/design/v2/model/session-features-header.md。经正式 SDK 发出的 HTTP 请求验证。                                |
| [model-tool-error-transform.test.ts](model-tool-error-transform.test.ts)                               | core 把提醒以空行接在失败结果的字符串后面；error-text 必须原样带上，不能只留错误本身。                                  |
| [model-transform-deepseek-anthropic.test.ts](model-transform-deepseek-anthropic.test.ts)               | model-transform-deepseek-anthropic.test 的实现文件。                                                                    |
| [model-transform-tool-media.test.ts](model-transform-tool-media.test.ts)                               | model-transform-tool-media.test 的实现文件。                                                                            |
| [model-transform.test.ts](model-transform.test.ts)                                                     | model-transform.test 的实现文件。                                                                                       |
| [model.test.ts](model.test.ts)                                                                         | 测试夹具必须显式绑定执行预算，不能借已删除的 Option Spec default 偷渡请求值。                                           |
| [native-system-message-boundaries-wire.test.ts](native-system-message-boundaries-wire.test.ts)         | native-system-message-boundaries-wire.test 的实现文件。                                                                 |
| [network-capture.test.ts](network-capture.test.ts)                                                     | network-capture.test 的实现文件。                                                                                       |
| [new-model-round2-wire.test.ts](new-model-round2-wire.test.ts)                                         | new-model-round2-wire.test 的实现文件。                                                                                 |
| [new-model-wire.test.ts](new-model-wire.test.ts)                                                       | 厂商的无预算 enabled 不能穿透到 OpenRouter；验证最终 SDK wire 而非只编译 Map。                                          |
| [off-peak-request-auth-refresh.test.ts](off-peak-request-auth-refresh.test.ts)                         | 将测试依赖在文件加载阶段准备好，断言只测每次请求刷新，不包含冷加载耗时。                                                |
| [official-coding-plan-gateway.test.ts](official-coding-plan-gateway.test.ts)                           | official-coding-plan-gateway.test 的实现文件。                                                                          |
| [official-glm-selection-migration.test.ts](official-glm-selection-migration.test.ts)                   | official-glm-selection-migration.test 的实现文件。                                                                      |
| [official-marketplace.test.ts](official-marketplace.test.ts)                                           | 根已存在；让 admission 前的元数据步骤立即完成，以受控 Promise 决定 writer 顺序。                                        |
| [offpeak-retry.test.ts](offpeak-retry.test.ts)                                                         | off-peak 排队协议：429/3105 豁免重试预算；3102/3106 保留原码并通知 Host 结束任务。                                      |
| [openai-compatible-empty-user-wire.test.ts](openai-compatible-empty-user-wire.test.ts)                 | openai-compatible-empty-user-wire.test 的实现文件。                                                                     |
| [openai-compatible-extra-body-wire.test.ts](openai-compatible-extra-body-wire.test.ts)                 | openai-compatible-extra-body-wire.test 的实现文件。                                                                     |
| [openai-compatible-stream-usage-wire.test.ts](openai-compatible-stream-usage-wire.test.ts)             | 修复原因：此断言遗漏了旧 Registry 测试替身迁移；保持真实请求和 raw reason 断言不变。                                    |
| [openai-compatible-system-messages-wire.test.ts](openai-compatible-system-messages-wire.test.ts)       | openai-compatible-system-messages-wire.test 的实现文件。                                                                |
| [openai-responses-json-compat.test.ts](openai-responses-json-compat.test.ts)                           | openai-responses-json-compat.test 的实现文件。                                                                          |
| [opencode-go-wire.test.ts](opencode-go-wire.test.ts)                                                   | 每种 Go 映射走正式 SDK / transport；只截获假 Key 请求，不消耗用户额度。                                                 |
| [output-collector-tail.test.ts](output-collector-tail.test.ts)                                         | \* 请求级尾部（`ExecutionOutputLimit.tailBytes` → `ExecutionStreamResult.tail`）。                                      |
| [pdf.test.ts](pdf.test.ts)                                                                             | pdf.test 的实现文件。                                                                                                   |
| [permission-full-access.test.ts](permission-full-access.test.ts)                                       | permission-full-access.test 的实现文件。                                                                                |
| [plugin-mcp-always-load.test.ts](plugin-mcp-always-load.test.ts)                                       | plugin-mcp-always-load.test 的实现文件。                                                                                |
| [plugin-mcp-isolation.test.ts](plugin-mcp-isolation.test.ts)                                           | 只有官方市场插件能声明工作区共享 server（文档插件查看面板 spec §8）；                                                   |
| [plugin-mcp-tool-search-wire.test.ts](plugin-mcp-tool-search-wire.test.ts)                             | plugin-mcp-tool-search-wire.test 的实现文件。                                                                           |
| [plugin-official-mcp-auth.test.ts](plugin-official-mcp-auth.test.ts)                                   | OMCP-001/002/007/018/020 —— Plugin loader 对 zcode_official 的严格解析（spec §4.2 / §5.2）。                            |
| [plugins.test.ts](plugins.test.ts)                                                                     | plugins.test 的实现文件。                                                                                               |
| [process-probe.test.ts](process-probe.test.ts)                                                         | macOS `ps -eo pid=,ppid=,rss=,cputime=` 的典型输出：100 → 101 → 102 一棵树，200、300 各自独立。                         |
| [project-token-cancellation.test.ts](project-token-cancellation.test.ts)                               | project-token-cancellation.test 的实现文件。                                                                            |
| [project-token-cold-recovery.test.ts](project-token-cold-recovery.test.ts)                             | project-token-cold-recovery.test 的实现文件。                                                                           |
| [project-token-refresh.test.ts](project-token-refresh.test.ts)                                         | ZCT-2111046389485834240：最终失败保留固定类别；未分类的 HttpClientPort 错误仍归 request_failed。                        |
| [project-token-request-auth.test.ts](project-token-request-auth.test.ts)                               | 旧夹具依赖不完整凭据绕过校验；此处注入中性端口，安全合同由独立用例验证。                                                |
| [project-token-retry.test.ts](project-token-retry.test.ts)                                             | project-token-retry.test 的实现文件。                                                                                   |
| [project-token-runner-recovery.test.ts](project-token-runner-recovery.test.ts)                         | project-token-runner-recovery.test 的实现文件。                                                                         |
| [provider-builtin-tool-rounds-fixture.ts](provider-builtin-tool-rounds-fixture.ts)                     | 服务端内置工具（analyze_image）多轮回放：真实 GLM 流（脱敏 fixture）经 compat → AI SDK → Runtime，                      |
| [provider-builtin-tool-rounds.test.ts](provider-builtin-tool-rounds.test.ts)                           | 服务端内置工具（analyze_image）多轮回放：真实 GLM 流（脱敏 fixture）经 compat → AI SDK → Runtime，                      |
| [provider-config-model-creation.test.ts](provider-config-model-creation.test.ts)                       | provider-config-model-creation.test 的实现文件。                                                                        |
| [provider-database-migration.test.ts](provider-database-migration.test.ts)                             | 直接播种发布格式，不能先过新版 Writer 再冒充旧数据。                                                                    |
| [provider-endpoint-routing-fetch.test.ts](provider-endpoint-routing-fetch.test.ts)                     | provider-endpoint-routing-fetch.test 的实现文件。                                                                       |
| [README.md](README.md)                                                                                 | 本目录用途、子目录与逐文件说明。                                                                                        |
| [reasoning-history-normalization.test.ts](reasoning-history-normalization.test.ts)                     | 删除回复只在 core 投影的第一步做；adapter 删掉会让 core 放好的 system 直接接 user。                                     |
| [reasoning-provider-compatibility.test.ts](reasoning-provider-compatibility.test.ts)                   | reasoning-provider-compatibility.test 的实现文件。                                                                      |
| [request-capabilities.test.ts](request-capabilities.test.ts)                                           | request-capabilities.test 的实现文件。                                                                                  |
| [retry-budget.test.ts](retry-budget.test.ts)                                                           | docs/dynamic-workflow/concurrency.md「Unbounded retries for workflow traffic」：unbounded 只放宽瞬态失败的放弃条件，    |
| [runner-admission.test.ts](runner-admission.test.ts)                                                   | 旧 adapter 直接返回 AsyncIterableIterator；夹具返回 AsyncIterable，这里取它的迭代器以逐步驱动。                         |
| [runner-debug-failed-stream.test.ts](runner-debug-failed-stream.test.ts)                               | 回归（2026-07-06，v4 stop 失效根因）：用户 stop / sendQueuedNow 抢占 abort 流式请求后，                                 |
| [runner-debug-media-redaction.test.ts](runner-debug-media-redaction.test.ts)                           | P1 回归：image/video dataUrl 不得全量落 model-io。                                                                      |
| [runner-empty-completion-finish.test.ts](runner-empty-completion-finish.test.ts)                       | runner-empty-completion-finish.test 的实现文件。                                                                        |
| [runner-empty-delta-retry.test.ts](runner-empty-delta-retry.test.ts)                                   | runner-empty-delta-retry.test 的实现文件。                                                                              |
| [runner-network-headers.test.ts](runner-network-headers.test.ts)                                       | runner-network-headers.test 的实现文件。                                                                                |
| [runner-options.test.ts](runner-options.test.ts)                                                       | runner-options.test 的实现文件。                                                                                        |
| [runner-provider-business-network.test.ts](runner-provider-business-network.test.ts)                   | runner-provider-business-network.test 的实现文件。                                                                      |
| [runner-retry.test.ts](runner-retry.test.ts)                                                           | 修复原因：同一批被限流的请求拿到同一个 retry-after，不加抖动会在同一毫秒一起醒来再撞限流。                              |
| [runner-status-fanout.test.ts](runner-status-fanout.test.ts)                                           | runner-status-fanout.test 的实现文件。                                                                                  |
| [runner-status-session-type.test.ts](runner-status-session-type.test.ts)                               | runner-status-session-type.test 的实现文件。                                                                            |
| [runner-stream-timing-wire.test.ts](runner-stream-timing-wire.test.ts)                                 | runner-stream-timing-wire.test 的实现文件。                                                                             |
| [runner.test.ts](runner.test.ts)                                                                       | runner.test 的实现文件。                                                                                                |
| [runtime-reasoning-provider-replay.test.ts](runtime-reasoning-provider-replay.test.ts)                 | 合并修复：空库建表后移除尚未播种的迁移记录，模拟升级前数据；只操作临时夹具。                                            |
| [session-data-files.test.ts](session-data-files.test.ts)                                               | 已删除的会话再次删除返回 0，不报错。                                                                                    |
| [session-database-identity-migration.test.ts](session-database-identity-migration.test.ts)             | Agent 更早的迁移也在同一事务内回滚，损坏记录不会被覆盖。                                                                |
| [session-mailbox.test.ts](session-mailbox.test.ts)                                                     | session-mailbox.test 的实现文件。                                                                                       |
| [session-migration-boundaries.test.ts](session-migration-boundaries.test.ts)                           | 前序迁移必须经 runner 回放：0022 的 SQL JOIN schema_migration 读取 0020 的记账时间，                                    |
| [session-model-selection-migration.test.ts](session-model-selection-migration.test.ts)                 | 此夹具只用新版建空表；删除尚未播种数据的 0020 记录，模拟升级前库。                                                      |
| [session-reasoning-repair-migration.test.ts](session-reasoning-repair-migration.test.ts)               | session-reasoning-repair-migration.test 的实现文件。                                                                    |
| [session-recency.test.ts](session-recency.test.ts)                                                     | session-recency.test 的实现文件。                                                                                       |
| [session-store-compact-bundle.test.ts](session-store-compact-bundle.test.ts)                           | 空闲整批通知一条消息多个文本 part，同一毫秒内 part id 的随机段不保证顺序；读回必须按写入顺序。                          |
| [session-store-fork-source.test.ts](session-store-fork-source.test.ts)                                 | session-store-fork-source.test 的实现文件。                                                                             |
| [session-store-model-selection-codec.test.ts](session-store-model-selection-codec.test.ts)             | session-store-model-selection-codec.test 的实现文件。                                                                   |
| [session-store-permanent-deletion.test.ts](session-store-permanent-deletion.test.ts)                   | 固定已发布 SQL 的摘要，防止测试夹具随实现一起变化而漏掉旧库 checksum 不兼容。                                           |
| [session-store-transaction-isolation.test.ts](session-store-transaction-isolation.test.ts)             | session-store-transaction-isolation.test 的实现文件。                                                                   |
| [session-store-transaction-writers.test.ts](session-store-transaction-writers.test.ts)                 | BigInt 无法序列化：在事务内、已有写入之后失败并回滚。                                                                   |
| [session-store.test.ts](session-store.test.ts)                                                         | 五轮真实进程冷启动的加载时间已接近十秒，整组预算按轮数计算，避免把加载耗时误报为迁移失败。                              |
| [shell-init-snapshot-cleanup.test.ts](shell-init-snapshot-cleanup.test.ts)                             | shell-init-snapshot-cleanup.test 的实现文件。                                                                           |
| [shell-init-snapshot.test.ts](shell-init-snapshot.test.ts)                                             | shell-init-snapshot.test 的实现文件。                                                                                   |
| [skills.test.ts](skills.test.ts)                                                                       | 仅保留未被禁用的 skill；load 采用 discover 也应拒绝被禁用项                                                             |
| [stdio-transport.test.ts](stdio-transport.test.ts)                                                     | stdio-transport.test 的实现文件。                                                                                       |
| [streaming-migration-backup.test.ts](streaming-migration-backup.test.ts)                               | streaming-migration-backup.test 的实现文件。                                                                            |
| [strict-tool-schema.test.ts](strict-tool-schema.test.ts)                                               | Anthropic strict 工具 schema：资格判定 + 子集折叠                                                                       |
| [task-output-wire.test.ts](task-output-wire.test.ts)                                                   | task-output-wire.test 的实现文件。                                                                                      |
| [test-adapter-model.ts](test-adapter-model.ts)                                                         | 准入端口与重试预算（docs/dynamic-workflow/concurrency.md「Where the port is bound」）同样经调用上下文到 runner。        |
| [test-model-format.ts](test-model-format.ts)                                                           | 实现或公开接口：createTestInputFormat、createTestModelProperties。                                                      |
| [test-provider-config.ts](test-provider-config.ts)                                                     | \* 仅供旧 Adapter 行为测试组织多组输入数据。                                                                            |
| [tool-artifact-store.test.ts](tool-artifact-store.test.ts)                                             | tool-artifact-store.test 的实现文件。                                                                                   |
| [tool-input-normalization.test.ts](tool-input-normalization.test.ts)                                   | tool-input-normalization.test 的实现文件。                                                                              |
| [tool-result-cache-wire.test.ts](tool-result-cache-wire.test.ts)                                       | tool-result-cache-wire.test 的实现文件。                                                                                |
| [tool-search-capability.test.ts](tool-search-capability.test.ts)                                       | tool-search-capability.test 的实现文件。                                                                                |
| [tool-search-mcp.test.ts](tool-search-mcp.test.ts)                                                     | tool-search-mcp.test 的实现文件。                                                                                       |
| [tool-search-wire.test.ts](tool-search-wire.test.ts)                                                   | tool-search-wire.test 的实现文件。                                                                                      |
| [tool-transform.test.ts](tool-transform.test.ts)                                                       | Model Tool Transform Tests                                                                                              |
| [usage-query.test.ts](usage-query.test.ts)                                                             | 两条 model_usage 落在两个不同的本地日                                                                                   |
| [version-compare.test.ts](version-compare.test.ts)                                                     | Version axis: only when the manifest (latest) advertises a semver version.                                              |
| [video-wire.test.ts](video-wire.test.ts)                                                               | video 输入的 wire 形状测试：                                                                                            |
| [websearch.test.ts](websearch.test.ts)                                                                 | Internal Provider-Native WebSearch Model Tool Tests                                                                     |
| [windows-job-object.test.ts](windows-job-object.test.ts)                                               | 子进程已被 Job 或测试主体回收。                                                                                         |
| [workflow-model-failure-policy.test.ts](workflow-model-failure-policy.test.ts)                         | apps/zcode-cli/packages/dynamic-workflow/docs/execution-engine.md「Terminal states」：Stop 集逐行一例，其余一切 retry。 |
| [workflow-store.test.ts](workflow-store.test.ts)                                                       | workflow-store.test 的实现文件。                                                                                        |
| [workspace-hook-digest-parity.test.ts](workspace-hook-digest-parity.test.ts)                           | \* D17/M2 双 builder parity（Runtime 侧真实入口版）：                                                                   |
| [workspace-hook-trust-identity.test.ts](workspace-hook-trust-identity.test.ts)                         | Hook Trust identity 的 CLI adapter（docs/specs/workspace-hook-trust.md D23）。                                          |
| [workspace-hook-trust-phase0.test.ts](workspace-hook-trust-phase0.test.ts)                             | workspace-hook-trust-phase0.test 的实现文件。                                                                           |
| [workspace-hook-trust-phase1.test.ts](workspace-hook-trust-phase1.test.ts)                             | workspace-hook-trust-phase1.test 的实现文件。                                                                           |
| [workspace-hook-trust-store-lock-ownership.test.ts](workspace-hook-trust-store-lock-ownership.test.ts) | \* 锁所有权与 stale 回收（CR-02 回归）。                                                                                |
| [workspace-hook-trust-store.test.ts](workspace-hook-trust-store.test.ts)                               | workspace-hook-trust-store.test 的实现文件。                                                                            |
| [zai-business-token-cache.test.ts](zai-business-token-cache.test.ts)                                   | zai-business-token-cache.test 的实现文件。                                                                              |
| [zai-business-token-refresh-fixture.ts](zai-business-token-refresh-fixture.ts)                         | 实现或公开接口：fixture。                                                                                               |
| [zai-business-token-refresh.test.ts](zai-business-token-refresh.test.ts)                               | zai-business-token-refresh.test 的实现文件。                                                                            |

<!-- qingqi-directory-index:end -->
