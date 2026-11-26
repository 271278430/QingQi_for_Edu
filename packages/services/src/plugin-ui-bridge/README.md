# plugin-ui-bridge

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 plugin ui bridge 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                                                          |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| [appToolsContract.ts](appToolsContract.ts)               | \* App-Provided Tools 的 renderer → agent 通道。页面实例身份 = 会话 + 沙箱作用域 + 代际（与资源订阅同一三元组）。 |
| [contract.example.ts](contract.example.ts)               | UI 侧典型用法：先准备沙箱拿句柄，再把句柄交给 webview 挂载；面板作用域用 `surface:<id>`。                         |
| [CONTRACT.md](CONTRACT.md)                               | 模块职责、公共接口、依赖方向和状态约定。                                                                          |
| [contract.ts](contract.ts)                               | 与 zcodeAgentService 其余方法一致的 workspace 定位；身份用 workspaceIdentity，路径用 workspacePath。              |
| [index.ts](index.ts)                                     | 扩展视图（extensions-service）采用同一套 HTML 挑选与限额。                                                        |
| [instanceAccounts.ts](instanceAccounts.ts)               | Host 的账号上下文来自凭据 owner；不接收页面传入的账号或访问令牌。                                                 |
| [module.ts](module.ts)                                   | \* plugin-ui-bridge 模块清单（architecture-governance managed 模块）。                                            |
| [pluginUiAppToolsService.ts](pluginUiAppToolsService.ts) | 四条 agent 调用都是透传；缺省（web / 远程）时登记与认领抛 unavailable，注销静默。                                 |
| [pluginUiBridgeService.ts](pluginUiBridgeService.ts)     | 取消带 callId 的进行中调用。                                                                                      |
| [pluginUiSamplingService.ts](pluginUiSamplingService.ts) | 实现或公开接口：createPluginUiSamplingService。                                                                   |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                                                  |
| [samplingContract.ts](samplingContract.ts)               | 无状态透传；Agent 持有实例凭证、并发限额和唯一调用终态。                                                          |

<!-- qingqi-directory-index:end -->
