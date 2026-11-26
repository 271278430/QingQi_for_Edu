# conversation-user-input-presentation

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 conversation user input presentation 实现源码。

### 文件

| 文件                                       | 简要说明                                                 |
| ------------------------------------------ | -------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：userInputPresentationExample。           |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                 |
| [contract.ts](contract.ts)                 | 展示输入以实际组件为唯一类型源，调用方继续持有消息状态。 |
| [module.ts](module.ts)                     | 用户消息正文组合的展示层归属；不拥有消息或队列状态。     |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                         |

<!-- qingqi-directory-index:end -->
