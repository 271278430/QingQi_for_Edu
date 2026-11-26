# global-notice

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 global notice 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                        |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| [globalNoticeStore.ts](globalNoticeStore.ts)       | Bug 根因：早期 Highspeed mock 通知使用 latest-only 持久化，关闭 mock 后重启仍会恢复假分享数据。 |
| [GlobalNoticeSurface.tsx](GlobalNoticeSurface.tsx) | Bug 根因：expiresAt 只在 store 事件时重算，页面持续打开会让过期卡一直留在界面上。               |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                |

<!-- qingqi-directory-index:end -->
