# plugin-sync

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 plugin sync 实现源码。

### 文件

| 文件                                         | 简要说明                                                                                            |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [pluginSync.ts](pluginSync.ts)               | \* 数据同步弹窗使用 IDataSyncCategoryService 的统一形状（inline 插件，key 为 `name@inline` 小写）。 |
| [pluginSyncArchive.ts](pluginSyncArchive.ts) | writeFile 新建文件会受远端 umask 影响；plugin 脚本的可执行位必须按归档 header 恢复。                |
| [pluginSyncPath.ts](pluginSyncPath.ts)       | 实现或公开接口：normalizePluginSyncRelativePath、resolvePluginSyncPathWithin。                      |
| [pluginSyncService.ts](pluginSyncService.ts) | manifest 的 userConfig（options schema），原样保留。                                                |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                                                    |

<!-- qingqi-directory-index:end -->
