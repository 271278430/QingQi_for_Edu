# extensions

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 extensions 实现源码。

### 子目录

| 目录                        | 存放内容                                       |
| --------------------------- | ---------------------------------------------- |
| [grants/](grants/README.md) | @zcode/services 基础工程中的 grants 实现源码。 |
| [views/](views/README.md)   | @zcode/services 基础工程中的 views 实现源码。  |

### 文件

| 文件                                               | 简要说明                                                                                                      |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| [auditLog.ts](auditLog.ts)                         | 审计日志（docs/plugins/extension-host.md §17.8）：`~/.zcode/v2/extensions/audit/<日期>.jsonl`，只由本服务写， |
| [capabilityGateway.ts](capabilityGateway.ts)       | 能力网关（docs/plugins/extension-host.md §3.5、§7.2、§17.1）：插件访问 App 的唯一入口。                       |
| [capabilityTypes.ts](capabilityTypes.ts)           | 能力网关与各后端共用的调用类型（docs/plugins/extension-host.md §7.2、§17.3）。单独成文件，                    |
| [contextPump.ts](contextPump.ts)                   | context 组成数据泵（docs/plugins/extension-host.md §9）：CLI 是唯一 owner，这里只转发变更通知                 |
| [contract.example.ts](contract.example.ts)         | Renderer 的用法：先订阅，第一条消息就是当前快照（或 detached），之后是增量与后续快照。                        |
| [CONTRACT.md](CONTRACT.md)                         | 模块职责、公共接口、依赖方向和状态约定。                                                                      |
| [contract.ts](contract.ts)                         | \* Renderer 收到的插槽数据消息（§16.1），一条流里有两个 owner 的数据：                                        |
| [draftRelay.ts](draftRelay.ts)                     | 能力 workbench.startDraft 在 Window Host 的一段（docs/plugins/extension-host.md §18.1 H2，③ 请 Renderer）：   |
| [envState.ts](envState.ts)                         | App 环境（docs/plugins/extension-host.md §16.11）：唯一 owner 是 Renderer（界面语言只在 Renderer）。          |
| [generationPump.ts](generationPump.ts)             | 生成速率（docs/plugins/extension-host.md §10）：Window Host 是唯一聚合点。                                    |
| [grantRequestRelay.ts](grantRequestRelay.ts)       | 能力 grants.request 在 Window Host 的一段（docs/plugins/extension-host.md §18.1 H12，③ 请 Renderer）：        |
| [grantsStore.ts](grantsStore.ts)                   | 授权记录（docs/plugins/extension-host.md §17.7）：唯一 owner 是本服务，文件                                   |
| [index.ts](index.ts)                               | 浏览器安全的公共入口：只导出契约。Renderer 经 @zcode/services 引到这里。                                      |
| [manifestReader.ts](manifestReader.ts)             | 读插件的 plugin.json（docs/plugins/extension-host.md §16.1）：异步 IO，只在 Window Host 运行。                |
| [mentionItems.ts](mentionItems.ts)                 | composer.mention 的候选项路由（docs/plugins/extension-host.md §16.6）：                                       |
| [modelsBackend.ts](modelsBackend.ts)               | 能力 models.list 的后端（docs/plugins/extension-host.md §18.1 H9，① 调现有服务）：                            |
| [module.ts](module.ts)                             | \* extensions-service 模块清单（architecture-governance managed 模块）。                                      |
| [node.ts](node.ts)                                 | Window Host 侧实现入口，由 @zcode/services/node 转出。                                                        |
| [notificationRelay.ts](notificationRelay.ts)       | 能力 notifications.show 在 Window Host 的一段（docs/plugins/extension-host.md §18.1 H8）：                    |
| [pluginProjects.ts](pluginProjects.ts)             | 插件项目（docs/plugins/extension-host.md §17.4，实现 P3c-2）：扩展 createSession 不带 project 时放进这里。    |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                              |
| [sessionControls.ts](sessionControls.ts)           | 插件回答审批、提问与切换权限模式（docs/plugins/extension-host.md §17.12，P3e）。                              |
| [sessionListPump.ts](sessionListPump.ts)           | 会话列表泵（docs/plugins/extension-host.md §17.5，P3b）：读 Window Host 控制器的任务投影，与桌面侧栏、        |
| [sessionReads.ts](sessionReads.ts)                 | 会话读连接（docs/plugins/extension-host.md §17.5，P3b）：插件是与手机同级的客户端，读走自己的连接。           |
| [sessionsAudit.ts](sessionsAudit.ts)               | 写动作的审计行（docs/plugins/extension-host.md §17.8，实现 P3c-1）：只从入参与结果里取身份、目标与长度，      |
| [sessionsBackend.ts](sessionsBackend.ts)           | 会话能力的后端（docs/plugins/extension-host.md §17.2、§17.3，① 调现有服务）：扩展以客户端类调用方             |
| [settingsBackend.ts](settingsBackend.ts)           | 插件设置后端（docs/plugins/extension-host.md §16.7、§18.1 H1，① 调现有服务）：                                |
| [viewRelay.ts](viewRelay.ts)                       | 扩展视图在 Window Host 的一段（docs/plugins/extension-host.md §8）：                                          |
| [windowHostExtensions.ts](windowHostExtensions.ts) | Window Host 的扩展门面实现（docs/plugins/extension-host.md §3.4、§3.5、§13、§16.1）：                         |
| [workbenchState.ts](workbenchState.ts)             | 屏幕上的会话（docs/plugins/extension-host.md §3.4、§3.5 ③）：唯一 owner 是 Renderer。                         |

<!-- qingqi-directory-index:end -->
