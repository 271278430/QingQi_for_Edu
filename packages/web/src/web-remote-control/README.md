# web-remote-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 web remote control 实现源码。

### 子目录

| 目录                              | 存放内容                                              |
| --------------------------------- | ----------------------------------------------------- |
| [adapters/](adapters/README.md)   | @zcode/web 基础工程中的 adapters 外部能力与平台适配。 |
| [app/](app/README.md)             | @zcode/web 基础工程中的 app 实现源码。                |
| [contracts/](contracts/README.md) | @zcode/web 基础工程中的 contracts 公共契约。          |
| [domain/](domain/README.md)       | @zcode/web 基础工程中的 domain 实现源码。             |
| [ui/](ui/README.md)               | @zcode/web 基础工程中的 ui 实现源码。                 |

### 文件

| 文件                                       | 简要说明                                                                       |
| ------------------------------------------ | ------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：emptyDeviceList。                                              |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                       |
| [contract.ts](contract.ts)                 | relay meta.platform（darwin / win32 / linux 等），离线时回退到本机记住的平台。 |
| [index.ts](index.ts)                       | index 的实现文件。                                                             |
| [module.ts](module.ts)                     | 依赖与 architecture-policy.yaml 同步；新增文件必须属于此 managed 边界。        |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                               |
| [views.ts](views.ts)                       | views 的实现文件。                                                             |

<!-- qingqi-directory-index:end -->
