# settings-search

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 settings search 实现源码。

### 文件

| 文件                                                       | 简要说明                                                                  |
| ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                 | 搜索结果交给 SettingsPage 原导航；设置行挂载后按 id 定位。                |
| [CONTRACT.md](CONTRACT.md)                                 | 模块职责、公共接口、依赖方向和状态约定。                                  |
| [contract.ts](contract.ts)                                 | 仅导航到分类或固定设置行；调用方不得据此修改设置值。                      |
| [index.ts](index.ts)                                       | index 的实现文件。                                                        |
| [module.ts](module.ts)                                     | \* settings-search 模块清单（architecture-governance managed 模块）。     |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                          |
| [settingsNavigationSearch.ts](settingsNavigationSearch.ts) | 实现或公开接口：settingsNavigationSearchKeys、matchesSettingsNavigation。 |
| [SettingsSearch.tsx](SettingsSearch.tsx)                   | 说明较长，只做片段匹配，避免顺序字符在整段说明中产生大量无关结果。        |
| [settingsSearchIndex.ts](settingsSearchIndex.ts)           | 翻译 key 同时作为稳定定位 id；索引只描述入口，不持有任何配置值。          |
| [SettingsSearchTarget.tsx](SettingsSearchTarget.tsx)       | 分区可能异步挂载；由真实设置行消费目标，避免定时滚动抢在控件出现之前。    |

<!-- qingqi-directory-index:end -->
