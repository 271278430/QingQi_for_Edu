# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 pending 测试场景。

### 文件

| 文件                                                       | 简要说明                                                                                                           |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                                                   |
| [regional-login.mjs](regional-login.mjs)                   | 独立浏览器验收；所有账号、OAuth和业务接口均为本地合成响应，不访问真实授权。                                        |
| [remote-login-v2.helpers.mjs](remote-login-v2.helpers.mjs) | 按 SID 指定 relay 回复（"matched" / "waiting" / 错误码），用于旧 SID 接续；提供时覆盖 relayError。                 |
| [remote-login-v2.mjs](remote-login-v2.mjs)                 | ML01–ML07、ML09、MD01–MD06、MD11–MD13：真实 Web 入口 + 浏览器 OAuth 回跳/登录门禁；外部 OAuth/relay 使用受控响应。 |

<!-- qingqi-directory-index:end -->
