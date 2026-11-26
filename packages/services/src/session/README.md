# session

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 session 实现源码。

### 子目录

| 目录                                      | 存放内容                                              |
| ----------------------------------------- | ----------------------------------------------------- |
| [claude-native/](claude-native/README.md) | @zcode/services 基础工程中的 claude native 实现源码。 |
| [tasksDatabase/](tasksDatabase/README.md) | @zcode/services 基础工程中的 tasksDatabase 实现源码。 |

### 文件

| 文件                                                                         | 简要说明                                                                                                                                        |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| [automationCron.ts](automationCron.ts)                                       | 一次性固定月日 cron「目标刚过去」的识别窗口。模型对“现在”的时刻常是陈旧的（时间上下文停留在                                                     |
| [automationCronValidation.ts](automationCronValidation.ts)                   | 校验 cron 表达式是否合法（5 段，本地时区）。                                                                                                    |
| [automationIntervalCarrier.ts](automationIntervalCarrier.ts)                 | 会话侧自定义重复 carrier 的受控上限；不要收紧管理页历史 scheduleRule 的领域上限。                                                               |
| [automationRepo.ts](automationRepo.ts)                                       | 在调用方的归档事务内暂停全部绑定任务，不撤销已认领轮次或改变终态。                                                                              |
| [automationService.ts](automationService.ts)                                 | 写/单查操作的 workspace 归属；用于跨 workspace 隔离校验。                                                                                       |
| [continuousStreamCoalescer.ts](continuousStreamCoalescer.ts)                 | Bugfix: api_retry 会以 session_info_update 高频推送，但 title/target 是会话元信息变更。                                                         |
| [controllerRemoteIdentityMigration.ts](controllerRemoteIdentityMigration.ts) | 实现或公开接口：ControllerRemoteIdentityMigrationOptions、ControllerRemoteIdentityMigrationReport、migrateControllerRemoteWorkspaceIdentity。   |
| [fileChangeTracker.ts](fileChangeTracker.ts)                                 | \* Session 文件变更追踪器                                                                                                                       |
| [legacyTaskSessionFile.ts](legacyTaskSessionFile.ts)                         | Claude 原生迁移会按清洗路径删除 meta.mode。                                                                                                     |
| [mcpWorkspaceScope.ts](mcpWorkspaceScope.ts)                                 | 用户目录里的 filesystem MCP 可能只包含固定目录，                                                                                                |
| [offPeakMockGateway.ts](offPeakMockGateway.ts)                               | off-peak 进程内 mock 网关。                                                                                                                     |
| [offPeakResidentExecutions.ts](offPeakResidentExecutions.ts)                 | Host 只关联驻留执行和票据请求；后台工作清单与完成判断仍由 CLI 唯一维护。                                                                        |
| [offPeakRuntimeModel.ts](offPeakRuntimeModel.ts)                             | Host 派发时按当前票据构造逐请求鉴权材料；Provider/Model 静态事实由 Built-in Config 提供。                                                       |
| [offPeakServerClient.ts](offPeakServerClient.ts)                             | off-peak 服务端五接口客户端。                                                                                                                   |
| [offPeakTask.ts](offPeakTask.ts)                                             | 闲时任务管理服务通道（与 automation 服务面互不采用）。                                                                                          |
| [offPeakTaskRepo.ts](offPeakTaskRepo.ts)                                     | off-peak 任务仓库：off_peak_tasks 的 sqlite schema、状态机守卫写入与调度认领。                                                                  |
| [offPeakTaskService.ts](offPeakTaskService.ts)                               | off-peak 任务编排服务（host 域，仿 automationService 形态）。                                                                                   |
| [offPeakWorkspaceIdentityMigration.ts](offPeakWorkspaceIdentityMigration.ts) | 在调用方的身份迁移写事务内执行，紧接着由调用方统一 rekey。                                                                                      |
| [README.md](README.md)                                                       | 本目录用途、子目录与逐文件说明。                                                                                                                |
| [sessionMailbox.ts](sessionMailbox.ts)                                       | 实现或公开接口：SessionMessageSendRequested、SessionMessageDeliveryResult。                                                                     |
| [sessionModeOptions.ts](sessionModeOptions.ts)                               | Bugfix: provider 原生 modeId 和本地持久化的 session mode 不是一套枚举。                                                                         |
| [sessionRealtimePort.ts](sessionRealtimePort.ts)                             | 实现或公开接口：SessionRealtimePort。                                                                                                           |
| [sessionTitle.ts](sessionTitle.ts)                                           | 实现或公开接口：deriveSessionTitle。                                                                                                            |
| [sourceServerWorkspaceAliasRepo.ts](sourceServerWorkspaceAliasRepo.ts)       | 实现或公开接口：SourceServerWorkspaceAliasRepoOptions、WORKSPACE_MIGRATION_PHASES、WorkspaceMigrationPhase、ResolveCanonicalWorkspaceKeyInput。 |
| [taskChangeSummary.ts](taskChangeSummary.ts)                                 | \* 按轮次分组构建文件变更摘要。                                                                                                                 |
| [taskIndexRepo.ts](taskIndexRepo.ts)                                         | Bugfix: ZCode Agent 列表入口只展示当前 glm runtime 产生的 task。                                                                                |
| [toolPlanAdapter.ts](toolPlanAdapter.ts)                                     | toolPlanAdapter 的实现文件。                                                                                                                    |
| [zcodeTaskListTypes.ts](zcodeTaskListTypes.ts)                               | host 由存储 owner 确定全部范围，不接受 UI 已打开工作区作为历史目录。                                                                            |
| [zcodeTaskService.ts](zcodeTaskService.ts)                                   | 同一 workspace 的固定归档删除集合；每个去重后的目标恰好属于一种结果。                                                                           |

<!-- qingqi-directory-index:end -->
