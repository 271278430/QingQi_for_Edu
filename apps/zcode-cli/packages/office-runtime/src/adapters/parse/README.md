# parse

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 parse 外部能力与平台适配。

### 文件

| 文件                           | 简要说明                                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------- |
| [docx.ts](docx.ts)             | 0 = title, 1–9 = heading level, undefined = body text.                                            |
| [dommatrix.ts](dommatrix.ts)   | \* Minimal 2D DOMMatrix for pdf.js in Node. pdf.js constructs one at module load and uses it for  |
| [ooxml.ts](ooxml.ts)           | Order-preserving XML node from fast-xml-parser: `{ [tag]: children, ":@"?: attributes }`.         |
| [parse.test.ts](parse.test.ts) | 按模块解析定位 pdfjs-dist：仓库使用 hoisted node_modules，包目录下不一定有自己的 node_modules。   |
| [pdf.ts](pdf.ts)               | Directory with pdf.js `cmaps/` and `standard_fonts/`, ending in a slash.                          |
| [pptx.ts](pptx.ts)             | The group carries its members' text so a click on the group (the viewer's hit target) reads well. |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                                                                  |
| [xlsx.ts](xlsx.ts)             | 实现或公开接口：parseXlsx。                                                                       |

<!-- qingqi-directory-index:end -->
