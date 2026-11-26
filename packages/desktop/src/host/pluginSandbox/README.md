# pluginSandbox

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/desktop 基础工程中的 pluginSandbox 实现源码。

### 文件

| 文件                       | 简要说明                                                                 |
| -------------------------- | ------------------------------------------------------------------------ |
| [contract.ts](contract.ts) | Host 到 Main 的登记请求关联；只拥有 pending 传输，不保存沙箱或会话事实。 |
| [index.ts](index.ts)       | 请求/响应/关闭共享同一生命周期，入口不再维护第二处 pending Map。         |
| [README.md](README.md)     | 本目录用途、子目录与逐文件说明。                                         |

<!-- qingqi-directory-index:end -->
