# agent-crash-diagnostic

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 agent crash diagnostic 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                         |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [agentCrashDiagnostic.ts](agentCrashDiagnostic.ts) | \* Agent runtime 进程异常退出的诊断：从退出码与 stderr 尾部提取 error 名称、错误码、摘要和指纹。 |
| [contract.example.ts](contract.example.ts)         | Windows 系统可提交内存耗尽：退出码直接定性，stderr 只保留在 errorStack。                         |
| [CONTRACT.md](CONTRACT.md)                         | 模块职责、公共接口、依赖方向和状态约定。                                                         |
| [contract.ts](contract.ts)                         | contract 的实现文件。                                                                            |
| [index.ts](index.ts)                               | index 的实现文件。                                                                               |
| [module.ts](module.ts)                             | 实现或公开接口：moduleDefinition。                                                               |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                 |

<!-- qingqi-directory-index:end -->
