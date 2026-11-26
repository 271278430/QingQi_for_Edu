# common

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/session-control 基础工程中的 common 实现源码。

### 文件

| 文件                       | 简要说明                                                                                       |
| -------------------------- | ---------------------------------------------------------------------------------------------- |
| [boundary.ts](boundary.ts) | \* 把工具层的二选一目标解析为完整引用。只给 sessionId 时由可信端口在本 Host 或本机会话库查找； |
| [README.md](README.md)     | 本目录用途、子目录与逐文件说明。                                                               |
| [wait.ts](wait.ts)         | self_wait 只对会话类调用方有意义：客户端类没有根会话，等待任何会话都不会等到自己。             |

<!-- qingqi-directory-index:end -->
