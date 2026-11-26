# app-control-navigation

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 app control navigation 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                                                                   |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts)     | 实现或公开接口：registerNavigationSurface。                                                                                                |
| [CONTRACT.md](CONTRACT.md)                     | 模块职责、公共接口、依赖方向和状态约定。                                                                                                   |
| [contract.ts](contract.ts)                     | 实现或公开接口：APP_NAVIGATION_IPC、appNavigationHostMessageSchema、appNavigationResultMessageSchema、appNavigationRendererMessageSchema。 |
| [discovery-contract.ts](discovery-contract.ts) | 只读发现的连接证明；读取后由调用者复验，不能用于正文或写操作授权。                                                                         |
| [electronBridge.ts](electronBridge.ts)         | 同一窗口只创建一次 surface 与监听器。reload 只失效 renderer generation，不替换 owner。                                                     |
| [host.ts](host.ts)                             | 旧 Server 也可能注册兼容项目服务；必须核对握手能力，不能借兼容投影扩大只读发现范围。                                                       |
| [hostBridge.ts](hostBridge.ts)                 | 只关联在途导航 RPC；项目权限与会话事实仍由 AppControlService 校验。                                                                        |
| [index.ts](index.ts)                           | index 的实现文件。                                                                                                                         |
| [main.ts](main.ts)                             | main 的实现文件。                                                                                                                          |
| [module.ts](module.ts)                         | 实现或公开接口：appControlNavigationModule。                                                                                               |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                                                                           |
| [renderer.ts](renderer.ts)                     | renderer 的实现文件。                                                                                                                      |
| [rendererBridge.ts](rendererBridge.ts)         | 同一窗口只有一个导航意图，新请求让旧远端连接结果失去选择资格。                                                                             |
| [windowBridge.ts](windowBridge.ts)             | BrowserWindow 生命周期内的在途关联；不持有 session、项目或已接纳命令状态。                                                                 |

<!-- qingqi-directory-index:end -->
