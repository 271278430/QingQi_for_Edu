# test

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/design-plugin 基础工程中的 test 测试场景。

### 子目录

| 目录                            | 存放内容                                                    |
| ------------------------------- | ----------------------------------------------------------- |
| [fixtures/](fixtures/README.md) | @zcode/design-plugin 基础工程中的 fixtures 测试夹具与样例。 |

### 文件

| 文件                                                         | 简要说明                                                                                                    |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| [catalog.test.ts](catalog.test.ts)                           | references/catalog.md 由 build-catalog.mjs 从 design-resources 生成；这里守住新鲜度、体量、覆盖和配置漂移。 |
| [design-lint.test.ts](design-lint.test.ts)                   | design-lint：设计稿里的颜色 / 字体 / 间距是否都出自设计系统文件。机判在前，人工只看它管不到的部分。         |
| [design-plugin.test.ts](design-plugin.test.ts)               | 设计工作流插件 design：入口技能 + 设计资源 + SessionStart 注入。                                            |
| [import-design-system.test.ts](import-design-system.test.ts) | 设计系统导入：从工作区的 CSS 变量、Tailwind 配置（只做文本解析，不执行）和已有页面抽出设计系统文件，        |
| [README.md](README.md)                                       | 本目录用途、子目录与逐文件说明。                                                                            |

<!-- qingqi-directory-index:end -->
