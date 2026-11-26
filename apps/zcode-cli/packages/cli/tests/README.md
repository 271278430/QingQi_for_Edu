# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/cli 基础工程中的 tests 验收与回归场景。

### 子目录

| 目录                                            | 存放内容                                                  |
| ----------------------------------------------- | --------------------------------------------------------- |
| [argument-parsing/](argument-parsing/README.md) | @zcode/cli 基础工程中的 argument parsing 验收与回归场景。 |
| [fixtures/](fixtures/README.md)                 | @zcode/cli 基础工程中的 fixtures 测试夹具与样例。         |

### 文件

| 文件                                                                       | 简要说明                                                                                        |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| [build-sea.test.mjs](build-sea.test.mjs)                                   | build-sea.test 的实现文件。                                                                     |
| [build.test.mjs](build.test.mjs)                                           | 实现或公开接口：schema。                                                                        |
| [cli.unit.test.ts](cli.unit.test.ts)                                       | 协议 Model Option 测试夹具；TUI 登录态由 App 模型目录中是否存在可选模型推导。                   |
| [clipboard-image.test.ts](clipboard-image.test.ts)                         | clipboard-image.test 的实现文件。                                                               |
| [clipboard-text.test.ts](clipboard-text.test.ts)                           | clipboard-text.test 的实现文件。                                                                |
| [cwd-option.test.ts](cwd-option.test.ts)                                   | cwd-option.test 的实现文件。                                                                    |
| [dwf-child-command-fixture.ts](dwf-child-command-fixture.ts)               | \* 子进程语境的 RunContext：stdin 必须是**真** Readable（childMain 拿它建 readline，            |
| [dwf-child-command.test.ts](dwf-child-command.test.ts)                     | \* 隐藏子命令 `__zcode-dwf-child` 的分派与执行。                                                |
| [dwf-command.test.ts](dwf-command.test.ts)                                 | \* `/dwf` 的命令面测试（docs/dynamic-workflow/launch.md「`/dwf`」）。                           |
| [headless-workflow-option.test.ts](headless-workflow-option.test.ts)       | \* `--workflow-mode` 在 headless / resume / stdio 各入口上的取值与隔离                          |
| [headless-workflow.test.ts](headless-workflow.test.ts)                     | —————————————————————————————————————————————————————————————                                   |
| [hooks-trust-command.test.ts](hooks-trust-command.test.ts)                 | hooks-trust-command.test 的实现文件。                                                           |
| [internal-search.node-test.ts](internal-search.node-test.ts)               | 子进程启动后才写 pid 文件；轮询能让测试稳定等待到真实 native child。                            |
| [memory-bench.test.ts](memory-bench.test.ts)                               | memory-bench.test 的实现文件。                                                                  |
| [mode-menu.test.ts](mode-menu.test.ts)                                     | mode-menu.test 的实现文件。                                                                     |
| [output-format-stream-json.test.ts](output-format-stream-json.test.ts)     | Two events, one carrying a newline, so NDJSON framing is actually exercised.                    |
| [plugin-host-entry.test.mjs](plugin-host-entry.test.mjs)                   | 回归要挡住模块求值，而非只看包大小；构建仍保留普通 CLI 所需代码。                               |
| [plugins-command.test.ts](plugins-command.test.ts)                         | plugins-command.test 的实现文件。                                                               |
| [process-errors.test.ts](process-errors.test.ts)                           | process-errors.test 的实现文件。                                                                |
| [process-name.test.mjs](process-name.test.mjs)                             | process-name.test 的实现文件。                                                                  |
| [provider-runtime-env.test.ts](provider-runtime-env.test.ts)               | 随包配置按入口真实路径（解析软链接后）定位，入口文件必须真实存在。                              |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                                |
| [sea-official-plugin-assets.test.mjs](sea-official-plugin-assets.test.mjs) | 夹具必须覆盖清单里除 documents 之外的所有条目：collect 按清单顺序对每个                         |
| [sea-runtime-tools.test.ts](sea-runtime-tools.test.ts)                     | sea-runtime-tools.test 的实现文件。                                                             |
| [skills-command.test.ts](skills-command.test.ts)                           | skills-command.test 的实现文件。                                                                |
| [tui-console.test.ts](tui-console.test.ts)                                 | tui-console.test 的实现文件。                                                                   |
| [tui-login-polling.test.ts](tui-login-polling.test.ts)                     | tui-login-polling.test 的实现文件。                                                             |
| [tui-mode-switch.test.ts](tui-mode-switch.test.ts)                         | 循环顺序以 TUI_SWITCHABLE_MODES 为准：staging 新增 guarded 并把 edit 移出 Shift+Tab 循环。      |
| [tui-model-selection.test.ts](tui-model-selection.test.ts)                 | tui-model-selection.test 的实现文件。                                                           |
| [tui-session-event-relay.test.ts](tui-session-event-relay.test.ts)         | TUI 常驻会话事件中继：换 app 时必须重挂（docs/dynamic-workflow/launch.md「The inline card」）。 |
| [tui-signals.test.ts](tui-signals.test.ts)                                 | Closing an old session's pipes can deliver this signal to the TUI process.                      |
| [tui-startup.test.ts](tui-startup.test.ts)                                 | tui-startup.test 的实现文件。                                                                   |
| [tui-subagent-observation.test.ts](tui-subagent-observation.test.ts)       | tui-subagent-observation.test 的实现文件。                                                      |
| [tui-subagents.test.ts](tui-subagents.test.ts)                             | tui-subagents.test 的实现文件。                                                                 |
| [upload-sea-smb.test.mjs](upload-sea-smb.test.mjs)                         | upload-sea-smb.test 的实现文件。                                                                |
| [workflow-mode-option.test.ts](workflow-mode-option.test.ts)               | \* 独立 CLI 的 `--workflow-mode`（docs/dynamic-workflow/launch.md「The standalone CLI:          |

<!-- qingqi-directory-index:end -->
