# hooks

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 hooks 生命周期与操作入口。

### 子目录

| 目录                                      | 存放内容                                                       |
| ----------------------------------------- | -------------------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 生命周期与操作入口。 |

### 文件

| 文件                                                                                         | 简要说明                                                                                    |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [conversation-session-hook-trust.test.ts](conversation-session-hook-trust.test.ts)           | \* 正式 E2E —— Workspace Hook Trust 软门禁与逐条持久信任（HK05–HK07）。                     |
| [conversation-session-hooks-lifecycle.test.ts](conversation-session-hooks-lifecycle.test.ts) | 工具 Hook 的 context 不进工具原文：作为批次后的提醒，每条一个 system-reminder，按顺序相邻； |
| [README.md](README.md)                                                                       | 本目录用途、子目录与逐文件说明。                                                            |

<!-- qingqi-directory-index:end -->
