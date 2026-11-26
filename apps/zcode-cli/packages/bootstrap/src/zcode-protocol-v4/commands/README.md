# commands

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 commands 实现源码。

### 子目录

| 目录                            | 存放内容                                          |
| ------------------------------- | ------------------------------------------------- |
| [handlers/](handlers/README.md) | @zcode/bootstrap 基础工程中的 handlers 实现源码。 |

### 文件

| 文件                                     | 简要说明                                                                          |
| ---------------------------------------- | --------------------------------------------------------------------------------- |
| [attachment-refs.ts](attachment-refs.ts) | 附件命令面：AttachmentRef（引用模型）→ core TurnAttachment 的协议边界映射。       |
| [executor.ts](executor.ts)               | // 逐命令原生化的推进方式：handlers/ 注册表列出已原生的命令；binder 只在 supports |
| [input-admission.ts](input-admission.ts) | V4 用户输入准入共用件：正文/附件非空校验、held 队列裁决、以及旧发送端的           |
| [input-intent.ts](input-intent.ts)       | live intent 过去只带 kind/来源，projection 只能回退可见 command 文案；            |
| [prompt-turn.ts](prompt-turn.ts)         | 原生 prompt turn 运行器。                                                         |
| [README.md](README.md)                   | 本目录用途、子目录与逐文件说明。                                                  |
| [record-access.ts](record-access.ts)     | 会话查找共用件（各命令组 handler 采用）。                                         |
| [types.ts](types.ts)                     | v4 原生命令层的 core 能力契约（原生重做版）。                                     |

<!-- qingqi-directory-index:end -->
