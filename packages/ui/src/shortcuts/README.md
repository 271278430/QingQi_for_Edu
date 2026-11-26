# shortcuts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 shortcuts 实现源码。

### 文件

| 文件                                             | 简要说明                                                                |
| ------------------------------------------------ | ----------------------------------------------------------------------- |
| [bindings.ts](bindings.ts)                       | \* 快捷键执行内核 —— 匹配、录制、生效表与冲突检测的唯一实现。           |
| [composerShortcuts.ts](composerShortcuts.ts)     | \* composer 作用域快捷键解析——独立模块，唯一消费方是                    |
| [conflicts.ts](conflicts.ts)                     | \* 快捷键冲突策略——保留键黑名单、物理等价归一、占用检测与二次确认抢绑。 |
| [label.ts](label.ts)                             | \* 快捷键展示 label——绑定串 → 平台展示格式化。                          |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                        |
| [useShortcutBindings.ts](useShortcutBindings.ts) | \* 快捷键内核的 React 桥接：生效表与展示 label 的唯一 hook 出口。       |

<!-- qingqi-directory-index:end -->
