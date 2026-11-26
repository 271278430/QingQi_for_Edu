# navigation

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 navigation 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                                 | 简要说明                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- |
| [conversation-session-chat-device-return.test.ts](conversation-session-chat-device-return.test.ts)                                   | conversation-session-chat-device-return.test 的实现文件。                                 |
| [conversation-session-chat-remote-folder-create.test.ts](conversation-session-chat-remote-folder-create.test.ts)                     | conversation-session-chat-remote-folder-create.test 的实现文件。                          |
| [conversation-session-chat-remote-folder.test.ts](conversation-session-chat-remote-folder.test.ts)                                   | 用既有 RPC 接缝回放旧端只读目录投影；不声称运行了旧 Server 二进制。                       |
| [conversation-session-chat-remote-project-choice.test.ts](conversation-session-chat-remote-project-choice.test.ts)                   | 候选弹窗打开后 Composer 只读；禁发用例必须从用户能输入的连接前草稿开始。                  |
| [conversation-session-existing-remote-project.test.ts](conversation-session-existing-remote-project.test.ts)                         | 窄窗口会按原产品规则收起侧栏；恢复尺寸后仍须用可见入口显式展开。                          |
| [conversation-session-r3-device-row.test.ts](conversation-session-r3-device-row.test.ts)                                             | RDUX-27：设置连接成功留在设备管理，不再进入项目选目录。                                   |
| [conversation-session-r3-entry-attribution.test.ts](conversation-session-r3-entry-attribution.test.ts)                               | 旧路径不存在时 before/after 都变成 0，会让整个同步断言假通过。                            |
| [conversation-session-r3-mixed-entries.test.ts](conversation-session-r3-mixed-entries.test.ts)                                       | 远端项目 A/B 与本地 workspace 混合恢复；旧 conversation 不属于 open set。                 |
| [conversation-session-remote-device-cards.test.ts](conversation-session-remote-device-cards.test.ts)                                 | RDUX-13：设备默认收起成一行；连接、项目、日志等详情在展开区。                             |
| [conversation-session-remote-dialog-closes-workspace-menu.test.ts](conversation-session-remote-dialog-closes-workspace-menu.test.ts) | conversation-session-remote-dialog-closes-workspace-menu.test 的实现文件。                |
| [conversation-session-remote-kind-double-click.test.ts](conversation-session-remote-kind-double-click.test.ts)                       | 先访问另一类型再返回，确保新入口不采用上一份表单类型。                                    |
| [conversation-session-remote-presentation-states.test.ts](conversation-session-remote-presentation-states.test.ts)                   | RDUX-13：断开在设备行「更多」菜单里。                                                     |
| [conversation-session-remote-project-policy.test.ts](conversation-session-remote-project-policy.test.ts)                             | 仅验证离线入口与真实侧栏交互；SSH 执行和手机 shared-host 使用各自链路用例。               |
| [conversation-session-remote-sidebar-menus.test.ts](conversation-session-remote-sidebar-menus.test.ts)                               | Escape 会关闭当前悬停浮层；下一轮必须真正离开再进入，不能把原地 moveTo 当成新的进入事件。 |
| [conversation-session-remote-sidebar-pending.test.ts](conversation-session-remote-sidebar-pending.test.ts)                           | 只读远端当前 release；走 docker exec，不占用被测 SSH 连接。                               |
| [conversation-session-ssh-remote-new-project-sidebar.test.ts](conversation-session-ssh-remote-new-project-sidebar.test.ts)           | conversation-session-ssh-remote-new-project-sidebar.test 的实现文件。                     |
| [conversation-session-ssh-remote-three-screen.test.ts](conversation-session-ssh-remote-three-screen.test.ts)                         | conversation-session-ssh-remote-three-screen.test 的实现文件。                            |
| [README.md](README.md)                                                                                                               | 本目录用途、子目录与逐文件说明。                                                          |

<!-- qingqi-directory-index:end -->
