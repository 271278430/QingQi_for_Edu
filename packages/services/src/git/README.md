# git

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 git 实现源码。

### 子目录

| 目录                                            | 存放内容                                                 |
| ----------------------------------------------- | -------------------------------------------------------- |
| [managed-worktree/](managed-worktree/README.md) | @zcode/services 基础工程中的 managed worktree 实现源码。 |
| [providers/](providers/README.md)               | @zcode/services 基础工程中的 providers 实现源码。        |
| [repo/](repo/README.md)                         | @zcode/services 基础工程中的 repo 实现源码。             |

### 文件

| 文件                                                         | 简要说明                                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| [commitMessageFileScope.ts](commitMessageFileScope.ts)       | 实现或公开接口：filterCommitMessageFilesByCurrentSession。                     |
| [config.ts](config.ts)                                       | `git push` 可能会被仓库的 pre-push hook 阻塞较长时间（例如执行 `pnpm test`）。 |
| [git.ts](git.ts)                                             | 实现或公开接口：IGitService。                                                  |
| [gitCheckpoint.ts](gitCheckpoint.ts)                         | 实现或公开接口：IGitCheckpointService。                                        |
| [gitCheckpointService.ts](gitCheckpointService.ts)           | 实现或公开接口：createGitCheckpointService。                                   |
| [gitCommitMessageGenerator.ts](gitCommitMessageGenerator.ts) | 模型可能重复 prompt 或返回解释性长文本，直接塞给 UI 会让错误提示失控。         |
| [gitService.ts](gitService.ts)                               | 构建目录里常见大量未跟踪的空文件、失效链接或不可读产物。                       |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                               |

<!-- qingqi-directory-index:end -->
