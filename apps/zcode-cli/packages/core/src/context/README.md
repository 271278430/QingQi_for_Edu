# context

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 context 实现源码。

### 子目录

| 目录                            | 存放内容                                     |
| ------------------------------- | -------------------------------------------- |
| [sections/](sections/README.md) | @zcode/core 基础工程中的 sections 实现源码。 |

### 文件

| 文件                                       | 简要说明                                              |
| ------------------------------------------ | ----------------------------------------------------- |
| [builder.ts](builder.ts)                   | Context Builder - System prompt assembly              |
| [dynamic-sections.ts](dynamic-sections.ts) | 插件发现工具已改为 deferred，暂不注入插件推荐指导段。 |
| [index.ts](index.ts)                       | Context Builder exports                               |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                      |
| [total-tokens.ts](total-tokens.ts)         | 模型可见的 token 预算；固定值，不提供模式或配置。     |
| [types.ts](types.ts)                       | Context Builder Types                                 |
| [utils.ts](utils.ts)                       | Token Estimation                                      |

<!-- qingqi-directory-index:end -->
