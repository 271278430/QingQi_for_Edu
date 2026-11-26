# presets

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 presets 实现源码。

### 文件

| 文件                                           | 简要说明                                                                                  |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [apply.ts](apply.ts)                           | \* `applyArtifactItems` —— 把一串 `report(item, artifactId)` 条目折成预置看板的视图模型。 |
| [ArtifactBoard.tsx](ArtifactBoard.tsx)         | \* `board` 预置渲染器：按 `status` 分列的卡片墙，卡片按 `key` upsert。                    |
| [ArtifactChart.tsx](ArtifactChart.tsx)         | \* `chart` 预置渲染器的**入口**：懒加载 + 局部故障隔离，本模块自己不碰 recharts。         |
| [ArtifactChartView.tsx](ArtifactChartView.tsx) | \* `chart` 预置渲染器的**实现**（recharts 在这个模块里，且只在这里）。                    |
| [ArtifactMetrics.tsx](ArtifactMetrics.tsx)     | \* `metrics` 预置渲染器：一排瓦片，每块显示**最后一条带该字段**的条目里的值。             |
| [ArtifactTable.tsx](ArtifactTable.tsx)         | \* `table` 预置渲染器：一行一条（或按 `key` upsert 的一行一实体）。                       |
| [index.ts](index.ts)                           | \* 四个渲染器 + 两个纯函数层：                                                            |
| [palette.ts](palette.ts)                       | \* 预置图表的序列调色板与**次级编码**。                                                   |
| [parts.tsx](parts.tsx)                         | \* 四个预置渲染器共用的小零件：labels 契约、空态、字段标签、揭示动画的类名。              |
| [README.md](README.md)                         | 本目录用途、子目录与逐文件说明。                                                          |
| [spec.ts](spec.ts)                             | \* 预置产物（chart / table / metrics / board）的 spec 类型镜像 + 宽松解析。               |

<!-- qingqi-directory-index:end -->
