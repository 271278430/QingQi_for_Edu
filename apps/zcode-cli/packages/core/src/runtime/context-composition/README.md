# context-composition

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 context composition 实现源码。

### 文件

| 文件                           | 简要说明                                                                                                         |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| [classifier.ts](classifier.ts) | Context 组成的分类纯函数：一次请求 → 细类别；细类别 → 圆环的 7 个粗类别；细类别 → 线格式。                       |
| [index.ts](index.ts)           | context-composition（CLI core 部分）公开入口。规格：apps/zcode-cli/docs/design/v2/model/context-composition.md。 |
| [items.ts](items.ts)           | 技能与指令文件的条目（名字与元数据大小）。类别大小按请求里公告的真实文本计，这里只出明细。                       |
| [preview.ts](preview.ts)       | 草稿预演：按所查模型模拟「下一个请求」，在 entries 的副本上走一遍请求准备，再用同一分类函数出数。                |
| [query.ts](query.ts)           | context 组成的查询入口：有效的请求组成且模型相同时返回它，否则按所查模型预演。                                   |
| [README.md](README.md)         | 本目录用途、子目录与逐文件说明。                                                                                 |
| [state.ts](state.ts)           | 每个 runtime 的 context 组成状态：最近一次请求的组成与变更监听器。查询入口在 query.ts。                          |

<!-- qingqi-directory-index:end -->
