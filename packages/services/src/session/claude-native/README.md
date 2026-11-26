# claude-native

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 claude native 实现源码。

### 文件

| 文件                                                                       | 简要说明                                                                                                                                                                   |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [buildImportedClaudeTaskFile.ts](buildImportedClaudeTaskFile.ts)           | Claude 原生 session 的 mode/model/provider 是来源端运行态，                                                                                                                |
| [claudeNativeImportedSessionTypes.ts](claudeNativeImportedSessionTypes.ts) | 导入来源身份：外部原生 CLI（Claude Code），与 agent runtime 的 ZCodeProvider 无关。                                                                                        |
| [claudeNativeSessionHeadParser.ts](claudeNativeSessionHeadParser.ts)       | 实现或公开接口：hasClaudeNativeSidechainMarker、extractClaudeNativeSessionHeadInfo。                                                                                       |
| [claudeNativeSessionImportParser.ts](claudeNativeSessionImportParser.ts)   | 实现或公开接口：hasClaudeNativeSidechainMarker、stripClaudeNativeSyntheticNoResponsePlaceholderText、extractClaudeNativeSessionHeadInfo、parseClaudeNativeSessionRecords。 |
| [claudeNativeSessionImportRepo.ts](claudeNativeSessionImportRepo.ts)       | 关键业务逻辑：扫描 Claude Code 原生历史目录 ~/.claude/projects，不是 zcode 自己的数据目录。                                                                                |
| [claudeNativeSessionImportService.ts](claudeNativeSessionImportService.ts) | 实现或公开接口：importClaudeNativeSessions。                                                                                                                               |
| [importedClaudeHistoryRepair.ts](importedClaudeHistoryRepair.ts)           | user-only / assistant-first 只是异常形态，不等于 Claude 导入。                                                                                                             |
| [importedClaudeTaskFileFilter.ts](importedClaudeTaskFileFilter.ts)         | 实现或公开接口：DEFAULT_IMPORTED_CLAUDE_TASK_FILTER_PATHS、filterImportedClaudeTaskFilePaths。                                                                             |
| [jsonLineRecord.ts](jsonLineRecord.ts)                                     | 实现或公开接口：JsonLineRecord、isObjectRecord、readTrimmedString。                                                                                                        |
| [persistImportedClaudeTask.ts](persistImportedClaudeTask.ts)               | legacy ACP 下线后 importClaudeSessions 变成空桩，导入虽复制了 jsonl 却没有写                                                                                               |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                                                                                                           |
| [sessionHistoryJsonl.ts](sessionHistoryJsonl.ts)                           | 实现或公开接口：readJsonLinesFile、readJsonLinesFileHead。                                                                                                                 |

<!-- qingqi-directory-index:end -->
