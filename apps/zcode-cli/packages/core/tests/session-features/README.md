# session-features

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 session features 验收与回归场景。

### 文件

| 文件                                                                     | 简要说明                                                                                                            |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| [contract.test.ts](contract.test.ts)                                     | 行为与失败路径见 session-features.test.ts；本契约钉住打点入口与读取快照的形状。                                     |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                                    |
| [session-features.test.ts](session-features.test.ts)                     | 规格：docs/design/v2/model/session-features-header.md。                                                             |
| [tool-search-turn.test.ts](tool-search-turn.test.ts)                     | 规格：docs/design/v2/model/session-features-header.md 的 ToolSearch 标签：主循环打点与旁路请求。                    |
| [tool-search.test.ts](tool-search.test.ts)                               | 规格：docs/design/v2/model/session-features-header.md 的 ToolSearch 标签；主循环端到端见 tool-search-turn.test.ts。 |
| [workflow-auto-attempt-turn.test.ts](workflow-auto-attempt-turn.test.ts) | 规格：docs/design/v2/model/session-features-header.md「CreateWorkflow 尝试口径的补充规则」。                        |
| [workflow-auto-attempt.test.ts](workflow-auto-attempt.test.ts)           | 规格：docs/design/v2/model/session-features-header.md「CreateWorkflow 尝试口径的补充规则」。                        |

<!-- qingqi-directory-index:end -->
