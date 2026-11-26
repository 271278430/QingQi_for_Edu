# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                                 | 简要说明                                                              |
| -------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| [conversation-session-compact-auto-actions.test.ts](conversation-session-compact-auto-actions.test.ts)               | 当前 planner 保留最近一轮；仅一轮历史没有可压缩分区，必须先完成两轮。 |
| [conversation-session-compact-timeline-projection.test.ts](conversation-session-compact-timeline-projection.test.ts) | planner 保留最近一轮；只造一轮高 usage 无法形成可压缩前缀。           |
| [README.md](README.md)                                                                                               | 本目录用途、子目录与逐文件说明。                                      |

<!-- qingqi-directory-index:end -->
