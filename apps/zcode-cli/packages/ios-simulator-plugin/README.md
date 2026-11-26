# iOS Simulator Plugin

ZCode plugin for model-driven iOS app development on macOS.

The package root is the plugin root:

```bash
zcode --plugin-dir /absolute/path/to/ios-simulator-plugin
```

When enabled, ZCode loads:

- `.zcode-plugin/plugin.json` for plugin metadata and skill/command paths.
- `.mcp.json` for the stdio MCP server.
- `skills/ios-dev/SKILL.md` for the model workflow.
- `commands/ios-dev.md` as a convenience slash command.

## ZCode CLI Usage

ZCode bundles this package as the official `ios-simulator@zcode-plugins-official`
plugin. Enable the plugin to project its skill, slash command, and MCP server
into the session.
At startup ZCode copies the packaged plugin files into
`~/.zcode/cli/plugins/cache/zcode-plugins-official/ios-simulator/0.1.0/` and
runs the MCP server from that cache directory. SEA builds rewrite the official
plugin's ZCode manifest to launch the cached MCP server through ZCode's internal
plugin host, so the server uses the embedded Node.js runtime. Third-party
plugins are not rewritten automatically and keep their own declared `command`.

Example `~/.zcode/cli/config.json` entry:

```json
{
  "plugins": {
    "enabledPlugins": {
      "ios-simulator@zcode-plugins-official": true
    },
    "options": {
      "ios-simulator@zcode-plugins-official": {
        "default_device": "iPhone 16",
        "ui_backend": "auto"
      }
    }
  }
}
```

The plugin MCP server name is `ios-simulator`. ZCode normalizes that name for model-visible MCP tools, so the model sees `mcp__ios_simulator__<tool>`, for example `mcp__ios_simulator__ios_preflight`. The MCP server still implements the raw MCP tool names such as `ios_preflight`; ZCode maps between the model-visible name and the server tool name.

Use stdio for the normal local workflow. HTTP is only useful if you later wrap this package as a long-running daemon shared by multiple clients.

## MVP Scope

- Use Apple's macOS Simulator app for rendering.
- Create a minimal SwiftUI app when no Xcode project exists.
- Discover projects, schemes, and bundle identifiers.
- Build with `xcodebuild` for iOS Simulator.
- Boot, show, install, launch, terminate, open URL, screenshot, and read logs through `simctl`.
- Expose optional UI actions through an isolated `idb` backend.

## MCP Tools

- `ios_preflight`
- `ios_list_simulators`
- `ios_boot_simulator`
- `ios_show_simulator`
- `ios_discover_project`
- `ios_create_app`
- `ios_build_app`
- `ios_build_and_run`
- `ios_install_app`
- `ios_launch_app`
- `ios_terminate_app`
- `ios_open_url`
- `ios_screenshot`
- `ios_logs`
- `ios_ui_status`
- `ios_ui_tap`
- `ios_ui_swipe`
- `ios_ui_type_text`
- `ios_ui_button`
- `ios_ui_describe`

## Requirements

- macOS.
- Full Xcode selected by `xcode-select`.
- An installed iOS Simulator runtime.
- Node.js 24.
- Optional: `idb` and `idb-companion` for tap/swipe/type/accessibility UI automation.

Run `ios_preflight` inside a model session to get precise missing setup checks.

## Development

```bash
pnpm install
pnpm --filter @zcode/ios-simulator-plugin typecheck
pnpm --filter @zcode/ios-simulator-plugin build
```

The Claude-compatible `.mcp.json` and the ZCode manifest both execute
`dist/mcp/server.js` with Node.js. Run the package build after changing
TypeScript sources.

## Extension Points

- `src/providers/ui.ts` owns UI automation backend selection. P0 uses `idb`; future implementations can add XcodeBuildMCP or native Accessibility without changing tool names.
- `src/providers/project.ts` owns project discovery and creation.
- `src/providers/build.ts` owns Xcode build/install/launch orchestration.
- `src/providers/sim.ts` owns `simctl` device operations.

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ios-simulator-plugin 基础工程中的 ios simulator plugin 模块文件。

### 子目录

| 目录                                      | 存放内容                                                            |
| ----------------------------------------- | ------------------------------------------------------------------- |
| [.zcode-plugin/](.zcode-plugin/README.md) | @zcode/ios-simulator-plugin 基础工程中的 .zcode plugin 模块文件。   |
| [commands/](commands/README.md)           | @zcode/ios-simulator-plugin 基础工程中的 commands 模块文件。        |
| [hooks/](hooks/README.md)                 | @zcode/ios-simulator-plugin 基础工程中的 hooks 生命周期与操作入口。 |
| [output-styles/](output-styles/README.md) | @zcode/ios-simulator-plugin 基础工程中的 output styles 模块文件。   |
| [scripts/](scripts/README.md)             | @zcode/ios-simulator-plugin 基础工程中的 scripts 工程脚本。         |
| [skills/](skills/README.md)               | @zcode/ios-simulator-plugin 基础工程中的 skills 技能指导和资源。    |
| [src/](src/README.md)                     | @zcode/ios-simulator-plugin 基础工程中的 src 实现源码。             |
| [templates/](templates/README.md)         | @zcode/ios-simulator-plugin 基础工程中的 templates 模板。           |
| [test/](test/README.md)                   | @zcode/ios-simulator-plugin 基础工程中的 test 测试场景。            |

### 文件

| 文件                           | 简要说明                                               |
| ------------------------------ | ------------------------------------------------------ |
| [.mcp.json](.mcp.json)         | .mcp 的数据或配置定义。                                |
| [package.json](package.json)   | @zcode/ios-simulator-plugin 的包信息、依赖和开发命令。 |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                       |
| [tsconfig.json](tsconfig.json) | 本模块的 TypeScript 编译、类型检查或构建范围。         |

<!-- qingqi-directory-index:end -->
