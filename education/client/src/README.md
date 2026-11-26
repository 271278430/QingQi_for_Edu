# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

HTTP、SSE、图片、模型和系统管理的公共通信契约。

### 文件

| 文件                                                 | 简要说明                                                                                                         |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [chat-model-contract.ts](chat-model-contract.ts)     | 会话模型列表、角色选择与推理档位的类型契约。                                                                     |
| [contract.example.ts](contract.example.ts)           | 实现或公开接口：identityAnimationExample、identityStoryExample、initializeStudent、nonnegativeReasoningExample。 |
| [CONTRACT.md](CONTRACT.md)                           | 模块职责、公共接口、依赖方向和状态约定。                                                                         |
| [contract.ts](contract.ts)                           | 实现或公开接口：Bootstrap、Session、Evidence、TeachingRequest。                                                  |
| [http.ts](http.ts)                                   | 带会话、CSRF和错误处理的HTTP客户端，解析SSE增量回复。                                                            |
| [index.ts](index.ts)                                 | index 的实现文件。                                                                                               |
| [management-contract.ts](management-contract.ts)     | 模型、系统管理与架构目录的无密钥类型契约。                                                                       |
| [module.ts](module.ts)                               | module 的实现文件。                                                                                              |
| [problem-reasoning.ts](problem-reasoning.ts)         | 函数与几何解题过程的可视化数据结构。                                                                             |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                                                 |
| [student-task-contract.ts](student-task-contract.ts) | 题卡、学习摘要和学生任务结果的公共类型。                                                                         |
| [teaching-decision.ts](teaching-decision.ts)         | 教学方式、当前小问与响应预算的数据结构。                                                                         |
| [teaching-visual.ts](teaching-visual.ts)             | 单张教学图与动画的展示数据结构。                                                                                 |

<!-- qingqi-directory-index:end -->
