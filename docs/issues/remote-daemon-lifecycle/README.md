# remote-daemon-lifecycle

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

remote daemon lifecycle 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                                             | 简要说明                                                             |
| ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| [01-stop-restart-remote-service.md](01-stop-restart-remote-service.md)                           | 01 — 在设备卡上停止和重启远端服务：说明文档。                        |
| [02-prefactor-stop-wait-and-lifecycle-flight.md](02-prefactor-stop-wait-and-lifecycle-flight.md) | 02 — 预备重构：统一“停止并等待”，泛化生命周期操作 flight：说明文档。 |
| [03-stop-remote-service.md](03-stop-remote-service.md)                                           | 03 — 停止远端服务（端到端）：说明文档。                              |
| [04-restart-remote-service.md](04-restart-remote-service.md)                                     | 04 — 重启远端服务（端到端）：说明文档。                              |
| [05-confirm-running-tasks-and-impact.md](05-confirm-running-tasks-and-impact.md)                 | 05 — 确认弹窗：运行中任务清单与影响说明：说明文档。                  |
| [06-online-error-shown-as-failed.md](06-online-error-shown-as-failed.md)                         | 06 — 生命周期操作失败但连接仍在时，设备显示“连接失败”：说明文档。    |
| [README.md](README.md)                                                                           | 本目录用途、子目录与逐文件说明。                                     |

<!-- qingqi-directory-index:end -->
