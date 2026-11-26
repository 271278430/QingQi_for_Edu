# active-transcript

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 active transcript 实现源码。

### 文件

| 文件                                       | 简要说明                                                          |
| ------------------------------------------ | ----------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 读取方先取持久消息、会话行与 rewind 事件，再投影 active 分支。    |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                          |
| [contract.test.ts](contract.test.ts)       | contract.test 的实现文件。                                        |
| [contract.ts](contract.ts)                 | contract 的实现文件。                                             |
| [index.ts](index.ts)                       | 会话 active 分支投影：协议读取与独立 CLI 会话读取共用同一份规则。 |
| [module.ts](module.ts)                     | 实现或公开接口：activeTranscriptModule。                          |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                  |

<!-- qingqi-directory-index:end -->
