# adapters

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 adapters 外部能力与平台适配。

### 子目录

| 目录                      | 存放内容                                                      |
| ------------------------- | ------------------------------------------------------------- |
| [parse/](parse/README.md) | @zcode/office-runtime 基础工程中的 parse 外部能力与平台适配。 |

### 文件

| 文件                             | 简要说明                                                                                        |
| -------------------------------- | ----------------------------------------------------------------------------------------------- |
| [assets.test.ts](assets.test.ts) | pdf.js 解 JPEG 2000（openjpeg）与 ICC 颜色（qcms）的 wasm。                                     |
| [assets.ts](assets.ts)           | \* Names served from `${ASSET_PREFIX}{name}`: bundle chunks, styles, wasm, pdf.js data and the  |
| [files.test.ts](files.test.ts)   | files.test 的实现文件。                                                                         |
| [files.ts](files.ts)             | Workspace-relative path with forward slashes.                                                   |
| [main.ts](main.ts)               | 官方插件宿主通过导出的 main 启动；导入时直接连接会被宿主判定为无效入口。                        |
| [parsers.ts](parsers.ts)         | One line per format, tagged `kind:<format>`: scripts/build.mjs keeps only the plugin's formats, |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。                                                                |
| [server.test.ts](server.test.ts) | 宿主在每次 tools/call 的 \_meta 里写 session_id（agent 与面板调用相同）。                       |
| [server.ts](server.ts)           | Model-facing summary of a document: what it is, its outline and how to address it.              |

<!-- qingqi-directory-index:end -->
