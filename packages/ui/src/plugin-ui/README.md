# plugin-ui

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 plugin ui 实现源码。

### 子目录

| 目录                                | 存放内容                                             |
| ----------------------------------- | ---------------------------------------------------- |
| [adapters/](adapters/README.md)     | @zcode/ui 基础工程中的 adapters 外部能力与平台适配。 |
| [app/](app/README.md)               | @zcode/ui 基础工程中的 app 实现源码。                |
| [components/](components/README.md) | @zcode/ui 基础工程中的 components 界面组件。         |
| [domain/](domain/README.md)         | @zcode/ui 基础工程中的 domain 实现源码。             |
| [sidePane/](sidePane/README.md)     | @zcode/ui 基础工程中的 sidePane 实现源码。           |

### 文件

| 文件                                                   | 简要说明                                                                                    |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)             | 内联卡片 / 面板入口请求打开侧栏时的载荷，以及据此创建的 tab。                               |
| [CONTRACT.md](CONTRACT.md)                             | 模块职责、公共接口、依赖方向和状态约定。                                                    |
| [contract.ts](contract.ts)                             | \* 从 ToolCallRow.display.ui 读出的插件 UI 呈现信息；与 agent 侧 `display.ui` schema 同构， |
| [hostPrimitives.ts](hostPrimitives.ts)                 | Shared sandbox transport/presentation and existing session admission binding.               |
| [index.ts](index.ts)                                   | index 的实现文件。                                                                          |
| [module.ts](module.ts)                                 | \* plugin-ui 模块清单（architecture-governance managed 模块）。                             |
| [officeViewerOpen.ts](officeViewerOpen.ts)             | \* `.xlsx` 文件打开到内置查看面板的路由表：扩展名 → 插件 surface。                          |
| [PluginUiSidePane.tsx](PluginUiSidePane.tsx)           | 页面请求回到 inline 时宿主关闭本 tab。                                                      |
| [PluginUiToolCallBlock.tsx](PluginUiToolCallBlock.tsx) | 宿主工具行渲染插槽，普通 MCP 卡片作为模块外的展示依赖注入。                                 |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                            |

<!-- qingqi-directory-index:end -->
