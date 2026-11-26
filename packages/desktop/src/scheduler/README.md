# scheduler

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 scheduler 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                                           |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [index.ts](index.ts)                                           | 常驻 cron scheduler 进程：由 desktop main 通过 electronUtilityProcess.fork 拉起。                  |
| [manualClaimRelease.ts](manualClaimRelease.ts)                 | scheduler 重启 / inFlight 丢失后仍可能收到 main 的迟到回报；manual                                 |
| [offPeakDispatchSettlement.ts](offPeakDispatchSettlement.ts)   | \* 不能忽略 failureKind：缺模型/凭证等确定性配置错误若也无限退避，                                 |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                   |
| [schedulerProtocol.d.ts](schedulerProtocol.d.ts)               | scheduler → main                                                                                   |
| [schedulerProtocol.d.ts.map](schedulerProtocol.d.ts.map)       | schedulerProtocol.d.ts 模块的资源或工程文件。                                                      |
| [schedulerProtocol.js](schedulerProtocol.js)                   | scheduler(utilityProcess) ↔ main 的控制消息协议。两端都在 Electron 侧，走 parentPort.postMessage。 |
| [schedulerProtocol.js.map](schedulerProtocol.js.map)           | schedulerProtocol.js 模块的资源或工程文件。                                                        |
| [schedulerProtocol.ts](schedulerProtocol.ts)                   | scheduler(utilityProcess) ↔ main 的控制消息协议。两端都在 Electron 侧，走 parentPort.postMessage。 |
| [schedulerResourceTelemetry.ts](schedulerResourceTelemetry.ts) | \* cron scheduler 进程自身的资源遥测。                                                             |

<!-- qingqi-directory-index:end -->
