# runtime

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

基于 ZCode 构建的 Node 运行层，负责工具注册、执行、权限、MCP、Skills 和有界记忆。

### 子目录

| 目录                  | 存放内容                                            |
| --------------------- | --------------------------------------------------- |
| [src/](src/README.md) | 运行层的公开契约、能力实现和 Python/Node 通信入口。 |

### 文件

| 文件                           | 简要说明                                                                     |
| ------------------------------ | ---------------------------------------------------------------------------- |
| [build.mjs](build.mjs)         | 公共能力从同一源码构建，消除逐轮 TS 加载；不注册或执行被裁剪的 Coding 工具。 |
| [package.json](package.json)   | @qingqi/education-runtime 的包信息、依赖和开发命令。                         |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                                             |
| [tsconfig.json](tsconfig.json) | 本模块的 TypeScript 编译、类型检查或构建范围。                               |

<!-- qingqi-directory-index:end -->
