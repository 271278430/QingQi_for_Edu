# memory-diagnostics

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 memory diagnostics 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：exampleMemoryDiagnostics。                                                              |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                |
| [contract.ts](contract.ts)                 | 幂等停止采样；不等待写盘，不改变任务生命周期。                                                          |
| [index.ts](index.ts)                       | disable 清除采样状态，不使用 stopSampling 再复制一次完整 profile。                                      |
| [module.ts](module.ts)                     | \* cli-memory-diagnostics 模块清单（architecture-governance managed 模块）。                            |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                        |
| [recorder.ts](recorder.ts)                 | 只保留已知发布 bundle 的位置，eval、插件和用户脚本的名称/路径不能进入日志。                             |
| [storage.ts](storage.ts)                   | 采用跨进程锁的存活 owner 判据；竞争只试一次，不创建进程内等待队列。                                     |
| [types.ts](types.ts)                       | 实现或公开接口：AllocationNode、AllocationProfiler、MemoryDiagnosticRecorder、MemoryDiagnosticOptions。 |

<!-- qingqi-directory-index:end -->
