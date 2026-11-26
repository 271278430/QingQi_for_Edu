# theme

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/tui 基础工程中的 theme 实现源码。

### 文件

| 文件                                   | 简要说明                                                                                            |
| -------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [defaults.ts](defaults.ts)             | 实现或公开接口：DEFAULT_TUI_THEME_MODE、DARK_TUI_THEME、LIGHT_TUI_THEME、BUILTIN_TUI_THEMES。       |
| [index.ts](index.ts)                   | index 的实现文件。                                                                                  |
| [legacy-palette.ts](legacy-palette.ts) | 实现或公开接口：themeToLegacyPalette、palette。                                                     |
| [README.md](README.md)                 | 本目录用途、子目录与逐文件说明。                                                                    |
| [state.ts](state.ts)                   | 实现或公开接口：activeTuiTheme、getActiveTuiThemeMode、setActiveTuiThemeMode、resolveTuiThemeMode。 |
| [terminal.ts](terminal.ts)             | 实现或公开接口：resolveInitialTerminalThemeMode、inferThemeModeFromTerminalColors。                 |
| [types.ts](types.ts)                   | 实现或公开接口：TuiThemeTokens、TuiLegacyPalette。                                                  |

<!-- qingqi-directory-index:end -->
