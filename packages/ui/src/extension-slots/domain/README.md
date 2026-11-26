# domain

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 domain 实现源码。

### 文件

| 文件                                     | 简要说明                                                                                            |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [logSelectors.ts](logSelectors.ts)       | 日志标签的纯函数（docs/plugins/extension-host.md §16.8）：合入、过滤、格式化。不读 store，不做 IO。 |
| [README.md](README.md)                   | 本目录用途、子目录与逐文件说明。                                                                    |
| [slotSelectors.ts](slotSelectors.ts)     | 纯函数：静态表 ⊕ 运行状态 ⊕ 动态值 → 插槽要渲染的条目（docs/plugins/extension-host.md §16.1）。     |
| [workbenchReport.ts](workbenchReport.ts) | 纯函数：把各窗格的报告合成一份屏幕会话报告（docs/plugins/extension-host.md §3.4）。                 |

<!-- qingqi-directory-index:end -->
