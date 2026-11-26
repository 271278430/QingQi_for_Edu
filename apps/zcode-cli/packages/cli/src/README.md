# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/cli 基础工程中的 src 实现源码。

### 子目录

| 目录                                            | 存放内容                                            |
| ----------------------------------------------- | --------------------------------------------------- |
| [argument-parsing/](argument-parsing/README.md) | @zcode/cli 基础工程中的 argument parsing 实现源码。 |
| [command-center/](command-center/README.md)     | @zcode/cli 基础工程中的 command center 实现源码。   |
| [internal-search/](internal-search/README.md)   | @zcode/cli 基础工程中的 internal search 实现源码。  |

### 文件

| 文件                                                             | 简要说明                                                                                                                                             |
| ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [arguments.ts](arguments.ts)                                     | `zcode plugins` 子命令旗标：strict 解析器要求                                                                                                        |
| [bootstrap-loader.ts](bootstrap-loader.ts)                       | 实现或公开接口：loadBootstrapModule。                                                                                                                |
| [cli-types.ts](cli-types.ts)                                     | \* Session-event shaper for --output-format stream-json. Defaults to the                                                                             |
| [clipboard-image.ts](clipboard-image.ts)                         | 实现或公开接口：createNodeClipboardImageReader。                                                                                                     |
| [clipboard-text.ts](clipboard-text.ts)                           | 实现或公开接口：createNodeClipboardTextWriter。                                                                                                      |
| [command-center-custom.ts](command-center-custom.ts)             | 实现或公开接口：CommandCenterCustomCommandListOutcome、CommandCenterCustomCommand、CommandCenterCustomCommandContent、listCustomCommandSuggestions。 |
| [command-center.ts](command-center.ts)                           | command-center 的实现文件。                                                                                                                          |
| [commands-command.ts](commands-command.ts)                       | 实现或公开接口：runCommandsCommand。                                                                                                                 |
| [custom-command-expand.ts](custom-command-expand.ts)             | 与 app 路径同一规则：`!` shell 块改写成交给模型的 Bash 指令，不执行也不报错；                                                                        |
| [cwd.ts](cwd.ts)                                                 | 实现或公开接口：resolveCliCwd。                                                                                                                      |
| [dwf-child-command.ts](dwf-child-command.ts)                     | \* 隐藏子命令 `__zcode-dwf-child <entry path>`：dynamic workflow 的沙箱子进程入口。                                                                  |
| [env.ts](env.ts)                                                 | 用户可能把 .env 当作目录使用（如 ~/.env/modelscope）。                                                                                               |
| [headless-browser.ts](headless-browser.ts)                       | 实现或公开接口：createCliHeadlessBrowserRuntime。                                                                                                    |
| [headless-workflow.ts](headless-workflow.ts)                     | \* headless（`-p`）下的 CreateWorkflow 审批旁路。                                                                                                    |
| [help.ts](help.ts)                                               | 实现或公开接口：formatCliHelp。                                                                                                                      |
| [hooks-trust-command.ts](hooks-trust-command.ts)                 | 实现或公开接口：runHooksCommand、workspaceTrustCommandArgument。                                                                                     |
| [index.ts](index.ts)                                             | index 的实现文件。                                                                                                                                   |
| [locale.ts](locale.ts)                                           | 实现或公开接口：detectCliLocale、resolveDisplayLocale。                                                                                              |
| [login-command.ts](login-command.ts)                             | 实现或公开接口：runLoginCommand、runLogoutCommand。                                                                                                  |
| [main.ts](main.ts)                                               | 存储模式也可运行在 Host Worker 中，不能修改整个 Host 的进程名称。                                                                                    |
| [plugin-host-command.ts](plugin-host-command.ts)                 | \_\_zcode-plugin-host 在 agent 子进程里运行 official plugin 的 MCP server（server.js）。                                                             |
| [plugins-command-format.ts](plugins-command-format.ts)           | 实现或公开接口：writeWarnings、formatDiagnosticLines、formatHumanPluginList、formatHumanAvailableList。                                              |
| [plugins-command-shared.ts](plugins-command-shared.ts)           | \* CLI 依赖名 → bootstrap 导出名。测试按依赖名注入假实现；生产路径按导出名懒加载 bootstrap，                                                         |
| [plugins-command.ts](plugins-command.ts)                         | 实现或公开接口：runPluginsCommand。                                                                                                                  |
| [plugins-marketplace-command.ts](plugins-marketplace-command.ts) | marketplaces 只有 Host 级一份，这里仅校验拼写以保持参数面一致。                                                                                      |
| [process-errors.ts](process-errors.ts)                           | \* 为协议型 CLI 安装最后一道进程级异常边界。                                                                                                         |
| [process-name.ts](process-name.ts)                               | 实现或公开接口：CLI_COMMAND_NAME、CLI_PROCESS_NAME、setCliProcessTitle。                                                                             |
| [prompt-command.ts](prompt-command.ts)                           | \* Does this run print a JSON summary at the end?                                                                                                    |
| [protocol-console.ts](protocol-console.ts)                       | \* 为独占 stdout 的 CLI（stdio protocol / TUI）安装 console 输出边界。                                                                               |
| [protocol-lifecycle.ts](protocol-lifecycle.ts)                   | CLI 入口的唯一退出 owner；在加载 runtime 之前安装，不依赖 run() 返回。                                                                               |
| [protocol-stderr.ts](protocol-stderr.ts)                         | \* 协议进程的诊断出口只有一个。必须监听真实流的异步 error，而不只是 catch write：                                                                    |
| [provider-runtime-env.ts](provider-runtime-env.ts)               | TTL 检查不是生产事件；成功更新才默认留痕，不能输出 CDN URL 查询参数或内容。                                                                          |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                                                                                     |
| [resume.ts](resume.ts)                                           | 实现或公开接口：resolveResumeSession。                                                                                                               |
| [run.ts](run.ts)                                                 | 实现或公开接口：run。                                                                                                                                |
| [runtime-event-subscriber.ts](runtime-event-subscriber.ts)       | runtime 上「跨回合会话事件订阅」的能力读取。                                                                                                         |
| [runtime-warnings.ts](runtime-warnings.ts)                       | Node/AI SDK dependency warnings can be emitted during headless                                                                                       |
| [sea-playwright-runtime.ts](sea-playwright-runtime.ts)           | 实现或公开接口：loadCliPlaywrightChromium。                                                                                                          |
| [sea-runtime-tools.ts](sea-runtime-tools.ts)                     | 实现或公开接口：SeaRuntimeModule、EnsureSeaRuntimeToolsOptions、ensureSeaRuntimeTools。                                                              |
| [shutdown.ts](shutdown.ts)                                       | detached shell processes form their own process group, so parent                                                                                     |
| [skills-command.ts](skills-command.ts)                           | 实现或公开接口：runSkillsCommand。                                                                                                                   |
| [tui-auth.ts](tui-auth.ts)                                       | 实现或公开接口：loginForTui、loginBigmodelForTui、configureApiKeyForTui、logoutForTui。                                                              |
| [tui-command-data.ts](tui-command-data.ts)                       | 实现或公开接口：listCustomCommandsForTui、loadCustomCommandForTui、listSkillsForTui、listSessionsForTui。                                            |
| [tui-command-state.ts](tui-command-state.ts)                     | The TUI's Plan entry projects the runtime's independent planning flag.                                                                               |
| [tui-command.ts](tui-command.ts)                                 | 实现或公开接口：runTuiCommand。                                                                                                                      |
| [tui-login-state.ts](tui-login-state.ts)                         | Registry already applies provider/account availability, including personal providers.                                                                |
| [tui-prompt-handler-queries.ts](tui-prompt-handler-queries.ts)   | tui-prompt-handler.ts 顶到 oxlint max-lines 上限（400 行），把 submitPrompt 上                                                                       |
| [tui-prompt-handler-runtime.ts](tui-prompt-handler-runtime.ts)   | tui-prompt-handler.ts 顶到 oxlint max-lines 上限（400 行），把 createApp 里                                                                          |
| [tui-prompt-handler.ts](tui-prompt-handler.ts)                   | 采用防御式 runtime 读取：subscribeEvents 不在 app 的静态类型面上，                                                                                   |
| [tui-runtime-loader.ts](tui-runtime-loader.ts)                   | 实现或公开接口：loadTuiRuntime。                                                                                                                     |
| [tui-session-event-relay.ts](tui-session-event-relay.ts)         | // 单独成模块是为了让「换 app 时重挂」这条性质可被直接单测：若埋在 tui-prompt-handler                                                                |
| [tui-startup-locale.ts](tui-startup-locale.ts)                   | login-required startup renders local TUI panels before ZCodeApp                                                                                      |
| [tui-stderr.ts](tui-stderr.ts)                                   | 与 run 共享参数定义，包括 locale/browser/force-mcs 和多值工具限制。                                                                                  |
| [tui-submit-metadata.ts](tui-submit-metadata.ts)                 | 实现或公开接口：withTuiMetadata。                                                                                                                    |
| [tui-workspace-git.ts](tui-workspace-git.ts)                     | 实现或公开接口：resolveWorkspaceGitBranch。                                                                                                          |
| [tui-workspace-paths.ts](tui-workspace-paths.ts)                 | 实现或公开接口：createWorkspacePathSuggestionProvider。                                                                                              |
| [workflow-mode.ts](workflow-mode.ts)                             | 独立 CLI 的动态工作流 mode（docs/dynamic-workflow/launch.md「The standalone CLI: `--workflow-mode`」）。                                             |

<!-- qingqi-directory-index:end -->
