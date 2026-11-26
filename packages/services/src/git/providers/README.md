# providers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 providers 实现源码。

### 文件

| 文件                                                   | 简要说明                                                                            |
| ------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| [gitCommandProvider.ts](gitCommandProvider.ts)         | 逐块回调原始输出（例如受管 worktree 创建进度）；不影响 stdout/stderr 的收集与截断。 |
| [gitEnvironmentProvider.ts](gitEnvironmentProvider.ts) | Git binary 的探测在一次会话里不会频繁变化，                                         |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                    |

<!-- qingqi-directory-index:end -->
