# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pending 测试场景。

### 文件

| 文件                                                                                                                                           | 简要说明                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [conversation-session-project-behavior.test.ts](conversation-session-project-behavior.test.ts)                                                 | 统一 runner 与旧手工入口均使用隔离 HOME；不能因 runId 前缀不同拒绝安全夹具。                |
| [conversation-session-project-device-visibility.test.ts](conversation-session-project-device-visibility.test.ts)                               | conversation-session-project-device-visibility.test 的实现文件。                            |
| [conversation-session-project-settings-return.test.ts](conversation-session-project-settings-return.test.ts)                                   | 本入口完成后会弹出项目的换设备确认；普通连接 helper 会把它误判为连接失败。                  |
| [conversation-session-rpn-18-concurrent-remote-task-navigation.test.ts](conversation-session-rpn-18-concurrent-remote-task-navigation.test.ts) | RPN-18（2026-10-20 用户日志回归）：Source 在线、窗口内没有项目 session 时点击远程任务，首连 |
| [conversation-session-rpn-same-path-local-task.test.ts](conversation-session-rpn-same-path-local-task.test.ts)                                 | Header 的工作区按钮：远程 workspace 才渲染设备名，本地只显示文件夹图标。                    |
| [conversation-session-virtual-project-cold-roots.test.ts](conversation-session-virtual-project-cold-roots.test.ts)                             | 统一 runner 与旧手工入口均使用隔离 HOME；不能因 runId 前缀不同拒绝安全夹具。                |
| [README.md](README.md)                                                                                                                         | 本目录用途、子目录与逐文件说明。                                                            |

<!-- qingqi-directory-index:end -->
