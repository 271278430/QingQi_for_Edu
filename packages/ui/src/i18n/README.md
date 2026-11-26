# i18n

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 i18n 实现源码。

### 子目录

| 目录                          | 存放内容                                  |
| ----------------------------- | ----------------------------------------- |
| [locales/](locales/README.md) | @zcode/ui 基础工程中的 locales 语言资源。 |

### 文件

| 文件                                     | 简要说明                                                           |
| ---------------------------------------- | ------------------------------------------------------------------ |
| [index.ts](index.ts)                     | index 的实现文件。                                                 |
| [IntlProvider.tsx](IntlProvider.tsx)     | 简易 intl 工具：根据 id 查找翻译，支持 {key} 占位符替换            |
| [localeMessages.ts](localeMessages.ts)   | \* 语言 → 翻译消息映射。IntlProvider 与 ErrorBoundary 共用这一份。 |
| [LocaleSwitcher.tsx](LocaleSwitcher.tsx) | 按钮上的短标签用各语言本名缩写，不随界面语言翻译。                 |
| [README.md](README.md)                   | 本目录用途、子目录与逐文件说明。                                   |

<!-- qingqi-directory-index:end -->
