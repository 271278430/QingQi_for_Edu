# session-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 session control 实现源码。

### 文件

| 文件                                       | 简要说明                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：bindCliSessionControl。                                               |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                              |
| [contract.test.ts](contract.test.ts)       | contract.test 的实现文件。                                                            |
| [contract.ts](contract.ts)                 | taskType 的子会话种类并不都使用 runtimeScope=subagent，必须从同一入口收口注册与执行。 |
| [index.ts](index.ts)                       | \* 规格 0.11 / 0.14：模型只看 `tool` 变体——没有完整引用，也没有 `requestId`。         |
| [module.ts](module.ts)                     | 实现或公开接口：sessionControlToolsModule。                                           |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
