# Monitoring 文档入口

本目录保留 App/RUM、Conversation 业务事件、资源监控、产品专项埋点和测试监控。
CLI Agent 的 OpenTelemetry 执行链路已独立到
[`docs/trace/`](../trace/README.md)，不再与其他监控文档混放。

## App、Renderer 与进程

- [性能监控](./performance-monitoring.md)
- [性能埋点事件字典](./performance-telemetry-catalog.md)
- [ARMS Electron 监控](./arms-browser-monitoring.md)
- [Agent 进程崩溃 ARMS 上报](./agent-process-crash-arms.md)
- [全进程 CPU / 内存监控埋点](./process-resource-telemetry.md)
- [全进程资源仪表盘与查询](./dashboards/process-resource-dashboard.md)
- [MCP 进程生命周期 ARMS 上报](./mcp-process-arms-telemetry.md)
- [进程内存本地诊断日志](./memory-diagnostics-log.md)

## Conversation 与业务事件

- [V4 对话埋点兼容规范](./conversation-telemetry-v4.md)
- [业务质量监控](./business-monitoring.md)
- [Agent Step 真实模型与 Token 归属](./agent-step-model-token-attribution.md)

## 产品专项

- [Plan Usage ARMS 自定义事件](./plan-usage-arms-telemetry.md)
- [远程场景使用量埋点 V1](./remote-usage-telemetry-v1.md)
- [远程工作区连接 ARMS 自定义事件](./remote-usage-arms-telemetry.md)
- [Off-Peak Task telemetry V1](./off-peak-task-telemetry-v1.md)
- [Session 首次打开 ARMS 埋点](./session-open-telemetry.md)
- [定时任务 / 闲时任务消息埋点](./automation-message-telemetry.md)

## 工程质量

- [E2E Metrics Bitable Dashboard](./e2e-metrics-bitable-dashboard.md)

本目录中的文档只负责各自监控通道或产品功能，不得重新定义 CLI Agent Trace 的 Span、
Attribute、Event、Metric、隐私和统计口径。相关变更统一更新
[`docs/trace/cli-agent-telemetry.md`](../trace/cli-agent-telemetry.md)。

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

monitoring 设计与维护文档，属于 docs 目录。

### 子目录

| 目录                                | 存放内容                                    |
| ----------------------------------- | ------------------------------------------- |
| [dashboards/](dashboards/README.md) | dashboards 设计与维护文档，属于 docs 目录。 |

### 文件

| 文件                                                                           | 简要说明                                                                               |
| ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| [agent-process-crash-arms.md](agent-process-crash-arms.md)                     | Agent 进程崩溃 ARMS 上报：说明文档。                                                   |
| [agent-step-model-token-attribution.md](agent-step-model-token-attribution.md) | Agent Step 真实模型与 Token 归属：说明文档。                                           |
| [arms-browser-monitoring.md](arms-browser-monitoring.md)                       | ARMS Electron 监控：说明文档。                                                         |
| [automation-message-telemetry.md](automation-message-telemetry.md)             | 定时任务 / 闲时任务消息埋点：说明文档。                                                |
| [business-monitoring.md](business-monitoring.md)                               | 业务质量监控：说明文档。                                                               |
| [composer-send-funnel-telemetry.md](composer-send-funnel-telemetry.md)         | Composer 发送漏斗埋点（ARMS：send_input_focus / send_click / send_result）：说明文档。 |
| [conversation-telemetry-v4.md](conversation-telemetry-v4.md)                   | V4 对话埋点兼容规范：说明文档。                                                        |
| [e2e-metrics-bitable-dashboard.md](e2e-metrics-bitable-dashboard.md)           | E2E Metrics Bitable Dashboard：说明文档。                                              |
| [event-report-delivery-reliability.md](event-report-delivery-reliability.md)   | `/event/report` 桌面投递可靠性：说明文档。                                             |
| [event-report-privacy.md](event-report-privacy.md)                             | `/event/report` 登录地址与错误正文隐私边界：说明文档。                                 |
| [local-ttft-diagnostics-evidence.json](local-ttft-diagnostics-evidence.json)   | local-ttft-diagnostics-evidence 的数据或配置定义。                                     |
| [local-ttft-evidence.json](local-ttft-evidence.json)                           | local-ttft-evidence 的数据或配置定义。                                                 |
| [local-ttft-platform-evidence.json](local-ttft-platform-evidence.json)         | local-ttft-platform-evidence 的数据或配置定义。                                        |
| [local-ttft-queries.md](local-ttft-queries.md)                                 | 本地 TTFT 查询与验收：说明文档。                                                       |
| [local-ttft-rollout-checklist.md](local-ttft-rollout-checklist.md)             | 本地 TTFT 上线与 ARMS 验收清单：说明文档。                                             |
| [local-ttft-trace-reading.md](local-ttft-trace-reading.md)                     | 怎么读一条本地 TTFT Trace：说明文档。                                                  |
| [mcp-process-arms-telemetry.md](mcp-process-arms-telemetry.md)                 | MCP 进程 ARMS 可观测性：说明文档。                                                     |
| [memory-diagnostics-log.md](memory-diagnostics-log.md)                         | 进程内存本地诊断日志：说明文档。                                                       |
| [off-peak-task-telemetry-v1.md](off-peak-task-telemetry-v1.md)                 | Off-Peak Task telemetry V1：说明文档。                                                 |
| [onboarding-telemetry.md](onboarding-telemetry.md)                             | 用户引导埋点 Spec：说明文档。                                                          |
| [performance-monitoring.md](performance-monitoring.md)                         | 性能监控：说明文档。                                                                   |
| [performance-telemetry-catalog.md](performance-telemetry-catalog.md)           | 性能埋点事件字典：说明文档。                                                           |
| [plan-usage-arms-telemetry.md](plan-usage-arms-telemetry.md)                   | Plan Usage ARMS 自定义事件：说明文档。                                                 |
| [plugin-lifecycle-telemetry.md](plugin-lifecycle-telemetry.md)                 | 插件生命周期业务埋点：说明文档。                                                       |
| [process-resource-telemetry-fixes.md](process-resource-telemetry-fixes.md)     | 进程资源遥测复审修复：影响与验证：说明文档。                                           |
| [process-resource-telemetry.md](process-resource-telemetry.md)                 | 全进程 CPU / 内存监控埋点（Process Resource Telemetry）：说明文档。                    |
| [README.md](README.md)                                                         | 本目录用途、子目录与逐文件说明。                                                       |
| [remote-usage-arms-telemetry.md](remote-usage-arms-telemetry.md)               | 远程工作区连接 ARMS 自定义事件埋点：说明文档。                                         |
| [remote-usage-telemetry-v1.md](remote-usage-telemetry-v1.md)                   | 远程场景使用量埋点 V1：说明文档。                                                      |
| [session-create-telemetry.md](session-create-telemetry.md)                     | Session 创建业务埋点：说明文档。                                                       |
| [session-open-telemetry.md](session-open-telemetry.md)                         | Session 首次打开 ARMS 埋点：说明文档。                                                 |
| [session-stop-source-diagnostics.md](session-stop-source-diagnostics.md)       | Session 停止来源诊断：说明文档。                                                       |
| [skill-agent-step-telemetry.md](skill-agent-step-telemetry.md)                 | Skill `agent_step` telemetry：说明文档。                                               |
| [ttft-stage-telemetry.md](ttft-stage-telemetry.md)                             | 桌面本地消息 TTFT 分阶段遥测：说明文档。                                               |
| [zcode-cli-resource-telemetry.md](zcode-cli-resource-telemetry.md)             | ZCode CLI 资源占用 ARMS 上报：说明文档。                                               |
| [zcode-data-size-arms-telemetry.md](zcode-data-size-arms-telemetry.md)         | ZCode 数据目录占用 ARMS 上报：说明文档。                                               |

<!-- qingqi-directory-index:end -->
