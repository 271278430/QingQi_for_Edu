# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/design-runtime 基础工程中的 src 实现源码。

### 文件

| 文件                                       | 简要说明                                                                                                       |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 宿主通过任意「在页面里执行脚本」的出口驱动运行时：先安装，再发固定命令。                                       |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                       |
| [contract.ts](contract.ts)                 | 设计运行时与宿主之间的数据形状（docs/browser-use/2026-11-03-browser-design-mode-spec.md）。                    |
| [designMessages.ts](designMessages.ts)     | 设计相关的纯计算：颜色解析、CSS 变量 → 面板控件。                                                              |
| [elementInspector.ts](elementInspector.ts) | 页面侧的元素读取工具：选择元素脚本和设计运行时共用这一份（以前在 webElementPickerScript.ts 里）。              |
| [hostScripts.ts](hostScripts.ts)           | 宿主侧：生成交给 webview.executeJavaScript 的脚本，并校验页面回来的值。                                        |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                             |
| [module.ts](module.ts)                     | 实现或公开接口：designRuntimeModule。                                                                          |
| [pageRuntime.ts](pageRuntime.ts)           | 注入 guest 页面的设计运行时（docs/browser-use/2026-11-03-browser-design-mode-spec.md）。                       |
| [pageSignals.ts](pageSignals.ts)           | 读设计稿信号：data-zcode-design 标记、:root / html 规则里声明的 CSS 变量名、data-variant 方案、section.slide。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                               |
| [sourceEdit.ts](sourceEdit.ts)             | 属性面板写回源码（docs/browser-use/2026-11-03-browser-design-mode-spec.md 第五节）。只在宿主侧用，不进页面。   |

<!-- qingqi-directory-index:end -->
