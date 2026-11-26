# debug

Development-only trace and context viewer for ZCode.

Run from the repository root:

```sh
pnpm --filter debug dev
```

The Hono API reads existing local diagnostics only:

- `~/.zcode/cli/log/*.jsonl`
- `~/.zcode/cli/db/db.sqlite`
- an optional session event JSONL file or directory selected in the UI

It does not modify agent runtime behavior or write back to the agent database.

The debug server also starts a local network capture proxy by default:

- API/UI: `http://127.0.0.1:4174`
- Proxy: `http://127.0.0.1:4184`
- Local CA: `packages/debug/certs/network-ca/certs/ca.pem`

Run the CLI you want to inspect with the environment values shown in the Network panel, usually `ZCODE_HTTP_PROXY` and `ZCODE_AGENT_CA_CERT`. The agent derives standard proxy and CA variables only inside controlled subprocess boundaries. Disable the proxy with `ZCODE_DEBUG_NETWORK_CAPTURE=0` when you only want log/DB inspection.

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

debug 基础工程中的 debug 模块文件。

### 子目录

| 目录                          | 存放内容                                  |
| ----------------------------- | ----------------------------------------- |
| [certs/](certs/README.md)     | debug 基础工程中的 certs 模块文件。       |
| [scripts/](scripts/README.md) | debug 基础工程中的 scripts 工程脚本。     |
| [server/](server/README.md)   | debug 基础工程中的 server 模块文件。      |
| [src/](src/README.md)         | debug 基础工程中的 src 实现源码。         |
| [tests/](tests/README.md)     | debug 基础工程中的 tests 验收与回归场景。 |

### 文件

| 文件                                         | 简要说明                                       |
| -------------------------------------------- | ---------------------------------------------- |
| [.gitignore](.gitignore)                     | 不进入 Git 的依赖、缓存、凭据和运行产物规则。  |
| [index.html](index.html)                     | index 模块的资源或工程文件。                   |
| [package.json](package.json)                 | debug 的包信息、依赖和开发命令。               |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。               |
| [tsconfig.json](tsconfig.json)               | 本模块的 TypeScript 编译、类型检查或构建范围。 |
| [tsconfig.server.json](tsconfig.server.json) | 本模块的 TypeScript 编译、类型检查或构建范围。 |
| [vite.config.ts](vite.config.ts)             | vite.config 的实现文件。                       |

<!-- qingqi-directory-index:end -->
