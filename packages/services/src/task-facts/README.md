# task-facts

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 task facts 实现源码。

### 文件

| 文件                                                     | 简要说明                                                                             |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [contract.example.ts](contract.example.ts)               | 调用者发送意图；不能先更新本地标题或另建重试队列。                                   |
| [CONTRACT.md](CONTRACT.md)                               | 模块职责、公共接口、依赖方向和状态约定。                                             |
| [contract.ts](contract.ts)                               | 存储端口只接受 CLI 事实，不能据 Host 时钟或运行态推导会话事实。                      |
| [index.ts](index.ts)                                     | 仅保留在途请求的代际，不缓存会话状态。新帧到达即撤销旧请求的落库资格。               |
| [module.ts](module.ts)                                   | \* task-facts 模块清单（architecture-governance managed 模块）。                     |
| [README.md](README.md)                                   | 本目录用途、子目录与逐文件说明。                                                     |
| [repairSubagentTaskIndex.ts](repairSubagentTaskIndex.ts) | 旧版本曾把冷恢复 child 写入主列表；只清理权威身份确认的派生索引，不删除 Agent 转录。 |

<!-- qingqi-directory-index:end -->
