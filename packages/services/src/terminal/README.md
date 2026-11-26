# terminal

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 terminal 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                    |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                            |
| [terminal.ts](terminal.ts)                         | 启动 cwd 位于 path 内的终端 id；只看启动目录，shell 内 cd 不追踪。                          |
| [terminalProfile.ts](terminalProfile.ts)           | 实现或公开接口：resolveTerminalFontProfile。                                                |
| [terminalProfileMacOs.ts](terminalProfileMacOs.ts) | macOS 终端来源只是 best-effort 插件，plist 缺失、二进制格式异常或 plutil 失败都应静默跳过。 |
| [terminalProfileTypes.ts](terminalProfileTypes.ts) | 实现或公开接口：TerminalFontFamilySource、TerminalThemeProfile、TerminalDetectedProfile。   |
| [terminalService.ts](terminalService.ts)           | 启动时的工作目录；shell 内 cd 之后的目录无法追踪（docs/git/worktree.md §12 第 4 项）。      |

<!-- qingqi-directory-index:end -->
