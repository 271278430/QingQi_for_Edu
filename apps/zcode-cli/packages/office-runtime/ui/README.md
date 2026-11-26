# ui

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 ui 模块文件。

### 子目录

| 目录                          | 存放内容                                              |
| ----------------------------- | ----------------------------------------------------- |
| [shell/](shell/README.md)     | @zcode/office-runtime 基础工程中的 shell 模块文件。   |
| [viewers/](viewers/README.md) | @zcode/office-runtime 基础工程中的 viewers 模块文件。 |

### 文件

| 文件                                           | 简要说明                                                                                            |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [assets.ts](assets.ts)                         | Binary asset (wasm, pdf.js cMaps and fonts); cached for the life of the page.                       |
| [bootstrap.ts](bootstrap.ts)                   | Small loader inlined in panel.html: connect once, then pull the UI bundle through MCP resources     |
| [cjkFontRuntime.ts](cjkFontRuntime.ts)         | _ Registers the `zcode-cjk-_` faces and the bundled fallback for the PDF canvas. scripts/build.mjs  |
| [cjkFonts.test.ts](cjkFonts.test.ts)           | pdf.js 把字体名的原始字节逐个当作 Latin-1 字符保存（TextEncoder 只有 UTF-8，样例字节写死）。        |
| [cjkFonts.ts](cjkFonts.ts)                     | \* 未嵌入 CJK 字体的字体链（纯函数部分；注册与加载见 cjkFontRuntime.ts，规格见                      |
| [dom.ts](dom.ts)                               | Only http(s) and mailto links leave the document; everything else is blocked.                       |
| [host.ts](host.ts)                             | \* Tools the page exposes to the model while it is open (MCP Apps app-provided tools). The          |
| [i18n.test.ts](i18n.test.ts)                   | The default profile opens every format.                                                             |
| [i18n.ts](i18n.ts)                             | What the user can select, e.g. "any passage, cell or slide".                                        |
| [icons.tsx](icons.tsx)                         | \* The few Lucide icons the panel uses (ZCode's icon set), as inline SVG so the bundle stays small. |
| [main.tsx](main.tsx)                           | Viewers with fit modes and zoom in the page control.                                                |
| [panel.css](panel.css)                         | \* Document viewer panel. Colours come from the host's style variables (ZCode passes its theme      |
| [panel.html](panel.html)                       | panel 模块的资源或工程文件。                                                                        |
| [profile.test.ts](profile.test.ts)             | Single-format plugins: wording names only what each one opens.                                      |
| [raster.ts](raster.ts)                         | \* Render a live DOM element to a PNG without network access: the element is cloned with its        |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                                    |
| [rpc.ts](rpc.ts)                               | A failed server tool call; `code` is the server's OfficeErrorCode when it sent one.                 |
| [windowStorage.test.ts](windowStorage.test.ts) | windowStorage.test 的实现文件。                                                                     |
| [windowStorage.ts](windowStorage.ts)           | 按最近使用顺序保留有限窗口，避免关闭标签页后无限累积独立 localStorage 键。                          |

<!-- qingqi-directory-index:end -->
