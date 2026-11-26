# request-security-edition

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/shared 基础工程中的 request security edition 实现源码。

### 文件

| 文件                                             | 简要说明                                                                                                                           |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)       | Host 先判定账号是否需要交互，再以读取到的同一配置快照决定投递。                                                                    |
| [CONTRACT.md](CONTRACT.md)                       | 模块职责、公共接口、依赖方向和状态约定。                                                                                           |
| [contract.test.ts](contract.test.ts)             | contract.test 的实现文件。                                                                                                         |
| [contract.ts](contract.ts)                       | 是否需要交互由发行策略决定；配置缺失的失败处理由 Host 负责。                                                                       |
| [index.ts](index.ts)                             | index 的实现文件。                                                                                                                 |
| [module.ts](module.ts)                           | 发行策略边界；请求状态与异步编排仍由调用方持有。                                                                                   |
| [policy.ts](policy.ts)                           | 实现或公开接口：requestSecuritySensitiveHeaders、isRequestSecurityFailure。                                                        |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                                                                   |
| [verification-policy.ts](verification-policy.ts) | 实现或公开接口：RequestVerificationConfig、RequestVerificationProof、RequestVerificationClientConfig、requestVerificationReasons。 |

<!-- qingqi-directory-index:end -->
