# system-reminder

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 system reminder 实现源码。

### 文件

| 文件                                         | 简要说明                                                                           |
| -------------------------------------------- | ---------------------------------------------------------------------------------- |
| [incoming-message.ts](incoming-message.ts)   | 回信都来自本会话派生的子 agent（后代），说明段按这种发送方书写。                   |
| [prompt-attachment.ts](prompt-attachment.ts) | source-less inline text 没有对应的真实读取工具，不能提示模型使用虚构工具继续读取。 |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                                   |
| [source.ts](source.ts)                       | 页面状态是不可信数据，必须留在 user 侧 untrusted 包装里，不能升为 system。         |

<!-- qingqi-directory-index:end -->
