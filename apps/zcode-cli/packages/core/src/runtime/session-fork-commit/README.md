# session-fork-commit

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 session fork commit 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| [builders.ts](builders.ts)                 | \* Gen UI 目录随 session id 变化，子会话复制的历史里是父会话的目录。                    |
| [contract.example.ts](contract.example.ts) | 先一次分配身份，再由原子提交构建消息、Goal、notice，避免各自生成不一致引用。            |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                |
| [contract.test.ts](contract.test.ts)       | contract.test 的实现文件。                                                              |
| [contract.ts](contract.ts)                 | stable/compact-edit fork 一次性预分配的完整 child-local 身份。                          |
| [index.ts](index.ts)                       | index 的实现文件。                                                                      |
| [module.ts](module.ts)                     | 隐藏提醒（如停止后的中断标记）只记 provider/model，不带 options，不是这一点的选型事实。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                        |

<!-- qingqi-directory-index:end -->
