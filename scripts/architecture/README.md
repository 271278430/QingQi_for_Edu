# architecture

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

architecture 工程脚本，属于 scripts 目录。

### 文件

| 文件                                                         | 简要说明                                                                                        |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| [adopt.mjs](adopt.mjs)                                       | \* architecture:adopt —— 把一个目录登记为 managed 模块。                                        |
| [architecture-check.mjs](architecture-check.mjs)             | architecture-check 的实现文件。                                                                 |
| [context.mjs](context.mjs)                                   | CONTRACT.md 不是源码扩展名，不在 discoverFiles 结果里，要按 root 直接探测。                     |
| [default-branch.mjs](default-branch.mjs)                     | Bug 原因：新分支首次 push 没有 remote SHA；若直接回退 origin/main，                             |
| [git-base.mjs](git-base.mjs)                                 | \* 选择 --changed 的比较基线。                                                                  |
| [git-file-names.mjs](git-file-names.mjs)                     | Git 会给纯日期补上当前时刻和宿主时区，导致相同 ref 的准入集合随执行时间漂移。                   |
| [index.mjs](index.mjs)                                       | manifest-policy-mismatch：文档写"策略与模块声明必须互相校验"，首版只是优先读 module.ts。        |
| [policy.mjs](policy.mjs)                                     | 契约文档也是必需产物；只枚举源码会把实际存在的 CONTRACT.md 误报为缺失。                         |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                |
| [report.mjs](report.mjs)                                     | 实现或公开接口：formatReport、formatMarkdownReport。                                            |
| [resolver.mjs](resolver.mjs)                                 | \* 修复原因（2026-09 review）：首版 `resolveImport` 只解析 `./` `../` 开头的相对路径，          |
| [session-control-boundary.mjs](session-control-boundary.mjs) | 补上 lint 不检查的动态 import 与 globalThis 绕过；只约束本功能核心，不改变宿主 adapter。        |
| [upstream-admission.mjs](upstream-admission.mjs)             | --no-commit 的合并尚未成为 HEAD 祖先；只接受 Git 当前正在合入的父提交，避免先提交才可检查。     |
| [upstream-snapshot.json](upstream-snapshot.json)             | upstream-snapshot 的数据或配置定义。                                                            |
| [upstream-snapshot.mjs](upstream-snapshot.mjs)               | 独立公开历史没有源仓库对象；固定内容与模式仍须同时匹配暂存区和工作区。                          |
| [violations.mjs](violations.mjs)                             | \* 违规文件路径统一为相对 cwd 的 posix 路径。修复原因：首版写入绝对路径，fingerprint 随之含机器 |

<!-- qingqi-directory-index:end -->
