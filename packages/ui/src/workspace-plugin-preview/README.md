# workspace-plugin-preview

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 workspace plugin preview 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                                   |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts)               | 实现或公开接口：previewExample。                                                           |
| [CONTRACT.md](CONTRACT.md)                               | 模块职责、公共接口、依赖方向和状态约定。                                                   |
| [contract.ts](contract.ts)                               | Workspace catalog preview; selection emits a canonical mention without installing plugins. |
| [index.ts](index.ts)                                     | index 的实现文件。                                                                         |
| [module.ts](module.ts)                                   | \* workspace-plugin-preview 模块清单（architecture-governance managed 模块）。             |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                           |
| [WorkspacePluginPreview.tsx](WorkspacePluginPreview.tsx) | canonical mention 使用 manifest name；本地化显示名只用于菜单展示。                         |

<!-- qingqi-directory-index:end -->
