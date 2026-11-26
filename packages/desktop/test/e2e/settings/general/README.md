# general

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 general 测试场景。

### 文件

| 文件                                                                                 | 简要说明                                                                                   |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| [README.md](README.md)                                                               | 本目录用途、子目录与逐文件说明。                                                           |
| [settings-client-language-header.test.ts](settings-client-language-header.test.ts)   | 与 Main 启动默认语言（DEFAULT_LOCALE = zh-CN）不同，预热请求带它就说明拿到的是持久化语言。 |
| [settings-language-system-default.test.ts](settings-language-system-default.test.ts) | settings-language-system-default.test 的实现文件。                                         |
| [settings-navigation-search.test.ts](settings-navigation-search.test.ts)             | 每个固定设置项都走真实搜索和导航，验证索引没有悬空的定位 id。                              |
| [settings-ui-polish.test.ts](settings-ui-polish.test.ts)                             | 上一个用例可能停在设置页，先真实关闭遮挡层再操作侧栏项目。                                 |
| [settings-window-size-persistence.test.ts](settings-window-size-persistence.test.ts) | 后台 E2E 不保证 OS 焦点；按主 renderer 定位，避免 getFocusedWindow 返回空。                |

<!-- qingqi-directory-index:end -->
