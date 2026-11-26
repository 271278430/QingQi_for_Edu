# mcp-sync

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 mcp sync 实现源码。

### 文件

| 文件                                   | 简要说明                                                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [mcpSync.ts](mcpSync.ts)               | \* MCP 通道：设置页配置读写 + 数据同步（IDataSyncCategoryService，docs/remote/data-sync.md「MCP 服务器」）。 |
| [mcpSyncService.ts](mcpSyncService.ts) | 历史遗留：桌面端早期把停用状态写成 enable，而 CLI 契约字段（contracts McpServerConfigBase）                  |
| [README.md](README.md)                 | 本目录用途、子目录与逐文件说明。                                                                             |

<!-- qingqi-directory-index:end -->
