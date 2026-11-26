# memory

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 memory 实现源码。

### 子目录

| 目录                        | 存放内容                                   |
| --------------------------- | ------------------------------------------ |
| [recall/](recall/README.md) | @zcode/core 基础工程中的 recall 实现源码。 |

### 文件

| 文件                                                                     | 简要说明                                                                                                                                |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| [directory.ts](directory.ts)                                             | 目录预创建失败不阻断执行；实际 Write/Edit 仍返回原始文件错误。                                                                          |
| [dream.ts](dream.ts)                                                     | 不存在或不可读都按无 owner 处理，后续 write-readback 决定所有权。                                                                       |
| [extraction.ts](extraction.ts)                                           | 实现或公开接口：MemoryExtractionExecutionStatus、MemoryExtractionSnapshot、MemoryExtractionDecision、MemoryExtractionExecutionInput。   |
| [index-content.ts](index-content.ts)                                     | 记忆目录里的索引文件名；上下文前缀注入它，compaction 补回据此排除它。                                                                   |
| [memory-agent-loop.ts](memory-agent-loop.ts)                             | 渲染器给出的一轮请求：消息、工具目录与 ToolSearch 开关。                                                                                |
| [memory-file-path.ts](memory-file-path.ts)                               | 实现或公开接口：resolveContainedMemoryFilePath、resolveSafeMemoryFilePath、memoryFileRelativePath、containsSensitiveMemoryPathSegment。 |
| [origin-session.ts](origin-session.ts)                                   | 基线只在缺少 origin 时序列化 frontmatter，并在同一次写入补齐 node_type。                                                                |
| [project-memory-retrieval-branch.ts](project-memory-retrieval-branch.ts) | 当前默认检索分支关闭 Semantic Recall；未来切换只修改这一处值。                                                                          |
| [project-root.ts](project-root.ts)                                       | 实现或公开接口：resolveProjectMemoryRoot。                                                                                              |
| [README.md](README.md)                                                   | 本目录用途、子目录与逐文件说明。                                                                                                        |

<!-- qingqi-directory-index:end -->
