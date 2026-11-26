# scripts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/design-plugin 基础工程中的 scripts 工程脚本。

### 文件

| 文件                                                 | 简要说明                                                                                                                 |
| ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| [adapt-canvas.mjs](adapt-canvas.mjs)                 | Explicit authoring helper. It never runs during pack loading or changes the source template.                             |
| [build-catalog.mjs](build-catalog.mjs)               | Generates references/catalog.md from design-resources/. Run: node scripts/build-catalog.mjs [--max-bytes=N] [--out=path] |
| [design-lint.mjs](design-lint.mjs)                   | design-lint: checks that the colors, font families and (optionally) spacing in an HTML design file come                  |
| [design-tokens.mjs](design-tokens.mjs)               | Shared by design-lint.mjs and import-design-system.mjs: color parsing and the design-system file format.                 |
| [frontmatter.mjs](frontmatter.mjs)                   | YAML-subset frontmatter parser for design-resources SKILL.md files; no dependencies.                                     |
| [import-design-system.mjs](import-design-system.mjs) | CSS custom properties, Tailwind config and existing HTML pages. Node standard library only.                              |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                                                         |

<!-- qingqi-directory-index:end -->
