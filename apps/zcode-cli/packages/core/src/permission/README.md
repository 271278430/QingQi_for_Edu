# permission

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 permission 实现源码。

### 文件

| 文件                                             | 简要说明                                                                            |
| ------------------------------------------------ | ----------------------------------------------------------------------------------- |
| [broker.ts](broker.ts)                           | Permission Broker - async client permission coordination                            |
| [index.ts](index.ts)                             | Permission exports                                                                  |
| [plan-mode-policy.ts](plan-mode-policy.ts)       | 实现或公开接口：PlanModeTransitionPermission、resolvePlanModeTransitionPermission。 |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                    |
| [rule-matching.ts](rule-matching.ts)             | 实现或公开接口：wildcardToRegExp、domainRuleSubject、webFetchRuleSubjects。         |
| [service.ts](service.ts)                         | Permission Service - Permission checking and decision making                        |
| [workflow-draft-path.ts](workflow-draft-path.ts) | Workflow draft path - 「这个写入目标落在草稿目录里吗」的纯判定                      |

<!-- qingqi-directory-index:end -->
