# tool-search-comparison-contract

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/prompt-trajectory 基础工程中的 tool search comparison contract 实现源码。

### 文件

| 文件                                       | 简要说明                                              |
| ------------------------------------------ | ----------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 比较副本与原始请求分别保留，导出方继续使用 original。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。              |
| [contract.ts](contract.ts)                 | 输出仅用于离线比较，原始请求仍用于保存和导出轨迹。    |
| [module.ts](module.ts)                     | 离线轨迹比较只派生视图，与运行时搜索状态分开。        |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                      |

<!-- qingqi-directory-index:end -->
