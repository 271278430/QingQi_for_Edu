# test

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/session-control 基础工程中的 test 测试场景。

### 文件

| 文件                                                     | 简要说明                                                                                           |
| -------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [client-caller.test.ts](client-caller.test.ts)           | 调用方两类（docs/plugins/extension-host.md §17.2）：App 上下文分成 session（模型工具，有根会话）与 |
| [control.test.ts](control.test.ts)                       | 规格 0.14：cwd 已从契约删除，多传即被 strictObject 拒。                                            |
| [isolation.test.ts](isolation.test.ts)                   | / <reference types="node" />                                                                       |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                                   |
| [review-regressions.test.ts](review-regressions.test.ts) | review-regressions.test 的实现文件。                                                               |
| [session-id.test.ts](session-id.test.ts)                 | 会话 ID 写法：与完整引用二选一，由可信端口解析后沿原有授权与 owner 校验执行。                      |
| [wait.test.ts](wait.test.ts)                             | wait.test 的实现文件。                                                                             |

<!-- qingqi-directory-index:end -->
