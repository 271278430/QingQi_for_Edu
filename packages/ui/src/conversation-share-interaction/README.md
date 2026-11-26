# conversation-share-interaction

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 conversation share interaction 实现源码。

### 文件

| 文件                                                                           | 简要说明                                                                             |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts)                                     | effect 返回取消函数；依赖变化或卸载即作废旧代际，状态仍由传入的 owner 回调更新。     |
| [CONTRACT.md](CONTRACT.md)                                                     | 模块职责、公共接口、依赖方向和状态约定。                                             |
| [contract.ts](contract.ts)                                                     | UI 状态只用于展示，预检结果与缓存的唯一 owner 是 SessionPane。                       |
| [ConversationShareExpiryPicker.tsx](ConversationShareExpiryPicker.tsx)         | 有效期按整天优先展示，否则按小时；服务端默认值可能不在预设里，也要能读。             |
| [ConversationSharePopover.tsx](ConversationSharePopover.tsx)                   | 设置仍由 SessionPane 提供，锚点采用 workspace 顶栏入口，避免跨层传递第二份分享状态。 |
| [conversationSharePopoverActions.ts](conversationSharePopoverActions.ts)       | 同一 store 的范围事务命令；只持有临时 UI 勾选，不产生第二份已确认分享状态。          |
| [conversationSharePreflightRequest.ts](conversationSharePreflightRequest.ts)   | \* 预检 effect 的一次请求代际。清理时不仅撤销 debounce，也作废已经发出的 RPC 回调。  |
| [conversationSharePreflightResponse.ts](conversationSharePreflightResponse.ts) | 响应只提交到 SessionPane 持有的缓存；请求代际仍由 scheduler 和 isCurrent 共同约束。  |
| [ConversationSharePreflightStatus.tsx](ConversationSharePreflightStatus.tsx)   | 修复原因：memo 组件的默认对象每次创建会破坏引用稳定性；idle 默认值仅供读取。         |
| [index.ts](index.ts)                                                           | index 的实现文件。                                                                   |
| [module.ts](module.ts)                                                         | \* conversation-share-interaction 模块清单（architecture-governance managed 模块）。 |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                                     |
| [SettingsShareManagement.tsx](SettingsShareManagement.tsx)                     | 桌面登录态；未登录时只显示登录提示，不请求管理 API。                                 |

<!-- qingqi-directory-index:end -->
