# plugin-discovery

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 plugin discovery 实现源码。

### 文件

| 文件                                       | 简要说明                                                               |
| ------------------------------------------ | ---------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 搜索只读取官方目录；即使有命中，也需要另一个经用户确认的动作才能安装。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                               |
| [contract.ts](contract.ts)                 | contract 的实现文件。                                                  |
| [module.ts](module.ts)                     | 实现或公开接口：agentPluginDiscoveryModule。                           |
| [port.ts](port.ts)                         | 同一工具调用的重复派发采用结果；不同调用仍需各自用户确认。             |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                       |
| [refresh.ts](refresh.ts)                   | 目标插件存储根持有刷新事实；不把 UI 的模块变量当作跨端权威。           |
| [search.ts](search.ts)                     | 汉字不能跨标点、语言或字段拼接；单汉字只通过完整名称命中。             |
| [subscription.ts](subscription.ts)         | 旧客户端严格解析交互 kind；只裁剪该连接的载荷，保留原序号和其他交互。  |

<!-- qingqi-directory-index:end -->
