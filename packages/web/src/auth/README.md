# auth

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 auth 实现源码。

### 文件

| 文件                                                           | 简要说明                                                                                       |
| -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| [browserOAuthCredentialRepo.ts](browserOAuthCredentialRepo.ts) | 同一浏览器多个标签页可以同时发起登录；只留最近几条，放弃的登录不会无限累积。                   |
| [contract.example.ts](contract.example.ts)                     | 读取只恢复缓存；显式登录由点击事件发起，取消信号覆盖全部网络等待。                             |
| [CONTRACT.md](CONTRACT.md)                                     | 模块职责、公共接口、依赖方向和状态约定。                                                       |
| [contract.ts](contract.ts)                                     | 会话归仓储所有；读取不写入，登录/退出等待持久化；订阅不携带凭据。                              |
| [index.ts](index.ts)                                           | index 的实现文件。                                                                             |
| [module.ts](module.ts)                                         | \* web-auth 模块清单（architecture-governance managed 模块）。                                 |
| [oauthStateCodec.ts](oauthStateCodec.ts)                       | 测试入口也经过登录门禁，必须保留原路径与扫码参数；OAuth 回调仍只使用已登记的 v4。              |
| [README.md](README.md)                                         | 本目录用途、子目录与逐文件说明。                                                               |
| [webAuthLocale.ts](webAuthLocale.ts)                           | 实现或公开接口：getWebAuthCopy。                                                               |
| [webAuthService.ts](webAuthService.ts)                         | 缺省 zai，保持 /remote 等既有入口行为不变。                                                    |
| [WebCallbackPage.tsx](WebCallbackPage.tsx)                     | 实现或公开接口：WebCallbackPage。                                                              |
| [WebLoginPage.tsx](WebLoginPage.tsx)                           | 实现或公开接口：WebLoginPage。                                                                 |
| [WebRegionalLoginActions.tsx](WebRegionalLoginActions.tsx)     | 实现或公开接口：WebRegionalLoginActionsProps、WebRegionalLoginActions。                        |
| [webRegionalOAuth.ts](webRegionalOAuth.ts)                     | Bug 原因：AbortSignal.any 从 Chrome 116 才有，Chrome/Edge 111–115 在 init 请求前抛 TypeError， |
| [webZaiOAuthConfig.ts](webZaiOAuthConfig.ts)                   | \* BigModel 的授权入口。                                                                       |
| [zaiWebOAuthProvider.ts](zaiWebOAuthProvider.ts)               | BigModel 授权入口；参数名与 ZAI 不同（redirect/appId vs redirect_uri/client_id）。             |

<!-- qingqi-directory-index:end -->
