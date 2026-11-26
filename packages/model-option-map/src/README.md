# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/model-option-map 基础工程中的 src 实现源码。

### 文件

| 文件                             | 简要说明                                                                            |
| -------------------------------- | ----------------------------------------------------------------------------------- |
| [compiler.ts](compiler.ts)       | 实现或公开接口：compileRestrictedCel、compileModelOptionMap。                       |
| [evaluator.ts](evaluator.ts)     | 实现或公开接口：evaluateRestrictedCel。                                             |
| [index.ts](index.ts)             | index 的实现文件。                                                                  |
| [merge-patch.ts](merge-patch.ts) | 实现或公开接口：NamedJsonMergePatch、applyOrderedJsonMergePatches。                 |
| [option-maps.ts](option-maps.ts) | Model 创建时编译一次；每个请求只绑定本轮冻结的 Option value。                       |
| [parser.ts](parser.ts)           | 实现或公开接口：RestrictedCelExpression、parseRestrictedCel。                       |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。                                                    |
| [tokenizer.ts](tokenizer.ts)     | 实现或公开接口：RestrictedCelTokenKind、RestrictedCelToken、tokenizeRestrictedCel。 |
| [types.ts](types.ts)             | 实现或公开接口：JsonPrimitive、JsonValue、JsonObject、RestrictedCelValue。          |

<!-- qingqi-directory-index:end -->
