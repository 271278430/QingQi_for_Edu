# quickpick

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 quickpick 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                                                                                                          |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [conversationFindSearch.ts](conversationFindSearch.ts)   | 实现或公开接口：resolveConversationFindNavigationDirection、getConversationFindState、moveConversationFindSelection、resolveConversationFindNavigationSelection。 |
| [HighlightedMatchText.tsx](HighlightedMatchText.tsx)     | 实现或公开接口：findTextMatchRanges、HighlightedMatchText。                                                                                                       |
| [QuickPickCommandDialog.tsx](QuickPickCommandDialog.tsx) | 实现或公开接口：QuickPickCommandDialog。                                                                                                                          |
| [quickPickCommandIcons.tsx](quickPickCommandIcons.tsx)   | 实现或公开接口：QUICK_PICK_ICON_BY_KIND。                                                                                                                         |
| [quickPickCommands.ts](quickPickCommands.ts)             | 只有桌面本机 Host 提供扩展门面时才有（docs/plugins/extension-host.md §12.1）。                                                                                    |
| [quickPickStyles.ts](quickPickStyles.ts)                 | 实现或公开接口：quickPickDialogClassName、quickPickCommandClassName、quickPickInputClassName、quickPickListClassName。                                            |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                                                                                                  |
| [TaskFindDialog.tsx](TaskFindDialog.tsx)                 | Cmd/Ctrl+F 在查找框已打开时不会改变 open 状态，常规聚焦 effect 不会重跑。                                                                                         |
| [taskFindNavigationState.ts](taskFindNavigationState.ts) | 单命中环绕时 query/index 不变，导航身份必须在状态持有层独立递增。                                                                                                 |
| [taskFindSearch.ts](taskFindSearch.ts)                   | 实现或公开接口：createTaskFindEntries、getTaskFindState、moveTaskFindSelection。                                                                                  |

<!-- qingqi-directory-index:end -->
