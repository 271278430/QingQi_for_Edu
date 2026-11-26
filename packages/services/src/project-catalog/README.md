# project-catalog

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 project catalog 实现源码。

### 文件

| 文件                                       | 简要说明                                                              |
| ------------------------------------------ | --------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：example。                                             |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                              |
| [contract.ts](contract.ts)                 | 实现或公开接口：ProjectCatalogPort、ProjectCatalogSnapshot。          |
| [index.ts](index.ts)                       | 尚未转换的旧入口只在目录唯一匹配时展示；不据读取结果新增/更新入口。   |
| [module.ts](module.ts)                     | \* project-catalog 模块清单（architecture-governance managed 模块）。 |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                      |
| [selection-id.ts](selection-id.ts)         | 选择项只按 Host/项目隔离，不承担 workspace 身份或路径语义。           |

<!-- qingqi-directory-index:end -->
