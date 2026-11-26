# runtime

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 runtime 测试场景。

### 文件

| 文件                                                                   | 简要说明                                                                    |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [bot-deleted-task-recovery.test.ts](bot-deleted-task-recovery.test.ts) | 数据文件位置按当前 spec 计算，fixture 仍在 E2E 根目录下。                   |
| [bot-effective-selection.test.ts](bot-effective-selection.test.ts)     | bot-effective-selection.test 的实现文件。                                   |
| [bot-polling-retry-backoff.test.ts](bot-polling-retry-backoff.test.ts) | runtime 只读取 token；其余凭据能力与本用例无关。                            |
| [bot-r3-workspace-identity.test.ts](bot-r3-workspace-identity.test.ts) | bot-r3-workspace-identity.test 的实现文件。                                 |
| [bot-remote-disconnected.test.ts](bot-remote-disconnected.test.ts)     | bot-remote-disconnected.test 的实现文件。                                   |
| [bot-runtime-authority.test.ts](bot-runtime-authority.test.ts)         | 与 services/node.ts 的 !isDesktopAttachedRemote 装配一致；这是 owner 权限， |
| [feishu-runtime-error-ui.test.ts](feishu-runtime-error-ui.test.ts)     | E2E runner 首帧会跟随系统语言；刷新后读取本用例写入的中文设置，             |
| [README.md](README.md)                                                 | 本目录用途、子目录与逐文件说明。                                            |

<!-- qingqi-directory-index:end -->
