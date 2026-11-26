# hooks

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 hooks 生命周期与操作入口。

### 文件

| 文件                                                             | 简要说明                                                                                            |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [hooks.ts](hooks.ts)                                             | \* 加载 workspace 的 hooks 配置                                                                     |
| [hooksService.ts](hooksService.ts)                               | Trust identity resolver 的只读文件端口（Host 侧 node:fs/promises 适配）。                           |
| [index.ts](index.ts)                                             | index 的实现文件。                                                                                  |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                                    |
| [workspaceHookConfigMutation.ts](workspaceHookConfigMutation.ts) | workspaceHookConfigMutation 的实现文件。                                                            |
| [workspaceHookSettingsModel.ts](workspaceHookSettingsModel.ts)   | 实现或公开接口：LegacyHookDefinition、LegacyHooksConfig、fromProjectSnapshot、fromUserZCodeSource。 |

<!-- qingqi-directory-index:end -->
