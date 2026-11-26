# providers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 providers 实现源码。

### 文件

| 文件                                                         | 简要说明                                                                     |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| [fileMentionProvider.ts](fileMentionProvider.ts)             | Bugfix: 文件 mention 的标准转译格式需要保持 `filename`，                     |
| [pluginsMentionProvider.ts](pluginsMentionProvider.ts)       | - 只展示 catalog 中 enabled 的 Plugin；disabled 条目不可被引用，不进入候选。 |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                             |
| [sessionsMentionProvider.ts](sessionsMentionProvider.ts)     | 只在候选聚合阶段分桶，不写入 Lexical node 或 canonical mention。             |
| [skillsMentionProvider.ts](skillsMentionProvider.ts)         | `$` 面板是执行入口，不是来源管理页。                                         |
| [subagentsMentionProvider.ts](subagentsMentionProvider.ts)   | Bugfix：subagent 候选通常数量很少，空 query 时也是执行入口。                 |
| [whiteboardMentionProvider.ts](whiteboardMentionProvider.ts) | 实现或公开接口：useWhiteboardMentionProvider。                               |

<!-- qingqi-directory-index:end -->
