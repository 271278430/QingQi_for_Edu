# 清启教育 Agent

产品介绍、截图、教学动画与克隆运行步骤见[仓库README](../README.md)。

这是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。本目录是产品主体：个性化辅导、学习路径、学情看板和每次三题的个性化练习。设置管理包含模型连接与单张系统关系图，图中展示Agent Loop的决策、调用、观察与返回。

```sh
pnpm education:build
pnpm education:demo
```

演示无需密钥，使用独立合成学生与45道自编数值题。已有真实模型与资料的本机入口继续使用 `education:start` 或 `education:flash`；配置、学生状态、题库和模型权重不随源码上传。

- [运行与数据导入](docs/operations.md)
- [模块职责与系统关系](docs/architecture.md)
- [ZCode 基础与教育业务](docs/zcode-foundation.md)
- [维护所有者](docs/ownership.md)
- [当前56组验收与独立真实API检查](docs/verification.md)

`service/src/qingqi`拥有教学与状态；`runtime/src`适配ZCode运行能力；`client/src`提供HTTP/SSE合同；`web/src`只管理交互与草稿；`tools/review_manifest.json`是当前回归入口。历史审查文档保留当时实现，当前行为以`specs/education`和上述维护说明为准。

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

学生端教育产品，包含个性化辅导、学习路径、学情看板、个性化练习及模型和系统设置。

### 子目录

| 目录                          | 存放内容                                                                                           |
| ----------------------------- | -------------------------------------------------------------------------------------------------- |
| [.local/](.local/README.md)   | .local 模块文件，属于 education 目录。                                                             |
| [client/](client/README.md)   | 教育 Web 与服务端之间的类型化客户端。                                                              |
| [docs/](docs/README.md)       | 当前架构、部署、维护、源码来源与目录管理说明。                                                     |
| [reports/](reports/README.md) | reports 模块文件，属于 education 目录。                                                            |
| [runtime/](runtime/README.md) | 基于 ZCode 构建的 Node 运行层，负责工具注册、执行、权限、MCP、Skills 和有界记忆。                  |
| [server/](server/README.md)   | 可选的课程、困难分析与审查模型服务。                                                               |
| [service/](service/README.md) | Python 教学服务；接收 Web 请求，执行教学循环，核验数学结果并维护学生状态。                         |
| [tests/](tests/README.md)     | 教学产品验收、浏览器场景、模型夹具和真实服务探针；当前自动清单由 tools/review_manifest.json 管理。 |
| [tools/](tools/README.md)     | 启动、账户配置、数据导入、素材制作与维护工具。验收及模型夹具位于 education/tests。                 |
| [web/](web/README.md)         | 学生 Web 应用的包配置、入口和页面源码。                                                            |

### 文件

| 文件                       | 简要说明                         |
| -------------------------- | -------------------------------- |
| [README.md](README.md)     | 本目录用途、子目录与逐文件说明。 |
| [source.json](source.json) | source 的数据或配置定义。        |

<!-- qingqi-directory-index:end -->
