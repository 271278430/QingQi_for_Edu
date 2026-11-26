# @zcode-dev/plugin-api

Type definitions for ZCode plugin extensions. The package has types only; it has no runtime code.

ZCode 插件扩展代码用的类型包。只有类型，没有运行时代码。

## Install

```sh
npm install --save-dev @zcode-dev/plugin-api
```

## Entries

| Import                              | Types                                                        |
| ----------------------------------- | ------------------------------------------------------------ |
| `@zcode-dev/plugin-api`             | `ExtensionContext`, `Disposable`, scopes, views, error codes |
| `@zcode-dev/plugin-api/manifest`    | The manifest `extension` key, slots, grants                  |
| `@zcode-dev/plugin-api/sessions`    | Session projection, session action inputs and results        |
| `@zcode-dev/plugin-api/protocol-v4` | Conversation rows, context composition, generation metrics   |

```ts
import type { ExtensionContext } from "@zcode-dev/plugin-api";

export function activate(ctx: ExtensionContext): void {
  ctx.commands.register("hello", () => ctx.log.info("hello"));
}
```

Use `import type` only. The package has no JavaScript.

## Versions

The package version is the plugin API version of ZCode. Set `extension.engines.zcode` in the plugin manifest to the version you build against, for example `"^1.4.0"`.

- A new capability or a new optional field raises the minor version.
- A removed capability or a changed meaning raises the major version.
- ZCode loads an extension only when its plugin API version satisfies `engines.zcode`.

插件清单的 `extension.engines.zcode` 写你构建时用的版本，例如 `"^1.4.0"`。ZCode 的插件 API 版本满足这个范围时才加载扩展。

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode-dev/plugin-api 基础工程中的 plugin api 模块文件。

### 子目录

| 目录                          | 存放内容                                              |
| ----------------------------- | ----------------------------------------------------- |
| [scripts/](scripts/README.md) | @zcode-dev/plugin-api 基础工程中的 scripts 工程脚本。 |
| [src/](src/README.md)         | @zcode-dev/plugin-api 基础工程中的 src 实现源码。     |
| [test/](test/README.md)       | @zcode-dev/plugin-api 基础工程中的 test 测试场景。    |

### 文件

| 文件                             | 简要说明                                                               |
| -------------------------------- | ---------------------------------------------------------------------- |
| [LICENSE](LICENSE)               | 代码许可原文。                                                         |
| [package.json](package.json)     | @zcode-dev/plugin-api 的包信息、依赖和开发命令。                       |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。                                       |
| [tsconfig.json](tsconfig.json)   | 本模块的 TypeScript 编译、类型检查或构建范围。                         |
| [tsup.config.ts](tsup.config.ts) | 给仓库外的插件作者用的声明包（docs/plugins/extension-host.md §17.9）： |

<!-- qingqi-directory-index:end -->
