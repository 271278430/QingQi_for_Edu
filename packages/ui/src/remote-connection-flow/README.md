# remote-connection-flow

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 remote connection flow 实现源码。

### 子目录

| 目录                | 存放内容                             |
| ------------------- | ------------------------------------ |
| [ui/](ui/README.md) | @zcode/ui 基础工程中的 ui 实现源码。 |

### 文件

| 文件                                                                   | 简要说明                                                                       |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts)                             | 项目向导在设备连通后接管选目录；保存成功前不会准备会话。                       |
| [CONTRACT.md](CONTRACT.md)                                             | 模块职责、公共接口、依赖方向和状态约定。                                       |
| [contract.ts](contract.ts)                                             | 新的显式入口；卡片恢复不改变该标识。                                           |
| [index.ts](index.ts)                                                   | 实现或公开接口：useRemoteConnectionFlow。                                      |
| [module.ts](module.ts)                                                 | \* remote-connection-flow 模块清单（architecture-governance managed 模块）。   |
| [README.md](README.md)                                                 | 本目录用途、子目录与逐文件说明。                                               |
| [requestRemoteProjectConnection.ts](requestRemoteProjectConnection.ts) | 只分派用户意图；连接状态、失败和日志仍归 Root/Host，向导仅接管需要交互的流程。 |

<!-- qingqi-directory-index:end -->
