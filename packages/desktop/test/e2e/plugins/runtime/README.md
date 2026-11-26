# runtime

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 runtime 测试场景。

### 子目录

| 目录                                      | 存放内容                                             |
| ----------------------------------------- | ---------------------------------------------------- |
| [manual-review/](manual-review/README.md) | @zcode/desktop 基础工程中的 manual review 测试场景。 |

### 文件

| 文件                                                                                       | 简要说明                                                                      |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| [plugin-runtime-env-agent-projection.test.ts](plugin-runtime-env-agent-projection.test.ts) | 新市场提交后还会异步持久化并刷新列表，必须等弹窗关闭后再操作下层页面。        |
| [plugin-subagent-override-cold.test.ts](plugin-subagent-override-cold.test.ts)             | 官方文档插件已拆分；旧 document-skills:judge 不在当前目录，不能验证模型覆盖。 |
| [plugin-ui-session-ready.test.ts](plugin-ui-session-ready.test.ts)                         | 同一套真实 Electron / Agent / MCP 断言；正式集合不另写一份近似实现。          |
| [README.md](README.md)                                                                     | 本目录用途、子目录与逐文件说明。                                              |

<!-- qingqi-directory-index:end -->
