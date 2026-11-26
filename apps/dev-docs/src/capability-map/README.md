# capability-map

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/dev-docs 基础工程中的 capability map 实现源码。

### 文件

| 文件                                                               | 简要说明                                                                                                                                       |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| [CapabilityMapDetail.tsx](CapabilityMapDetail.tsx)                 | 实现或公开接口：CapabilityMapDetail。                                                                                                          |
| [CapabilityMapFlowElements.tsx](CapabilityMapFlowElements.tsx)     | 实现或公开接口：capabilityMapNodeTypes、capabilityMapEdgeTypes。                                                                               |
| [capabilityMapGeometry.ts](capabilityMapGeometry.ts)               | 修复原因：双语标题、owner 与 LOC/入出度徽标的真实高度超过旧版 ELK 顶部留白，                                                                   |
| [CapabilityMapGraph.tsx](CapabilityMapGraph.tsx)                   | 交互约定：滚轮缩放，平移只通过拖拽；panOnScroll 会吞掉滚轮缩放。                                                                               |
| [capabilityMapGroupOrder.ts](capabilityMapGroupOrder.ts)           | 实现或公开接口：orderGroupsByRelations。                                                                                                       |
| [capabilityMapLayout.ts](capabilityMapLayout.ts)                   | 实现或公开接口：CapabilitySystemLayout、CapabilityGroupLayout、CapabilityNodeLayout、CapabilityEdgeRoute。                                     |
| [capabilityMapSystemPlacement.ts](capabilityMapSystemPlacement.ts) | 实现或公开接口：ENGINEERING_INFRASTRUCTURE_SYSTEM_ID、CAPABILITY_MAP_ROOT_PADDING、CAPABILITY_MAP_SYSTEM_GAP、CapabilitySystemPlacementInput。 |
| [CapabilityMapToolbar.tsx](CapabilityMapToolbar.tsx)               | 实现或公开接口：CapabilityMapToolbar。                                                                                                         |
| [capabilityMapTypes.ts](capabilityMapTypes.ts)                     | 实现或公开接口：EdgeScope、CapabilitySelection、CapabilitySystemNodeData、CapabilityGroupNodeData。                                            |
| [CapabilityMapView.tsx](CapabilityMapView.tsx)                     | 实现或公开接口：CapabilityMapView。                                                                                                            |
| [README.md](README.md)                                             | 本目录用途、子目录与逐文件说明。                                                                                                               |
| [useCapabilityMapHighlight.ts](useCapabilityMapHighlight.ts)       | 实现或公开接口：useCapabilityMapHighlight。                                                                                                    |
| [useCapabilityMapLayout.ts](useCapabilityMapLayout.ts)             | 实现或公开接口：useCapabilityMapLayout。                                                                                                       |

<!-- qingqi-directory-index:end -->
