# Browser Use

The official built-in ZCode plugin for browser automation. It ships the `node_repl` MCP server, browser-client bootstrap module, skill, and documentation/capability manifests.

## What it provides

- `node_repl` MCP server — exposes a single `js` tool, which the model sees as `mcp__node_repl__js`. Shared with Computer Use, so its model-facing text is scoped to both official capabilities. (`js_reset` and `js_add_node_module_dir` were removed on 2026-09-18 along with the moduleDirs machinery: every `js` call already starts fresh, and module search roots are the host's job to inject, not the model's to configure. Imports are limited to `node:*` builtins and absolute `file://` URLs under the skill root.)
- `scripts/browser-client.mjs` — explicitly bootstraps `agent.browsers` inside each fresh `js` kernel; BrowserControl tabs, not JavaScript globals, provide continuity.
- `scripts/computer-use-client.mjs` — shared-host copy of the CUA SDK bootstrap; it keeps the CUA skill on the same `ZCODE_PLUGIN_ROOT` while the CUA plugin remains SDK/skill/docs-only.
- `control-browser` skill — tells the agent how to bootstrap and drive an advertised ZCode browser backend (Desktop IAB or CLI-managed headless CDP), select a browser and read `browser.documentation()` once, use the Playwright DOM snapshot→locator→act workflow, observe controlled and user tab registries together after a possible popup action, and request screenshots only for visual evidence.
- `web-gui-tester` skill — layers a pure-GUI black-box testing workflow on top of `control-browser`, requiring Browser Use semantic evidence plus inspected screenshots while respecting current console, upload, and runtime capability boundaries.

The IAB runtime is provided by the desktop host; the managed headless CDP runtime is provided only by an explicitly opted-in CLI process. The plugin assets define the model guidance and the effective runtime object graph; unsupported members are removed by the manifest interpreter instead of failing after invocation.

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/browser-use-plugin 基础工程中的 browser use plugin 模块文件。

### 子目录

| 目录                                      | 存放内容                                                        |
| ----------------------------------------- | --------------------------------------------------------------- |
| [.zcode-plugin/](.zcode-plugin/README.md) | @zcode/browser-use-plugin 基础工程中的 .zcode plugin 模块文件。 |
| [docs/](docs/README.md)                   | @zcode/browser-use-plugin 基础工程中的 docs 设计与维护文档。    |
| [e2e/](e2e/README.md)                     | @zcode/browser-use-plugin 基础工程中的 e2e 模块文件。           |
| [scripts/](scripts/README.md)             | @zcode/browser-use-plugin 基础工程中的 scripts 工程脚本。       |
| [skills/](skills/README.md)               | @zcode/browser-use-plugin 基础工程中的 skills 技能指导和资源。  |
| [src/](src/README.md)                     | @zcode/browser-use-plugin 基础工程中的 src 实现源码。           |
| [test/](test/README.md)                   | @zcode/browser-use-plugin 基础工程中的 test 测试场景。          |

### 文件

| 文件                           | 简要说明                                             |
| ------------------------------ | ---------------------------------------------------- |
| [.gitignore](.gitignore)       | 不进入 Git 的依赖、缓存、凭据和运行产物规则。        |
| [package.json](package.json)   | @zcode/browser-use-plugin 的包信息、依赖和开发命令。 |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                     |
| [tsconfig.json](tsconfig.json) | 本模块的 TypeScript 编译、类型检查或构建范围。       |

<!-- qingqi-directory-index:end -->
