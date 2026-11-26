# lib

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

lib 工程脚本，属于 scripts 目录。

### 文件

| 文件                                                                                                     | 简要说明                                                                                                         |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [conversation-session-formal-admission-audit.mjs](conversation-session-formal-admission-audit.mjs)       | 实现或公开接口：buildFormalAdmissionAuditIntegration、getCoverageAuditExitCode。                                 |
| [conversation-session-formal-admission-contract.mjs](conversation-session-formal-admission-contract.mjs) | 实现或公开接口：validateFormalAdmissionManifest。                                                                |
| [conversation-session-formal-admission-ledger.mjs](conversation-session-formal-admission-ledger.mjs)     | 实现或公开接口：validateRequestLedger、validateProviderFixture、validateRequestArray、validateSyntheticReasons。 |
| [conversation-session-formal-admission-paths.mjs](conversation-session-formal-admission-paths.mjs)       | 运行时 descriptor 只有在生产者来源可审计且描述完整时才豁免存在检查，                                             |
| [conversation-session-formal-admission-utils.mjs](conversation-session-formal-admission-utils.mjs)       | 实现或公开接口：readJson、exists、diagnostic、toRepoPath。                                                       |
| [conversation-session-formal-admission.mjs](conversation-session-formal-admission.mjs)                   | 修复原因：pending 文件仍可能采用已录制 fixture，但这些 JSON 属于未来 formal                                      |
| [README.md](README.md)                                                                                   | 本目录用途、子目录与逐文件说明。                                                                                 |
| [retired-app-unit-evidence.mjs](retired-app-unit-evidence.mjs)                                           | 保留项不能套用 App 退役标签；避免再次把 CLI/CUA 或工程证据误报为已删。                                           |

<!-- qingqi-directory-index:end -->
