# parsers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 parsers 实现源码。

### 文件

| 文件                                   | 简要说明                                                                                         |
| -------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [critic.ts](critic.ts)                 | 实现或公开接口：parseCriticResult、dedupeReopenProposals。                                       |
| [graph-seed.ts](graph-seed.ts)         | 实现或公开接口：parseWorkflowGraphSeed、gateRootSeedNodes、normalizeWorkflowGraphSeedCandidate。 |
| [json.ts](json.ts)                     | 实现或公开接口：parsePlannerJson、isRecord、readLooseValue、readLooseArray。                     |
| [node-prompts.ts](node-prompts.ts)     | 实现或公开接口：parseWorkflowNodePromptUpdateSet。                                               |
| [planner-result.ts](planner-result.ts) | 实现或公开接口：parseWorkflowPlannerResult。                                                     |
| [README.md](README.md)                 | 本目录用途、子目录与逐文件说明。                                                                 |

<!-- qingqi-directory-index:end -->
