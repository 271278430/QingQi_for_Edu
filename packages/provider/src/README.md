# src

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/provider 基础工程中的 src 实现源码。

### 子目录

| 目录                        | 存放内容                                       |
| --------------------------- | ---------------------------------------------- |
| [config/](config/README.md) | @zcode/provider 基础工程中的 config 实现源码。 |

### 文件

| 文件                                                             | 简要说明                                                                                                                               |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| [account-provider-resolution.ts](account-provider-resolution.ts) | 账号/组织身份变化后禁止沿用旧快照；仅用于本轮解析，不进入配置。                                                                        |
| [account-provider-service.ts](account-provider-service.ts)       | \* 维护当前账号状态投影出的第三层 Provider Config Overlay。                                                                            |
| [account-provider-state.ts](account-provider-state.ts)           | \* 账号不可用原因，只回答"为什么不可用"。                                                                                              |
| [config-overlay.ts](config-overlay.ts)                           | \* 稀疏配置层和覆盖完成后的配置使用同一类型。                                                                                          |
| [config-service.ts](config-service.ts)                           | Facade 提供的 Host 内部成员事实；不得接受 Renderer 自报的模型名单。                                                                    |
| [effective-model-selection.ts](effective-model-selection.ts)     | \* 只解析未来执行的意图，不改原选择、持久记录或已固定请求。                                                                            |
| [facades.ts](facades.ts)                                         | 主动重读上游事实后再刷新 Registry。                                                                                                    |
| [index.ts](index.ts)                                             | index 的实现文件。                                                                                                                     |
| [model-selection-config.ts](model-selection-config.ts)           | 这里只构造 Host 的初始推荐，不解析已有会话意图。失效默认是可丢弃偏好，                                                                 |
| [owned-order.ts](owned-order.ts)                                 | \* 规范化 Built-in/Personal 共同拥有的可排序成员。                                                                                     |
| [README.md](README.md)                                           | 本目录用途、子目录与逐文件说明。                                                                                                       |
| [registry-service.ts](registry-service.ts)                       | 启动只负责就绪；业务读取必须使用 getSnapshot，不能长期保留首次启动快照。                                                               |
| [registry.ts](registry.ts)                                       | 实现或公开接口：ModelSelectionOptions、ModelSelectionValidation、ProviderRegistryView、ProviderRegistryChangedEvent。                  |
| [resolver.ts](resolver.ts)                                       | 实现或公开接口：RegistryZhipuAccountAccessConfig、RegistryProviderAccessConfig、RegistryProviderConfig、RegistryProviderConfigObject。 |
| [sources.ts](sources.ts)                                         | 首次 Account 事实尚未到达时，基于当前 Built-in 生成可发布的 fail-closed Overlay。                                                      |

<!-- qingqi-directory-index:end -->
