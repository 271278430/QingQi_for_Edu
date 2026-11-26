# settings-scope

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 settings scope 实现源码。

### 子目录

| 目录                        | 存放内容                                 |
| --------------------------- | ---------------------------------------- |
| [app/](app/README.md)       | @zcode/ui 基础工程中的 app 实现源码。    |
| [domain/](domain/README.md) | @zcode/ui 基础工程中的 domain 实现源码。 |
| [ui/](ui/README.md)         | @zcode/ui 基础工程中的 ui 实现源码。     |

### 文件

| 文件                                       | 简要说明                                                                                                  |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* settings-scope 标准调用示例：配置目录目录表 + 管理快照 → 菜单分组；选中 key → 读写目标。               |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                  |
| [contract.ts](contract.ts)                 | \* settings-scope 合同：设置页 Scope 菜单按设备分组（docs/remote/data-sync.md「Scope 菜单按设备分组」）。 |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                        |
| [module.ts](module.ts)                     | \* settings-scope 模块清单（architecture-governance managed 模块）。                                      |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                          |

<!-- qingqi-directory-index:end -->
