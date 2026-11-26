# storage

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 storage 实现源码。

### 子目录

| 目录                            | 存放内容                                                   |
| ------------------------------- | ---------------------------------------------------------- |
| [adapters/](adapters/README.md) | @zcode/services 基础工程中的 adapters 外部能力与平台适配。 |
| [app/](app/README.md)           | @zcode/services 基础工程中的 app 实现源码。                |
| [domain/](domain/README.md)     | @zcode/services 基础工程中的 domain 实现源码。             |

### 文件

| 文件                                       | 简要说明                                                                    |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | \* 契约用法示例：进入分区时订阅进度并开始扫描，离开时取消；清理后重新扫描。 |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                    |
| [contract.ts](contract.ts)                 | \* storage 模块公开契约：资源管理器「存储」tab 使用的服务接口与类型再导出。 |
| [module.ts](module.ts)                     | \* storage 模块清单：设置页「存储管理」的磁盘占用扫描与清理。               |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                            |

<!-- qingqi-directory-index:end -->
