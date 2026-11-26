# web-remote-relay

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 web remote relay 实现源码。

### 子目录

| 目录                            | 存放内容                                                 |
| ------------------------------- | -------------------------------------------------------- |
| [adapters/](adapters/README.md) | @zcode/shared 基础工程中的 adapters 外部能力与平台适配。 |
| [domain/](domain/README.md)     | @zcode/shared 基础工程中的 domain 实现源码。             |

### 文件

| 文件                                       | 简要说明                                                                      |
| ------------------------------------------ | ----------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts) | 实现或公开接口：matchedDevice。                                               |
| [CONTRACT.md](CONTRACT.md)                 | 模块职责、公共接口、依赖方向和状态约定。                                      |
| [contract.ts](contract.ts)                 | 请求与 WebSocket 消息严格校验 V2，HTTP 响应允许新增字段。                     |
| [index.ts](index.ts)                       | 新源码原来散落在 legacy 根目录，CI 无法确认归属；公开入口统一收口到受管模块。 |
| [mobileLog.ts](mobileLog.ts)               | \* 手机日志通道（远控 app payload）：                                         |
| [module.ts](module.ts)                     | 依赖与 architecture-policy.yaml 同步；新增文件必须属于此 managed 边界。       |
| [README.md](README.md)                     | 本目录用途、子目录与逐文件说明。                                              |

<!-- qingqi-directory-index:end -->
