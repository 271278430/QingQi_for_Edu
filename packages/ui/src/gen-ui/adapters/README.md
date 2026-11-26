# adapters

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 adapters 外部能力与平台适配。

### 文件

| 文件                               | 简要说明                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------- |
| [page.ts](page.ts)                 | 实现或公开接口：GenUiPageInput、createGenUiPage。                         |
| [README.md](README.md)             | 本目录用途、子目录与逐文件说明。                                          |
| [retainedPage.ts](retainedPage.ts) | 回收的是 guest；锚点观察属于窗口 owner，离屏回收后重新滚入视口仍能唤醒。  |
| [theme.ts](theme.ts)               | Gen UI 使用正文层级与中性色控件；不覆盖第三方 MCP App 的标准 token 投影。 |

<!-- qingqi-directory-index:end -->
