# desktop

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 desktop 模块文件。

### 子目录

| 目录                          | 存放内容                                       |
| ----------------------------- | ---------------------------------------------- |
| [build/](build/README.md)     | @zcode/desktop 基础工程中的 build 模块文件。   |
| [native/](native/README.md)   | @zcode/desktop 基础工程中的 native 模块文件。  |
| [scripts/](scripts/README.md) | @zcode/desktop 基础工程中的 scripts 工程脚本。 |
| [src/](src/README.md)         | @zcode/desktop 基础工程中的 src 实现源码。     |
| [test/](test/README.md)       | @zcode/desktop 基础工程中的 test 测试场景。    |

### 文件

| 文件                                                               | 简要说明                                                                                     |
| ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| [dev-app-update.yml](dev-app-update.yml)                           | dev-app-update 的数据或配置定义。                                                            |
| [electron-builder.config.js](electron-builder.config.js)           | 修复原因：Windows Chrome 导入入口已暂时隐藏，默认安装包不应继续携带、签名或校验原生 helper。 |
| [package.json](package.json)                                       | @zcode/desktop 的包信息、依赖和开发命令。                                                    |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                             |
| [tsconfig.app-navigation.json](tsconfig.app-navigation.json)       | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.e2e.json](tsconfig.e2e.json)                             | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.extension-host.json](tsconfig.extension-host.json)       | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.host.json](tsconfig.host.json)                           | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.json](tsconfig.json)                                     | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.main.json](tsconfig.main.json)                           | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.preload.json](tsconfig.preload.json)                     | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.remote-main.json](tsconfig.remote-main.json)             | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.renderer-services.json](tsconfig.renderer-services.json) | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.renderer.json](tsconfig.renderer.json)                   | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsconfig.scheduler.json](tsconfig.scheduler.json)                 | 本模块的 TypeScript 编译、类型检查或构建范围。                                               |
| [tsup.config.ts](tsup.config.ts)                                   | tsup 会先打包配置文件；动态加载构建工具，避免其 import.meta.dirname 被重定位到 desktop。     |
| [vite.config.ts](vite.config.ts)                                   | 动态加载仓库根的构建工具，避免配置打包后其 import.meta.dirname 被重定位到 desktop。          |
| [wdio.conf.ts](wdio.conf.ts)                                       | 实现或公开接口：stagedGitCommitDialogE2E、unstagedGitCommitDialogE2E、config。               |

<!-- qingqi-directory-index:end -->
