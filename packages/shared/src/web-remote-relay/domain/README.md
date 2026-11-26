# domain

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 domain 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                       |
| -------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [heartbeatTiming.ts](heartbeatTiming.ts)                 | 心跳 jitter 必须小于基准间隔，避免把合法的 transport heartbeat 变成 0ms 风暴。 |
| [notification.ts](notification.ts)                       | 只接受相邻实时投影；调用方在 snapshot/recovery 时只更新基线。                  |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                               |
| [retry.ts](retry.ts)                                     | \* 连接建立后第一次重连的打散窗口，电脑与手机共用。                            |
| [webRemoteControlActions.ts](webRemoteControlActions.ts) | \* 手机远控的任务置顶/归档与新建本地项目契约。                                 |

<!-- qingqi-directory-index:end -->
