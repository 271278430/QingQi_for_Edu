# mcp-apps-host-fixture

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 mcp apps host fixture 工程脚本。

### 文件

| 文件                                                         | 简要说明                                                                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [agent.ts](agent.ts)                                         | 不继承 API key、真实用户认证及 Electron Node 标志，模型测试也只通过显式传入的隔离配置访问本地 fixture。 |
| [background-main.ts](background-main.ts)                     | 先打开外壳但没有任何会话卡片/订阅，再让真实模型调用返回 UI 工具结果。                                   |
| [chain-combinations.ts](chain-combinations.ts)               | 实现或公开接口：checkCombinations。                                                                     |
| [chain-main.ts](chain-main.ts)                               | chain-main 的实现文件。                                                                                 |
| [guest-evaluation.ts](guest-evaluation.ts)                   | Chromium 不保证已销毁 frame 的 executeJavaScript Promise 回包；以真实销毁事件结束观察。                 |
| [interaction-main.ts](interaction-main.ts)                   | 真实等待握手时限；不伪造 controller 的错误态或直接卸载 webview。                                        |
| [main.ts](main.ts)                                           | 旧分区探针会先关闭临时窗口；完整测试结束前不能触发 Electron 默认退出。                                  |
| [managed-checks.ts](managed-checks.ts)                       | 测试 IPC 的异常只保留 message，页面侧核对拒绝原因；结构化 reason 由 Agent 单测覆盖。                    |
| [managed-empty-main.ts](managed-empty-main.ts)               | managed-empty-main 的实现文件。                                                                         |
| [managed-environment.ts](managed-environment.ts)             | 实现或公开接口：managedEnvironment。                                                                    |
| [managed-late-checks.ts](managed-late-checks.ts)             | 空白会话关闭后不会保留；先经真实发送链路写入一轮历史，再模拟闲置卸载。                                  |
| [managed-lifecycle-checks.ts](managed-lifecycle-checks.ts)   | 实现或公开接口：checkLifecycle。                                                                        |
| [managed-main.ts](managed-main.ts)                           | managed-main 的实现文件。                                                                               |
| [managed-model-checks.ts](managed-model-checks.ts)           | 实现或公开接口：checkModel。                                                                            |
| [managed-permission-checks.ts](managed-permission-checks.ts) | 只替代原生确认框的用户回答；Chromium 请求、frame 绑定及权限 gate 均为生产代码。                         |
| [managed-renderer.tsx](managed-renderer.tsx)                 | managed-renderer 的React 组件。                                                                         |
| [managed-retention-checks.ts](managed-retention-checks.ts)   | 实现或公开接口：checkRetention。                                                                        |
| [mcp-server.mjs](mcp-server.mjs)                             | 独立 MCP 进程：控制 socket 只用于可重复地安排完成顺序，不替代 MCP 数据链路。                            |
| [model.ts](model.ts)                                         | 确定性本地模型只返回预置工具调用；授权、认领、执行、取消仍走真实 Agent。                                |
| [pointer-input.ts](pointer-input.ts)                         | 从宿主坐标发送鼠标事件，避免直接向 guest 注入点击绕过透明层命中测试。                                   |
| [preload.ts](preload.ts)                                     | preload 的实现文件。                                                                                    |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                        |
| [renderer.ts](renderer.ts)                                   | 记录生产承载层的活动 window 监听器，重复切换后必须保持恒定。                                            |
| [retention-main.ts](retention-main.ts)                       | retention-main 的实现文件。                                                                             |
| [retention-renderer.ts](retention-renderer.ts)               | retention-renderer 的实现文件。                                                                         |
| [rows-main.ts](rows-main.ts)                                 | rows-main 的实现文件。                                                                                  |
| [rows-renderer.tsx](rows-renderer.tsx)                       | 使用真实时间线和工具行，不直接挂 PluginUiCard；避免绕过展示资格/替代/折叠策略。                         |
| [sampling-database.mjs](sampling-database.mjs)               | Electron 与 Agent 已退出后重新打开 SQLite，验证统计确实持久化而非内存投影。                             |
| [sampling-extra-checks.ts](sampling-extra-checks.ts)         | 实现或公开接口：checkSamplingExtras。                                                                   |
| [sampling-main.ts](sampling-main.ts)                         | sampling-main 的实现文件。                                                                              |
| [session-ready-main.ts](session-ready-main.ts)               | 单例回归只使用显式注入的 MCP；默认内置插件会引入认证和网络等待，污染恢复时序。                          |
| [showcase-main.ts](showcase-main.ts)                         | 独立 fixture 只批准本测试的两个演示工具；审批仍通过真实 Agent/宿主链路。                                |
| [storage-checks.ts](storage-checks.ts)                       | 只控制真实清理开始的时序；释放后仍调用 Electron 原生实现，不用 mock 成功代替持久化验证。                |
| [widget.tsx](widget.tsx)                                     | widget 的React 组件。                                                                                   |

<!-- qingqi-directory-index:end -->
