# test

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dev-docs 基础工程中的 test 测试场景。

### 文件

| 文件                                                                                   | 简要说明                                                                                             |
| -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| [capabilityMapComplexity.test.ts](capabilityMapComplexity.test.ts)                     | 原测试依赖当前能力图，并把缺失端点误计为跨群边，导致 136 != 137。                                    |
| [capabilityMapNoPersonnelOwnership.test.ts](capabilityMapNoPersonnelOwnership.test.ts) | 开源前移除了真实人名黑名单：改为正向约束，owner 必须是“<职责>负责人（<Role> Owner）”形态的角色描述， |
| [capabilityMapSystemPlacement.test.ts](capabilityMapSystemPlacement.test.ts)           | capabilityMapSystemPlacement.test 的实现文件。                                                       |
| [featureBoundaryGraph.test.ts](featureBoundaryGraph.test.ts)                           | featureBoundaryGraph.test 的实现文件。                                                               |
| [README.md](README.md)                                                                 | 本目录用途、子目录与逐文件说明。                                                                     |

<!-- qingqi-directory-index:end -->
