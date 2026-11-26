# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/office-runtime 基础工程中的 src 实现源码。

### 子目录

| 目录                            | 存放内容                                                         |
| ------------------------------- | ---------------------------------------------------------------- |
| [adapters/](adapters/README.md) | @zcode/office-runtime 基础工程中的 adapters 外部能力与平台适配。 |
| [app/](app/README.md)           | @zcode/office-runtime 基础工程中的 app 实现源码。                |
| [domain/](domain/README.md)     | @zcode/office-runtime 基础工程中的 domain 实现源码。             |

### 文件

| 文件                       | 简要说明                                                                                        |
| -------------------------- | ----------------------------------------------------------------------------------------------- |
| [CONTRACT.md](CONTRACT.md) | 模块职责、公共接口、依赖方向和状态约定。                                                        |
| [contract.ts](contract.ts) | Formats this plugin opens.                                                                      |
| [kinds.ts](kinds.ts)       | \* Every format the runtime knows; a plugin opens the subset in its profile.                    |
| [profile.ts](profile.ts)   | \* Which plugin this build is. Each plugin package declares its title and formats under         |
| [README.md](README.md)     | 本目录用途、子目录与逐文件说明。                                                                |
| [types.d.ts](types.d.ts)   | types.d 的实现文件。                                                                            |
| [wording.ts](wording.ts)   | \* Model-facing wording that names formats, limited to the formats this plugin opens. Each list |

<!-- qingqi-directory-index:end -->
