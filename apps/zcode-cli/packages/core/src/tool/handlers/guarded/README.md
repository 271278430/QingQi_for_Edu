# guarded

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 guarded 实现源码。

### 文件

| 文件                                   | 简要说明                                                                                              |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [cmd.ts](cmd.ts)                       | CMD 的有限入口：双引号与 caret；单引号是普通字符。复杂块/变量展开不解释。                             |
| [command.ts](command.ts)               | 解析失败没有可依赖的定位；局部 unsupported 节点则不丢弃其它独立命令。                                 |
| [find.ts](find.ts)                     | 有限 find 表达式；未知 arity 后不把参数值猜成动作，不递归分析 exec 载荷。                             |
| [git.ts](git.ts)                       | 前置参数走 abort 策略，未知即整体 unsupported，因此这里必须认识 -c/-p/-P/--exec-path 这类常见前置项； |
| [options.ts](options.ts)               | \* 扫描策略必须由调用方显式声明，没有默认值。                                                         |
| [README.md](README.md)                 | 本目录用途、子目录与逐文件说明。                                                                      |
| [windows-delete.ts](windows-delete.ts) | CMD 内建删除：斜杠开关只在 CMD 分支解释；独立帮助不是删除调用。                                       |
| [word.ts](word.ts)                     | AST 定位后的单词事实；不执行 expansion，也不将未知词当作已知选项。                                    |
| [wrappers.ts](wrappers.ts)             | wrapper 的未知选项决定真实命令从哪个词开始，猜不出只能整体放弃。                                      |

<!-- qingqi-directory-index:end -->
