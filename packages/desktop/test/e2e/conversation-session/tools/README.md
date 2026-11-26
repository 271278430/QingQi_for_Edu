# tools

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 tools 测试场景。

### 文件

| 文件                                                                                                                                       | 简要说明                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| [conversation-session-bash-direct-output.test.ts](conversation-session-bash-direct-output.test.ts)                                         | 合并适配：全局新任务落到独立聊天目录，Bash fixture 必须从 ZCodeProject 发起。                 |
| [conversation-session-bash-read-state.test.ts](conversation-session-bash-read-state.test.ts)                                               | 完成后历史和工具组默认收起；先展开真实内容，再逐条检查 Bash/Edit。                            |
| [conversation-session-custom-command-shell-handoff.test.ts](conversation-session-custom-command-shell-handoff.test.ts)                     | 自定义命令正文里的 `!` 块在解析阶段只改写成交给模型的 Bash 指令，说明文字写明来源是命令文件； |
| [conversation-session-file-tools-atomic-write.test.ts](conversation-session-file-tools-atomic-write.test.ts)                               | Windows 不具备 POSIX 执行位语义，明确记为跳过。                                               |
| [conversation-session-native-search-setting.test.ts](conversation-session-native-search-setting.test.ts)                                   | NSE01-NSE04/NSE09：增强 Find/Grep 只在根 Session runtime 物化时读取全局设置。                 |
| [conversation-session-tool-actions.test.ts](conversation-session-tool-actions.test.ts)                                                     | V4 将工具历史与最终正文分开；不能按正文查找旧 assistant 容器。                                |
| [conversation-session-tool-cross-product.test.ts](conversation-session-tool-cross-product.test.ts)                                         | 修复原因：WDIO 的 async wrapper 在 Windows 上仍可能按全局 120s 截断单个                       |
| [conversation-session-tool-detail-toggle-stability.test.ts](conversation-session-tool-detail-toggle-stability.test.ts)                     | 修复原因：正式 v4 replay 可能在下一条 DOM 断言前已完成整轮，工具块此时                        |
| [conversation-session-tool-discovery-card.test.ts](conversation-session-tool-discovery-card.test.ts)                                       | 工作区 helper 通过 Escape 退出新 profile 引导，避免旧跳过按钮路径等待隐藏元素。               |
| [conversation-session-tool-error-surface.test.ts](conversation-session-tool-error-surface.test.ts)                                         | 最终回复会收起工具历史；先确认回合完成，再由公共 helper 展开历史检查两张卡。                  |
| [conversation-session-tool-groups-history-restore.test.ts](conversation-session-tool-groups-history-restore.test.ts)                       | 工具摘要字段用布局间距分隔，不能重新插入装饰性中点。                                          |
| [conversation-session-tool-history-order.test.ts](conversation-session-tool-history-order.test.ts)                                         | D19：保留更早轮的工具记录，再编辑最新用户消息，核对真实 provider 历史。                       |
| [conversation-session-tool-input-validation-provider-content.test.ts](conversation-session-tool-input-validation-provider-content.test.ts) | Bug 回归边界：renderer refresh 仍可能采用 CLI 内存；必须等待旧 Electron、                     |
| [conversation-session-toolsearch-catalog.test.ts](conversation-session-toolsearch-catalog.test.ts)                                         | 目录由隔离 driver 注入；HTTP adapter、Runtime、SQLite 和 compact 均是真实实现。               |
| [conversation-session-toolsearch-cli.test.ts](conversation-session-toolsearch-cli.test.ts)                                                 | conversation-session-toolsearch-cli.test 的实现文件。                                         |
| [conversation-session-toolsearch-compact.test.ts](conversation-session-toolsearch-compact.test.ts)                                         | conversation-session-toolsearch-compact.test 的实现文件。                                     |
| [conversation-session-toolsearch-feedback.test.ts](conversation-session-toolsearch-feedback.test.ts)                                       | conversation-session-toolsearch-feedback.test 的实现文件。                                    |
| [conversation-session-toolsearch-lifecycle.test.ts](conversation-session-toolsearch-lifecycle.test.ts)                                     | 摘要移走旧调用；默认关闭时仍按当前目录发送完整 schema。                                       |
| [conversation-session-toolsearch-local-feedback.test.ts](conversation-session-toolsearch-local-feedback.test.ts)                           | conversation-session-toolsearch-local-feedback.test 的实现文件。                              |
| [conversation-session-toolsearch-local.test.ts](conversation-session-toolsearch-local.test.ts)                                             | conversation-session-toolsearch-local.test 的实现文件。                                       |
| [conversation-session-toolsearch-recording.test.ts](conversation-session-toolsearch-recording.test.ts)                                     | 比较 ToolSearch 相关有序片段，不把 adapter 的相邻 user 合并或 cache_control 当作差异。        |
| [conversation-session-toolsearch-recovery.test.ts](conversation-session-toolsearch-recovery.test.ts)                                       | conversation-session-toolsearch-recovery.test 的实现文件。                                    |
| [conversation-session-toolsearch-scope.test.ts](conversation-session-toolsearch-scope.test.ts)                                             | conversation-session-toolsearch-scope.test 的实现文件。                                       |
| [conversation-session-toolsearch-settings.test.ts](conversation-session-toolsearch-settings.test.ts)                                       | conversation-session-toolsearch-settings.test 的实现文件。                                    |
| [conversation-session-toolsearch-tui.test.ts](conversation-session-toolsearch-tui.test.ts)                                                 | 动画也会触发重绘；仅等帧数会在输入状态尚未提交时按 Enter，导致旧文本回写。                    |
| [conversation-session-toolsearch.test.ts](conversation-session-toolsearch.test.ts)                                                         | 批量运行时会保留测试账号，但新 renderer profile 仍需完成职业引导。                            |
| [conversation-session-unregistered-tool-cold-snapshot.test.ts](conversation-session-unregistered-tool-cold-snapshot.test.ts)               | 复现关键：renderer refresh 创建全新订阅，cold snapshot 只带最后 60 行；                       |
| [conversation-session-webfetch.test.ts](conversation-session-webfetch.test.ts)                                                             | conversation-session-webfetch.test 的实现文件。                                               |
| [README.md](README.md)                                                                                                                     | 本目录用途、子目录与逐文件说明。                                                              |

<!-- qingqi-directory-index:end -->
