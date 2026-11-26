# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow-runtime 基础工程中的 src 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                   |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [child-cell-streams.ts](child-cell-streams.ts) | \* cell 的第二段引导脚本：流水线原语 channel / future 与停滞检测                           |
| [child-entry-file.ts](child-entry-file.ts)     | \* 为什么有这个文件：Windows 的命令行上限是 32,767 字符，payload 不能再过 argv。harness 把 |
| [child-source.ts](child-source.ts)             | \* 沙箱子进程逻辑。**一份实现，一份入口文件，两种启动方式**：                              |
| [harness.ts](harness.ts)                       | \* 父进程 harness（Boundary A 的宿主侧 + 沙箱进程编排）。                                  |
| [index.ts](index.ts)                           | \* `@zcode/dynamic-workflow-runtime`：沙箱 harness。                                       |
| [protocol.ts](protocol.ts)                     | \* NDJSON 线协议（Boundary A 的传输编码）。                                                |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                           |

<!-- qingqi-directory-index:end -->
