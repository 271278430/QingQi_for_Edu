# commands

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 commands 实现源码。

### 文件

| 文件                                         | 简要说明                                                                                         |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [commandFileParser.ts](commandFileParser.ts) | 实现或公开接口：CommandFileFormat、CommandFileParser。                                           |
| [commands.ts](commands.ts)                   | 实现或公开接口：ICommandsService。                                                               |
| [commandsService.ts](commandsService.ts)     | 只用于列表展示：config.json 损坏时按空配置展示命令，不影响浏览。写入一律走 updateUserCliConfig。 |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                                                 |

<!-- qingqi-directory-index:end -->
