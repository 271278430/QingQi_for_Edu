# projects

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 projects 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                   | 简要说明                                                                                  |
| ---------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [conversation-session-conversation-workspace.test.ts](conversation-session-conversation-workspace.test.ts)             | conversation-session-conversation-workspace.test 的实现文件。                             |
| [conversation-session-deleted-project-new-task.test.ts](conversation-session-deleted-project-new-task.test.ts)         | conversation-session-deleted-project-new-task.test 的实现文件。                           |
| [conversation-session-git-review-entry.test.ts](conversation-session-git-review-entry.test.ts)                         | 通过真实文件 watcher 刷新；无需打开 Git pane，也不创建会话或调用模型。                    |
| [conversation-session-new-task-missing-root-mobile.test.ts](conversation-session-new-task-missing-root-mobile.test.ts) | 配对材料只经内存与 loopback 传递，不写 WebDriver 日志。                                   |
| [conversation-session-project-composer.test.ts](conversation-session-project-composer.test.ts)                         | 列表先收到保存结果，编辑器遮罩在退出动画结束后才卸载；不能先点击下一个创建入口。          |
| [conversation-session-project-device-selection.test.ts](conversation-session-project-device-selection.test.ts)         | 保留真实 SSH 连接，只阻挡完成响应，让活动页签断言覆盖连接进行中。                         |
| [conversation-session-project-management.test.ts](conversation-session-project-management.test.ts)                     | \* 设置 › 项目管理（docs/superpowers/specs/2026-10-24-project-management.md）。           |
| [conversation-session-project-missing-primary-root.test.ts](conversation-session-project-missing-primary-root.test.ts) | 暂时跳过原因：Agent 进程以主目录为 cwd 常驻，Windows 不允许重命名任一进程的 cwd           |
| [conversation-session-project-new-order-mobile.test.ts](conversation-session-project-new-order-mobile.test.ts)         | PRO02 独立成 spec：它会新建项目、切换当前工作区并打开远控弹窗，中途失败时不恢复这些状态。 |
| [conversation-session-project-upgrade-order.test.ts](conversation-session-project-upgrade-order.test.ts)               | 失败原因：新增 tasks_index 迁移（0009、两个 0010）后，这份完整清单没有同步。              |
| [conversation-session-rpn-project-navigation.test.ts](conversation-session-rpn-project-navigation.test.ts)             | 高级区展开时按钮先挂载、文字仍被动画裁切；等待实际可见文案，不能把这一帧当成缺少选项。    |
| [conversation-session-system-open-folder-project.test.ts](conversation-session-system-open-folder-project.test.ts)     | 使用 Explorer 的 argv 入口，保留真实 Main → preload → Root → Host 项目保存链路。          |
| [conversation-session-unavailable-project-draft.test.ts](conversation-session-unavailable-project-draft.test.ts)       | 原因：启动 helper 不能点击“新建任务”修复前置，否则会掩盖默认选中失效项目的空白页。        |
| [conversation-session-virtual-project-mentions.test.ts](conversation-session-virtual-project-mentions.test.ts)         | 同时接受统一 runner 与旧手工入口的隔离 HOME，禁止写入日常用户目录。                       |
| [conversation-session-virtual-project-mobile.test.ts](conversation-session-virtual-project-mobile.test.ts)             | 统一 runner 与旧手工入口均使用隔离 HOME；不能因 runId 前缀不同拒绝安全夹具。              |
| [conversation-session-virtual-project.test.ts](conversation-session-virtual-project.test.ts)                           | 统一 runner 与旧手工入口均使用隔离 HOME；不能因 runId 前缀不同拒绝安全夹具。              |
| [conversation-session-workspace-file-search-filter.test.ts](conversation-session-workspace-file-search-filter.test.ts) | E2E case for catalog SFF01（Workspace File Search Default Filter）。                      |
| [conversation-session-workspace-readonly-notice.test.ts](conversation-session-workspace-readonly-notice.test.ts)       | 两库夹具只在旧 Main/Host/Agent 完整退出后写入，再经 UI 打开真实持久历史。                 |
| [conversation-session-workspace-zcodeignore.test.ts](conversation-session-workspace-zcodeignore.test.ts)               | gitignore 解析按行识别，行尾风格不影响规则；统一写 \n 避免 e2e 源码里出现跨行字面量。     |
| [README.md](README.md)                                                                                                 | 本目录用途、子目录与逐文件说明。                                                          |

<!-- qingqi-directory-index:end -->
