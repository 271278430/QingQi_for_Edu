# design

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 design 测试场景。

### 文件

| 文件                                                                                   | 简要说明                                                                                                        |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| [browser-capture-guest-timeout.test.ts](browser-capture-guest-timeout.test.ts)         | BU-E2E-027（docs/browser-use/2026-11-03-browser-element-screenshot-and-live-reload-spec.md）：main 取帧超时后， |
| [browser-design-mode-cross-session.test.ts](browser-design-mode-cross-session.test.ts) | BU-E2E-022（docs/browser-use/2026-11-03-browser-design-mode-spec.md 第四节）：                                  |
| [browser-design-mode.test.ts](browser-design-mode.test.ts)                             | 内置浏览器设计工具（docs/browser-use/2026-11-03-browser-design-mode-spec.md）：                                 |
| [browser-design-page-tools.test.ts](browser-design-page-tools.test.ts)                 | BU-E2E-023：内置浏览器给设计稿用的页面工具（不经模型）。                                                        |
| [browser-human-viewport-preference.test.ts](browser-human-viewport-preference.test.ts) | 普通 Browser 用例无需账号；启动假 OAuth 会触发登录过期弹窗并遮挡真实点击。                                      |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                                                                                |

<!-- qingqi-directory-index:end -->
