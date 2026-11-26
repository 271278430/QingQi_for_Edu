# session-execution

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 session execution 实现源码。

### 文件

| 文件                                       | 简要说明                                                                    |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 使用现有 record；不把租约当作 busy/idle 或命令准入依据。                    |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                    |
| [contract.ts](contract.ts)                 | 原 session record 拥有计数；租约不创建第二个运行态或调度锁。                |
| [index.ts](index.ts)                       | index 的实现文件。                                                          |
| [model-context.ts](model-context.ts)       | 两种输入协议共用执行材料投影；不把 Secret/Ticket 放入可持久化的 intent。    |
| [module.ts](module.ts)                     | \* cli-session-execution 模块清单（architecture-governance managed 模块）。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                            |
| [residency-lease.ts](residency-lease.ts)   | 只等待原 record 的执行收尾；调用者须先关闭新执行准入。                      |

<!-- qingqi-directory-index:end -->
