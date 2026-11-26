# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server-cli 基础工程中的 src 实现源码。

### 子目录

| 目录                                  | 存放内容                                              |
| ------------------------------------- | ----------------------------------------------------- |
| [ipc/](ipc/README.md)                 | @zcode/server-cli 基础工程中的 ipc 实现源码。         |
| [packaging/](packaging/README.md)     | @zcode/server-cli 基础工程中的 packaging 实现源码。   |
| [platform/](platform/README.md)       | @zcode/server-cli 基础工程中的 platform 实现源码。    |
| [runtime/](runtime/README.md)         | @zcode/server-cli 基础工程中的 runtime 实现源码。     |
| [server-core/](server-core/README.md) | @zcode/server-cli 基础工程中的 server core 实现源码。 |
| [supervisor/](supervisor/README.md)   | @zcode/server-cli 基础工程中的 supervisor 实现源码。  |

### 文件

| 文件                         | 简要说明                                                                                           |
| ---------------------------- | -------------------------------------------------------------------------------------------------- |
| [cli.ts](cli.ts)             | process/service manager 是更新协调器的外部边界；测试可注入受控实现。                               |
| [contracts.ts](contracts.ts) | Supervisor 停止/更新链路的时间预算唯一来源；等待 Supervisor 的调用方必须由这里推导，不能各自写死。 |
| [index.ts](index.ts)         | index 的实现文件。                                                                                 |
| [main.ts](main.ts)           | 自动接线只作为本次 CLI 的显式依赖传入，不能污染全局 env；candidate release 启动时                  |
| [README.md](README.md)       | 本目录用途、子目录与逐文件说明。                                                                   |

<!-- qingqi-directory-index:end -->
