# providers

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 providers 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                       |
| -------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [bigmodelProviderAdapter.ts](bigmodelProviderAdapter.ts) | OAuth 启动恢复允许的最长等待时间（1 分钟）                                     |
| [bigmodelProviderConfig.ts](bigmodelProviderConfig.ts)   | 历史 fallback secret 已废弃，不能再把内置密钥打进运行时配置。                  |
| [configUtils.ts](configUtils.ts)                         | OAuth provider 是运行时配置，必须跟随传入 env.ZCODE_ENV；                      |
| [index.ts](index.ts)                                     | 根据运行时配置创建可用 provider adapter                                        |
| [providerAdapter.ts](providerAdapter.ts)                 | Provider 执行上下文                                                            |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                               |
| [zaiProviderAdapter.ts](zaiProviderAdapter.ts)           | OAuth 启动恢复允许的最长等待时间（1 分钟）                                     |
| [zaiProviderConfig.ts](zaiProviderConfig.ts)             | ZAI 当前 OAuth 授权入口使用 /api/oauth 前缀，继续走 /auth/oauth 会打开旧入口。 |

<!-- qingqi-directory-index:end -->
