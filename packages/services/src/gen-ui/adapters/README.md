# adapters

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 adapters 外部能力与平台适配。

### 文件

| 文件                               | 简要说明                                                                      |
| ---------------------------------- | ----------------------------------------------------------------------------- |
| [files.ts](files.ts)               | 根因：fork 会保留父会话的 HTML 路径，生成目录分组不能作为当前会话的读取限制。 |
| [README.md](README.md)             | 本目录用途、子目录与逐文件说明。                                              |
| [service.ts](service.ts)           | 实现或公开接口：createGenUiService。                                          |
| [stateStorage.ts](stateStorage.ts) | watch 事件与写入 ACK 可以同时触发；串行读取防止较早快照迟到覆盖较新通知。     |

<!-- qingqi-directory-index:end -->
