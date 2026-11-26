# domain

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 domain 实现源码。

### 文件

| 文件                             | 简要说明                                                                           |
| -------------------------------- | ---------------------------------------------------------------------------------- |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。                                                   |
| [references.ts](references.ts)   | 引用字段均为字符串；完整字符串后仍可能停在 key、冒号、value 或逗号处。             |
| [sourceFiles.ts](sourceFiles.ts) | 这里只识别完整引用以去重，不挂载页面；执行时机和文件授权仍由原有 Gen UI 链路负责。 |

<!-- qingqi-directory-index:end -->
