# agent

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 agent 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                                   | 简要说明                                                                           |
| ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| [README.md](README.md)                                                                                 | 本目录用途、子目录与逐文件说明。                                                   |
| [settings-agent-behavior.test.ts](settings-agent-behavior.test.ts)                                     | settings-agent-behavior.test 的实现文件。                                          |
| [settings-personalization.test.ts](settings-personalization.test.ts)                                   | 个性化编辑的文件就是 Agent 读取的 ~/.zcode/AGENTS.md；e2e 的 HOME 已指向隔离目录。 |
| [settings-subagent-create-edit-persistence.test.ts](settings-subagent-create-edit-persistence.test.ts) | 模型选择控件和 Subagent 的 model overlay 都依赖已初始化的 Provider/Registry。      |

<!-- qingqi-directory-index:end -->
