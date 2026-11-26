# provider-provisioning-status

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 provider provisioning status 实现源码。

### 文件

| 文件                                                                   | 简要说明                                                                                           |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)                             | \* provider-provisioning-status 标准调用示例：读取最近结果，只在有 lane 且最近一次失败时重试。     |
| [CONTRACT.md](CONTRACT.md)                                             | 模块职责、公共接口、依赖方向和状态约定。                                                           |
| [contract.ts](contract.ts)                                             | \* 数据同步页「模型提供商」分类读取 / 重试该设备的 Provisioning lane（docs/remote/data-sync.md）。 |
| [hostProviderProvisioningStatus.ts](hostProviderProvisioningStatus.ts) | \* 本机 Host 到 Main 协调器的 Provisioning lane 访问。                                             |
| [index.ts](index.ts)                                                   | 浏览器安全的公共入口：只导出契约。Renderer 经 @zcode/services 引到这里。                           |
| [module.ts](module.ts)                                                 | \* provider-provisioning-status 模块清单（architecture-governance managed 模块）。                 |
| [node.ts](node.ts)                                                     | Host 侧实现入口，由 @zcode/services/node 转出。                                                    |
| [README.md](README.md)                                                 | 本目录用途、子目录与逐文件说明。                                                                   |

<!-- qingqi-directory-index:end -->
