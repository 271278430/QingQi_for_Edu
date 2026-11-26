# lowering

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 lowering 实现源码。

### 文件

| 文件                           | 简要说明                                                                                                |
| ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [index.ts](index.ts)           | index 的实现文件。                                                                                      |
| [lower-hole.ts](lower-hole.ts) | \* 留白的降级（execution-engine.md「From script to sandbox input: lowering」的两行 hole，               |
| [lower.ts](lower.ts)           | \* Lowering（instrumentation emit step）：把已 typecheck + analyze 干净的 workflow 脚本降级为沙箱可跑的 |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                                                                        |

<!-- qingqi-directory-index:end -->
