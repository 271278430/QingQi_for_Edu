# shared

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 shared 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                   |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [armsBrowserInit.ts](armsBrowserInit.ts)           | \* 在 preload 或 renderer 入口尽早初始化 Browser SDK。                                     |
| [armsRumBridgeForward.ts](armsRumBridgeForward.ts) | 与 @arms/rum-electron 内置 preload 一致                                                    |
| [armsRumShared.ts](armsRumShared.ts)               | 主进程 init 的 browserCollectors，经 autoInject 注入到 renderer 的 RumSDK.init(collectors) |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                           |

<!-- qingqi-directory-index:end -->
