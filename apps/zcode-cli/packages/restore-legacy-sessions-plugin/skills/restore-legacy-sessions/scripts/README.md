# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/restore-legacy-sessions-plugin 基础工程中的 scripts 工程脚本。

### 文件

| 文件                                                 | 简要说明                                                                            |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------- |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                    |
| [restore-conversation.mjs](restore-conversation.mjs) | \* Restore a single legacy ACP-era conversation snapshot into the new ZCode stores. |
| [scan-legacy-sessions.mjs](scan-legacy-sessions.mjs) | 只读扫描依赖 node:sqlite 访问本地 DB；过滤该实验提示，避免污染给用户选择用的表格。  |

<!-- qingqi-directory-index:end -->
