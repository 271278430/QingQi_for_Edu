# specs

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

specs 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                                                                                           | 简要说明                                                                     |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [2026-03-31-bigmodel-oauth-login-design.md](2026-03-31-bigmodel-oauth-login-design.md)                                                         | BigModel OAuth 登录设计：说明文档。                                          |
| [2026-04-01-first-run-default-project-design.md](2026-04-01-first-run-default-project-design.md)                                               | 启动时自动兜底非项目对话工作区（已替代默认项目）：说明文档。                 |
| [2026-04-27-zai-backend-oauth-token-design.md](2026-04-27-zai-backend-oauth-token-design.md)                                                   | ZAI 后端 OAuth Token 改造设计：说明文档。                                    |
| [2026-04-28-web-remote-login-design.md](2026-04-28-web-remote-login-design.md)                                                                 | Web 远控页面登录校验设计：说明文档。                                         |
| [2026-04-28-window-level-web-remote-control-design.md](2026-04-28-window-level-web-remote-control-design.md)                                   | 窗口级 Web 远程控制设计：说明文档。                                          |
| [2026-06-01-dep-refs-design.md](2026-06-01-dep-refs-design.md)                                                                                 | dep-refs：变量级 export 引用查询脚本：说明文档。                             |
| [2026-06-02-app-usage-db-migration-design.md](2026-06-02-app-usage-db-migration-design.md)                                                     | 应用用量改造：数据源迁移到 zcode agent 数据库：说明文档。                    |
| [2026-06-03-model-provider-catalog-metadata-design.md](2026-06-03-model-provider-catalog-metadata-design.md)                                   | Model Provider Catalog And Metadata Design：说明文档。                       |
| [2026-06-03-remove-long-running-terminal-panel-design.md](2026-06-03-remove-long-running-terminal-panel-design.md)                             | 移除「运行中终端」面板设计：说明文档。                                       |
| [2026-06-04-model-provider-endpoint-path-editing-design.md](2026-06-04-model-provider-endpoint-path-editing-design.md)                         | Model Provider Endpoint Path Editing Design：说明文档。                      |
| [2026-06-04-model-provider-model-editor-design.md](2026-06-04-model-provider-model-editor-design.md)                                           | Model Provider Model Editor Design：说明文档。                               |
| [2026-06-04-web-remote-test-static-deployment-design.md](2026-06-04-web-remote-test-static-deployment-design.md)                               | Web Remote Test 静态资源部署设计：说明文档。                                 |
| [2026-06-04-web-remote-v3-static-deployment-design.md](2026-06-04-web-remote-v3-static-deployment-design.md)                                   | Web Remote v3 静态资源并行部署设计：说明文档。                               |
| [2026-06-08-glm-responses-model-selection-design.md](2026-06-08-glm-responses-model-selection-design.md)                                       | GLM Responses Model Selection Design：说明文档。                             |
| [2026-06-09-agent-model-request-session-header-design.md](2026-06-09-agent-model-request-session-header-design.md)                             | Agent 模型请求归因 Header：说明文档。                                        |
| [2026-06-09-mobile-composer-model-label-design.md](2026-06-09-mobile-composer-model-label-design.md)                                           | Mobile Composer Model Label Design：说明文档。                               |
| [2026-06-10-agent-auto-compact-output-reserve-design.md](2026-06-10-agent-auto-compact-output-reserve-design.md)                               | Agent Auto Compact Output Reserve Design：说明文档。                         |
| [2026-06-10-agent-query-id-design.md](2026-06-10-agent-query-id-design.md)                                                                     | Agent Query ID 设计：说明文档。                                              |
| [2026-06-10-app-request-id-header.md](2026-06-10-app-request-id-header.md)                                                                     | App 网络请求 Request ID Header：说明文档。                                   |
| [2026-06-10-bot-state-cache-v2-migration-design.md](2026-06-10-bot-state-cache-v2-migration-design.md)                                         | Bot State/Cache V2 迁移设计：说明文档。                                      |
| [2026-06-10-glm-52-hide-high-thought-level-design.md](2026-06-10-glm-52-hide-high-thought-level-design.md)                                     | GLM-5.2 Default Max Thought Level：说明文档。                                |
| [2026-06-10-hide-runtime-model-unavailable-banner-design.md](2026-06-10-hide-runtime-model-unavailable-banner-design.md)                       | Hide Runtime Model Unavailable Banner Design：说明文档。                     |
| [2026-06-10-model-switch-context-window-guard-design.md](2026-06-10-model-switch-context-window-guard-design.md)                               | Model Switch Context Window Guard Design：说明文档。                         |
| [2026-06-11-browser-empty-state-compact-style.md](2026-06-11-browser-empty-state-compact-style.md)                                             | Browser Empty State Compact Style：说明文档。                                |
| [2026-06-11-context-usage-breakdown-bar.md](2026-06-11-context-usage-breakdown-bar.md)                                                         | Context Usage Breakdown Bar：说明文档。                                      |
| [2026-06-11-docker-container-select-refresh-design.md](2026-06-11-docker-container-select-refresh-design.md)                                   | Docker Container Select Refresh Design：说明文档。                           |
| [2026-06-11-side-pane-tab-overview-position.md](2026-06-11-side-pane-tab-overview-position.md)                                                 | Side Pane Tab Overview Entry Position：说明文档。                            |
| [2026-06-11-start-plan-preview-entitlements.md](2026-06-11-start-plan-preview-entitlements.md)                                                 | Start Plan Preview Entitlements：说明文档。                                  |
| [2026-06-12-coding-plan-billing-discount.md](2026-06-12-coding-plan-billing-discount.md)                                                       | Coding Plan 限时配额活动提示：说明文档。                                     |
| [2026-06-14-anthropic-thinking-max-output-budget.md](2026-06-14-anthropic-thinking-max-output-budget.md)                                       | Anthropic Thinking Max Output Budget：说明文档。                             |
| [2026-06-15-coding-plan-card-renew-time.md](2026-06-15-coding-plan-card-renew-time.md)                                                         | Coding Plan Plan Card Renew Time：说明文档。                                 |
| [2026-06-15-goal-mention-node-icon.md](2026-06-15-goal-mention-node-icon.md)                                                                   | Goal Mention Node Icon：说明文档。                                           |
| [2026-06-16-local-remote-asset-archive-design.md](2026-06-16-local-remote-asset-archive-design.md)                                             | Local Remote Asset Archive Design：说明文档。                                |
| [2026-06-16-ui-perf-arms-telemetry-design.md](2026-06-16-ui-perf-arms-telemetry-design.md)                                                     | 端侧 UI 性能 ARMS 上报设计：说明文档。                                       |
| [2026-06-17-feedback-tickets-back-button-design.md](2026-06-17-feedback-tickets-back-button-design.md)                                         | 我的反馈返回按钮设计：说明文档。                                             |
| [2026-06-17-issue-report-auto-screenshot-design.md](2026-06-17-issue-report-auto-screenshot-design.md)                                         | 问题上报自动截图设计：说明文档。                                             |
| [2026-06-17-launch-to-input-telemetry-design.md](2026-06-17-launch-to-input-telemetry-design.md)                                               | 桌面端「应用启动 → 能输入」分阶段耗时埋点设计：说明文档。                    |
| [2026-06-18-goal-manual-review-case-coverage.md](2026-06-18-goal-manual-review-case-coverage.md)                                               | Goal Manual Review Case Coverage：说明文档。                                 |
| [2026-06-22-queued-prompt-panel-blur-style.md](2026-06-22-queued-prompt-panel-blur-style.md)                                                   | Queued Prompt Panel Blur Style：说明文档。                                   |
| [2026-06-22-superpowers-zcode-p0-compat.md](2026-06-22-superpowers-zcode-p0-compat.md)                                                         | Superpowers ZCode P0 兼容规范：说明文档。                                    |
| [2026-06-22-task-list-permission-pill-style.md](2026-06-22-task-list-permission-pill-style.md)                                                 | Task List Permission Pill Style：说明文档。                                  |
| [2026-06-23-arms-user-id-design.md](2026-06-23-arms-user-id-design.md)                                                                         | ARMS RUM user.id 注入登录账号 userId — 设计：说明文档。                      |
| [2026-06-23-task-restore-model-list-fallback-design.md](2026-06-23-task-restore-model-list-fallback-design.md)                                 | Task Restore Model List Fallback Design：说明文档。                          |
| [2026-06-23-web-replayable-task-model-readonly-restore-design.md](2026-06-23-web-replayable-task-model-readonly-restore-design.md)             | Web Replayable Task Model Readonly Restore Design：说明文档。                |
| [2026-06-24-mention-panel-folder-icon.md](2026-06-24-mention-panel-folder-icon.md)                                                             | Mention Panel Folder Entries：说明文档。                                     |
| [2026-06-25-input-lag-telemetry-design.md](2026-06-25-input-lag-telemetry-design.md)                                                           | 输入框卡顿埋点设计(perf_ui_input_lag)：说明文档。                            |
| [2026-06-25-openrouter-attribution-headers.md](2026-06-25-openrouter-attribution-headers.md)                                                   | OpenRouter Attribution Headers：说明文档。                                   |
| [2026-06-25-plugin-bundled-agents-discovery-design.md](2026-06-25-plugin-bundled-agents-discovery-design.md)                                   | 插件 Agent 发现（plugin-bundled agents discovery）— 设计：说明文档。         |
| [2026-06-26-compact-disable-thinking-flag.md](2026-06-26-compact-disable-thinking-flag.md)                                                     | Compact Thinking Control：说明文档。                                         |
| [2026-06-27-agent-model-runtime-platform-headers.md](2026-06-27-agent-model-runtime-platform-headers.md)                                       | Agent Model Runtime Platform Headers：说明文档。                             |
| [2026-06-27-bundled-skill-english-i18n.md](2026-06-27-bundled-skill-english-i18n.md)                                                           | `/` 与 `$` 面板内置 Skill 中英描述：说明文档。                               |
| [2026-06-27-settings-plugins-stable-subagents-emphasis.md](2026-06-27-settings-plugins-stable-subagents-emphasis.md)                           | Settings Plugins Stable Status and Subagents Scope Emphasis：说明文档。      |
| [2026-06-29-builtin-plugin-uninstall-and-update-design.md](2026-06-29-builtin-plugin-uninstall-and-update-design.md)                           | Built-in Plugin Uninstall & Plugin Update — Design：说明文档。               |
| [2026-06-29-remote-skill-sync-design.md](2026-06-29-remote-skill-sync-design.md)                                                               | SSH 远程 Skills 同步设计：说明文档。                                         |
| [2026-06-29-zcode-cli-default-reasoning-families-design.md](2026-06-29-zcode-cli-default-reasoning-families-design.md)                         | zcode-cli 默认思考强度族补全设计：说明文档。                                 |
| [2026-07-01-anthropic-authorization-header.md](2026-07-01-anthropic-authorization-header.md)                                                   | Anthropic Authorization Header：说明文档。                                   |
| [2026-07-02-agent-step-message-scope-e2e-design.md](2026-07-02-agent-step-message-scope-e2e-design.md)                                         | Agent Step Message Scope E2E Design：说明文档。                              |
| [2026-07-03-permission-waiting-telemetry-design.md](2026-07-03-permission-waiting-telemetry-design.md)                                         | Permission Waiting Telemetry 设计：说明文档。                                |
| [2026-07-03-remote-mcp-sync-design.md](2026-07-03-remote-mcp-sync-design.md)                                                                   | SSH 远程 MCP 同步设计：说明文档。                                            |
| [2026-07-06-remote-plugin-sync-design.md](2026-07-06-remote-plugin-sync-design.md)                                                             | SSH 远端 Plugin 同步设计：说明文档。                                         |
| [2026-07-08-fork-session-title-design.md](2026-07-08-fork-session-title-design.md)                                                             | Fork Session Title Design：说明文档。                                        |
| [2026-07-10-glm-52-suffixed-variant-media-fallback-design.md](2026-07-10-glm-52-suffixed-variant-media-fallback-design.md)                     | GLM-5.2 Suffixed Variant Media Fallback：说明文档。                          |
| [2026-07-10-non-project-conversation-workspace-design.md](2026-07-10-non-project-conversation-workspace-design.md)                             | 非项目对话工作区设计：说明文档。                                             |
| [2026-07-10-web-remote-control-favicon-design.md](2026-07-10-web-remote-control-favicon-design.md)                                             | Web Remote Control 浏览器标签图标设计：说明文档。                            |
| [2026-07-11-openai-compatible-extra-body-minimal-unwrapping-design.md](2026-07-11-openai-compatible-extra-body-minimal-unwrapping-design.md)   | OpenAI-compatible reasoning canonical request fields：说明文档。             |
| [2026-07-11-openai-responses-nonstream-json-compat-design.md](2026-07-11-openai-responses-nonstream-json-compat-design.md)                     | OpenAI Responses 非流式 JSON 最小兼容设计：说明文档。                        |
| [2026-07-12-feedback-base-service-boundary-design.md](2026-07-12-feedback-base-service-boundary-design.md)                                     | SSH 断连场景反馈服务边界设计：说明文档。                                     |
| [2026-07-13-background-result-title-and-navigator-design.md](2026-07-13-background-result-title-and-navigator-design.md)                       | 后台结果标题与真实用户轮次目录设计：说明文档。                               |
| [2026-07-13-bash-command-permission-registry-design.md](2026-07-13-bash-command-permission-registry-design.md)                                 | Bash Command Permission Registry Design：说明文档。                          |
| [2026-07-13-v4-sidebar-task-state-authority-design.md](2026-07-13-v4-sidebar-task-state-authority-design.md)                                   | V4 左侧任务状态权威收敛设计：说明文档。                                      |
| [2026-07-13-window-scoped-ssh-remote-host-pooling-design.md](2026-07-13-window-scoped-ssh-remote-host-pooling-design.md)                       | 窗口级 SSH Remote Host 共享设计：说明文档。                                  |
| [2026-07-14-wsl-remote-sync-design.md](2026-07-14-wsl-remote-sync-design.md)                                                                   | WSL 远端同步入口设计：说明文档。                                             |
| [2026-07-15-compact-stream-first-nonstream-fallback-design.md](2026-07-15-compact-stream-first-nonstream-fallback-design.md)                   | Compact Stream-first → Non-stream Fallback 设计：说明文档。                  |
| [2026-07-15-sqlite-concurrent-agent-startup-design.md](2026-07-15-sqlite-concurrent-agent-startup-design.md)                                   | SQLite 多 Agent 并发启动设计：说明文档。                                     |
| [2026-07-17-e2e-direct-failure-repairs-design.md](2026-07-17-e2e-direct-failure-repairs-design.md)                                             | 11 个可直接修复 E2E 失败修复设计：说明文档。                                 |
| [2026-07-17-kimi-k3-model-adapter-design.md](2026-07-17-kimi-k3-model-adapter-design.md)                                                       | Kimi K3 模型适配设计：说明文档。                                             |
| [2026-07-19-wsl-remote-process-cleanup-design.md](2026-07-19-wsl-remote-process-cleanup-design.md)                                             | WSL 远程进程确定性回收设计：说明文档。                                       |
| [2026-07-20-selected-key-migration-e2e-network-isolation-design.md](2026-07-20-selected-key-migration-e2e-network-isolation-design.md)         | SelectedKey Migration E2E Network Isolation Design：说明文档。               |
| [2026-07-20-sidebar-task-row-authority-design.md](2026-07-20-sidebar-task-row-authority-design.md)                                             | 左侧任务行存在权威收敛设计：说明文档。                                       |
| [2026-07-20-window-scoped-wsl-host-pooling-design.md](2026-07-20-window-scoped-wsl-host-pooling-design.md)                                     | 窗口级 WSL Remote Host 共享与资源生命周期设计：说明文档。                    |
| [2026-07-21-bg26-consecutive-429-lifecycle-design.md](2026-07-21-bg26-consecutive-429-lifecycle-design.md)                                     | BG26 429 Failure Projection Isolation Design：说明文档。                     |
| [2026-07-21-desktop-e2e-runtime-paths-design.md](2026-07-21-desktop-e2e-runtime-paths-design.md)                                               | Desktop E2E Runtime Paths Design：说明文档。                                 |
| [2026-07-21-openai-compatible-leading-system-merge-design.md](2026-07-21-openai-compatible-leading-system-merge-design.md)                     | OpenAI-compatible 前置 system message 合并设计：说明文档。                   |
| [2026-07-23-browser-background-screenshot-surface-design.md](2026-07-23-browser-background-screenshot-surface-design.md)                       | 内置浏览器后台 Tab 截图表面同步设计：说明文档。                              |
| [2026-07-24-browser-screenshot-negative-zoom-design.md](2026-07-24-browser-screenshot-negative-zoom-design.md)                                 | Windows 负缩放与 Fit 下 Browser Use 截图 raster surface 修复设计：说明文档。 |
| [2026-07-28-windows-cua-development-runtime-design.md](2026-07-28-windows-cua-development-runtime-design.md)                                   | Windows CUA 源码开发运行时设计：说明文档。                                   |
| [2026-07-29-windows-cua-native-clipboard-design.md](2026-07-29-windows-cua-native-clipboard-design.md)                                         | Windows CUA 原生文本剪贴板设计：说明文档。                                   |
| [2026-07-29-windows-cua-pointer-foundation-design.md](2026-07-29-windows-cua-pointer-foundation-design.md)                                     | Windows CUA 完整指针与虚拟桌面基础设计：说明文档。                           |
| [2026-07-29-windows-cua-tool-call-and-app-launch-reliability-design.md](2026-07-29-windows-cua-tool-call-and-app-launch-reliability-design.md) | Windows CUA 工具调用与应用启动可靠性设计：说明文档。                         |
| [2026-07-29-windows-cua-wgc-visual-capture-design.md](2026-07-29-windows-cua-wgc-visual-capture-design.md)                                     | Windows CUA WGC 视觉捕获设计：说明文档。                                     |
| [2026-08-04-cross-workspace-session-mention-design.md](2026-08-04-cross-workspace-session-mention-design.md)                                   | `#` 跨 Workspace 对话 Mention：说明文档。                                    |
| [2026-08-04-windows-cua-operation-indicator-design.md](2026-08-04-windows-cua-operation-indicator-design.md)                                   | Windows CUA 顶部操作提示设计：说明文档。                                     |
| [2026-08-04-windows-cua-upstream-main-forward-port-design.md](2026-08-04-windows-cua-upstream-main-forward-port-design.md)                     | Windows CUA 基于上游 Main 的正向迁移设计：说明文档。                         |
| [2026-08-06-windows-computer-use-settings-design.md](2026-08-06-windows-computer-use-settings-design.md)                                       | Windows 电脑控制设置设计：说明文档。                                         |
| [2026-08-07-dev-cua-sharp-reseed-design.md](2026-08-07-dev-cua-sharp-reseed-design.md)                                                         | Dev CUA Sharp Reseed Design：说明文档。                                      |
| [2026-08-07-workspace-file-search-default-filter-design.md](2026-08-07-workspace-file-search-default-filter-design.md)                         | Workspace 文件搜索默认过滤器：说明文档。                                     |
| [2026-08-14-background-task-posix-process-tree-stop.md](2026-08-14-background-task-posix-process-tree-stop.md)                                 | Background Task POSIX Process Tree Stop：说明文档。                          |
| [2026-08-14-cua-final-raster-integrity-contract.md](2026-08-14-cua-final-raster-integrity-contract.md)                                         | CUA 最终图像与像素坐标完整性契约：说明文档。                                 |
| [2026-08-14-glm-5-3-model-adapter-design.md](2026-08-14-glm-5-3-model-adapter-design.md)                                                       | GLM-5.3 模型适配设计：说明文档。                                             |
| [2026-08-17-cua-settings-surface-minimization.md](2026-08-17-cua-settings-surface-minimization.md)                                             | CUA 设置面收敛（helper 状态与实验性开关下线）：说明文档。                    |
| [2026-08-18-cua-composer-entry-design.md](2026-08-18-cua-composer-entry-design.md)                                                             | CUA 输入框常驻入口按钮（首期：按钮 + 状态机）：说明文档。                    |
| [2026-08-18-windows-cua-runtime-diagnostics.md](2026-08-18-windows-cua-runtime-diagnostics.md)                                                 | Windows CUA 运行时诊断与「陈旧安装」陷阱：说明文档。                         |
| [2026-08-18-windows-markdown-link-escape-recovery-design.md](2026-08-18-windows-markdown-link-escape-recovery-design.md)                       | Windows 路径 markdown 链接转义还原设计：说明文档。                           |
| [2026-08-19-cua-producer-0.5.7-integration.md](2026-08-19-cua-producer-0.5.7-integration.md)                                                   | CUA producer 0.5.7 接入与 consumer 收敛：说明文档。                          |
| [2026-08-20-draft-prewarm-runtime-rebuild-design.md](2026-08-20-draft-prewarm-runtime-rebuild-design.md)                                       | 草稿预热会话在 runtime 换代后的重建：说明文档。                              |
| [2026-08-21-model-provider-modality-settings-design.md](2026-08-21-model-provider-modality-settings-design.md)                                 | 3.9.0 模型输入输出类型设置设计：说明文档。                                   |
| [2026-08-21-ox-alpha-openrouter-reasoning-design.md](2026-08-21-ox-alpha-openrouter-reasoning-design.md)                                       | ox-alpha 系列 OpenRouter Reasoning 适配设计：说明文档。                      |
| [2026-08-23-computer-use-plugin-display-name-spec.md](2026-08-23-computer-use-plugin-display-name-spec.md)                                     | Computer Use 插件展示名规范：说明文档。                                      |
| [2026-08-25-host-api-proxy-design.md](2026-08-25-host-api-proxy-design.md)                                                                     | Host 外部业务 API 代理设计：说明文档。                                       |
| [2026-08-26-local-file-mention-stability.md](2026-08-26-local-file-mention-stability.md)                                                       | 文件 Mention 稳定性与 Host 搜索：说明文档。                                  |
| [2026-08-31-wsl-remote-proxy-resolution-design.md](2026-08-31-wsl-remote-proxy-resolution-design.md)                                           | WSL 远程工作区代理自动解析：说明文档。                                       |
| [2026-09-01-windows-cim-cleanup-alerts-design.md](2026-09-01-windows-cim-cleanup-alerts-design.md)                                             | Windows CIM 进程清理与告警降噪设计：说明文档。                               |
| [2026-09-09-virtual-project-design.md](2026-09-09-virtual-project-design.md)                                                                   | 虚拟项目设计规划：说明文档。                                                 |
| [2026-09-11-archive-management.md](2026-09-11-archive-management.md)                                                                           | 设置：归档管理：说明文档。                                                   |
| [2026-09-11-project-sidebar-width-stability.md](2026-09-11-project-sidebar-width-stability.md)                                                 | 项目侧栏宽度稳定性：说明文档。                                               |
| [2026-09-14-session-manage-upstream-merge.md](2026-09-14-session-manage-upstream-merge.md)                                                     | Session 管理分支同步上游：说明文档。                                         |
| [2026-10-10-session-manage-upstream-integration.md](2026-10-10-session-manage-upstream-integration.md)                                         | Session Manage 与远程上游整合：说明文档。                                    |
| [2026-10-24-project-management.md](2026-10-24-project-management.md)                                                                           | 设置：项目管理：说明文档。                                                   |
| [README.md](README.md)                                                                                                                         | 本目录用途、子目录与逐文件说明。                                             |

<!-- qingqi-directory-index:end -->
