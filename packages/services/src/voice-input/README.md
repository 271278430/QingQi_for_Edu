# voice-input

<!-- qingqi-directory-index:start -->

## 目录与文件

清启是基于 [ZCode](https://github.com/zai-org/ZCode) 开发的学生端教育 Agent 项目。

@zcode/services 基础工程中的 voice input 实现源码。

### 文件

| 文件                                         | 简要说明                                                                                     |
| -------------------------------------------- | -------------------------------------------------------------------------------------------- |
| [contract.example.ts](contract.example.ts)   | \* voice-input-service 标准调用示例：开始、发送音频、结束，并按 attemptId 只处理自己的事件。 |
| [CONTRACT.md](CONTRACT.md)                   | 模块职责、公共接口、依赖方向和状态约定。                                                     |
| [contract.ts](contract.ts)                   | \* 语音输入失败原因（docs/chat/composer-voice-input.md「服务端失败」）。                     |
| [index.ts](index.ts)                         | 浏览器安全的公共入口：只导出契约。Renderer 经 @zcode/services 引到这里。                     |
| [module.ts](module.ts)                       | \* voice-input-service 模块清单（architecture-governance managed 模块）。                    |
| [node.ts](node.ts)                           | Host 侧实现入口，由 @zcode/services/node 转出。                                              |
| [README.md](README.md)                       | 本目录用途、子目录与逐文件说明。                                                             |
| [voiceInputService.ts](voiceInputService.ts) | zcode-server ASR 协议见其仓库 docs/asr.md；这里只用 realtime 模式。                          |

<!-- qingqi-directory-index:end -->
