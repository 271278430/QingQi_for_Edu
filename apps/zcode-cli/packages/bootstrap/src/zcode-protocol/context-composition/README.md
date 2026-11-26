# context-composition

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 context composition 实现源码。

### 文件

| 文件                     | 简要说明                                                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| [handler.ts](handler.ts) | v4/conversation/contextComposition 的 CLI 侧处理。规格：apps/zcode-cli/docs/design/v2/model/context-composition.md §3.3。 |
| [index.ts](index.ts)     | context-composition（CLI bootstrap 部分）公开入口。规格：apps/zcode-cli/docs/design/v2/model/context-composition.md。     |
| [README.md](README.md)   | 本目录用途、子目录与逐文件说明。                                                                                          |
| [tracker.ts](tracker.ts) | context 组成修订号的唯一 owner。规格：apps/zcode-cli/docs/design/v2/model/context-composition.md §3.4。                   |

<!-- qingqi-directory-index:end -->
