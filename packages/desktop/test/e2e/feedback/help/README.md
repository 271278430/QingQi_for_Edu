# help

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 help 测试场景。

### 文件

| 文件                                                                   | 简要说明                                                                               |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [help-client-config.test.ts](help-client-config.test.ts)               | E2E 必须只改 worker 的隔离默认配置，绝不写开发者的真实安装目录。                       |
| [help-menu-about.test.ts](help-menu-about.test.ts)                     | Node 侧 shared 常量没有 renderer 的编译 define，不能据此跳过 production 分支。         |
| [help-report-vulnerability.test.ts](help-report-vulnerability.test.ts) | 只写 setting.json 不会改 renderer 语言：启动时的 locale 由 Main 生成，refresh 不重读。 |
| [README.md](README.md)                                                 | 本目录用途、子目录与逐文件说明。                                                       |

<!-- qingqi-directory-index:end -->
