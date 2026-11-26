# workflow-graph

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 workflow graph 界面组件。

### 文件

| 文件                                                     | 简要说明                                                                                 |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [instance-phases.ts](instance-phases.ts)                 | \* 静态的 may-set 拷贝按阶段索引（`ask#1~phase#3`），运行时实例带同一个坐标——引擎在铸造  |
| [lane-name.ts](lane-name.ts)                             | \* 站点 id（`actor#3`）是**身份**：journal 的 key、hover 标题里的锚、排查问题时的抓手。  |
| [name-pattern.ts](name-pattern.ts)                       | \* 「名字只在运行时才成形」这件事的唯一渲染点。                                          |
| [participant-model.ts](participant-model.ts)             | \* 载荷的 `participants` 已经是分析器排好的**交接序**（第一张是开局者），`handoffs` 已经 |
| [phase-model.ts](phase-model.ts)                         | \* 阶段层的纯选择器。阶段是图**上面的一层商**：                                          |
| [phase-name.ts](phase-name.ts)                           | \* 阶段显示名的唯一策略点，与 lane-name.ts 逐条同构（同一件事只有一套规则）：            |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                         |
| [run-status-presentation.ts](run-status-presentation.ts) | \* 状态灯的全部形与色。消费方自带尺寸与                                                  |
| [run-status.ts](run-status.ts)                           | \* 实时叠加视图（live view v1）的纯选择器。                                              |
| [types.ts](types.ts)                                     | \* The graph the renderer consumes is exactly the bounded display payload from the       |
| [use-now-ticker.ts](use-now-ticker.ts)                   | 倒计时的自然粒度：秒级文案再快一格文字也不会变。                                         |

<!-- qingqi-directory-index:end -->
