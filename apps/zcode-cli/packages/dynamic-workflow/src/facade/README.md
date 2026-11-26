# facade

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 facade 实现源码。

### 文件

| 文件                                     | 简要说明                                                                                                |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| [artifact-caps.ts](artifact-caps.ts)     | \* 产物（artifact）的上限常量。                                                                         |
| [dts-hole.ts](dts-hole.ts)               | \* facade 的 hole 段（docs/dynamic-workflow/authoring.md「Holes: `hole<T>()`」）：类型化的留白。        |
| [dts-model.ts](dts-model.ts)             | \* facade actor 段里的模型声明（docs/dynamic-workflow/authoring.md「Choosing a model per subagent」）： |
| [dts-stream.ts](dts-stream.ts)           | \* facade 的 stream 段（docs/dynamic-workflow/authoring.md「Streams」）：channel / future。             |
| [dts.ts](dts.ts)                         | \* The dynamic-workflow facade: the entire model-facing API surface, shipped as an                      |
| [README.md](README.md)                   | 本目录用途、子目录与逐文件说明。                                                                        |
| [registry.ts](registry.ts)               | \* world-read 注册表：                                                                                  |
| [report-caps.ts](report-caps.ts)         | \* `report` 的上限常量。                                                                                |
| [world-read-caps.ts](world-read-caps.ts) | \* world-read 的上限常量。                                                                              |

<!-- qingqi-directory-index:end -->
