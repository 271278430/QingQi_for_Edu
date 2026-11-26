# configuration

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 configuration 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                                                               | 简要说明                                                                                              |
| -------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [conversation-session-legacy-remote-credential-decrypt.test.ts](conversation-session-legacy-remote-credential-decrypt.test.ts)                     | IV/AuthTag 长度合法、内容为零：本机任何密钥都无法通过 GCM 校验，                                      |
| [conversation-session-r3-desktop-settings-authority.test.ts](conversation-session-r3-desktop-settings-authority.test.ts)                           | 冷重启后的 Main/Host 仍会写 customRoot，提前 rm 会与写入竞争并报 ENOTEMPTY。                          |
| [conversation-session-r3-hooks-local-scope.test.ts](conversation-session-r3-hooks-local-scope.test.ts)                                             | 项目在各设备的「项目」子菜单里（19 号票），逐个打开后合并。                                           |
| [conversation-session-r3-model-candidates.test.ts](conversation-session-r3-model-candidates.test.ts)                                               | 打开模型菜单读取候选（provider 分组 + 已展开模型项）后关闭；trigger 不可用时只记录状态。              |
| [conversation-session-r3-model-switch.test.ts](conversation-session-r3-model-switch.test.ts)                                                       | 第二个 provider/model（同回放隧道），首连同步前写入以便一次下发。                                     |
| [conversation-session-r3-remote-hooks.test.ts](conversation-session-r3-remote-hooks.test.ts)                                                       | hooks 在 Agent 启动时加载：若目标 workspace 已有存活 Agent（O-01），先终止让其重建。                  |
| [conversation-session-r3-settings-scopes.test.ts](conversation-session-r3-settings-scopes.test.ts)                                                 | 读取当前分区的 scope 选择器可选项（Source/项目/User 等），没有 scope 选择器时返回 null。              |
| [conversation-session-ssh-remote-settings-overlay-sidebar-status.test.ts](conversation-session-ssh-remote-settings-overlay-sidebar-status.test.ts) | 读取侧栏"项目"视图里该 task 行的前导指示器：running=转圈（sessions-index phase running/prewarming）。 |
| [README.md](README.md)                                                                                                                             | 本目录用途、子目录与逐文件说明。                                                                      |

<!-- qingqi-directory-index:end -->
