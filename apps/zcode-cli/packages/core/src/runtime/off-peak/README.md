# off-peak

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/core 基础工程中的 off peak 实现源码。

### 文件

| 文件                                 | 简要说明                                                                   |
| ------------------------------------ | -------------------------------------------------------------------------- |
| [lifecycle.ts](lifecycle.ts)         | 工作事实由 Runtime 登记表、CommandInbox 与通知队列提供；此处不再维护副本。 |
| [model-binding.ts](model-binding.ts) | 动态凭据仅驻内存；一次请求的票据记录隔离，避免并发请求把旧票错误归到新票。 |
| [README.md](README.md)               | 本目录用途、子目录与逐文件说明。                                           |
| [runtime.ts](runtime.ts)             | 终态控制器只保留幂等回执，不能继续覆盖随后普通用户选择的持久化。           |
| [turn.ts](turn.ts)                   | 用户接纳只改变归属；主轮在完整请求边界应用新选择，子轮不调用本钩子。       |

<!-- qingqi-directory-index:end -->
