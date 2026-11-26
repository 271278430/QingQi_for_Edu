# tasksDatabase

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 tasksDatabase 实现源码。

### 文件

| 文件                                                             | 简要说明                                                                              |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [controller-remote-schema-v4.ts](controller-remote-schema-v4.ts) | 冻结 Controller 审计表结构；workspace 数据迁移仍由业务事务单独记账。                  |
| [migrations.ts](migrations.ts)                                   | 冻结历史列声明，不能以实时 Repo/schema 代替，否则新版构建会改变已应用 checksum。      |
| [official-glm-selection-v3.ts](official-glm-selection-v3.ts)     | 冻结本次改名表与 SQL：不能改旧 migration 或引用会随发布变化的实时目录。               |
| [prepared.ts](prepared.ts)                                       | 仅当前进程的启动交接凭据；不落盘、不代替 SQLite 账本，不影响不同路径的新库。          |
| [provider-selection-v2.ts](provider-selection-v2.ts)             | 冻结 0002 的发布前已裁决编码；不能调用将来可能修改的运行时 parser/身份表。            |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                      |
| [schema-v1.ts](schema-v1.ts)                                     | 0001 接管已有分散建表；发布后保持声明不变，后续变更新增 migration。                   |
| [source-server-schema-v5.ts](source-server-schema-v5.ts)         | 冻结旧 v1/v2/v3 接管规则；新变更必须追加 migration，不修改这里的 SQL 或转换语义版本。 |

<!-- qingqi-directory-index:end -->
