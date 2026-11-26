# context

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 context 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                               | 简要说明                                                                                               |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| [conversation-session-compact-actions.test.ts](conversation-session-compact-actions.test.ts)                       | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。                                    |
| [conversation-session-compact-auto.test.ts](conversation-session-compact-auto.test.ts)                             | conversation-session-compact-auto.test 的实现文件。                                                    |
| [conversation-session-compact-interrupted.test.ts](conversation-session-compact-interrupted.test.ts)               | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。                                    |
| [conversation-session-compact-manual-queue.test.ts](conversation-session-compact-manual-queue.test.ts)             | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。                                    |
| [conversation-session-compact-stream-fallback.test.ts](conversation-session-compact-stream-fallback.test.ts)       | SF 是 catalog F08 的 transport 接线门禁：compact 必须先发 stream 请求，首腿失败后才回退到 non-stream。 |
| [conversation-session-compact.test.ts](conversation-session-compact.test.ts)                                       | 旧用例使用已删除的 Chat DOM 且假定非流式摘要。当前 V4 入口与摘要协议均为流式；                         |
| [conversation-session-context-window-cold-resume.test.ts](conversation-session-context-window-cold-resume.test.ts) | 先通过真实 UI/协议创建并完成 1M 会话；再创建一个 parking 会话保持选中，                                |
| [conversation-session-instruction-file-delta.test.ts](conversation-session-instruction-file-delta.test.ts)         | IFD01–IFD04 指令文件增量公告候选（docs/conversation-session-case-catalog.md「指令文件增量公告」）。    |
| [conversation-session-memory.test.ts](conversation-session-memory.test.ts)                                         | conversation-session-memory.test 的实现文件。                                                          |
| [conversation-session-v4-compact.test.ts](conversation-session-v4-compact.test.ts)                                 | M4 门禁：compact（v4 composer slash 命令 `/compact`）。                                                |
| [README.md](README.md)                                                                                             | 本目录用途、子目录与逐文件说明。                                                                       |

<!-- qingqi-directory-index:end -->
