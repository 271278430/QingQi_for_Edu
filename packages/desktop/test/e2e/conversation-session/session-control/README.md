# session-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 session control 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                     | 简要说明                                                                    |
| -------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [app-control-cross-project-search.test.ts](app-control-cross-project-search.test.ts)                     | 只读持久事实用于观测；被测发现必须经 Agent tool runner，不能用此 RPC 代替。 |
| [conversation-session-bot-channel-worker.test.ts](conversation-session-bot-channel-worker.test.ts)       | 默认工具注册与发送接线暂停；保留原用例及 fixture，待插件入口接入后恢复。    |
| [conversation-session-bot-continuous-worker.test.ts](conversation-session-bot-continuous-worker.test.ts) | conversation-session-bot-continuous-worker.test 的实现文件。                |
| [conversation-session-bot-topic-worker.test.ts](conversation-session-bot-topic-worker.test.ts)           | 原生 @ 指向别人时，运行中的真实 CLI 不能被停止，也不能接收对方任务。        |
| [README.md](README.md)                                                                                   | 本目录用途、子目录与逐文件说明。                                            |

<!-- qingqi-directory-index:end -->
