# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 pending 测试场景。

### 文件

| 文件                                                   | 简要说明                                                                                |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                        |
| [share-workflow-parity.mjs](share-workflow-parity.mjs) | SHARE-WF03：实际 session 的去执行化快照可通过 SHARE_PARITY_PREVIEW 指定，原数据不入仓。 |
| [share-workflow.mjs](share-workflow.mjs)               | SHARE-WF01：先启动 pnpm dev:web-share:test；API 由本测试拦截，不访问真实分享或账号。    |

<!-- qingqi-directory-index:end -->
