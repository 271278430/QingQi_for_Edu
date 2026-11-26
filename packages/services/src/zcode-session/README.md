# zcode-session

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 zcode session 实现源码。

### 文件

| 文件                                                             | 简要说明                                                                          |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [importedClaudeSessionRepair.ts](importedClaudeSessionRepair.ts) | 实现或公开接口：repairEmptyImportedClaudeSessionSnapshot。                        |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                  |
| [zcodeSession.ts](zcodeSession.ts)                               | 仅导入事务使用的预分配 ID；普通新会话继续由 Agent 分配。                          |
| [zcodeSessionApiRetry.ts](zcodeSessionApiRetry.ts)               | desktop-continuous 的 snapshot runtime 需要跟住 core recovery 进度；              |
| [zcodeSessionDraftRegistry.ts](zcodeSessionDraftRegistry.ts)     | 实现或公开接口：createZCodeDeferredDraftRegistry。                                |
| [zcodeSessionService.ts](zcodeSessionService.ts)                 | \* 后台 task index sqlite 同步器。注入后，每次 session 被创建/恢复/发送 prompt 或 |

<!-- qingqi-directory-index:end -->
