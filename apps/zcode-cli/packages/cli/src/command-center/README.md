# command-center

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/cli 基础工程中的 command center 实现源码。

### 子目录

| 目录                            | 存放内容                                    |
| ------------------------------- | ------------------------------------------- |
| [handlers/](handlers/README.md) | @zcode/cli 基础工程中的 handlers 实现源码。 |

### 文件

| 文件                                             | 简要说明                                                                                                |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [create.ts](create.ts)                           | 实现或公开接口：createCommandCenter。                                                                   |
| [effort-options.ts](effort-options.ts)           | 实现或公开接口：listAppEffortOptions、thoughtLevelsToEffortOptions。                                    |
| [formatters.ts](formatters.ts)                   | 实现或公开接口：formatResumeResult、formatNewSessionResult。                                            |
| [history.ts](history.ts)                         | Input history is recall UX; command execution must not depend on it.                                    |
| [login-flow.ts](login-flow.ts)                   | 实现或公开接口：buildLoginSelection、loginSetupResponse、formatLoginResult、formatProviderSetupResult。 |
| [metadata.ts](metadata.ts)                       | 实现或公开接口：normalizeTuiPromptInput、attachCurrentSessionMetadata。                                 |
| [model-selection.ts](model-selection.ts)         | 会话切换已经成功；偏好写入失败只追加提示，不能把成功的切换报告成失败。                                  |
| [modes.ts](modes.ts)                             | 菜单不再推荐 Edit；显式旧命令仍由完整值域校验，不触发模式迁移。                                         |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                                        |
| [selections.ts](selections.ts)                   | 实现或公开接口：buildSessionSelection、buildCheckpointSelection、buildTargetReplaceSelection。          |
| [slash-command-help.ts](slash-command-help.ts)   | slash-command-help 的实现文件。                                                                         |
| [slash-command-types.ts](slash-command-types.ts) | 实现或公开接口：SlashCommand。                                                                          |
| [slash-commands.ts](slash-commands.ts)           | 缺席不设门（单测、嵌入方）；CLI 入口总会传入解析后的 `--workflow-mode`。                                |
| [types.ts](types.ts)                             | null 表示该插件未安装（幂等 no-op）。                                                                   |
| [utils.ts](utils.ts)                             | 实现或公开接口：splitArgs、shortText、shortId、formatTime。                                             |

<!-- qingqi-directory-index:end -->
