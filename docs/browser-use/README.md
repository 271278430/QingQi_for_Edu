# browser-use

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

browser use 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                                                                                   | 简要说明                                                                               |
| -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [2026-07-07-agent-host-main-channel-spec.md](2026-07-07-agent-host-main-channel-spec.md)                                               | agent→host→main browser 执行通道规格（T4）：说明文档。                                 |
| [2026-07-07-browser-cdp-view-spec.md](2026-07-07-browser-cdp-view-spec.md)                                                             | main WebContentsView + CDP 执行规格（T5）：说明文档。                                  |
| [2026-07-07-browser-client-lib-spec.md](2026-07-07-browser-client-lib-spec.md)                                                         | browser-client 库 + node_repl 注入规格（T6，P0 验收）：说明文档。                      |
| [2026-07-07-browser-control-protocol-spec.md](2026-07-07-browser-control-protocol-spec.md)                                             | Browser 命令契约 + BrowserControlPort + 协议方法规格（T3）：说明文档。                 |
| [2026-07-07-browser-use-cdp-node-repl-spec.md](2026-07-07-browser-use-cdp-node-repl-spec.md)                                           | Browser-Use CDP + node_repl 总规格（重做）：说明文档。                                 |
| [2026-07-07-browser-view-display-spec.md](2026-07-07-browser-view-display-spec.md)                                                     | WebContentsView 覆盖 side-pane 显示规格（T7，P1）：说明文档。                          |
| [2026-07-07-interaction-core-snapshot-click-type-spec.md](2026-07-07-interaction-core-snapshot-click-type-spec.md)                     | 交互核心：DOM 快照 + click/type/press/scroll（CDP 真实输入）设计：说明文档。           |
| [2026-07-07-node-repl-engine-spec.md](2026-07-07-node-repl-engine-spec.md)                                                             | NodeReplSession 引擎规格（T1，通用基建）：说明文档。                                   |
| [2026-07-07-node-repl-tools-spec.md](2026-07-07-node-repl-tools-spec.md)                                                               | node_repl 三工具规格（T2，历史实现）：说明文档。                                       |
| [2026-07-07-phase1-webcontentsview-navigation-plan.md](2026-07-07-phase1-webcontentsview-navigation-plan.md)                           | 阶段 1：main 底座导航能力 实现计划：说明文档。                                         |
| [2026-07-07-phase2-unified-browser-view-plan.md](2026-07-07-phase2-unified-browser-view-plan.md)                                       | Phase 2 — Unified Browser View (去 webview) 实现计划：说明文档。                       |
| [2026-07-07-unified-webcontentsview-browser-design.md](2026-07-07-unified-webcontentsview-browser-design.md)                           | 统一浏览器：手动 tab 与 browser-use 共用 WebContentsView（去 webview）设计：说明文档。 |
| [2026-07-08-node-repl-toplevel-binding-persistence-spec.md](2026-07-08-node-repl-toplevel-binding-persistence-spec.md)                 | node_repl 顶层绑定跨调用持久（路线 B，A-ready 接缝）设计：说明文档。                   |
| [2026-07-08-webview-cdp-on-guest-pivot-spec.md](2026-07-08-webview-cdp-on-guest-pivot-spec.md)                                         | 内置浏览器改用 `<webview>` + CDP-on-guest（弃 WebContentsView）设计：说明文档。        |
| [2026-07-09-browser-use-phase1-spec.md](2026-07-09-browser-use-phase1-spec.md)                                                         | Browser Use Phase 1 Spec：说明文档。                                                   |
| [2026-07-10-browser-use-spec.md](2026-07-10-browser-use-spec.md)                                                                       | Browser Use 完整行为规格：说明文档。                                                   |
| [2026-07-12-browser-tab-process-lifetime-spec.md](2026-07-12-browser-tab-process-lifetime-spec.md)                                     | Browser Tab 进程内默认持久生命周期 Spec：说明文档。                                    |
| [2026-07-12-browser-tab-selection-activation-spec.md](2026-07-12-browser-tab-selection-activation-spec.md)                             | Browser Tab 选择、激活与操作预检 Spec：说明文档。                                      |
| [2026-07-12-browser-use-runtime-semantics-spec.md](2026-07-12-browser-use-runtime-semantics-spec.md)                                   | Browser Use 运行时语义收口规格：说明文档。                                             |
| [2026-07-13-browser-settings-spec.md](2026-07-13-browser-settings-spec.md)                                                             | Browser 设置页规格：说明文档。                                                         |
| [2026-07-13-cli-headless-cdp-backend-spec.md](2026-07-13-cli-headless-cdp-backend-spec.md)                                             | CLI Headless CDP Browser Backend 规格：说明文档。                                      |
| [2026-07-13-node-repl-mcp-runtime-spec.md](2026-07-13-node-repl-mcp-runtime-spec.md)                                                   | Browser Use Node REPL MCP 运行时规格：说明文档。                                       |
| [2026-07-14-browser-resize-operation-warning-spec.md](2026-07-14-browser-resize-operation-warning-spec.md)                             | Browser Use 操作期间 resize 弱提示：说明文档。                                         |
| [2026-07-14-browser-tab-conversation-isolation-spec.md](2026-07-14-browser-tab-conversation-isolation-spec.md)                         | Browser Use 对话级标签页隔离规格：说明文档。                                           |
| [2026-07-15-browser-turn-final-screenshot-spec.md](2026-07-15-browser-turn-final-screenshot-spec.md)                                   | Browser Use 轮次结束自动截图规格：说明文档。                                           |
| [2026-07-15-embedded-browser-javascript-dialog-origin-spec.md](2026-07-15-embedded-browser-javascript-dialog-origin-spec.md)           | 内置 Browser JavaScript 对话框来源标识 Spec：说明文档。                                |
| [2026-07-15-responsive-browser-viewport-spec.md](2026-07-15-responsive-browser-viewport-spec.md)                                       | 内置浏览器自由尺寸视口：说明文档。                                                     |
| [2026-07-16-subagent-browser-unavailable-spec.md](2026-07-16-subagent-browser-unavailable-spec.md)                                     | Subagent Browser Use 会话边界：说明文档。                                              |
| [2026-07-16-web-gui-tester-skill-spec.md](2026-07-16-web-gui-tester-skill-spec.md)                                                     | Browser Use Web GUI Tester Skill 规格：说明文档。                                      |
| [2026-07-19-desktop-iab-e2e-spec.md](2026-07-19-desktop-iab-e2e-spec.md)                                                               | Desktop IAB Browser Use E2E 规格：说明文档。                                           |
| [2026-07-28-stateless-browser-use-mcp-spec.md](2026-07-28-stateless-browser-use-mcp-spec.md)                                           | 2026-07-28 Browser Use MCP 方案归档：说明文档。                                        |
| [2026-07-31-browser-generic-target-popup-recovery-guidance-spec.md](2026-07-31-browser-generic-target-popup-recovery-guidance-spec.md) | Browser Use 新 URL 等待、通用目标点击与新标签恢复 Guidance Spec：说明文档。            |
| [2026-07-31-browser-tab-residency-budget-spec.md](2026-07-31-browser-tab-residency-budget-spec.md)                                     | Browser Tab 32 个硬上限与进程生命周期 Spec：说明文档。                                 |
| [2026-07-31-browser-toolbar-more-menu-spec.md](2026-07-31-browser-toolbar-more-menu-spec.md)                                           | 内置浏览器地址栏操作与更多菜单规格：说明文档。                                         |
| [2026-08-02-browser-use-plugin-version-0-1-3-spec.md](2026-08-02-browser-use-plugin-version-0-1-3-spec.md)                             | Browser Use Plugin 0.1.3 版本同步规格：说明文档。                                      |
| [2026-08-06-browser-use-plugin-version-0-2-1-spec.md](2026-08-06-browser-use-plugin-version-0-2-1-spec.md)                             | Browser Use Plugin 0.2.1 版本同步规格：说明文档。                                      |
| [2026-08-12-browser-webview-video-recording-spec.md](2026-08-12-browser-webview-video-recording-spec.md)                               | Browser Use 内置 WebView 视频录制 Spec：说明文档。                                     |
| [2026-08-14-browser-use-plugin-version-0-3-0-spec.md](2026-08-14-browser-use-plugin-version-0-3-0-spec.md)                             | Browser Use Plugin 0.3.0 版本与录屏资产同步规格：说明文档。                            |
| [2026-08-18-browser-view-event-subscription-visibility-spec.md](2026-08-18-browser-view-event-subscription-visibility-spec.md)         | Browser View 权威事件订阅与可见性解耦：说明文档。                                      |
| [2026-08-23-browser-guest-scope-recovery-spec.md](2026-08-23-browser-guest-scope-recovery-spec.md)                                     | Browser Use Guest scope 冻结与绑定自愈规格：说明文档。                                 |
| [2026-08-24-browser-open-reuse-tab.md](2026-08-24-browser-open-reuse-tab.md)                                                           | open() 同站 tab 采用（reuseTab）设计记录：说明文档。                                   |
| [2026-08-25-browser-guest-cdp-teardown-spec.md](2026-08-25-browser-guest-cdp-teardown-spec.md)                                         | Browser Use guest CDP teardown 与销毁顺序规格：说明文档。                              |
| [2026-08-25-browser-guest-route-residency-spec.md](2026-08-25-browser-guest-route-residency-spec.md)                                   | Browser Use Guest 跨主视图常驻规格（最小化延期）：说明文档。                           |
| [2026-08-26-browser-use-plugin-version-0-4-1-spec.md](2026-08-26-browser-use-plugin-version-0-4-1-spec.md)                             | Browser Use 插件 0.4.1 版本同步规格：说明文档。                                        |
| [2026-08-31-browser-use-plugin-version-0-4-2-spec.md](2026-08-31-browser-use-plugin-version-0-4-2-spec.md)                             | Browser Use 插件 0.4.2 版本同步规格：说明文档。                                        |
| [2026-09-07-desktop-zoom-coordinate-spec.md](2026-09-07-desktop-zoom-coordinate-spec.md)                                               | Desktop 缩放下的 Browser Use 坐标契约：说明文档。                                      |
| [2026-10-08-embedded-browser-permission-governance-spec.md](2026-10-08-embedded-browser-permission-governance-spec.md)                 | 内置浏览器权限治理 Spec：说明文档。                                                    |
| [2026-10-16-browser-device-presets-and-export-spec.md](2026-10-16-browser-device-presets-and-export-spec.md)                           | 内置浏览器设备预设与导出：说明文档。                                                   |
| [2026-10-28-browser-session-recent-visits.md](2026-10-28-browser-session-recent-visits.md)                                             | 浏览器会话最近访问：说明文档。                                                         |
| [2026-11-03-browser-design-mode-spec.md](2026-11-03-browser-design-mode-spec.md)                                                       | 内置浏览器：设计工具：说明文档。                                                       |
| [2026-11-03-browser-element-screenshot-and-live-reload-spec.md](2026-11-03-browser-element-screenshot-and-live-reload-spec.md)         | 内置浏览器：设计稿元素带截图、本地页面自动刷新、HTML 单击打开：说明文档。              |
| [browser-use-plugin-runtime-boundary.md](browser-use-plugin-runtime-boundary.md)                                                       | Browser 官方插件运行时边界：说明文档。                                                 |
| [local-html-preview.md](local-html-preview.md)                                                                                         | 内置浏览器本地 HTML 预览：说明文档。                                                   |
| [README.md](README.md)                                                                                                                 | 本目录用途、子目录与逐文件说明。                                                       |

<!-- qingqi-directory-index:end -->
