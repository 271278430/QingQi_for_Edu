# permissions

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 permissions 测试场景。

### 文件

| 文件                                                                                                                                                                   | 简要说明                                                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [conversation-session-ask-user-question-answer-visible.test.ts](conversation-session-ask-user-question-answer-visible.test.ts)                                         | V4 已移除旧历史属性；失败录                                                                 |
| [conversation-session-ask-user-question-auto-resolution-setting.test.ts](conversation-session-ask-user-question-auto-resolution-setting.test.ts)                       | conversation-session-ask-user-question-auto-resolution-setting.test 的实现文件。            |
| [conversation-session-ask-user-question-custom-click-multi-question.test.ts](conversation-session-ask-user-question-custom-click-multi-question.test.ts)               | conversation-session-ask-user-question-custom-click-multi-question.test 的实现文件。        |
| [conversation-session-ask-user-question-custom-enter-manual-multi-question.test.ts](conversation-session-ask-user-question-custom-enter-manual-multi-question.test.ts) | conversation-session-ask-user-question-custom-enter-manual-multi-question.test 的实现文件。 |
| [conversation-session-ask-user-question-custom-enter-multi-question.test.ts](conversation-session-ask-user-question-custom-enter-multi-question.test.ts)               | 回归点：custom input 的 Enter 不能绕过多题分页，否则第 1 题会把整个问答提前提交。           |
| [conversation-session-ask-user-question-custom-enter-single-question.test.ts](conversation-session-ask-user-question-custom-enter-single-question.test.ts)             | 对照多题 case：单题 custom input 的 Enter 应等价于最终提交。                                |
| [conversation-session-ask-user-question-custom-mixed-manual-multi-question.test.ts](conversation-session-ask-user-question-custom-mixed-manual-multi-question.test.ts) | conversation-session-ask-user-question-custom-mixed-manual-multi-question.test 的实现文件。 |
| [conversation-session-ask-user-question-keyboard-default-focus.test.ts](conversation-session-ask-user-question-keyboard-default-focus.test.ts)                         | Q15: 弹窗打开无预选 → 鼠标点 Submit → 提交空答案                                            |
| [conversation-session-ask-user-question-keyboard-navigation.test.ts](conversation-session-ask-user-question-keyboard-navigation.test.ts)                               | Bug 根因：已转正用例仍经由 legacy helper 定位消息，                                         |
| [conversation-session-permission-full-access.test.ts](conversation-session-permission-full-access.test.ts)                                                             | PA158：真实审批、风险勾选、混合 Plan 队列及队列项冻结编辑。                                 |
| [conversation-session-permission-hook-race.test.ts](conversation-session-permission-hook-race.test.ts)                                                                 | HK16（catalog HK 组）：PermissionRequest hook 与审批交互竞速（permission-responder-race）。 |
| [conversation-session-permission-hook-rewrite.test.ts](conversation-session-permission-hook-rewrite.test.ts)                                                           | DCA-V1-06：共享审批在旧 build 模式下的 Hook 改写交互，不修改 Guarded 产品合同。             |
| [conversation-session-v4-bash-command-prefix-permission.test.ts](conversation-session-v4-bash-command-prefix-permission.test.ts)                                       | BPR01/BPR02：Bash 项目始终允许使用 AST command prefix，而不是完整命令字符串。               |
| [conversation-session-v4-permission.test.ts](conversation-session-v4-permission.test.ts)                                                                               | M4 门禁：v4 前向命令 resolveInteraction 收口反向权限请求（catalog Q 组 / permission）。     |
| [conversation-session-v4-refresh-permission.test.ts](conversation-session-v4-refresh-permission.test.ts)                                                               | 刷新恢复×权限挂起（环境故障 catalog：权限弹窗挂起时刷新；case catalog 战役优先面）。        |
| [conversation-session-yolo-confirmation.test.ts](conversation-session-yolo-confirmation.test.ts)                                                                       | conversation-session-yolo-confirmation.test 的实现文件。                                    |
| [README.md](README.md)                                                                                                                                                 | 本目录用途、子目录与逐文件说明。                                                            |

<!-- qingqi-directory-index:end -->
