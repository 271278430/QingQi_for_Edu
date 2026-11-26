# workspace-config-catalog

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 workspace config catalog 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                       |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [catalog.ts](catalog.ts)                                       | 实现或公开接口：projectConfigTargets。                                         |
| [contract.example.ts](contract.example.ts)                     | 实现或公开接口：exampleWorkspaceConfigCatalog。                                |
| [CONTRACT.md](CONTRACT.md)                                     | 模块职责、公共接口、依赖方向和状态约定。                                       |
| [contract.ts](contract.ts)                                     | 配置目录地址不是 tab/session；连接信息只能采用已存在的 attachment。            |
| [index.ts](index.ts)                                           | index 的实现文件。                                                             |
| [module.ts](module.ts)                                         | \* workspace-config-catalog 模块清单（architecture-governance managed 模块）。 |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                               |
| [useConfigWorkspaceServices.ts](useConfigWorkspaceServices.ts) | 配置专用解析；不改变 conversation 的 workspace attachment / replay 边界。      |
| [useConfigWorkspaceTargets.ts](useConfigWorkspaceTargets.ts)   | 实现或公开接口：useConfigWorkspaceTargets。                                    |

<!-- qingqi-directory-index:end -->
