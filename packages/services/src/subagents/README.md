# subagents

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 subagents 实现源码。

### 文件

| 文件                                                   | 简要说明                                                                                                            |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                                                    |
| [subagentConfigScope.ts](subagentConfigScope.ts)       | 一个配置范围串行吸收文件变化，RPC 只消费上层已完成的 snapshot。                                                     |
| [subagentMarkdown.ts](subagentMarkdown.ts)             | runtime 使用 loose frontmatter 语义；Settings 也按同一语义读取，                                                    |
| [subagentModelSelection.ts](subagentModelSelection.ts) | 实现或公开接口：normalizeSubagentModelSelection。                                                                   |
| [subagentRuntimeConfig.ts](subagentRuntimeConfig.ts)   | 自定义 profile 的发现范围与 depth:0 监听一致，避免深层定义只在重扫时变化。                                          |
| [subagents.ts](subagents.ts)                           | 只写用户 state 的完整覆盖，不改插件 Markdown。                                                                      |
| [subagentsService.ts](subagentsService.ts)             | 仅供旧版本回滚保留；新版存在选择字段后，禁止再从这两个字段恢复覆盖。                                                |
| [subagentStorage.ts](subagentStorage.ts)               | 实现或公开接口：SubagentStorageOptions、resolveUserHomeDir、resolveUserSubagentRoot、resolveWorkspaceSubagentRoot。 |

<!-- qingqi-directory-index:end -->
