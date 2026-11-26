# session-features

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 session features 实现源码。

### 文件

| 文件                                       | 简要说明                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 打点后，同一 runtime 发出的下一次模型请求读到的快照里就有这个标签。            |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                       |
| [contract.ts](contract.ts)                 | \* 会话能力标签的公开入口（docs/design/v2/model/session-features-header.md）。 |
| [module.ts](module.ts)                     | \* session-features 模块清单（architecture-governance managed 模块）。         |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                               |
| [session-features.ts](session-features.ts) | 会话能力标签的 owner（docs/design/v2/model/session-features-header.md）        |

<!-- qingqi-directory-index:end -->
