# ZCode CLI

ZCode's Agent CLI provides an interactive terminal and non-interactive task execution. It is part of this pnpm workspace; build it from the repository root with the Node and pnpm versions in [mise.toml](../../mise.toml).

```sh
pnpm install --frozen-lockfile
pnpm --filter @zcode/cli... build
node apps/zcode-cli/packages/cli/dist/zcode.cjs doctor --json
```

The default artifact is a Node.js bundle with adjacent runtime resources. SEA packaging is optional. The Agent CLI differs from the root distribution launcher, which also supports Web startup.

See the [CLI usage guide (中文)](docs/usage/README.md) for setup, model configuration, permissions, sessions, MCP, skills, hooks, plugins, and reproducible batch tasks. The guide distinguishes current source behavior from older binaries and documents its verification limits.

Useful entry points:

- [Quick start and packaging](docs/usage/01-quickstart.md)
- [Model and runtime configuration](docs/usage/03-config.md)
- [Plugin development](docs/usage/10-plugins.md)
- [Hooks and workspace trust](docs/usage/09-hooks.md)
- [Batch tasks and trajectory capture](docs/usage/13-automation.md)
- [Design specifications](docs/design/v2/)
- [Contributor instructions](AGENTS.md)

Run `pnpm --filter @zcode/cli dev` for source development. CLI code validation follows the contributor instructions; CLI tests are separate from the root unit-test suite.

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

ZCode 的编码 Agent 工程，保留其包边界、基础运行源码和来源说明。

### 子目录

| 目录                                                        | 存放内容                                                                 |
| ----------------------------------------------------------- | ------------------------------------------------------------------------ |
| [.agents/](.agents/README.md)                               | zcode-cli 基础工程中的 .agents 模块文件。                                |
| [.husky/](.husky/README.md)                                 | zcode-cli 基础工程中的 .husky 模块文件。                                 |
| [dependencies/](dependencies/README.md)                     | zcode-cli 基础工程中的 dependencies 模块文件。                           |
| [docs/](docs/README.md)                                     | zcode-cli 基础工程中的 docs 设计与维护文档。                             |
| [e2e/](e2e/README.md)                                       | zcode-cli 基础工程中的 e2e 模块文件。                                    |
| [packages/](packages/README.md)                             | ZCode 的独立运行包，包括 contracts、core、adapters、模型与插件相关模块。 |
| [real-world-test-prompt/](real-world-test-prompt/README.md) | zcode-cli 基础工程中的 real world test prompt 模块文件。                 |
| [scripts/](scripts/README.md)                               | zcode-cli 基础工程中的 scripts 工程脚本。                                |
| [tests/](tests/README.md)                                   | zcode-cli 基础工程中的 tests 验收与回归场景。                            |
| [tools/](tools/README.md)                                   | zcode-cli 基础工程中的 tools 模块文件。                                  |

### 文件

| 文件                                       | 简要说明                                                                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| [.dockerignore](.dockerignore)             | .dockerignore 模块的资源或工程文件。                                                                                                  |
| [.editorconfig](.editorconfig)             | .editorconfig 模块的资源或工程文件。                                                                                                  |
| [.env.template](.env.template)             | .env 模块的资源或工程文件。                                                                                                           |
| [.gitignore](.gitignore)                   | 不进入 Git 的依赖、缓存、凭据和运行产物规则。                                                                                         |
| [.node-version](.node-version)             | .node-version 模块的资源或工程文件。                                                                                                  |
| [.nvmrc](.nvmrc)                           | .nvmrc 模块的资源或工程文件。                                                                                                         |
| [.oxfmtrc.json](.oxfmtrc.json)             | .oxfmtrc 的数据或配置定义。                                                                                                           |
| [.release-it.json](.release-it.json)       | .release-it 的数据或配置定义。                                                                                                        |
| [AGENTS.md](AGENTS.md)                     | 本目录的开发规范、模块边界与验证要求。                                                                                                |
| [package.json](package.json)               | zcode-cli 的包信息、依赖和开发命令。                                                                                                  |
| [pnpm-lock.yaml](pnpm-lock.yaml)           | pnpm 锁定的依赖版本和完整性信息。                                                                                                     |
| [pnpm-workspace.yaml](pnpm-workspace.yaml) | 工作区包、平台依赖与构建许可配置。                                                                                                    |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                                                      |
| [skills-lock.json](skills-lock.json)       | skills-lock 的数据或配置定义。                                                                                                        |
| [test-model.mjs](test-model.mjs)           | test-model 的实现文件。                                                                                                               |
| [turbo.json](turbo.json)                   | turbo 的数据或配置定义。                                                                                                              |
| [vitest.config.ts](vitest.config.ts)       | Bugfix: 外部 zcode-cli 历史里同时存在 test/ 和 tests/ 目录；合入 apps 后需要同时保留两种约定，避免新增包测试被根 include 规则过滤掉。 |

<!-- qingqi-directory-index:end -->
