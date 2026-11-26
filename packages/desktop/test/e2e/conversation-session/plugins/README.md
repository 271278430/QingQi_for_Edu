# plugins

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 plugins 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                                       | 简要说明                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| [conversation-session-mcp-oauth-status-isolation.test.ts](conversation-session-mcp-oauth-status-isolation.test.ts)                         | 修复原因：旧实现的 1s OAuth poll                                                               |
| [conversation-session-plugin-builtin-workspace-disable.test.ts](conversation-session-plugin-builtin-workspace-disable.test.ts)             | conversation-session-plugin-builtin-workspace-disable.test 的实现文件。                        |
| [conversation-session-plugin-marketplace-installed-roundtrip.test.ts](conversation-session-plugin-marketplace-installed-roundtrip.test.ts) | 先在 User 视图保存一个值，Workspace 视图应显示它，但不能把其它 default                         |
| [conversation-session-plugin-mcp-skill-disabled.test.ts](conversation-session-plugin-mcp-skill-disabled.test.ts)                           | 状态 C：插件 MCP skill 已安装但被禁用。                                                        |
| [conversation-session-plugin-mcp-skill-installed-enabled.test.ts](conversation-session-plugin-mcp-skill-installed-enabled.test.ts)         | 状态 B：插件 MCP skill 已安装并启用。                                                          |
| [conversation-session-plugin-mcp-skill-not-installed.test.ts](conversation-session-plugin-mcp-skill-not-installed.test.ts)                 | 状态 A：插件 MCP skill 未安装基线。                                                            |
| [conversation-session-plugin-mcp-skill-workspace-disabled.test.ts](conversation-session-plugin-mcp-skill-workspace-disabled.test.ts)       | resident App 的 Plugin catalog 在创建时冻结；先用 seed 的显式 false 验证新 Session             |
| [conversation-session-plugin-mcp-skill-workspace-enabled.test.ts](conversation-session-plugin-mcp-skill-workspace-enabled.test.ts)         | 仅用于验证隔离 fixture 的配置值；拆分字符串避免 fixture checker 把配置值误判为 prompt marker。 |
| [conversation-session-plugin-mcp-skill-workspace-inherited.test.ts](conversation-session-plugin-mcp-skill-workspace-inherited.test.ts)     | User/Workspace 是同一 Host inventory 的两个配置视图。切到 Workspace 后仍应看到                 |
| [conversation-session-plugin-mcp-skill-workspace-isolation.test.ts](conversation-session-plugin-mcp-skill-workspace-isolation.test.ts)     | conversation-session-plugin-mcp-skill-workspace-isolation.test 的实现文件。                    |
| [conversation-session-plugin-mcp-skill-workspace-root.test.ts](conversation-session-plugin-mcp-skill-workspace-root.test.ts)               | 仓库中的目录声明不是用户安装授权，真实模型请求不能携带该插件的 MCP 工具。                      |
| [conversation-session-plugin-missing-package-workspace.test.ts](conversation-session-plugin-missing-package-workspace.test.ts)             | 新草稿会恢复初始权限模式；必须在实际发送的草稿上开启完全访问，避免停在工具审批。               |
| [conversation-session-plugin-reference-append-only-resume.test.ts](conversation-session-plugin-reference-append-only-resume.test.ts)       | PLG13 / PLG14 provider-wire 候选：                                                             |
| [conversation-session-plugin-reference-subagent.test.ts](conversation-session-plugin-reference-subagent.test.ts)                           | PLG16 formal E2E：Plugin 引用的 model-only system reminder 必须把该 Plugin                     |
| [conversation-session-plugin-reference.test.ts](conversation-session-plugin-reference.test.ts)                                             | PLG01（wire 半区）+ PLG12/PLG15（商店试用）+ S01（plugins 分组半区）formal E2E：               |
| [conversation-session-plugin-resident-freeze-cold-resume.test.ts](conversation-session-plugin-resident-freeze-cold-resume.test.ts)         | 准备阶段已进入项目空草稿；设置权限后再新建会丢失该草稿的 full-access 选择。                    |
| [conversation-session-plugin-store-try-states.test.ts](conversation-session-plugin-store-try-states.test.ts)                               | 修复原因：录屏只是视觉复核证据，runner 缺 ffmpeg 时 stop() 编码会报 spawn ENOENT，             |
| [conversation-session-plugin-workspace-marketplace.test.ts](conversation-session-plugin-workspace-marketplace.test.ts)                     | 插件 bridge 由 workspace App 注册，不能在全局未归类草稿等待它出现。                            |
| [conversation-session-workspace-mcp-trust.test.ts](conversation-session-workspace-mcp-trust.test.ts)                                       | 仅为人工评审保留可读画面；状态就绪仍由下面的断言等待。                                         |
| [README.md](README.md)                                                                                                                     | 本目录用途、子目录与逐文件说明。                                                               |

<!-- qingqi-directory-index:end -->
