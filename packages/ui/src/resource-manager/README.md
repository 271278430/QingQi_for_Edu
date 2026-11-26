# resource-manager

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 resource manager 实现源码。

### 子目录

| 目录                          | 存放内容                                  |
| ----------------------------- | ----------------------------------------- |
| [storage/](storage/README.md) | @zcode/ui 基础工程中的 storage 实现源码。 |

### 文件

| 文件                                             | 简要说明                                                                                  |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)       | Desktop preload 注入既有快照查询与采样启停，不在 UI 重新归属进程。                        |
| [CONTRACT.md](CONTRACT.md)                       | 模块职责、公共接口、依赖方向和状态约定。                                                  |
| [contract.ts](contract.ts)                       | 指标由 Host/Main 提供；UI 只持有展示快照和展开状态。                                      |
| [module.ts](module.ts)                           | 资源管理器现有 Host 采样与 UI 展示边界；不创建新的运行时 owner。                          |
| [NetworkSection.tsx](NetworkSection.tsx)         | 网络页只轮询有界投影；采集生命周期属于 Main 中的窗口。                                    |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                          |
| [ResourceManagerApp.tsx](ResourceManagerApp.tsx) | 组件放在 packages/ui 内是为了纳入 Tailwind 扫描；desktop 的独立 renderer 入口只负责挂载。 |
| [resourceUsageParts.tsx](resourceUsageParts.tsx) | \* 资源管理器 CPU / 内存 tab 的展示零件：双层指标卡、分组列表、进程行。                   |
| [resourceUsageView.ts](resourceUsageView.ts)     | 四组固定顺序：基础服务 / 任务进程 / 内置插件 / 社区插件                                   |

<!-- qingqi-directory-index:end -->
