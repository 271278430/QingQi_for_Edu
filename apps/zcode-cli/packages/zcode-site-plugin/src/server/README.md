# server

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/zcode-site-plugin 基础工程中的 server 实现源码。

### 文件

| 文件                                 | 简要说明                                                                        |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| [api.test.ts](api.test.ts)           | api.test 的实现文件。                                                           |
| [api.ts](api.ts)                     | \* 宿主在每条发给 stdio 官方 MCP 的消息上附的身份结果，键与 `@zcode/shared` 的  |
| [commands.test.ts](commands.test.ts) | commands.test 的实现文件。                                                      |
| [commands.ts](commands.ts)           | _ 面板菜单项来自插件自己的 `commands/_.md`，提示词只维护一份（技术方案 4.4）。  |
| [main.ts](main.ts)                   | 官方插件宿主通过导出的 main 启动；导入时直接连接会被宿主判定为无效入口。        |
| [README.md](README.md)               | 本目录用途、子目录与逐文件说明。                                                |
| [routes.test.ts](routes.test.ts)     | routes.test 的实现文件。                                                        |
| [routes.ts](routes.ts)               | 每个查询参数的取值规则；cursor 是服务端给的不透明串，原样转交。                 |
| [server.test.ts](server.test.ts)     | server.test 的实现文件。                                                        |
| [server.ts](server.ts)               | 前缀由服务端规范化（小写、非 [a-z0-9] 变 -、截断 30），这里只挡明显过长的输入。 |

<!-- qingqi-directory-index:end -->
