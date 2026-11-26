# extension-slots

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/ui 基础工程中的 extension slots 实现源码。

### 子目录

| 目录                                | 存放内容                                             |
| ----------------------------------- | ---------------------------------------------------- |
| [adapters/](adapters/README.md)     | @zcode/ui 基础工程中的 adapters 外部能力与平台适配。 |
| [app/](app/README.md)               | @zcode/ui 基础工程中的 app 实现源码。                |
| [components/](components/README.md) | @zcode/ui 基础工程中的 components 界面组件。         |
| [domain/](domain/README.md)         | @zcode/ui 基础工程中的 domain 实现源码。             |

### 文件

| 文件                                       | 简要说明                                                                             |
| ------------------------------------------ | ------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 输入框工具栏在用量圆环左边挂 composer.status：传当前工作区与会话（草稿为预热会话）。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                             |
| [contract.ts](contract.ts)                 | extension-slots 的公开契约（docs/plugins/extension-host.md §4、§6、§16.1）。         |
| [index.ts](index.ts)                       | index 的实现文件。                                                                   |
| [module.ts](module.ts)                     | \* extension-slots 模块清单（architecture-governance managed 模块）。                |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                                     |

<!-- qingqi-directory-index:end -->
