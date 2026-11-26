# git-branch-switcher

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 git branch switcher 实现源码。

### 文件

| 文件                                         | 简要说明                                                                                                                          |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| [display.ts](display.ts)                     | 实现或公开接口：GitBranchCommitPreviewFile、getGitDirtyFileCount、resolveGitBranchTriggerLabel、matchesGitBranchSearch。          |
| [GitBranchDialogs.tsx](GitBranchDialogs.tsx) | 实现或公开接口：GitBranchCreateDialog、GitBranchSwitchAssistDialog。                                                              |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                                                                                  |
| [switchAssist.ts](switchAssist.ts)           | 实现或公开接口：GitBranchSwitchAssistDialogStep、GitBranchSwitchAssistState、formatGitBranchIssuePathList、hasGitCommitIdentity。 |

<!-- qingqi-directory-index:end -->
