# pending

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/web 基础工程中的 pending 测试场景。

### 文件

| 文件                                                       | 简要说明                                                                                        |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| [README.md](README.md)                                     | 本目录用途、子目录与逐文件说明。                                                                |
| [remote-abort-api-compat.mjs](remote-abort-api-compat.mjs) | ML08：真实 Web 入口移除静态 API，采用受控 HTTP/WS 验证配对到 bootstrap。                        |
| [remote-large-rpc.mjs](remote-large-rpc.mjs)               | MRL01/MRL02：真实 Web 与 RPC adapter 的大消息回归；账号、relay、业务数据均为合成夹具。          |
| [remote-submit-lifecycle.mjs](remote-submit-lifecycle.mjs) | MRS01–04：真实 Web Root/Composer/反馈表单、Host 装配和 raw RPC；外部账号/relay/Agent 返回受控。 |
| [remote-version.mjs](remote-version.mjs)                   | RV01–RV03：真实 Web 入口与浏览器导航；模拟 relay/桌面响应，不验证外部资源路由服务。             |

<!-- qingqi-directory-index:end -->
