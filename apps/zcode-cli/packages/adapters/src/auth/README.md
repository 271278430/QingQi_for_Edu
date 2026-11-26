# auth

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/adapters 基础工程中的 auth 实现源码。

### 文件

| 文件                                                       | 简要说明                                                                                                     |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| [bigmodel-oauth.ts](bigmodel-oauth.ts)                     | 实现或公开接口：BigmodelOAuthClientOptions、BigmodelOAuthTokenSet、BigmodelOAuthClient、BigmodelOAuthError。 |
| [browser.ts](browser.ts)                                   | 实现或公开接口：BrowserOpenResult、BrowserOpenOptions、openUrlInBrowser。                                    |
| [cli-oauth.ts](cli-oauth.ts)                               | 实现或公开接口：CliOAuthProviderId、CliOAuthClientOptions、CliOAuthInitInput、CliOAuthInitData。             |
| [coding-plan-api-key.ts](coding-plan-api-key.ts)           | CLI 进程内唯一换证入口；保留旧导出名兼容调用方，返回值已是短期 Token。                                       |
| [credential-cipher.ts](credential-cipher.ts)               | 仅兼容旧格式；正式凭据仓库默认使用系统安全存储。                                                             |
| [index.ts](index.ts)                                       | index 的实现文件。                                                                                           |
| [localhost-callback.ts](localhost-callback.ts)             | 授权服务器按 RFC 6749 §4.1.2.1 回传 `error` 时使用的稳定错误码。                                             |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                                             |
| [shared-credentials.ts](shared-credentials.ts)             | 仅保护其它文件的最终提交；调用方先取得其它文件锁，回调不能再次写凭据库。                                     |
| [zai-business-token-cache.ts](zai-business-token-cache.ts) | 业务 JWT 与 PAT 生命周期不同；缓存只由 CLI 换证 adapter 持有。                                               |

<!-- qingqi-directory-index:end -->
