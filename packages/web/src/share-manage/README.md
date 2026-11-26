# share-manage

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 share manage 实现源码。

### 文件

| 文件                                                                         | 简要说明                                                                                                       |
| ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                                   | \* web-share-manage 标准调用示例：撤销一个分享，并以服务端返回的视图替换本地行。                               |
| [CONTRACT.md](CONTRACT.md)                                                   | 模块职责、公共接口、依赖方向和状态约定。                                                                       |
| [contract.ts](contract.ts)                                                   | \* web-share-manage 对外契约：分享管理页依赖的服务端操作。真实 HTTP 实现与开发态 mock 共用这一契约。           |
| [conversationShareManageClient.ts](conversationShareManageClient.ts)         | 管理页只用有效期字段；只校验这三项，capabilities 其他字段的演进不影响管理页。                                  |
| [ConversationShareManagePage.tsx](ConversationShareManagePage.tsx)           | 实现或公开接口：ConversationShareManageLoader。                                                                |
| [index.ts](index.ts)                                                         | 分享管理页公开入口；开发态 mock 单独从 mockConversationShareManageClient.ts 动态加载，不进入生产包的静态依赖。 |
| [manageFailure.ts](manageFailure.ts)                                         | 只记录稳定字段：不记录 JWT、分享码或响应正文。                                                                 |
| [mockConversationShareManageClient.ts](mockConversationShareManageClient.ts) | 上限故意小于 30 天预设：SHARE-MG01 据此验收有效期选项受服务端范围约束。                                        |
| [module.ts](module.ts)                                                       | \* web-share-manage 模块清单（architecture-governance managed 模块）。                                         |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                                               |

<!-- qingqi-directory-index:end -->
