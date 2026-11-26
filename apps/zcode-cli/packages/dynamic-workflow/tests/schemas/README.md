# schemas

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 schemas 运行时数据结构。

### 子目录

| 目录                            | 存放内容                                                       |
| ------------------------------- | -------------------------------------------------------------- |
| [expected/](expected/README.md) | @zcode/dynamic-workflow 基础工程中的 expected 运行时数据结构。 |

### 文件

| 文件                                               | 简要说明                                                                             |
| -------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [collections.ts](collections.ts)                   | 数组、只读数组、元组（定长/可选/rest）、Record → additionalProperties。              |
| [jsdoc.ts](jsdoc.ts)                               | JSDoc 采集：description、数值/字符串约束标签、@default，以及顶层类型的 description。 |
| [objects.ts](objects.ts)                           | object：可选属性排除出 required、嵌套对象、闭合对象 additionalProperties: false。    |
| [primitives.ts](primitives.ts)                     | 基础类型、字面量、字面量 union → enum。                                              |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                     |
| [recursive.ts](recursive.ts)                       | 递归类型 → $defs/$ref：直接自引用与通过成员间接自引用。                              |
| [unions-intersections.ts](unions-intersections.ts) | 一般 union → anyOf（含 null 的对象 union），交叉类型展平为一个 object。              |
| [unknown-permissive.ts](unknown-permissive.ts)     | unknown → 许可式空 schema；与具体字段混用时只对 unknown 放行。                       |

<!-- qingqi-directory-index:end -->
