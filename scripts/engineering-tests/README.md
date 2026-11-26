# engineering-tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

engineering tests 工程脚本，属于 scripts 目录。

### 文件

| 文件                       | 简要说明                                                                     |
| -------------------------- | ---------------------------------------------------------------------------- |
| [process.mjs](process.mjs) | 实现或公开接口：run、git、cleanGitEnv。                                      |
| [README.md](README.md)     | 本目录用途、子目录与逐文件说明。                                             |
| [scope.mjs](scope.mjs)     | rebase / force-push 后远端 SHA 不再是 HEAD 的祖先；直接拿它当基线会让 Vitest |

<!-- qingqi-directory-index:end -->
