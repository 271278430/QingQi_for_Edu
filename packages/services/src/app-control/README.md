# app-control

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 app control 实现源码。

### 文件

| 文件                                             | 简要说明                                                                                    |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| [context.ts](context.ts)                         | 会话类（模型工具）或客户端类（§17.2）的连接事实，外加本次调用捕获的发现来源。               |
| [contract.example.ts](contract.example.ts)       | 实现或公开接口：discoverAppSessions。                                                       |
| [CONTRACT.md](CONTRACT.md)                       | 模块职责、公共接口、依赖方向和状态约定。                                                    |
| [contract.ts](contract.ts)                       | 两类调用方共有的连接事实：fence、所属 Host、取消与代际校验。                                |
| [discovery-directory.ts](discovery-directory.ts) | 入口 ID 和成员代际必须在 await 前固化；移除后重加不能接纳原连接的迟到结果。                 |
| [discovery.ts](discovery.ts)                     | 发现范围扩大不改变原 workspace 权限；同 cwd 的项目会话仍不能获得操作能力。                  |
| [execution.ts](execution.ts)                     | ReadSession 返回 transcript messageId；新投影 entityId/assistantResponseId 均由该事实派生。 |
| [index.ts](index.ts)                             | \* 把 owner 侧已知的协议错误映射成稳定的 SessionControlError。                              |
| [module.ts](module.ts)                           | 实现或公开接口：appControlModule。                                                          |
| [observation.ts](observation.ts)                 | 只读已活跃 session；缺 runtime 是明确未知，不订阅/恢复历史。                                |
| [README.md](README.md)                           | 本目录用途、子目录与逐文件说明。                                                            |
| [reverseRpc.ts](reverseRpc.ts)                   | 每个分支解析自己的封闭输入类型；没有 method 字符串下标执行任意服务的入口。                  |

<!-- qingqi-directory-index:end -->
