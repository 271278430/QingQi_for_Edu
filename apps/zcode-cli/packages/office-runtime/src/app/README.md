# app

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 app 实现源码。

### 文件

| 文件                                 | 简要说明                                                                             |
| ------------------------------------ | ------------------------------------------------------------------------------------ |
| [documents.ts](documents.ts)         | File handles each session keeps; a panel reads all chunks right after load_document. |
| [README.md](README.md)               | 本目录用途、子目录与逐文件说明。                                                     |
| [sessions.test.ts](sessions.test.ts) | 一个工作区共用一个 server：查看状态按 session 划分，解析缓存共享（spec §8）。        |
| [views.test.ts](views.test.ts)       | views.test 的实现文件。                                                              |

<!-- qingqi-directory-index:end -->
