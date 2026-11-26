# config

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 config 实现源码。

### 文件

| 文件                                                   | 简要说明                                                                                          |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| [config-factory.ts](config-factory.ts)                 | Config Factory - Load and merge all config sources                                                |
| [config-merger.ts](config-merger.ts)                   | Config Merger - Merge configs by priority                                                         |
| [env-config.adapter.ts](env-config.adapter.ts)         | Env Config Adapter - Parse the intentionally small ZCODE\_\* environment surface.                 |
| [file-config.adapter.ts](file-config.adapter.ts)       | File Config Adapter - Load and patch JSON configuration files                                     |
| [index.ts](index.ts)                                   | Config Port Implementation - Scoped configuration with change notification                        |
| [plugin-secrets.adapter.ts](plugin-secrets.adapter.ts) | Plugin Secrets Adapter - 敏感插件选项的私有文件（plugin-compat.md「Sensitive Option Storage」）。 |
| [project-config.adapter.ts](project-config.adapter.ts) | hooks 字段已由 loadFileConfig 经 ZCodeConfigFileSchema（shared 单源                               |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                                  |
| [schema.ts](schema.ts)                                 | Host DTO 和连接池已有 isolation；文件解析不能丢弃整条已支持的声明。                               |

<!-- qingqi-directory-index:end -->
