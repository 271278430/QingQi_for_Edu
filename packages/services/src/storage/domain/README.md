# domain

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 domain 实现源码。

### 文件

| 文件                                   | 简要说明                                                                              |
| -------------------------------------- | ------------------------------------------------------------------------------------- |
| [cleanPlan.ts](cleanPlan.ts)           | \* 清理计划：给定类别与候选文件列表，决定哪些能删。纯函数，删除动作由 adapters 执行。 |
| [README.md](README.md)                 | 本目录用途、子目录与逐文件说明。                                                      |
| [storageCatalog.ts](storageCatalog.ts) | \* 存储分类目录：把 .zcode 根下的相对路径映射到类别、聚合 key 与可清理性。            |
| [usageAggregate.ts](usageAggregate.ts) | \* 扫描条目 → 根目录占用快照的折叠器。纯函数式累加器，可在 Worker 内运行。            |

<!-- qingqi-directory-index:end -->
