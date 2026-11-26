# topic-history-attachment

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 topic history attachment 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                    |
| ------------------------------------------ | ------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 调用方只依赖附件结果，不解析正文格式。                                                      |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                    |
| [contract.ts](contract.ts)                 | \* 把一次话题增量写成随用户消息发送的 text/plain 附件；没有消息且没有缺口时返回 undefined。 |
| [module.ts](module.ts)                     | \* bot-topic-history-attachment 模块清单（architecture-governance managed 模块）。          |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                            |

<!-- qingqi-directory-index:end -->
