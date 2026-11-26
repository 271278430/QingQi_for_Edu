# composer-edit-mode

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 composer edit mode 实现源码。

### 文件

| 文件                                             | 简要说明                                                                                                  |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| [ComposerEditBar.tsx](ComposerEditBar.tsx)       | Composer 编辑态状态条（docs/ui/composer-edit-mode.md）：渲染在输入框卡片内顶部，                          |
| [contract.example.ts](contract.example.ts)       | 实现或公开接口：exampleComposerEditScope。                                                                |
| [CONTRACT.md](CONTRACT.md)                       | 模块职责、公共接口、依赖方向和状态约定。                                                                  |
| [contract.ts](contract.ts)                       | composer-edit-mode 契约（docs/ui/composer-edit-mode.md）：编辑态的目标、失效原因与 edit scope 规则。      |
| [editorIdentity.ts](editorIdentity.ts)           | 编辑器身份（docs/ui/composer-edit-mode.md「锁归属」）：editorId 存在 sessionStorage，刷新后沿用；         |
| [index.ts](index.ts)                             | index 的实现文件。                                                                                        |
| [module.ts](module.ts)                           | \* composer-edit-mode 模块清单（architecture-governance managed 模块）。                                  |
| [queueConfigApply.ts](queueConfigApply.ts)       | 编辑提交后把新模型/mode 应用到其他排队消息（docs/ui/composer-edit-mode.md「提交后应用到其他排队消息」）。 |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                                          |
| [store.ts](store.ts)                             | 编辑态的 renderer 内存状态：只属于发起端 renderer，不进入 snapshot、relay 或 main process；               |
| [useComposerEditMode.ts](useComposerEditMode.ts) | Composer 编辑态编排（docs/ui/composer-edit-mode.md）：进入/取消/结束编辑、队列项冻结锁、                  |

<!-- qingqi-directory-index:end -->
