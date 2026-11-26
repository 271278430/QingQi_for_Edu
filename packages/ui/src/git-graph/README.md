# git-graph

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 git graph 实现源码。

### 文件

| 文件                                                 | 简要说明                                                                              |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [GitGraphCommitDetail.tsx](GitGraphCommitDetail.tsx) | 实现或公开接口：GitGraphCommitDetailProps、GitGraphCommitDetail。                     |
| [GitGraphDialog.tsx](GitGraphDialog.tsx)             | 实现或公开接口：GitGraphDialog。                                                      |
| [GitGraphDisplay.tsx](GitGraphDisplay.tsx)           | 实现或公开接口：getShortHash、getRefIcon、formatCommitTime。                          |
| [GitGraphPane.tsx](GitGraphPane.tsx)                 | 单泳道图形宽度比 Graph 表头短，保留最小列宽避免表头被挤压。                           |
| [layout.ts](layout.ts)                               | 实现或公开接口：GitGraphRefKind、GitGraphRef、GitGraphCommit、GitGraphLayoutOptions。 |
| [layoutAlgorithm.ts](layoutAlgorithm.ts)             | 实现或公开接口：GraphPoint、BranchLineSeed、LayoutVertex、createGitGraphLayoutModel。 |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                      |

<!-- qingqi-directory-index:end -->
