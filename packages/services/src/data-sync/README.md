# data-sync

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 data sync 实现源码。

### 文件

| 文件                                                   | 简要说明                                                                                                     |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| [commandDataSync.ts](commandDataSync.ts)               | 相对命令根目录的路径，`/` 分隔，保留大小写。                                                                 |
| [contract.example.ts](contract.example.ts)             | \* data-sync-service 标准调用示例：source 导出、target 预检后按每项 mode 导入。                              |
| [CONTRACT.md](CONTRACT.md)                             | 模块职责、公共接口、依赖方向和状态约定。                                                                     |
| [contract.ts](contract.ts)                             | \* 数据同步分类服务的统一形状（docs/remote/data-sync.md「统一的同步服务形状」）。                            |
| [deviceSyncStateService.ts](deviceSyncStateService.ts) | \* 设备同步状态：本机 Host 的一个小文件，按 sourceServerId 记录上次推送的时间和结果。                        |
| [directoryContent.ts](directoryContent.ts)             | 目录内部存在软链（不跟随）。                                                                                 |
| [hookDataSync.ts](hookDataSync.ts)                     | 通过 schema 校验后的原始 hooks 对象：直接在原对象上合并，未知字段（定义上的透传字段）原样保留。              |
| [index.ts](index.ts)                                   | 浏览器安全的公共入口：只导出契约。Renderer 经 @zcode/services 引到这里，不能带入 node:fs 等实现。            |
| [inlinePluginDataSync.ts](inlinePluginDataSync.ts)     | \* 插件目录内的 `data/` 是该端的运行数据：不导出、不参与签名和哈希，覆盖时保留目标端的 `data/`。             |
| [mcpDataSync.ts](mcpDataSync.ts)                       | 比较时排除的启用状态字段（含历史遗留的 enable）。                                                            |
| [module.ts](module.ts)                                 | \* data-sync-service 模块清单（architecture-governance managed 模块）。                                      |
| [node.ts](node.ts)                                     | Node 侧实现入口（Host / Server 使用），由 @zcode/services/node 转出。                                        |
| [README.md](README.md)                                 | 本目录用途、子目录与逐文件说明。                                                                             |
| [skillDataSync.ts](skillDataSync.ts)                   | 技能目录（可能是软链路径）。                                                                                 |
| [subagentDataSync.ts](subagentDataSync.ts)             | \* 依赖只认运行时支持的字符串名称（见 CLI `parseAgentMcpServers`）：MCP 的对象形式是内联配置，不依赖目标端。 |
| [syncUtils.ts](syncUtils.ts)                           | 数据同步各分类共用的小工具（Node 侧实现内部使用，不经公共入口导出）。                                        |
| [userConfigSyncService.ts](userConfigSyncService.ts)   | \* 用户配置同步通道：按 category 分派到各分类的实现（新分类在 categories 中追加一项）。                      |

<!-- qingqi-directory-index:end -->
