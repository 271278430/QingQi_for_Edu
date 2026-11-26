# provider-tool-rounds

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 provider tool rounds 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                     |
| ------------------------------------------ | -------------------------------------------------------------------------------------------- |
| [cards.ts](cards.ts)                       | Provider 内置工具的实时卡片与持久化：客户端不执行这类工具，但要像普通工具一样                |
| [contract.example.ts](contract.example.ts) | \* provider-tool-rounds 标准调用示例：服务端执行完内置工具后，把收起的轮次写成回放 entries。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                     |
| [contract.ts](contract.ts)                 | \* Provider 内置工具轮次的公开入口（docs/design/v2/model/anthropic-stream-compat.md          |
| [module.ts](module.ts)                     | \* provider-tool-rounds 模块清单（architecture-governance managed 模块）。                   |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                             |
| [rounds.ts](rounds.ts)                     | Provider 内置工具轮次（GLM 的 analyze_image / webReader 等）。                               |

<!-- qingqi-directory-index:end -->
