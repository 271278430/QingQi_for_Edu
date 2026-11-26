# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/i18n 基础工程中的 src 实现源码。

### 子目录

| 目录                          | 存放内容                                    |
| ----------------------------- | ------------------------------------------- |
| [locales/](locales/README.md) | @zcode/i18n 基础工程中的 locales 语言资源。 |

### 文件

| 文件                   | 简要说明                                                                                     |
| ---------------------- | -------------------------------------------------------------------------------------------- |
| [index.ts](index.ts)   | 实现或公开接口：getZCodeCopy。                                                               |
| [locale.ts](locale.ts) | 实现或公开接口：DEFAULT_LOCALE、SUPPORTED_LOCALES、LocaleDetectionInput、isSupportedLocale。 |
| [README.md](README.md) | 本目录用途、子目录与逐文件说明。                                                             |
| [types.ts](types.ts)   | 审批请求来自主会话之外的会话（例如 CreateSession 建的后台会话）时，面板上方的来源标注。      |

<!-- qingqi-directory-index:end -->
