# http

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 http 实现源码。

### 文件

| 文件                                               | 简要说明                                                                                              |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| [index.ts](index.ts)                               | Node HTTP Client Adapter                                                                              |
| [public-egress-policy.ts](public-egress-policy.ts) | 实现或公开接口：DnsLookupAddress、DnsLookup、defaultPublicDnsLookup、assertPublicEgressDestination。  |
| [README.md](README.md)                             | 本目录用途、子目录与逐文件说明。                                                                      |
| [response-body.ts](response-body.ts)               | \* 读正文所需的最小形状：原生 fetch 的 `Response` 与 adapter 自己读出的 `IncomingResponse` 都满足它。 |

<!-- qingqi-directory-index:end -->
