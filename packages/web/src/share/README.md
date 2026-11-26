# share

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 share 实现源码。

### 文件

| 文件                                                                           | 简要说明                                                                             |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| [conversationShareLandingPage.css](conversationShareLandingPage.css)           | \* rail/row 必须撑满固定栏高度：三个元素现在沿连续几何轨道移动，不能让               |
| [ConversationShareLandingPage.tsx](ConversationShareLandingPage.tsx)           | 每个 provider 的登录按钮文案与区域徽标，对齐桌面端 login.oauth.\* 口径。             |
| [conversationSharePreviewClient.ts](conversationSharePreviewClient.ts)         | 页面语言由路径前缀决定：/cn/share 中文，裸 /share 英文；非分享路径回退到浏览器语言。 |
| [conversationShareRoute.ts](conversationShareRoute.ts)                         | \* 中文站 /cn/share 与英文站 /share 都是分享路由。                                   |
| [mockConversationSharePreviewClient.ts](mockConversationSharePreviewClient.ts) | 让 dev mock 覆盖 artifact 卡片：它的视觉要与正文的 AssistantPreviewCards 对齐，      |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                                     |
| [shareHeaderLayout.ts](shareHeaderLayout.ts)                                   | 分享 Header shell 的宽度。                                                           |

<!-- qingqi-directory-index:end -->
