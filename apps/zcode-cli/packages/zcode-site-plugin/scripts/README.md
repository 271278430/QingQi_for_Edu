# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/zcode-site-plugin 基础工程中的 scripts 工程脚本。

### 文件

| 文件                             | 简要说明                                                                                 |
| -------------------------------- | ---------------------------------------------------------------------------------------- |
| [build.mjs](build.mjs)           | 把插件 MCP server 和面板页面构建到 dist/：server.mjs 自包含（运行时不读 node_modules）， |
| [errors.mjs](errors.mjs)         | zcode-site 的错误：错误码到退出码和面向 Agent 的 message / hint 的映射（技术方案 5.8）。 |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。                                                         |
| [stage.mjs](stage.mjs)           | zcode-site deploy 的本地打包与 check 的本地启动检查，不调用云端。                        |
| [zcode-site.mjs](zcode-site.mjs) | zcode-site：ZCode Sites 的命令行客户端（技术方案 4.2、4.3、5.3）。                       |

<!-- qingqi-directory-index:end -->
