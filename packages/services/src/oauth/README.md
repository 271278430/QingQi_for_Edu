# oauth

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 oauth 实现源码。

### 子目录

| 目录                              | 存放内容                                          |
| --------------------------------- | ------------------------------------------------- |
| [providers/](providers/README.md) | @zcode/services 基础工程中的 providers 实现源码。 |
| [repo/](repo/README.md)           | @zcode/services 基础工程中的 repo 实现源码。      |

### 文件

| 文件                                                       | 简要说明                                                                   |
| ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| [callbackAttribution.ts](callbackAttribution.ts)           | 实现或公开接口：parseOAuthLoginAttribution、hasOAuthAuthorizationCode。    |
| [oauth.ts](oauth.ts)                                       | \* 在 host process 中运行，负责 OAuth 流程的全部业务逻辑：                 |
| [oauthProfileSchema.ts](oauthProfileSchema.ts)             | 上游业务userinfo只拥有展示字段；customerNumber或sub不能成为ZCode资产主体。 |
| [oauthProviderLogout.ts](oauthProviderLogout.ts)           | 新CN渠道没有旧Key清理映射，但退出同样必须使账号投影失效。                  |
| [oauthService.ts](oauthService.ts)                         | OAuth 超时时间（5 分钟）                                                   |
| [oauthUnauthorizedRequest.ts](oauthUnauthorizedRequest.ts) | 读取磁盘期间可能切换平台，不能拿上一平台残留 token 的 401 清理当前登录。   |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                           |
| [runtimeConfig.ts](runtimeConfig.ts)                       | Provider 运行时配置（仅 host process 可见）                                |

<!-- qingqi-directory-index:end -->
