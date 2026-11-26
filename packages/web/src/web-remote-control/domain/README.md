# domain

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 domain 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                                                                           |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                                                                   |
| [webRemoteControlDeviceGroups.ts](webRemoteControlDeviceGroups.ts) | \* MID 只负责设备展示；保留全部在线 SID，连接与业务状态仍按 SID 隔离。                                                                             |
| [webRemoteControlScreenCopy.ts](webRemoteControlScreenCopy.ts)     | 实现或公开接口：WebRemoteControlScreenLocale、WebRemoteControlScreenCopy、resolveWebRemoteControlScreenLocale、resolveWebRemoteControlScreenCopy。 |

<!-- qingqi-directory-index:end -->
