# bundled-skills

Skills that ship with the ZCode CLI as a built-in capability, outside the plugin system.

A skill lives here when a product feature depends on it: the feature's tools are registered
by the runtime, so the skill that teaches the model how to use them must be just as
unremovable. Unlike an official plugin, this pack is never listed in the plugin store, has no
enable/disable switch, cannot be uninstalled, and does not appear in the Settings skill list
or the composer's `$` skill picker. The runtime discovers its `skills/` directory as a
`source: "bundled"`, `scope: "system"` skill root on every start.

| Skill               | Feature                                           | Contract                             |
| ------------------- | ------------------------------------------------- | ------------------------------------ |
| `dynamic-workflows` | dynamic workflows (`/workflow`, `CreateWorkflow`) | `docs/dynamic-workflow/authoring.md` |

## How it reaches users

- **Development and Electron desktop**: the directory is resolved on disk next to the CLI entry
  (`packages/bundled-skills` relative to the entry, the same candidate walk official plugins
  use) and read in place; nothing is copied.
- **SEA binaries**: `scripts/sea-bundled-skill-assets.mjs` embeds `skills/**` under the
  `zcode-bundled-skills/` asset prefix. On start the CLI extracts them once into
  `~/.zcode/cli/bundled-skills/<content-hash>/` and reads from there.
- **Remote hosts**: `scripts/prepare-prebuilds.mjs` stages the directory next to the remote
  `zcode.cjs`, like the official plugin packages.

The resolver is `apps/zcode-cli/packages/bootstrap/src/app/bundled-skills.ts`. Every file
under `skills/dynamic-workflows/` is a required asset: a stage or seed that loses one refuses
the whole pack and logs a warning instead of shipping a skill with a missing reference file.

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

zcode-cli 基础工程中的 bundled skills 模块文件。

### 子目录

| 目录                        | 存放内容                                       |
| --------------------------- | ---------------------------------------------- |
| [skills/](skills/README.md) | zcode-cli 基础工程中的 skills 技能指导和资源。 |

### 文件

| 文件                   | 简要说明                         |
| ---------------------- | -------------------------------- |
| [README.md](README.md) | 本目录用途、子目录与逐文件说明。 |

<!-- qingqi-directory-index:end -->
