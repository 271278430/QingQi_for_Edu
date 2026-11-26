# remote

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

zcode 基础工程中的 remote 实现源码。

### 文件

| 文件                                                                 | 简要说明                                                           |
| -------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [README.md](README.md)                                               | 本目录用途、子目录与逐文件说明。                                   |
| [RemoteControlKeepAliveService.kt](RemoteControlKeepAliveService.kt) | Bugfix: 纯浏览器后台后 WebView/JS/WebSocket 容易被系统暂停或回收。 |
| [RemoteControlRecentLinksStore.kt](RemoteControlRecentLinksStore.kt) | RemoteControlRecentLinksStore 的Android 实现。                     |
| [RemoteControlUrlPolicy.kt](RemoteControlUrlPolicy.kt)               | Bugfix: 开发机真机调试时二维码会指向局域网 Vite 地址。             |

<!-- qingqi-directory-index:end -->
