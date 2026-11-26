# handlers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/cli 基础工程中的 handlers 实现源码。

### 文件

| 文件                     | 简要说明                                                                                  |
| ------------------------ | ----------------------------------------------------------------------------------------- |
| [custom.ts](custom.ts)   | 实现或公开接口：handleCustomCommand。                                                     |
| [dwf.ts](dwf.ts)         | `/dwf list` 的默认条数；服务端自己还有上限，这里只表达「一屏够看」。                      |
| [effort.ts](effort.ts)   | 实现或公开接口：handleEffortCommand。                                                     |
| [expert.ts](expert.ts)   | 实现或公开接口：handleExpertCommand。                                                     |
| [goal.ts](goal.ts)       | 实现或公开接口：handleTargetCommand。                                                     |
| [locale.ts](locale.ts)   | 实现或公开接口：handleLocaleCommand。                                                     |
| [mcp.ts](mcp.ts)         | error 可能含多行 stderr 诊断；列表只留首行，完整内容在设置页查看。                        |
| [mode.ts](mode.ts)       | 实现或公开接口：handleModeCommand。                                                       |
| [model.ts](model.ts)     | A deliberate new selection uses the catalog default; restored selections never pass here. |
| [plugins.ts](plugins.ts) | 斜杠命令是无状态的，无法做交互式 y/N；卸载这种破坏性操作改用显式 --force 作为确认闸门。   |
| [README.md](README.md)   | 本目录用途、子目录与逐文件说明。                                                          |
| [skill.ts](skill.ts)     | 实现或公开接口：handleSkillListCommand。                                                  |

<!-- qingqi-directory-index:end -->
