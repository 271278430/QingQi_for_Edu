# conversation-workspace-target

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 conversation workspace target 实现源码。

### 文件

| 文件                                       | 简要说明                                                                               |
| ------------------------------------------ | -------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | Root 从当前窗口注入只读查询与既有打开操作，每次调用读取最新事实。                      |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                               |
| [contract.ts](contract.ts)                 | 仅描述解析所需的只读视图；tab 的生命周期仍由窗口 store 管理。                          |
| [index.ts](index.ts)                       | index 的实现文件。                                                                     |
| [module.ts](module.ts)                     | \* conversation-workspace-target 模块清单（architecture-governance managed 模块）。    |
| [PluginAddMenu.tsx](PluginAddMenu.tsx)     | 市场顶栏与相邻动作统一 secondary + lg；设置页插件区保持默认主按钮。                    |
| [purpose.ts](purpose.ts)                   | 远程无项目聊天只保留历史数据，不进入任何 UI 导航或恢复候选。                           |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                       |
| [resolve.ts](resolve.ts)                   | 解析本地“在项目外工作”的目标，远程项目不提供该操作。                                   |
| [sourceIdentity.ts](sourceIdentity.ts)     | Direct URL Server 不属于 Source 管理域；不能仅凭相同的 identity 格式冒充 Source 设备。 |
| [usePluginCreator.ts](usePluginCreator.ts) | 实现或公开接口：usePluginCreator。                                                     |
| [workbenchTarget.ts](workbenchTarget.ts)   | 实现或公开接口：WorkbenchNewTaskTarget、resolveWorkbenchNewTaskTarget。                |

<!-- qingqi-directory-index:end -->
