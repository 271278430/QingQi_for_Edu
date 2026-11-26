# e2e-promotion

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

e2e promotion 设计与维护文档，属于 docs 目录。

### 文件

| 文件                                                                                                       | 简要说明                                                        |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [01-project-create-telemetry-source.md](01-project-create-telemetry-source.md)                             | 项目新建入口的会话来源埋点错误：说明文档。                      |
| [02-edit-fork-model-selection.md](02-edit-fork-model-selection.md)                                         | 编辑重发与 Fork 没有使用 Composer 当前模型：说明文档。          |
| [03-auto-compact-duplicate-command.md](03-auto-compact-duplicate-command.md)                               | 自动压缩期间重复 compact 被错误入队：说明文档。                 |
| [04-remote-join-before-renderer-attachment.md](04-remote-join-before-renderer-attachment.md)               | 远程重复连接在 renderer attachment 创建前失败：说明文档。       |
| [05-first-submit-project-frame-order.md](05-first-submit-project-frame-order.md)                           | 项目首发列表行先于详情绑定出现：说明文档。                      |
| [06-plugin-source-error-lost-on-auto-refresh.md](06-plugin-source-error-lost-on-auto-refresh.md)           | 插件目录自动刷新丢弃添加来源的错误：说明文档。                  |
| [07-remote-project-editor-escape.md](07-remote-project-editor-escape.md)                                   | 远程项目编辑器收到 Escape 后仍保持打开：说明文档。              |
| [08-file-tree-tooltip-contract.md](08-file-tree-tooltip-contract.md)                                       | 文件树更多按钮未提供 SBT03 约定的悬停提示：说明文档。           |
| [09-git-find-match-not-centered.md](09-git-find-match-not-centered.md)                                     | Git 文件变更查找只展开文件，未定位到命中文本：说明文档。        |
| [10-feishu-group-draft-mode-missing.md](10-feishu-group-draft-mode-missing.md)                             | 飞书群组草稿无法设置权限模式：说明文档。                        |
| [11-oversized-image-upload-error-code.md](11-oversized-image-upload-error-code.md)                         | 超限图片上传提示暴露内部错误码：说明文档。                      |
| [12-automation-task-membership-lost.md](12-automation-task-membership-lost.md)                             | 定时任务执行会话丢失自动化归属：说明文档。                      |
| [13-config-pending-blocks-first-submit.md](13-config-pending-blocks-first-submit.md)                       | 配置请求 pending 阻塞普通聊天首发：说明文档。                   |
| [14-additional-root-subagents-missing.md](14-additional-root-subagents-missing.md)                         | 附加目录的 Subagent 没有进入模型请求：说明文档。                |
| [15-browser-guest-destroyed-on-task-switch.md](15-browser-guest-destroyed-on-task-switch.md)               | 切到新草稿时内嵌浏览器 guest 被销毁：说明文档。                 |
| [16-offpeak-selection-leaks-into-resumed-composer.md](16-offpeak-selection-leaks-into-resumed-composer.md) | 闲时任务完成后恢复对话，Composer 仍引用隐藏闲时模型：说明文档。 |
| [18-electron-quit-window-not-closed.md](18-electron-quit-window-not-closed.md)                             | 项目列表回放结束后 Electron 窗口未关闭：说明文档。              |
| [19-login-guard-settings-hydration-order.md](19-login-guard-settings-hydration-order.md)                   | 冷恢复欢迎页与设置水合顺序：说明文档。                          |
| [20-edit-submit-rejected-near-title-update.md](20-edit-submit-rejected-near-title-update.md)               | 标题更新附近编辑提交没有发起重跑：说明文档。                    |
| [21-query-continues-after-runtime-close.md](21-query-continues-after-runtime-close.md)                     | 归档并删除首发任务后，已关闭运行时仍继续查询：说明文档。        |
| [22-start-plan-subagent-thought-menu.md](22-start-plan-subagent-thought-menu.md)                           | Start Plan 回放中思考档位菜单未打开：说明文档。                 |
| [23-production-model-trajectory-store-bridge.md](23-production-model-trajectory-store-bridge.md)           | 生产 renderer 无条件暴露模型轨迹测试 Store：说明文档。          |
| [24-remote-project-entry-overlapping-navigation.md](24-remote-project-entry-overlapping-navigation.md)     | 远程项目创建后立即新建任务，连接完成却返回本地草稿：说明文档。  |
| [README.md](README.md)                                                                                     | 本目录用途、子目录与逐文件说明。                                |

<!-- qingqi-directory-index:end -->
