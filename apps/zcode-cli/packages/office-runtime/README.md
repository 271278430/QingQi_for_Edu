# office-runtime

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 office runtime 模块文件。

### 子目录

| 目录                            | 存放内容                                                     |
| ------------------------------- | ------------------------------------------------------------ |
| [fixtures/](fixtures/README.md) | @zcode/office-runtime 基础工程中的 fixtures 测试夹具与样例。 |
| [scripts/](scripts/README.md)   | @zcode/office-runtime 基础工程中的 scripts 工程脚本。        |
| [src/](src/README.md)           | @zcode/office-runtime 基础工程中的 src 实现源码。            |
| [ui/](ui/README.md)             | @zcode/office-runtime 基础工程中的 ui 模块文件。             |

### 文件

| 文件                                       | 简要说明                                                                                           |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| [.gitignore](.gitignore)                   | 不进入 Git 的依赖、缓存、凭据和运行产物规则。                                                      |
| [contract.example.ts](contract.example.ts) | \* office-runtime 标准用法示例：PDF 插件在 package.json 里声明的面板配置，以及构建后可依赖的产物。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                           |
| [contract.test.ts](contract.test.ts)       | 契约测试只 import contract 与 module，不知道实现是谁。                                             |
| [contract.ts](contract.ts)                 | \* office-runtime 对外契约：内置文档插件（documents / pdf / presentations / spreadsheets）如何声明 |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                 |
| [LICENSE](LICENSE)                         | 代码许可原文。                                                                                     |
| [module.ts](module.ts)                     | \* office-runtime 模块清单（architecture-governance managed 模块）。                               |
| [package.json](package.json)               | @zcode/office-runtime 的包信息、依赖和开发命令。                                                   |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                   |
| [tsconfig.json](tsconfig.json)             | 本模块的 TypeScript 编译、类型检查或构建范围。                                                     |
| [vitest.config.ts](vitest.config.ts)       | vitest.config 的实现文件。                                                                         |

<!-- qingqi-directory-index:end -->
