# plugin-discovery

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 plugin discovery 实现源码。

### 文件

| 文件                                       | 简要说明                                                   |
| ------------------------------------------ | ---------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 客户端只展示经过校验的官方 ID 和请求动作，不接收下载地址。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                   |
| [contract.ts](contract.ts)                 | contract 的实现文件。                                      |
| [module.ts](module.ts)                     | 实现或公开接口：pluginInstallInteractionModule。           |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                           |

<!-- qingqi-directory-index:end -->
