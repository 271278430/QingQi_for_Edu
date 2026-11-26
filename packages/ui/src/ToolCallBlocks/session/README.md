# session

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 session 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                     |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)     | 注册表仅对四个精确工具名选择会话展示，其他工具继续原分流。                                   |
| [CONTRACT.md](CONTRACT.md)                     | 模块职责、公共接口、依赖方向和状态约定。                                                     |
| [contract.ts](contract.ts)                     | 会话工具展示入口；只消费既有 tool call，不发起会话操作或额外查询。                           |
| [module.ts](module.ts)                         | \* session-tool-presentation 模块清单（architecture-governance managed 模块）。              |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                             |
| [session.tsx](session.tsx)                     | 已有 output 是当前投影的唯一结果；只有字段缺失才读取旧快照 rawOutput，避免旧成功覆盖新失败。 |
| [ToolDetailSection.tsx](ToolDetailSection.tsx) | 实现或公开接口：ToolDetailSection。                                                          |

<!-- qingqi-directory-index:end -->
