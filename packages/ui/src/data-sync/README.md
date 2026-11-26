# data-sync

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 data sync 实现源码。

### 子目录

| 目录                        | 存放内容                                 |
| --------------------------- | ---------------------------------------- |
| [app/](app/README.md)       | @zcode/ui 基础工程中的 app 实现源码。    |
| [domain/](domain/README.md) | @zcode/ui 基础工程中的 domain 实现源码。 |
| [ui/](ui/README.md)         | @zcode/ui 基础工程中的 ui 实现源码。     |

### 文件

| 文件                                       | 简要说明                                                                                                           |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | \* data-sync 标准调用示例：设置页用本机 base services 作为 source，设备的 source-settings attachment 作为 target。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                                           |
| [contract.ts](contract.ts)                 | 当前已接入的数据同步分类；新分类在 categories.ts 注册适配器后加入这里。                                            |
| [index.ts](index.ts)                       | index 的实现文件。                                                                                                 |
| [module.ts](module.ts)                     | \* data-sync 模块清单（architecture-governance managed 模块）。                                                    |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                                                   |

<!-- qingqi-directory-index:end -->
