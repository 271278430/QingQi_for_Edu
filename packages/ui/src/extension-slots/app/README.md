# app

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 app 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                               |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [extensionGrantsStore.ts](extensionGrantsStore.ts) | Renderer 侧只持授权状态的最近一份（docs/plugins/extension-host.md §17.7）。owner 是 Window Host 的     |
| [extensionLogsStore.ts](extensionLogsStore.ts)     | Renderer 的扩展日志 store（docs/plugins/extension-host.md §16.8）。缓冲的唯一 owner 是 Main 的监管器， |
| [extensionSlotsStore.ts](extensionSlotsStore.ts)   | Renderer 侧只持三份数据的最近一份（docs/plugins/extension-host.md §3.4、§16.1）：                      |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                       |
| [workbenchReporter.ts](workbenchReporter.ts)       | 屏幕会话报告（③ Renderer 报告）：每个对话窗格登记自己的一项，变化时合成整份报告发给 Window Host。      |

<!-- qingqi-directory-index:end -->
