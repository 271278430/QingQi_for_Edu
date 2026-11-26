# schema-errors

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 schema errors 验收与回归场景。

### 文件

| 文件                                                 | 简要说明                                                                               |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------- |
| [any.ts](any.ts)                                     | any 几乎总是失误 —— 拒绝，逼迫改用 unknown 或具体接口。                                |
| [class-instance.ts](class-instance.ts)               | 类实例（自定义 class）承载行为，不是纯数据 —— 拒绝。                                   |
| [date.ts](date.ts)                                   | Date 是宿主对象，不是纯数据 —— 拒绝。                                                  |
| [function-type.ts](function-type.ts)                 | 函数类型不可序列化 —— 拒绝（顶层函数类型与对象上的方法成员都算）。                     |
| [map-set.ts](map-set.ts)                             | Map / Set 不可 JSON 序列化 —— 拒绝。两个独立 ask 各报一条。                            |
| [never.ts](never.ts)                                 | never 无法表达为任何值 —— 拒绝（顶层类型实参就是 never）。                             |
| [promise.ts](promise.ts)                             | Promise / thenable 不可序列化 —— 拒绝。                                                |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                       |
| [report-class-instance.ts](report-class-instance.ts) | 类实例不是纯数据（方法与原型都过不了 JSON 边界）—— report 与 ask<T> 同样拒绝。         |
| [report-date.ts](report-date.ts)                     | report(item) 的实参走与 ask<T> 结果同一套可序列化性判定：Date 是宿主对象，不是纯数据。 |
| [report-function.ts](report-function.ts)             | 函数值不可 JSON 序列化 —— report 在调用点拒绝它。                                      |
| [report-json-shapes.ts](report-json-shapes.ts)       | 正向覆盖：普通 JSON 形状与 `unknown` 都通过，一条诊断都不该有。                        |
| [symbol-bigint.ts](symbol-bigint.ts)                 | symbol 与 bigint 不可 JSON 序列化 —— 拒绝。                                            |
| [undefined-member.ts](undefined-member.ts)           | 非可选位置上的 undefined 成员 —— 拒绝（可选性应通过 `?` 表达，而不是 `\\               | undefined`）。 |

<!-- qingqi-directory-index:end -->
