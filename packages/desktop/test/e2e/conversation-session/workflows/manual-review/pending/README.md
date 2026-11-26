# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                       | 简要说明                                                                           |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                   |
| [workflow-digest-fixed.test.mjs](workflow-digest-fixed.test.mjs)           | 独立真实 renderer 验证 hover/focus；不依赖当前会话，不覆盖宿主侧栏路由。           |
| [workflow-digest-gate.test.mjs](workflow-digest-gate.test.mjs)             | 独立真实 renderer 验证 run 联接与主轮结束门控；不覆盖服务层事件传输。              |
| [workflow-face-motion.test.mjs](workflow-face-motion.test.mjs)             | 真实组件浏览器验证；仅 renderer 展示，无 provider / host 协议。                    |
| [workflow-notification-link.test.mjs](workflow-notification-link.test.mjs) | 独立真实 renderer 验证 hover/focus；不依赖当前会话，不覆盖宿主侧栏路由。           |
| [workflow-prelaunch.test.mjs](workflow-prelaunch.test.mjs)                 | 单独运行：node --test <此文件>；前置为 dev Vite/Electron 已启动（默认 CDP 9229）。 |
| [workflow-snippet.test.mjs](workflow-snippet.test.mjs)                     | 单独运行：node --test <此文件>；前置为 dev Vite/Electron 已启动（默认 CDP 9229）。 |
| [workflow-status.test.mjs](workflow-status.test.mjs)                       | 独立真实 renderer 验证状态、展开滚动与打开回调；不覆盖宿主侧栏路由。               |
| [workflow-summary-hover.test.mjs](workflow-summary-hover.test.mjs)         | 独立真实 renderer 验证 hover/focus；不依赖当前会话，不覆盖宿主侧栏路由。           |
| [workflow-tool-summary.test.mjs](workflow-tool-summary.test.mjs)           | 手动回归前置：dev Electron（9229）已打开包含 CreateWorkflow run 的会话。           |

<!-- qingqi-directory-index:end -->
