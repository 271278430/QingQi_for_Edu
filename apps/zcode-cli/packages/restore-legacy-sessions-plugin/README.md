# Restore Legacy Sessions Plugin

ZCode official plugin for restoring old ACP-era ZCode session snapshots into the new task index and CLI session DB.

This plugin is bundled as `restore-legacy-sessions@zcode-plugins-official` and is disabled by default. Enable it only when you need to inspect or restore old session data.

## Enable

```sh
zcode plugins enable restore-legacy-sessions
```

Or inside a ZCode session:

```text
/plugins enable restore-legacy-sessions
```

Changes apply to new sessions. After enabling, use:

```text
/restore-legacy-sessions
```

## Data Boundaries

- Default source: `~/.zcode/v2/sessions`
- Task index destination: `~/.zcode/v2/tasks-index.sqlite`
- CLI session DB destination: `~/.zcode/cli/db/db.sqlite`

The restore scripts create timestamped DB backups before writing. Restored ACP-era conversations are persisted as normal `glm` ZCode Agent history and do not write `migration_source`.

## Development

This is a skill-only / command-only plugin. It has no MCP server and no build step.

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/restore-legacy-sessions-plugin 基础工程中的 restore legacy sessions plugin 模块文件。

### 子目录

| 目录                                      | 存放内容                                                                    |
| ----------------------------------------- | --------------------------------------------------------------------------- |
| [.zcode-plugin/](.zcode-plugin/README.md) | @zcode/restore-legacy-sessions-plugin 基础工程中的 .zcode plugin 模块文件。 |
| [commands/](commands/README.md)           | @zcode/restore-legacy-sessions-plugin 基础工程中的 commands 模块文件。      |
| [skills/](skills/README.md)               | @zcode/restore-legacy-sessions-plugin 基础工程中的 skills 技能指导和资源。  |

### 文件

| 文件                         | 简要说明                                                         |
| ---------------------------- | ---------------------------------------------------------------- |
| [package.json](package.json) | @zcode/restore-legacy-sessions-plugin 的包信息、依赖和开发命令。 |
| [README.md](README.md)       | 本目录用途、子目录与逐文件说明。                                 |

<!-- qingqi-directory-index:end -->
