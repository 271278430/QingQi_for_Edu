# session-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/bootstrap 基础工程中的 session control 验收与回归场景。

### 文件

| 文件                                                                       | 简要说明                                                                                 |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [app-client.test.ts](app-client.test.ts)                                   | app-client.test 的实现文件。                                                             |
| [protocol-binding.test.ts](protocol-binding.test.ts)                       | protocol-binding.test 的实现文件。                                                       |
| [README.md](README.md)                                                     | 本目录用途、子目录与逐文件说明。                                                         |
| [standalone-bootstrap-fixture.ts](standalone-bootstrap-fixture.ts)         | 实现或公开接口：CLI_TOOLS、APP_ONLY_TOOLS、cleanups。                                    |
| [standalone-bootstrap.test.ts](standalone-bootstrap.test.ts)               | 工具名统一后没有前缀：独立 CLI 只注册共有 8 个，App 独有的 4 个不出现。                  |
| [standalone-process.e2e.test.ts](standalone-process.e2e.test.ts)           | 预置在另一个 workspace 的历史会话：验证独立 CLI 读本机会话库、但不能写。                 |
| [standalone-tui-approval.e2e.test.ts](standalone-tui-approval.e2e.test.ts) | SCT08（会话工具设计 0.5）：真实 `zcode tui` 进程在伪终端中运行，键盘回答后台会话的审批。 |

<!-- qingqi-directory-index:end -->
