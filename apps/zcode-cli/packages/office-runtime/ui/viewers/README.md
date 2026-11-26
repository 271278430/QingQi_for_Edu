# viewers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 viewers 模块文件。

### 文件

| 文件                           | 简要说明                                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- |
| [align.test.ts](align.test.ts) | align.test 的实现文件。                                                                               |
| [align.ts](align.ts)           | \* Map rendered docx elements (paragraphs and top-level tables, in document order) to the server's    |
| [DocxView.tsx](DocxView.tsx)   | Block element for a locator: `p:N` / `t:N` map to rendered elements, `t:N/rRcC` to a cell.            |
| [PdfView.tsx](PdfView.tsx)     | pdf.js would fetch cMaps, fonts and wasm over the network; the sandbox has none, so read them         |
| [PptxView.tsx](PptxView.tsx)   | Bumped when a presentation finishes parsing; the ref alone would not re-render.                       |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                                                                      |
| [registry.ts](registry.ts)     | One line per format, tagged `kind:<format>`: scripts/build.mjs keeps only the plugin's formats,       |
| [types.ts](types.ts)           | PNG as base64 (no data: prefix).                                                                      |
| [XlsxView.tsx](XlsxView.tsx)   | \* react-xlsx parses workbooks with wasm in a module worker. The sandbox cannot fetch, so hand it the |

<!-- qingqi-directory-index:end -->
