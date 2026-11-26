# plugins

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 plugins 实现源码。

### 文件

| 文件                                                 | 简要说明                                                                                                                                 |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| [atomic-directory.ts](atomic-directory.ts)           | 读取 standalone 原子文件的完整一代；恢复清理由现有写入口负责，读者不抢占事务。                                                           |
| [github-archive-source.ts](github-archive-source.ts) | 实现或公开接口：PublicGitHubRepository、ResolveGitHubArchiveSourceInput、GitHubArchiveRequiresGitError、parsePublicGitHubRepositoryUrl。 |
| [helpers.ts](helpers.ts)                             | 与原写入语义一致：读失败继续写，让实际写入错误向上传递。                                                                                 |
| [hook-sources.ts](hook-sources.ts)                   | \* 统一发现插件 hook 来源文件，避免详情枚举和真实 loader 对 `hooks/hooks.json`                                                           |
| [index.ts](index.ts)                                 | 外部清单的扩展字段不能穿透到 strict 协议；采用已知字段校验，尤其不能丢掉 sensitive。                                                     |
| [markdown-frontmatter.ts](markdown-frontmatter.ts)   | 分批读取避免一次启动所有文件 IO；数组顺序保留同名组件的既有优先级。                                                                      |
| [marketplace.ts](marketplace.ts)                     | 内置 official 插件 seed 时写                                                                                                             |
| [mcp-official-auth.ts](mcp-official-auth.ts)         | \* Plugin `.mcp.json` 里 `auth: { type: "zcode_official" }` 的严格解析与 provenance 生成。                                               |
| [mcp.ts](mcp.ts)                                     | 实现或公开接口：loadPluginMcpServerDefinitions、resolvePluginMcpServers。                                                                |
| [official-marketplace.ts](official-marketplace.ts)   | 启动 seed 和商店刷新可来自不同进程。分片写入和合并发布同属一次事务，                                                                     |
| [plugin-components.ts](plugin-components.ts)         | 组件分组类型定义已上移到 @zcode/contracts（PluginMetadata 需要引用），这里再导出保持对外契约稳定。                                       |
| [README.md](README.md)                               | 本目录用途、子目录与逐文件说明。                                                                                                         |
| [source-errors.ts](source-errors.ts)                 | \* source materialization 错误现在会被持久化并投影到桌面/Web UI，不能把 URL                                                              |
| [types.ts](types.ts)                                 | 实现或公开接口：PluginCandidate、LoadedPlugin、PluginComponents、PluginAbortOptions。                                                    |
| [ui-surfaces.ts](ui-surfaces.ts)                     | \* 清单 `ui.surfaces[]` 解析。                                                                                                           |
| [version-compare.ts](version-compare.ts)             | \* Compare an installed plugin version against the latest manifest version.                                                              |
| [zip-source.ts](zip-source.ts)                       | 实现或公开接口：ResolvedZipPluginSourceRoot、ResolveZipPluginSourceInput、ResolveHttpZipSourceInput、PluginZipDownloadError。            |

<!-- qingqi-directory-index:end -->
