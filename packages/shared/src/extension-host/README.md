# extension-host

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 extension host 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                               |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| [capabilities.ts](capabilities.ts)         | 能力表（docs/plugins/extension-host.md §7.2）：能力的唯一定义。表里没有的能力就不存在。                |
| [channels.ts](channels.ts)                 | L1 业务面（docs/plugins/extension-host.md §3.2）：Window Host 与扩展进程经 Main 牵线的                 |
| [context.ts](context.ts)                   | ExtensionContext（docs/plugins/extension-host.md §7.1、§7.4）是唯一定义：                              |
| [contract.example.ts](contract.example.ts) | 清单两步校验：新版本插件装在旧宿主上得到 incompatible，而不是 invalid。                                |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                               |
| [contract.ts](contract.ts)                 | extension-host-protocol 的公开契约：清单 schema、插槽目录、静态表、贡献表、能力表、ExtensionContext、  |
| [contributions.ts](contributions.ts)       | 贡献表（docs/plugins/extension-host.md §3.4、§6、§16.1）。唯一 owner 是扩展进程；                      |
| [control.ts](control.ts)                   | L0 控制面（docs/plugins/extension-host.md §3.2、§12.1）：Main ⇄ 扩展进程、Main ⇄ Window Host           |
| [env.ts](env.ts)                           | App 环境（docs/plugins/extension-host.md §16.11）：唯一 owner 是 Renderer（界面语言只在 Renderer）。   |
| [errors.ts](errors.ts)                     | 扩展错误码（docs/plugins/extension-host.md §7.1）。判断一律用 code，不依赖错误文本。                   |
| [generation.ts](generation.ts)             | 生成速率（docs/plugins/extension-host.md §10）。唯一聚合点是 Window Host：                             |
| [grants.ts](grants.ts)                     | 权限档位与协议版本（docs/plugins/extension-host.md §7.3、§17.3、§17.6、§17.7）。                       |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                     |
| [interactions.ts](interactions.ts)         | 插件回答审批、提问与切换权限模式（docs/plugins/extension-host.md §17.12，P3e）。                       |
| [logs.ts](logs.ts)                         | 扩展日志控制台（docs/plugins/extension-host.md §16.8）。缓冲的唯一 owner 是 Main 的监管器：            |
| [manifest.ts](manifest.ts)                 | 插件清单 `extension` 键（docs/plugins/extension-host.md §5）。插槽条目在清单顶层 `slots`（§16.2），    |
| [manifestSlots.ts](manifestSlots.ts)       | 清单顶层 `slots`（docs/plugins/extension-host.md §16.2）：按插槽 id 分组的入口条目，                   |
| [mention.ts](mention.ts)                   | composer.mention 的候选项查询（docs/plugins/extension-host.md §16.6）：Renderer → Window Host。        |
| [models.ts](models.ts)                     | 能力 models.list 的返回（docs/plugins/extension-host.md §18.1 H9）：与输入框模型选择器同一份视图。     |
| [module.ts](module.ts)                     | \* extension-host-protocol 模块清单（architecture-governance managed 模块）。                          |
| [notifications.ts](notifications.ts)       | 能力 notifications.show（docs/plugins/extension-host.md §18.1 H8）：插件请宿主弹系统通知。             |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                       |
| [sessionActions.ts](sessionActions.ts)     | ctx.sessions 上 call 动作的入参与返回（docs/plugins/extension-host.md §17.9，类型包 /sessions 入口）。 |
| [sessions.ts](sessions.ts)                 | 会话读连接的投影（docs/plugins/extension-host.md §17.3、§17.5、§17.6，P3b）：                          |
| [settings.ts](settings.ts)                 | 插件设置（docs/plugins/extension-host.md §16.7）：能力 settings.get / settings.onDidChange 的形状。    |
| [slots.ts](slots.ts)                       | 插槽目录与动态值（docs/plugins/extension-host.md §6、§16.2、§16.3）。                                  |
| [staticTable.ts](staticTable.ts)           | 静态表（docs/plugins/extension-host.md §16.1）：清单里的静态声明，唯一 owner 是 Window Host 的         |
| [views.ts](views.ts)                       | 扩展视图（docs/plugins/extension-host.md §8）：页面是 MCP App 页面，后端是扩展进程里的 MCP server。    |
| [workbench.ts](workbench.ts)               | 屏幕上的会话（docs/plugins/extension-host.md §3.4、§7.1、§9）。唯一 owner 是 Renderer：                |

<!-- qingqi-directory-index:end -->
