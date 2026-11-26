# adapters

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 adapters 外部能力与平台适配。

### 文件

| 文件                                                           | 简要说明                                                                                                     |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [messagePortTransport.ts](messagePortTransport.ts)             | \* 宿主 renderer 侧的 MCP `Transport`：一条 MessagePort（main 建的 channel 的 port2）上跑原始 JSON-RPC，     |
| [pluginUiBackground.ts](pluginUiBackground.ts)                 | 窗口订阅真实工具结果；会话组件卸载不会撤掉创建入口。                                                         |
| [PluginUiBackgroundHost.tsx](PluginUiBackgroundHost.tsx)       | 实现或公开接口：PluginUiBackgroundHost。                                                                     |
| [pluginUiDownloads.ts](pluginUiDownloads.ts)                   | 桌面 IPlatformService.saveFile：原生另存为对话框；main 侧再做一次 50 MiB 与文件名校验。                      |
| [pluginUiHostTypes.ts](pluginUiHostTypes.ts)                   | 投喂的是哪次调用；变化（面板换到新一次调用）时把 toolInput 作为 tool-input 通知推给页面。                    |
| [pluginUiInteractions.ts](pluginUiInteractions.ts)             | 工具卡片或面板；决定 widgetState 的 surfaceKey 以及来源标记 / 上下文 id。                                    |
| [pluginUiManagedPage.ts](pluginUiManagedPage.ts)               | 实现或公开接口：createPage。                                                                                 |
| [PluginUiModelContextChip.tsx](PluginUiModelContextChip.tsx)   | composer 与历史用户消息共用的"插件上下文"pill；与 WebElementContextAttachmentChip 同构。                     |
| [pluginUiModelContextEvents.ts](pluginUiModelContextEvents.ts) | 待发送上下文随 session 保存在窗口内；卸载 Composer 只撤销投递能力。                                          |
| [pluginUiPagePlane.ts](pluginUiPagePlane.ts)                   | \* 非主 frame 导航是否指向沙箱文档（插件 frame 自身重载）。webview 的 did-start-navigation 不带 frame 层级； |
| [pluginUiPageRegistry.ts](pluginUiPageRegistry.ts)             | 冷后台页面没有 visibility 边沿，也必须启动普通页面的五分钟期限。                                             |
| [pluginUiPaneSession.ts](pluginUiPaneSession.ts)               | 这里只投影挂载 pane 的有效绑定；创建、换代与回收仍由草稿协调器唯一持有。                                     |
| [PluginUiProviders.tsx](PluginUiProviders.tsx)                 | Shell 只在边界提供面板动作，中间布局组件不感知插件请求。                                                     |
| [pluginUiResourceDeltaFeed.ts](pluginUiResourceDeltaFeed.ts)   | \* 把一个会话投影 store 的 live-only 增量接到资源通知路由表。                                                |
| [pluginUiSessionActions.ts](pluginUiSessionActions.ts)         | 实现或公开接口：registerPluginUiSessionActions、getPluginUiSessionActions。                                  |
| [pluginUiSessionBinding.ts](pluginUiSessionBinding.ts)         | 会话动作统一翻译 ACK；状态与发送配置始终由原会话入口管理。                                                   |
| [pluginUiStateKey.ts](pluginUiStateKey.ts)                     | 页面只需要稳定标识，不能把包含工作区路径与会话身份的内部键直接下发。                                         |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                             |
| [readPluginUiStyleVariables.ts](readPluginUiStyleVariables.ts) | \* 从宿主根元素读主题 token 的计算值（`.dark` / zai 主题类切换后随之变化），                                 |
| [sandboxPageOwners.ts](sandboxPageOwners.ts)                   | 实现或公开接口：SandboxPageOwner、sandboxPages、onSandboxPageRemoved。                                       |
| [useMarketPluginUi.ts](useMarketPluginUi.ts)                   | 市场只接现有会话与面板契约；不创建会话，也不保存另一份安装状态。                                             |
| [usePluginUiContextImages.ts](usePluginUiContextImages.ts)     | \* 撤附件的语义按调用方区分，插件上下文保持原有行为：                                                        |
| [usePluginUiHost.ts](usePluginUiHost.ts)                       | 锚点订阅唯一窗口 owner；切位置、重渲染和卡片卸载不销毁页面。                                                 |
| [usePluginUiSidePaneModel.tsx](usePluginUiSidePaneModel.tsx)   | 4b-2 R4：侧栏不在 SessionPane 树内，自己把会话投影的资源通知接到路由表（按 store 引用计数，不重复投递）。    |
| [usePluginUiSurfaces.ts](usePluginUiSurfaces.ts)               | false 时不拉取（无会话 / 平台不支持），返回空数组。                                                          |
| [usePluginUiToolCallModel.ts](usePluginUiToolCallModel.ts)     | 工具行到插件 UI 的适配；React 生命周期与宿主动作集中于此，视图只接收展示模型。                               |
| [useRecommendedUiPlugins.ts](useRecommendedUiPlugins.ts)       | 推荐曝光读取完整市场目录；安装和启用继续由现有管理 store 与 CLI 负责。                                       |
| [useUiPluginRecommendations.ts](useUiPluginRecommendations.ts) | 缓存和请求合并归 Host 配置服务；此处只持有当前入口的展示投影。                                               |

<!-- qingqi-directory-index:end -->
