# mcp

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 mcp 测试夹具与样例。

### 文件

| 文件                                                                                 | 简要说明                                                                      |
| ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| [dual-era-version-server.mjs](dual-era-version-server.mjs)                           | dual-era-version-server 的实现文件。                                          |
| [oauth-status-isolation-direct-server.mjs](oauth-status-isolation-direct-server.mjs) | oauth-status-isolation-direct-server 的实现文件。                             |
| [official-auth-routing-proxy.mjs](official-auth-routing-proxy.mjs)                   | 运行真实 CLI，仅在反向授权边界注入恶意协议请求；不伪造 MCP 连接或 Host 响应。 |
| [plan-mode-mcp-permission-server.mjs](plan-mode-mcp-permission-server.mjs)           | plan-mode-mcp-permission-server 的实现文件。                                  |
| [README.md](README.md)                                                               | 本目录用途、子目录与逐文件说明。                                              |
| [startup-diagnostic-server.mjs](startup-diagnostic-server.mjs)                       | 真实 stderr/退出路径；只模拟外部进程的失败内容，不写 App 状态。               |
| [toolsearch-server.mjs](toolsearch-server.mjs)                                       | toolsearch-server 的实现文件。                                                |

<!-- qingqi-directory-index:end -->
