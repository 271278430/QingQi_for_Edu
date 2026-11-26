# skill-sync

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 skill sync 实现源码。

### 文件

| 文件                                       | 简要说明                                                                          |
| ------------------------------------------ | --------------------------------------------------------------------------------- |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                  |
| [skillSync.ts](skillSync.ts)               | 技能同步服务：数据同步弹窗使用 IDataSyncCategoryService 的统一形状。              |
| [skillSyncArchive.ts](skillSyncArchive.ts) | 发现大小超限或归档损坏时主动销毁流，避免 gzip 在后台继续膨胀或触发未处理错误。    |
| [skillSyncErrors.ts](skillSyncErrors.ts)   | 原始错误只携带字节数拼接文本，跨 RPC 后 UI 无法可靠区分导出内容、归档和解压阶段。 |
| [skillSyncPath.ts](skillSyncPath.ts)       | 实现或公开接口：normalizeSkillSyncRelativePath、resolveSkillSyncPathWithin。      |
| [skillSyncService.ts](skillSyncService.ts) | 用户级技能候选：path 指向技能目录下的 SKILL.md。                                  |

<!-- qingqi-directory-index:end -->
