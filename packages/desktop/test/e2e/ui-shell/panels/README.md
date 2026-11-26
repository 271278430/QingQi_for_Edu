# panels

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 panels 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                             | 简要说明                                                                                            |
| ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| [preview-pane-image-copy.test.ts](preview-pane-image-copy.test.ts)                               | PIC-01/02/05：只验证文件预览和原生剪贴板，不调用模型或修改会话状态。                                |
| [README.md](README.md)                                                                           | 本目录用途、子目录与逐文件说明。                                                                    |
| [side-pane-draft-promotion.test.ts](side-pane-draft-promotion.test.ts)                           | main 关闭入口按 owner 校验；owner 未升级时 UI 壳会一直留着。                                        |
| [side-pane-full-view.test.ts](side-pane-full-view.test.ts)                                       | spec：docs/ui/side-pane-full-view.md；用例：docs/testing/side-pane-tabs-e2e-case-catalog.md（SPFV） |
| [side-pane-scope.test.ts](side-pane-scope.test.ts)                                               | 本组只验证 UI scope：通过现有 store bridge 准备 A/B 对话，关闭/恢复使用真实菜单，                   |
| [side-pane-tabs-responsive-interactions.test.ts](side-pane-tabs-responsive-interactions.test.ts) | Darwin 25 起对应 Tahoe，Sequoia 及旧系统的工作区使用更小的内层圆角。                                |

<!-- qingqi-directory-index:end -->
