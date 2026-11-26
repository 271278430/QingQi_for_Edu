# telemetry

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 telemetry 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                     | 简要说明                                                                            |
| -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| [conversation-session-telemetry-parity-core.test.ts](conversation-session-telemetry-parity-core.test.ts) | 原因：旧聚合 helper 隐式创建只读文件；V4 用例显式保留工具执行前置。                 |
| [conversation-session-ttft-diagnostics.test.ts](conversation-session-ttft-diagnostics.test.ts)           | Electron bridge 移除第一个形参；形参解构会静默 ReferenceError，必须在函数体内解构。 |
| [conversation-session-ttft-local-logs.test.ts](conversation-session-ttft-local-logs.test.ts)             | 冷启动首轮可能重建订阅；先等待真实轮次结束，正向样本只验证连续在线内容。            |
| [conversation-session-ttft-stages.test.ts](conversation-session-ttft-stages.test.ts)                     | wdio-electron-service 会移除第一个形参；在函数体内解构才能真正执行窗口操作。        |
| [README.md](README.md)                                                                                   | 本目录用途、子目录与逐文件说明。                                                    |

<!-- qingqi-directory-index:end -->
