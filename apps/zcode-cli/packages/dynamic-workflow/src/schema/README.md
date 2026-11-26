# schema

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dynamic-workflow 基础工程中的 schema 实现源码。

### 文件

| 文件                                                 | 简要说明                                                                                            |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [actor-submit-profiles.ts](actor-submit-profiles.ts) | \* 每个 actor 站点的 **submit profile**：决定该 actor 的子代理会话拿到哪一种 `submit_result` 工具。 |
| [emit.ts](emit.ts)                                   | \* 类型 → JSON Schema 的发射器（emitter），由 checker 的结构化视图驱动（泛型/别名                   |
| [jsdoc.ts](jsdoc.ts)                                 | \* JSDoc 采集：把符号（interface 成员、类型别名、ask 结果类型）上的文档注释与受支持的               |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                                    |
| [serialize.ts](serialize.ts)                         | \* 确定性序列化：把 schema 的对象键递归排序后再 JSON.stringify，保证快照稳定，与发射                |
| [synthesize.ts](synthesize.ts)                       | AskSpec 是引擎的入参词汇表，这里只 import type（编译期抹除，无运行时边）。engine 侧                 |
| [types.ts](types.ts)                                 | \* schema 子系统的共享词汇：我们「发射（emit）」的 JSON Schema 子集类型，以及校验器                 |
| [validate.ts](validate.ts)                           | \* 纯校验器，覆盖范围恰好是 {@link synthesizeAskSchemas} 会发射的 JSON Schema 子集                  |

<!-- qingqi-directory-index:end -->
