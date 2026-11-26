# project-workflow

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 project workflow 实现源码。

### 文件

| 文件                                                         | 简要说明                                                                                                |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                   | 保存是否成功由 Agent 返回，调用方不能提前把卡片标为已保存。                                             |
| [CONTRACT.md](CONTRACT.md)                                   | 模块职责、公共接口、依赖方向和状态约定。                                                                |
| [contract.ts](contract.ts)                                   | 转写自对话的候选（`buildWorkflowSaveCandidatesByRunId`）。                                              |
| [module.ts](module.ts)                                       | \* project-workflow 模块清单（architecture-governance managed 模块）。                                  |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                        |
| [useWorkflowRunSave.ts](useWorkflowRunSave.ts)               | 完成卡与 run 侧板共用的「保存 / 再次运行」控制器（docs/dynamic-workflow/transcript-and-notifications.md |
| [WorkflowRunPaneSaveSlots.tsx](WorkflowRunPaneSaveSlots.tsx) | run 侧板状态头上的「保存 / 再次运行」接线（docs/dynamic-workflow/transcript-and-notifications.md        |
| [WorkflowRunSaveControls.tsx](WorkflowRunSaveControls.tsx)   | 完成卡与 run 侧板表头上的那一对控件（docs/dynamic-workflow/transcript-and-notifications.md              |

<!-- qingqi-directory-index:end -->
