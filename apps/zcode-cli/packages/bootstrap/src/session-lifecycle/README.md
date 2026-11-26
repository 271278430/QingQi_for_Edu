# session-lifecycle

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 session lifecycle 实现源码。

### 文件

| 文件                                       | 简要说明                                                                          |
| ------------------------------------------ | --------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* session-lifecycle 标准调用示例：agent 靠模仿写代码，这里放的就是该模仿的那份。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                          |
| [contract.test.ts](contract.test.ts)       | contract.test 的实现文件。                                                        |
| [contract.ts](contract.ts)                 | 仅管理当前进程内的运行实例，不创建/删除持久会话，不替代停止生成接口。             |
| [controller.ts](controller.ts)             | 每个 session 一个操作所有者，覆盖初始化、部分失败清理及完整重启区间。             |
| [index.ts](index.ts)                       | index 的实现文件。                                                                |
| [module.ts](module.ts)                     | \* session-lifecycle 模块清单（architecture-governance managed 模块）。           |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                  |

<!-- qingqi-directory-index:end -->
