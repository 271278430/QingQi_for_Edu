# domain

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 domain 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                 |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [compare.ts](compare.ts)                       | \* 数据同步比较（docs/remote/data-sync.md「行状态与默认选择」）。纯函数，不做 IO。       |
| [entry.ts](entry.ts)                           | 旧同步入口（连接向导、Header、侧栏项目菜单、设置页）只在这三种 Source 远端上显示。       |
| [marketplacePlugins.ts](marketplacePlugins.ts) | \* marketplace 插件分类的纯映射（docs/remote/data-sync.md「插件 · marketplace 插件」）。 |
| [providers.ts](providers.ts)                   | 模型提供商分类的一行（只读）。API Key 在投影时就掩码，明文不进入弹窗状态。               |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                         |

<!-- qingqi-directory-index:end -->
