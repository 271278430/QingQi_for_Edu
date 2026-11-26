# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/zcode-site-plugin 基础工程中的 src 实现源码。

### 子目录

| 目录                        | 存放内容                                                |
| --------------------------- | ------------------------------------------------------- |
| [server/](server/README.md) | @zcode/zcode-site-plugin 基础工程中的 server 实现源码。 |
| [ui/](ui/README.md)         | @zcode/zcode-site-plugin 基础工程中的 ui 实现源码。     |

### 文件

| 文件                                       | 简要说明                                                                                    |
| ------------------------------------------ | ------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* zcode-site-panel 标准用法示例：面板读一个站点、处理失败，以及改名工具的参数。            |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                    |
| [contract.test.ts](contract.test.ts)       | 契约测试只 import contract 与 module，不知道实现是谁。                                      |
| [contract.ts](contract.ts)                 | \* zcode-site 插件面板（UI plugin）的对外契约：插件 MCP server 提供的资源、工具与结果形状， |
| [index.ts](index.ts)                       | index 的实现文件。                                                                          |
| [module.ts](module.ts)                     | \* zcode-site-panel 模块清单（architecture-governance managed 模块）。                      |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                            |
| [vitest.config.ts](vitest.config.ts)       | 放在模块目录里：包根目录往上会先找到 apps/zcode-cli 的配置，它只收 test/ 下的用例。         |

<!-- qingqi-directory-index:end -->
