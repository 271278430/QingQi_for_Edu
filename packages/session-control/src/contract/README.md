# contract

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/session-control 基础工程中的 contract 实现源码。

### 文件

| 文件                             | 简要说明                                                                          |
| -------------------------------- | --------------------------------------------------------------------------------- |
| [app.ts](app.ts)                 | 规格 0.14：删除 host——它是已连接 Source Server 的 id，没有任何工具返回候选集；    |
| [cli.ts](cli.ts)                 | 规格 0.14：删除 workspace 过滤器——模型要先 ListSessions 才能拿到 workspace 引用， |
| [common.ts](common.ts)           | 命令与会话身份不能静默 trim，否则两个不同请求会被合并到同一个幂等键。             |
| [observation.ts](observation.ts) | \* 规格 0.14：回执里的 operation 必须能被原样放进 WaitSessions 的 operations[]。  |
| [README.md](README.md)           | 本目录用途、子目录与逐文件说明。                                                  |
| [results.ts](results.ts)         | 规格 0.14：重试身份由回执给出，模型不发明 id。                                    |

<!-- qingqi-directory-index:end -->
