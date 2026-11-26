# navigation

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 navigation 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                 | 简要说明                                                                           |
| ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| [command-center-focus.test.ts](command-center-focus.test.ts)                         | command-center-focus.test 的实现文件。                                             |
| [command-center-history-search.test.ts](command-center-history-search.test.ts)       | 旧 basename 守卫误拒 runner 默认的 .e2e-home；采用统一守卫，仍禁止写普通 HOME。    |
| [command-center-selection.test.ts](command-center-selection.test.ts)                 | 同时接受统一 runner 与旧手工入口的隔离 HOME，禁止写入日常用户目录。                |
| [general-coding-mode.test.ts](general-coding-mode.test.ts)                           | MODE-01/02/03：只操作应用 UI 和本地 PTY，不发送模型请求。                          |
| [README.md](README.md)                                                               | 本目录用途、子目录与逐文件说明。                                                   |
| [sidebar-rich-content-performance.test.ts](sidebar-rich-content-performance.test.ts) | 一次预热后采样；交替 A/B 由相同构建产物分别运行本例，不能关闭动画换取数字。        |
| [sidebar-toggle-performance.test.ts](sidebar-toggle-performance.test.ts)             | macOS 开关没有 test id；使用两个受测语言的可访问名称，避免依赖其他功能分支的标记。 |
| [sidebar-tooltips.test.ts](sidebar-tooltips.test.ts)                                 | 实现或公开接口：fixture。                                                          |
| [task-list-archive-confirmation.test.ts](task-list-archive-confirmation.test.ts)     | 修复原因：v4 taskId 就是 pane 绑定的 sessionId；legacy ChatView root 已退出 DOM。  |

<!-- qingqi-directory-index:end -->
