# gen-ui-fixture

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 gen ui fixture 工程脚本。

### 文件

| 文件                                                 | 简要说明                                                                             |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [compact-button-checks.ts](compact-button-checks.ts) | 用真实文字 Range 检查字号变化后的边界，避免只验证 min-height。                       |
| [control-state-checks.ts](control-state-checks.ts)   | CDP 固定伪类验证级联组合；不把后台窗口的焦点当作真实键盘验收。                       |
| [external-links-checks.ts](external-links-checks.ts) | 使用生产桥接与手势校验；只替换最终 opener，避免测试启动系统浏览器。                  |
| [file-summary-checks.ts](file-summary-checks.ts)     | 先证明普通 HTML 可以正常出现，再验证 visualize 去重，避免空组件假阳性。              |
| [file-summary.tsx](file-summary.tsx)                 | 实现或公开接口：FileSummaryFixture。                                                 |
| [main.ts](main.ts)                                   | No synthetic native gesture: programmatic follow-up must use confirmation.           |
| [offline-checks.ts](offline-checks.ts)               | 独立 profile 中，在第一次导航前禁网；不覆盖生产 onBeforeRequest 闸门。               |
| [output-files.ts](output-files.ts)                   | 回归：打开 Home 一类包含应用数据目录的工作区，固定 Gen UI 输出仍须可读。             |
| [preload.ts](preload.ts)                             | preload 的实现文件。                                                                 |
| [presentation-checks.ts](presentation-checks.ts)     | Electron 44 移除了 readImage；夹具读取真实 PNG，保留非空与裁剪尺寸断言。             |
| [preview-corner-checks.ts](preview-corner-checks.ts) | 实现或公开接口：checkPreviewCorners、checkLoading。                                  |
| [react.tsx](react.tsx)                               | react 的React 组件。                                                                 |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                     |
| [renderer.ts](renderer.ts)                           | renderer 的实现文件。                                                                |
| [runtime-checks.ts](runtime-checks.ts)               | 上游只为 focus-visible 自动打开；脚本 focus 不等于用户键盘输入，悬停走实际延迟路径。 |
| [standalone-checks.ts](standalone-checks.ts)         | 导出资源必须独立工作，不能依赖桌面 preload 或正在运行的 Agent。                      |
| [style-checks.ts](style-checks.ts)                   | 用真实 guest computed style 验证 token 同步和容器层级，不用 CSS 字符串模拟浏览器。   |

<!-- qingqi-directory-index:end -->
