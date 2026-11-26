# onboarding

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 onboarding 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                          |
| -------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [localUsageEvidence.ts](localUsageEvidence.ts)           | \* 引导资格的"本机使用证据"判定（docs/onboarding-record-spec.md §4）。            |
| [onboardingRecord.ts](onboardingRecord.ts)               | 登录态变化时按 record 回填 settings 的字段范围（settings 仍是运行时唯一事实源）。 |
| [onboardingRecordService.ts](onboardingRecordService.ts) | 记录是设备级数据，必须跟随 dataBaseDir（用户自定义数据目录时落在其 .zcode/v2 下， |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                  |

<!-- qingqi-directory-index:end -->
