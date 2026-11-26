# network

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 network 实现源码。

### 文件

| 文件                                         | 简要说明                                                                                                                  |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| [http-config.ts](http-config.ts)             | 实现或公开接口：resolveProxyUrlForRequest、resolveWebFetchProxyForRequest、resolveProxyForRequest、resolveTlsCaCertFile。 |
| [incoming-response.ts](incoming-response.ts) | \* adapter 自己发请求时（代理、自定义 CA、公网 DNS 校验），把 Node 的 `IncomingMessage` 交给上层的唯一入口                |
| [proxy-fetch.ts](proxy-fetch.ts)             | 临时 Request 的 controller 可被 GC，不能把其从属 signal 留作取消来源。                                                    |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                                                                          |
| [subprocess-env.ts](subprocess-env.ts)       | 实现或公开接口：NetworkEgressEnvPolicy、applyNetworkEgressEnv。                                                           |

<!-- qingqi-directory-index:end -->
