# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 src 实现源码。

### 子目录

| 目录                                            | 存放内容                                             |
| ----------------------------------------------- | ---------------------------------------------------- |
| [agent/](agent/README.md)                       | @zcode/core 基础工程中的 agent 实现源码。            |
| [browser-client/](browser-client/README.md)     | @zcode/core 基础工程中的 browser client 实现源码。   |
| [compact/](compact/README.md)                   | @zcode/core 基础工程中的 compact 实现源码。          |
| [context/](context/README.md)                   | @zcode/core 基础工程中的 context 实现源码。          |
| [embedded-search/](embedded-search/README.md)   | @zcode/core 基础工程中的 embedded search 实现源码。  |
| [errors/](errors/README.md)                     | @zcode/core 基础工程中的 errors 实现源码。           |
| [hooks/](hooks/README.md)                       | @zcode/core 基础工程中的 hooks 生命周期与操作入口。  |
| [mcp/](mcp/README.md)                           | @zcode/core 基础工程中的 mcp 实现源码。              |
| [memory/](memory/README.md)                     | @zcode/core 基础工程中的 memory 实现源码。           |
| [model/](model/README.md)                       | @zcode/core 基础工程中的 model 实现源码。            |
| [permission/](permission/README.md)             | @zcode/core 基础工程中的 permission 实现源码。       |
| [plugin-reference/](plugin-reference/README.md) | @zcode/core 基础工程中的 plugin reference 实现源码。 |
| [repl/](repl/README.md)                         | @zcode/core 基础工程中的 repl 实现源码。             |
| [runtime/](runtime/README.md)                   | @zcode/core 基础工程中的 runtime 实现源码。          |
| [runtime-task/](runtime-task/README.md)         | @zcode/core 基础工程中的 runtime task 实现源码。     |
| [session-context/](session-context/README.md)   | @zcode/core 基础工程中的 session context 实现源码。  |
| [subagent/](subagent/README.md)                 | @zcode/core 基础工程中的 subagent 实现源码。         |
| [system-reminder/](system-reminder/README.md)   | @zcode/core 基础工程中的 system reminder 实现源码。  |
| [telemetry/](telemetry/README.md)               | @zcode/core 基础工程中的 telemetry 实现源码。        |
| [tool/](tool/README.md)                         | @zcode/core 基础工程中的 tool 实现源码。             |
| [workflow/](workflow/README.md)                 | @zcode/core 基础工程中的 workflow 实现源码。         |

### 文件

| 文件                             | 简要说明                                           |
| -------------------------------- | -------------------------------------------------- |
| [environment.ts](environment.ts) | 实现或公开接口：getRuntimeInfo。                   |
| [index.ts](index.ts)             | Core package exports                               |
| [output.ts](output.ts)           | 实现或公开接口：formatJson、supportsColor、color。 |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。                   |
| [runtime.ts](runtime.ts)         | 实现或公开接口：RuntimeFactory。                   |

<!-- qingqi-directory-index:end -->
