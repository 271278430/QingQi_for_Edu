# data

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dev-docs 基础工程中的 data 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                                                              |
| -------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [featureBoundaryGraph.ts](featureBoundaryGraph.ts)             | 实现或公开接口：featureBoundaryNodeKinds、FeatureBoundaryNodeKind、FeatureBoundaryRelationRank、FeatureBoundaryNode。 |
| [featureBoundaryGraphSource.ts](featureBoundaryGraphSource.ts) | 实现或公开接口：normalizeFeatureBoundaryGraph。                                                                       |
| [productCapabilityMap.ts](productCapabilityMap.ts)             | 能力群、节点与连线必须作为同一份审计数据集整体校验，避免跨文件产生悬空引用。                                          |
| [protocolDocs.ts](protocolDocs.ts)                             | 实现或公开接口：ConceptKind、Concept、FieldDoc、StructureDoc。                                                        |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                                                      |

<!-- qingqi-directory-index:end -->
