# server

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/server 基础工程中的 server 模块文件。

### 子目录

| 目录                    | 存放内容                                   |
| ----------------------- | ------------------------------------------ |
| [src/](src/README.md)   | @zcode/server 基础工程中的 src 实现源码。  |
| [test/](test/README.md) | @zcode/server 基础工程中的 test 测试场景。 |

### 文件

| 文件                                                 | 简要说明                                                                         |
| ---------------------------------------------------- | -------------------------------------------------------------------------------- |
| [build-remote.ts](build-remote.ts)                   | \* Let esbuild bundle node-pty's JS code normally, but keep .node native         |
| [buildRemoteValidation.ts](buildRemoteValidation.ts) | keyring 需要按目标平台加载原生模块，不能被 esbuild 展开成所有平台的 .node 文件。 |
| [package.json](package.json)                         | @zcode/server 的包信息、依赖和开发命令。                                         |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                 |
| [tsconfig.build.json](tsconfig.build.json)           | 本模块的 TypeScript 编译、类型检查或构建范围。                                   |
| [tsconfig.json](tsconfig.json)                       | 本模块的 TypeScript 编译、类型检查或构建范围。                                   |
| [tsup.config.ts](tsup.config.ts)                     | tsup 配置自身会被打包，构建工具需保留原始文件位置，不能被内联后重定位。          |

<!-- qingqi-directory-index:end -->
