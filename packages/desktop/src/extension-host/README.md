# extension-host

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 extension host 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                            |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| [capabilityClient.ts](capabilityClient.ts) | 能力部分的通用包装（docs/plugins/extension-host.md §7.2）：                                         |
| [contract.example.ts](contract.example.ts) | Main 的用法：创建一次；每个 Window Host spawn 后登记；退出屏障里并行 dispose。                      |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                            |
| [contract.ts](contract.ts)                 | extension-host 模块的公开契约（docs/plugins/extension-host.md §4、§12.1）。                         |
| [extensionContext.ts](extensionContext.ts) | 按插件创建的 ctx（docs/plugins/extension-host.md §7.1）。ctx 及其子对象冻结；                       |
| [index.ts](index.ts)                       | 全 App 唯一的扩展进程（docs/plugins/extension-host.md）：由 Main 的监管器                           |
| [module.ts](module.ts)                     | \* extension-host 模块清单（architecture-governance managed 模块）。                                |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                    |
| [registry.ts](registry.ts)                 | 扩展注册表：贡献表的唯一 owner（docs/plugins/extension-host.md §3.4、§6、§12.2、§13、§16.1）。      |
| [runtime.ts](runtime.ts)                   | 扩展进程的运行时护栏（docs/plugins/extension-host.md §7.1）：                                       |
| [viewHost.ts](viewHost.ts)                 | 扩展视图实例（docs/plugins/extension-host.md §8）：两种写法都经进程内 transport 连一个 MCP Client， |
| [viewServer.ts](viewServer.ts)             | 扩展视图写法一（docs/plugins/extension-host.md §8）：宿主把 ViewDefinition 包成一个 MCP server。    |
| [windowConnection.ts](windowConnection.ts) | L1 连接（docs/plugins/extension-host.md §3.2）：Main 牵线的端口上跑双向 @zcode/rpc。                |

<!-- qingqi-directory-index:end -->
