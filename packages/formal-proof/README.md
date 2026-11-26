# Formal Proof

这是 ZCode 的产品行为状态空间枚举器。当前版本聚焦对话场景里的 compact、fork、goal、消息队列和 query 编辑组合。

启动：

```sh
pnpm --filter @zcode/formal-proof dev
```

打开：

```text
http://127.0.0.1:4176/
```

核心 spec 见 `docs/conversation-product-state-space.md`。

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/formal-proof 基础工程中的 formal proof 模块文件。

### 子目录

| 目录                  | 存放内容                                        |
| --------------------- | ----------------------------------------------- |
| [src/](src/README.md) | @zcode/formal-proof 基础工程中的 src 实现源码。 |

### 文件

| 文件                             | 简要说明                                       |
| -------------------------------- | ---------------------------------------------- |
| [.oxlintrc.json](.oxlintrc.json) | .oxlintrc 的数据或配置定义。                   |
| [index.html](index.html)         | index 模块的资源或工程文件。                   |
| [package.json](package.json)     | @zcode/formal-proof 的包信息、依赖和开发命令。 |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。               |
| [tsconfig.json](tsconfig.json)   | 本模块的 TypeScript 编译、类型检查或构建范围。 |
| [vite.config.ts](vite.config.ts) | vite.config 的实现文件。                       |

<!-- qingqi-directory-index:end -->
