# domain

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 domain 实现源码。

### 文件

| 文件                             | 简要说明                                                                                       |
| -------------------------------- | ---------------------------------------------------------------------------------------------- |
| [anchor.test.ts](anchor.test.ts) | anchor.test 的实现文件。                                                                       |
| [anchor.ts](anchor.ts)           | \* Anchors are the shared address format of the panel, the server and the model:               |
| [cjk.test.ts](cjk.test.ts)       | Chrome 打印的 PDF：文→⽂(U+2F42)、方→⽅(U+2F45)、玄→⽞(U+2F5E)、黑→⿊(U+2FCA)、黄→⻩(U+2EE9)。 |
| [cjk.ts](cjk.ts)                 | \* PDF 文字提取的 CJK 归一。                                                                   |
| [model.ts](model.ts)             | One search hit: a locator in the document and a short snippet around the match.                |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。                                                               |
| [text.test.ts](text.test.ts)     | text.test 的实现文件。                                                                         |
| [text.ts](text.ts)               | \* JavaScript strings are UTF-16: characters outside the basic plane, such as the math letters |

<!-- qingqi-directory-index:end -->
