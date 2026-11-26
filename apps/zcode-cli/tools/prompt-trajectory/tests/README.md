# tests

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/prompt-trajectory 基础工程中的 tests 验收与回归场景。

### 子目录

| 目录                                                        | 存放内容                                                                      |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [tool-search-comparison/](tool-search-comparison/README.md) | @zcode/prompt-trajectory 基础工程中的 tool search comparison 验收与回归场景。 |

### 文件

| 文件                                                                             | 简要说明                                                                           |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [continuity.test.ts](continuity.test.ts)                                         | continuity.test 的实现文件。                                                       |
| [derive.test.ts](derive.test.ts)                                                 | derive.test 的实现文件。                                                           |
| [fixture.test.ts](fixture.test.ts)                                               | fixture.test 的实现文件。                                                          |
| [model-io-continuity.test.ts](model-io-continuity.test.ts)                       | 请求里每个文字块单独一块（docs/design/v2/model/assistant-block-order.md）；        |
| [model-io.test.ts](model-io.test.ts)                                             | model-io.test 的实现文件。                                                         |
| [openai-provider-proxy.test.ts](openai-provider-proxy.test.ts)                   | 第一片带完整内容，最后一片只带结束原因和 usage；SDK 按流式解析即可拿到同一条回复。 |
| [README.md](README.md)                                                           | 本目录用途、子目录与逐文件说明。                                                   |
| [record-isolation.test.ts](record-isolation.test.ts)                             | 本文件跑真实录制，与 `record` 命令一样依赖已构建的 bootstrap dist。                |
| [record.test.ts](record.test.ts)                                                 | record.test 的实现文件。                                                           |
| [response-assembler.test.ts](response-assembler.test.ts)                         | response-assembler.test 的实现文件。                                               |
| [tool-search-continuity.test.ts](tool-search-continuity.test.ts)                 | tool-search-continuity.test 的实现文件。                                           |
| [tool-search-success-continuity.test.ts](tool-search-success-continuity.test.ts) | 最终 Anthropic wire 将整批结果、每个搜索的成功提示及后续 user 正文合并。           |

<!-- qingqi-directory-index:end -->
