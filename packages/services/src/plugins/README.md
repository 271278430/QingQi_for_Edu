# plugins

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 plugins 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                                                    |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| [installedPluginRoots.ts](installedPluginRoots.ts)       | 实现或公开接口：InstalledPluginRoot、readInstalledPluginRoots。                                             |
| [officialPluginCache.ts](officialPluginCache.ts)         | \* 与 apps/zcode-cli/packages/bootstrap/src/app/official-plugin-definitions.ts 的 defaultEnabled 保持一致。 |
| [pluginManagement.ts](pluginManagement.ts)               | 平台能力面收敛：设置页「插件管理」的薄服务接口。                                                            |
| [pluginManagementService.ts](pluginManagementService.ts) | 设置页插件管理薄服务实现——plugins/\* 旧协议词的唯一 host 侧消费点。                                         |
| [plugins.ts](plugins.ts)                                 | 实现或公开接口：IPluginsService。                                                                           |
| [pluginsService.ts](pluginsService.ts)                   | 实现或公开接口：createPluginsService。                                                                      |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                                            |

<!-- qingqi-directory-index:end -->
