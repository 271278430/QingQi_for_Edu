# voice-input

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 voice input 实现源码。

### 子目录

| 目录                            | 存放内容                                             |
| ------------------------------- | ---------------------------------------------------- |
| [adapters/](adapters/README.md) | @zcode/ui 基础工程中的 adapters 外部能力与平台适配。 |
| [domain/](domain/README.md)     | @zcode/ui 基础工程中的 domain 实现源码。             |
| [ui/](ui/README.md)             | @zcode/ui 基础工程中的 ui 实现源码。                 |

### 文件

| 文件                                       | 简要说明                                                                                |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* voice-input 标准用法：Composer 调用一次 hook，把按钮放在发送键左侧；                 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                                |
| [contract.ts](contract.ts)                 | \* voice-input（UI）对外契约：Composer 只依赖这里的类型与 index.ts 导出的 hook / 组件。 |
| [index.ts](index.ts)                       | index 的实现文件。                                                                      |
| [module.ts](module.ts)                     | \* voice-input 模块清单（architecture-governance managed 模块）。                       |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                        |

<!-- qingqi-directory-index:end -->
